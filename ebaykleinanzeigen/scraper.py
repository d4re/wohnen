import requests
import time
import logging

logger = logging.getLogger(__name__)

s = requests.Session()

search_url_tpl = 'https://www.ebay-kleinanzeigen.de/s-wohnung-mieten/10557/anzeige:angebote/preis::{max_rent}/c203l9672r9'

search_headers = {
    'accept': '*/*',
    'origin': 'https://www.ebay-kleinanzeigen.de',
}

common_headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'www.ebay-kleinanzeigen.de',
    'referer': 'https://www.ebay-kleinanzeigen.de'
}
s.headers.update(common_headers)

def get_search_url(max_rent):
    return search_url_tpl.replace('{max_rent}', str(max_rent))

def scrape(min_area, min_rooms, max_rooms, max_rent, wbs):
    search_url = get_search_url(max_rent + 100) # config states Kaltmiete

    search = s.get(search_url, headers=search_headers)
    search.raise_for_status()

    return search.text.encode("utf-8")