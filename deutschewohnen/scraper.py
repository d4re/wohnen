import requests
import logging
import json

logger = logging.getLogger(__name__)

s = requests.Session()

search_url = 'https://immo-api.deutsche-wohnen.com/estate/findByFilter'

search_headers = {
    'accept': '*/*',
    'origin': 'https://www.deutsche-wohnen.com',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
}

common_headers = {
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'immo-api.deutsche-wohnen.com',
    'referer': 'https://www.deutsche-wohnen.com'
}
s.headers.update(common_headers)

search_data = {
    "infrastructure" : {},
    "flatTypes" : {},
    "other" : {},
    "commercializationType" : "rent",
    "utilizationType" : "flat",
    "location" : "Berlin",
    "locale" : "de",
    "city" : "Berlin"
}

def get_search(min_area, min_rooms, max_rooms, max_rent, wbs):
    s = search_data.copy()
    # s['rooms_min'] = str(min_rooms)
    # s['rooms_max'] = str(max_rooms)
    s['area'] = str(min_area)
    s['price'] = str(max_rent + 100) # config states Kaltmiete
    # s['wbs'] = wbs
    return s

def scrape(min_area, min_rooms, max_rooms, max_rent, wbs):
    search_d = get_search(min_area, min_rooms, max_rooms, max_rent, wbs)
    search = s.post(search_url, data=json.dumps(search_d), headers=search_headers)
    search.raise_for_status()

    return search.text.encode("utf-8")