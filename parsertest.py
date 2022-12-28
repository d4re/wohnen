import argparse
import importlib.util
import logging
import sys

import config

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("sites", type=str, nargs="+", help="list of sites to check")
    parser.add_argument("--scrape", action="store_true", help="actually scrape")

    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(config.loglevel)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    for site in args.sites:
        logger.debug(site)

        html = None

        html_dump_file = f"{config.data_path}/{site}.html"

        if args.scrape:
            spec_scraper = importlib.util.find_spec(f"sites.{site}.scraper")
            if spec_scraper is None:
                logging.error(
                    f"Could not find scraper module for site {site}. Skipping..."
                )
                continue

            scraper = spec_scraper.loader.load_module()

            html = scraper.scrape(config.query_parameters)

            try:
                with open(html_dump_file, "w", encoding="utf-8") as f:
                    if isinstance(html, bytes):
                        html = html.decode("utf-8")
                    f.write(html)
            except IOError as e:
                logger.error(e)
        else:
            try:
                with open(html_dump_file, "r") as f:
                    html = f.read()
            except IOError as e:
                logger.error(e)

        if html is None:
            print("No HTML returned!")
        else:
            spec_parser = importlib.util.find_spec(f"sites.{site}.parser")
            if spec_parser is None:
                logging.error(
                    f"Could not find parser module for site {site}. Skipping..."
                )
                continue

            parser = spec_parser.loader.load_module()
            flats = parser.parse(html)

            print([flat for flat in flats])
