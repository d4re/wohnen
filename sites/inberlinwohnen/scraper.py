import functools
import logging
import time

import requests

from config import FlatParams

logger = logging.getLogger(__name__)

s = requests.Session()
s.request = functools.partial(s.request, timeout=5)

search_url = "https://inberlinwohnen.de/wp-content/themes/ibw/skript/wohnungsfinder.php"

search_headers = {
    "accept": "*/*",
    "origin": "https://inberlinwohnen.de",
    "x-requested-with": "XMLHttpRequest",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
}

common_headers = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "pragma": "no-cache",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "cache-control": "no-cache",
    "authority": "inberlinwohnen.de",
    "referer": "https://inberlinwohnen.de/wohnungsfinder/",
}
s.headers.update(common_headers)

search_data = {
    "q": "wf-save-srch",
    "save": False,
    "miete_min": False,
    "miete_max": False,
    "qm_min": False,
    "qm_max": False,
    "rooms_min": 2,
    "rooms_max": 5,
    "etage_min": False,
    "etage_max": False,
    "baujahr_min": False,
    "baujahr_max": False,
    "heizung_zentral": False,
    "heizung_etage": False,
    "energy_fernwaerme": False,
    "heizung_nachtstrom": False,
    "heizung_ofen": False,
    "heizung_gas": False,
    "heizung_oel": False,
    "heizung_solar": False,
    "heizung_erdwaerme": False,
    "heizung_fussboden": False,
    "seniorenwohnung": False,
    "maisonette": False,
    "etagen_dg": False,
    "balkon_loggia_terrasse": False,
    "garten": False,
    "wbs": 0,
    "barrierefrei": False,
    "gaeste_wc": False,
    "aufzug": False,
    "stellplatz": False,
    "keller": False,
    "badewanne": False,
    "dusche": False,
}

result_data = {
    "q": "change-wf-view",
    "view": "tiles",
}


def get_search(flat_params: FlatParams):
    s = search_data.copy()
    s["rooms_min"] = str(flat_params.rooms_min)
    s["rooms_max"] = str(flat_params.rooms_max)
    s["miete_max"] = str(flat_params.rent_base_max)
    s["wbs"] = flat_params.wbs
    return s


def scrape(flat_params: FlatParams):
    search_d = get_search(flat_params)
    search = s.post(search_url, data=search_d, headers=search_headers)
    search.raise_for_status()

    # The web UI sleeps for a few seconds here, lets mimick that
    # It seemst to work without, but better to mimick more
    logger.debug("Sleeping for two seconds before querying for the results")
    time.sleep(2.0)

    try:
        html_result = s.post(search_url, data=result_data, headers=search_headers)
    except requests.exceptions.Timeout:
        logger.info("Timed out, skipping inberlinwohnen.")

    return html_result.text.encode("utf-8")
