#coding: utf-8

import json
import logging
import re
import datetime

from urllib.parse import urljoin, quote
import urllib
from lxml import html

logger = logging.getLogger(__name__)

def parse(html_input):
    '''
    [
    {
        "id": "1172/0005/0954",
        "utilizationType": "flat",
        "commercializationType": "rent",
        "detailType": "Etagenwohnung",
        "title": "Hier l\u00e4sst es sich leben!",
        "geoLocation": {
            "latitude": 52.5328,
            "longitude": 13.6136
        },
        "price": 664.35,
        "address": {
            "street": "Riesaer Stra\u00dfe",
            "houseNumber": "61",
            "zip": "12627",
            "city": "Berlin",
            "district": "Hellersdorf"
        },
        "images": [
            {
                "filePath": "/images/11/11720005-954-M-1.jpg",
                "title": "Au\u00dfenansicht"
            },
            {
                "filePath": "/images/11/11720005-954-M-2.jpg",
                "title": "Grundriss"
            },
            {
                "filePath": "/images/11/11720005-954-M-3.jpg",
                "title": "Energieausweis"
            }
        ],
        "area": 57.4,
        "rooms": 2,
        "level": 2,
        "isTopLevel": false,
        "heatingCosts": 37.26,
        "date": "2022-01-24 17:26:50"
    },
]
    '''
    base_url = "https://www.deutsche-wohnen.com/"
    object_url = "https://www.deutsche-wohnen.com/expose/object/"

    # parse results
    all_flats = json.loads(html_input)

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        flat_dict = {}

        flat_dict['title'] = flat['title']
        flat_dict['id'] = flat['id']

        flat_dict['pos'] = {
          'long' : flat['geoLocation']['longitude'],
          'lat' : flat['geoLocation']['latitude']
        }

        flat_dict['addr'] = f"{flat['address']['street']} {flat['address']['houseNumber']}, {flat['address']['zip']} {flat['address']['city']}"
        flat_dict['kiez'] = ''
        if 'district' in flat['address']:
          flat['kiez'] = flat['address']['district']

        flat_dict['link'] = quote(urljoin(object_url, flat['id']), safe=":/")

        # Bild
        if 'images' in flat and len(flat['images']) > 0:
          flat_dict['image'] = quote(urljoin(base_url, flat['images'][0]['filePath']), safe=":/")

        flat_dict['date_found'] = datetime.datetime.strptime(flat['date'], '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y %H:%M')

        # Eigenschaften
        flat_dict['properties'] = {}
        possible_fields = {
            'detailType': 'Wohnungstyp',
            'price': 'Gesamtmiete',
            'heatingCosts': 'Heizkosten',
            'area': 'Fläche',
            'rooms': 'Zimmer',
            'level': 'Etage',
            'isTopLevel': 'Oberstes Stockwerk'
        }
        for field, name in possible_fields.items():
            if field not in flat:
                continue

            value = str(flat[field])

            if field in ['price', 'heatingCosts']:
                value += ' €'
            elif field == 'area':
                value += ' m²'
            elif field == 'isTopLevel':
                value = 'Ja' if value else 'Nein'

            flat_dict['properties'][name] = value

        flat_dict['features'] = []
        flat_dict['landlord'] = 'Deutsche Wohnen'

        yield flat_dict
