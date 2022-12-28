import json

import requests

search_url = "https://immo-api.deutsche-wohnen.com/estate/findByFilter"

search_headers = {
    "accept": "*/*",
    "origin": "https://www.deutsche-wohnen.com",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "cache-control": "no-cache",
    "authority": "immo-api.deutsche-wohnen.com",
    "referer": "https://www.deutsche-wohnen.com",
}

search_data = {
    "infrastructure": {},
    "flatTypes": {},
    "other": {},
    "commercializationType": "rent",
    "utilizationType": "flat",
    "location": "Berlin",
    "locale": "de",
    "city": "Berlin",
}


def get_search(params):
    s = search_data.copy()

    s["area"] = str(params["area_min"])
    s["price"] = str(params["rent_total_max"])

    return s


def scrape(params):
    search_d = get_search(params)
    search = requests.post(
        search_url, data=json.dumps(search_d), headers=search_headers
    )
    search.raise_for_status()

    return search.text.encode("utf-8")
