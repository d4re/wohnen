import asyncio
from dataclasses import dataclass
import importlib
import logging
from pathlib import Path
from types import ModuleType

import config
import flatfilter
from jsonfile import JsonFile

logger = logging.getLogger(__name__)

@dataclass
class SiteImpl:
    scraper: ModuleType
    parser: ModuleType
    applier: ModuleType

site_handlers: dict[str, SiteImpl] = {}


def init_handlers(sites: list[str]) -> None:
    global site_handlers
    for site in sites:
        spec_scraper = importlib.util.find_spec(f"sites.{site}.scraper")
        if spec_scraper is None:
            logging.error(f"Could not find scraper module for site {site}. Skipping site...")
            continue
        site_scraper = spec_scraper.loader.load_module()

        spec_parser = importlib.util.find_spec(f"sites.{site}.parser")
        if spec_parser is None:
            logging.error(f"Could not find parser module for site {site}. Skipping site...")
            continue
        site_parser = spec_parser.loader.load_module()

        spec_applier = importlib.util.find_spec(f"sites.{site}.applier")
        if spec_applier is None:
            logging.error(f"Could not find applier module for site {site}. Auto apply deactivated for this site...")
            site_applier = None
        else:
            site_applier = spec_applier.loader.load_module()

        site_handlers[site] = SiteImpl(site_scraper, site_parser, site_applier)


async def find_flats(search_conf: config.Search, cache_folder: Path) -> dict:
    global site_handlers
    if not site_handlers:
        init_handlers(search_conf.sites)
    sites = {}

    for site, site_impl in site_handlers.items():
        logger.debug(site)

        jsonfile = JsonFile.open(cache_folder / f"{site}.json")
        loop = asyncio.get_event_loop()

        try:
            scraping = loop.run_in_executor(
                None, site_impl.scraper.scrape, search_conf.flat_params
            )
            html = await scraping
        except Exception as error:
            logger.exception(error)
            continue

        try:
            parsing = loop.run_in_executor(None, site_impl.parser.parse, html)
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

async def apply_to_flats(sites: dict, applicant: config.Applicant):
    global site_handlers
    loop = asyncio.get_event_loop()
    for site, flats in sites.items():
        if applier := site_handlers[site].applier:
            for flat in flats:
                applying = loop.run_in_executor(None, applier.apply, flat, applicant)
                success = await applying
                if not success:
                    logger.error(f"Error applying for flat {flat['title']} on site {site}")

