import argparse
import logging
import sys
import config

import ebaykleinanzeigen.scraper
import ebaykleinanzeigen.parser

import deutschewohnen.parser
import deutschewohnen.scraper

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
    parser.add_argument("--scrape", action="store_true", help="actually scrape")

    args = parser.parse_args()

    logger = logging.getLogger()
    logger.setLevel(config.loglevel)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', "%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    for site in args.sites:
        logger.debug(site)
        sitem = getattr(sys.modules[__name__], site)

        html = None

        if args.scrape:
            scraper = getattr(sitem, "scraper")
            html = scraper.scrape(config.min_area, config.min_rooms, config.max_rooms, config.max_rent, config.wbs)

            try:
                with open(f'dumps/{site}.html', 'w') as f:
                    f.write(html.decode('utf-8'))
            except IOError as e:
                logger.error(e)
        else:
            try:
                with open(f'dumps/{site}.html', 'r') as f:
                    html = f.read()
            except IOError as e:
                logger.error(e)

        if html is None:
            print('No HTML returned!')
        else:
            parser = getattr(sitem, "parser")
            flats = parser.parse(html)

            print([flat for flat in flats])
