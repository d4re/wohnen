import sys
import argparse
import logging
import importlib

from jsonfile import JsonFile
import sendemail
import config
import flatfilter

parser = argparse.ArgumentParser()
parser.add_argument("sites", type=str, nargs='+', help="list of sites to check")
parser.add_argument("--scrape", action="store_true", help="actually scrape")
parser.add_argument("--quiet", action="store_true", help="hide log output")
parser.add_argument("--email", type=str, action='append', help="email addresses to send notify about new flats")
parser.add_argument("--formattest", action="store_true", help="test email formatting")

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
    sites = {}

    for site in args.sites:
        logger.debug(site)

        jsonfile = JsonFile.open(f'{config.data_path}/{site}.json')

        if args.formattest:
            sites[site] = jsonfile._json
            continue

        if args.scrape:
            spec_scraper = importlib.util.find_spec(f'sites.{site}.scraper')
            if spec_scraper is None:
                logging.error(f'Could not find scraper module for site {site}. Skipping...')
                continue

            scraper = spec_scraper.loader.load_module()

            html = scraper.scrape(config.query_parameters)
        else:
            html = get_sample(site)

        spec_parser = importlib.util.find_spec(f'sites.{site}.parser')
        if spec_parser is None:
            logging.error(f'Could not find parser module for site {site}. Skipping...')
            continue

        parser = spec_parser.loader.load_module()
        try:
            flats = parser.parse(html)

            # filter flats
            flats = flatfilter.filter_list(flats)
            logging.debug(f"Found {len(flats)} valid flats")
        except Exception as e:
            logging.exception("parsing or filtering failed")
            continue

        # add remaining flats to the list
        jsonfile.add_list(flats)

        if jsonfile.new_item_count > 0:
            logging.info("Found {} new flats".format(jsonfile.new_item_count))
            sites[site] = jsonfile.new_items[:]

        jsonfile.save()

    if len(sites) == 0:
        logging.info("Nothing to report")
        sys.exit(0)

    if args.formattest or not args.email:
        sendemail.test_format_body(sites)
    else:
        sendemail.send_email(sites, args.email)
