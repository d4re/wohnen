import json
import requests

search_url_tpl = 'https://www.immowelt.de/liste/berlin/wohnungen/mieten?ami={area_min}&d=true&efs=CERTIFICATE_OF_ELIGIBILITY&efs=NEW_BUILDING_PROJECT&pma={rent_base_max}&rmi={rooms_min}&sd=DESC&sf=RELEVANCE&sp=1'
# search_url = 'https://api.immowelt.com/residentialsearch/v1/searches'

search_data = {
    "estateType": "APARTMENT",
    "distributionTypes": ["RENT", "LEASE"], 
    "estateSubtypes": [], 
    "locationIds": [150696], 
    "featureFilters": [], 
    "excludedFeatureFilters": ["NEW_BUILDING_PROJECT"],
    "primaryPrice": {"max": 900}, 
    "primaryArea": {"min": 40}, 
    "areas": [{"areaType": "PLOT_AREA"}], 
    "rooms": {"min": 2}, 
    "geoRadius": {"point": {"lat": 52.50153956329474, "lon": 13.402144821833788}}, 
    "sort": {"direction": "DESC", "field": "RELEVANCE"}, 
    "immoItemTypes": ["ESTATE", "PROJECT"], 
    "paging": {"size": 20, "page": 0}
}

search_headers = {
    'accept': '*/*',
    'origin': 'https://www.immowelt.de',
    'accept-encoding': 'gzip, deflate',
    'accept-language': 'en-US,en;q=0.9',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
    'cache-control': 'no-cache',
    'authority': 'www.immowelt.de',
    'referer': 'https://www.immowelt.de'
}

def scrape(params):
    # data = search_data.copy()
    # data['rooms']['min'] = params['rooms_min']
    # data['primaryArea']['min'] = params['area_min']
    # data['primaryPrice']['max'] = params['rent_base_max']
    # if params['wbs'] == 0:
    #     data['excludedFeatureFilters'].append("CERTIFICATE_OF_ELIGIBILITY")

    search_url = (search_url_tpl
        .replace('{area_min}', str(params['area_min']))
        .replace('{rent_base_max}', str(params['rent_base_max']))
        .replace('{rooms_min}', str(params['rooms_min']))
    )

    #search=requests.post(search_url, data=json.dumps(data), headers = search_headers)
    search=requests.get(search_url, headers = search_headers)
    search.raise_for_status()

    # override encoding by real educated guess as provided by chardet
    search.encoding = search.apparent_encoding

    return search.text
