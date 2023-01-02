import asyncio
import importlib
import logging
from pathlib import Path

import config
import flatfilter
from jsonfile import JsonFile

logger = logging.getLogger(__name__)

site_handlers = {}


def init_handlers(sites: list[str]) -> None:
    global site_handlerss
    for site in sites:
        spec_scraper = importlib.util.find_spec(f"sites.{site}.scraper")
        if spec_scraper is None:
            logging.error(f"Could not find scraper module for site {site}. Skipping...")
            continue
        site_scraper = spec_scraper.loader.load_module()

        spec_parser = importlib.util.find_spec(f"sites.{site}.parser")
        if spec_parser is None:
            logging.error(f"Could not find parser module for site {site}. Skipping...")
            continue
        site_parser = spec_parser.loader.load_module()
        site_handlers[site] = (site_scraper, site_parser)


async def find_flats(search_conf: config.Search, cache_folder: Path) -> None:
    if not site_handlers:
        init_handlers(search_conf.sites)
    sites = {}

    for site, (site_scraper, site_parser) in site_handlers.items():
        logger.debug(site)

        jsonfile = JsonFile.open(cache_folder / f"{site}.json")
        loop = asyncio.get_event_loop()

        try:
            scraping = loop.run_in_executor(
                None, site_scraper.scrape, search_conf.flat_params
            )
            html = await scraping
        except Exception as error:
            logger.exception(error)
            continue

        try:
            parsing = loop.run_in_executor(None, site_parser.parse, html)
            flats = await parsing

            # filter flats
            flats = flatfilter.filter_list(flats, search_config=search_conf)
            logger.debug(f"Found {len(flats)} valid flats")
        except Exception:
            logger.exception("parsing or filtering failed")
            continue

        # add remaining flats to the list
        jsonfile.add_list(flats)

        if jsonfile.new_item_count > 0:
            logger.info("Found {} new flats".format(jsonfile.new_item_count))
            sites[site] = jsonfile.new_items[:]

        jsonfile.save()

    if len(sites) == 0:
        logger.info("Nothing to report")

    return sites
