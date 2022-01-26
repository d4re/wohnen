import sys
import argparse
import logging

import inberlinwohnen.parser
import inberlinwohnen.scraper
from jsonfile import JsonFile
import sendemail
import config

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")
parser.add_argument("--quiet", action="store_true", help="hide log output")
parser.add_argument("--email", type=str, nargs="+", help="email addresses to send notify about new flats")

args = parser.parse_args()

logger = logging.getLogger()
logger.setLevel(config.loglevel)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s', "%Y-%m-%d %H:%M:%S")
if hasattr(config, 'logfile'):
    fh = logging.FileHandler(config.logfile)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

if not args.quiet:
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def get_sample(site):
    logger.warning("Using sample file for {}".format(site))
    with open('{}/sample.txt'.format(site), 'r') as f:
        ## html will be a list
        return f.read()

if __name__ == "__main__":
    for site in args.sites:
        logger.debug(site)
        sitem = getattr(sys.modules[__name__], site)
        if args.scrape:
            scraper = getattr(sitem, "scraper")
            html = scraper.scrape(config.min_rooms, config.max_rooms, config.max_rent, config.wbs)
        else:
            scraper = None
            html = get_sample(site)

        parser = getattr(sitem, "parser")
        flats = parser.parse(html)

        jsonfile = JsonFile.open(config.jsonfile)
        jsonfile.add_list(flats)

        newflats = jsonfile.new_items[:]

        if jsonfile.new_item_count > 0:
            logging.info("Found {} new flats".format(jsonfile.new_item_count))

        jsonfile.save()

        if args.email and len(newflats) > 0:
            sendemail.send_email(newflats, args.email, site)
