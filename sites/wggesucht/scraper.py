import requests

search_url_tpl = 'https://www.wg-gesucht.de/wohnungen-in-Berlin.8.2.3.0.html?offer_filter=1&city_id=8&noDeact=1&categories%5B%5D=2&rent_types%5B%5D=2&sMin={area_min}&rMax={rent_total_max}&exc=2&img_only=1'

search_headers = {
    'accept': '*/*',
    'origin': 'https://www.wg-gesucht.de',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'www.wg-gesucht.de',
    'referer': 'https://www.wg-gesucht.de'
}

def scrape(params):

    search_url = (search_url_tpl
        .replace('{area_min}', str(params['area_min']))
        .replace('{rent_total_max}', str(params['rent_total_max']+200))
        .replace('{rooms_min}', str(params['rooms_min']))
    )

    search=requests.get(search_url, headers = search_headers)
    search.raise_for_status()

    # override encoding by real educated guess
    search.encoding = 'utf-8'

    return search.text
