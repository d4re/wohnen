import requests

from config import FlatParams

search_url = "https://www.wbm.de/wohnungen-berlin/angebote/"

search_headers = {
    "accept": "*/*",
    "origin": "https://www.wbm.de",
    "accept-encoding": "gzip, deflate",
    "accept-language": "en-US,en;q=0.9",
    "pragma": "no-cache",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "cache-control": "no-cache",
    "authority": "www.wbm.de",
    "referer": "https://www.wbm.de",
}


def scrape(flat_params: FlatParams):
    search = requests.get(search_url, headers=search_headers)
    search.raise_for_status()

    # override encoding by real educated guess
    search.encoding = "utf-8"

    return search.text
