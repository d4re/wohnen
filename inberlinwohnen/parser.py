#coding: utf-8

import logging

from urllib.parse import urljoin, quote
import urllib
from lxml import html

logger = logging.getLogger(__name__)

def parse(html_input):
    base_url = "https://inberlinwohnen.de/"

    tree = html.fromstring(html_input)
    all_flats = tree.xpath("//div[contains(@id,'cflat_')]")

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        # Parse HTML
        adresse = flat.xpath(".//p[@class='adresse']")[0].text_content().strip().split(",")
        link = flat.xpath(".//a[contains(@title,'Die detailierte')]/@href")[0]

        # The sub-header of Kaltmiete, Wohnflache, Zimmer. Always seems to be the same
        # and shares the same div class.
        #
        # If this breaks: Check the <dd> thing, that tells us which it is. Right now
        # we're assuming they're always in the same order.
        maincriteria = [a.text for a in flat.xpath(".//div[@class='maincriteria']/dl/dt")]
        addrcriteria = [a.text for a in flat.xpath(".//div[@class='addcriteria']/dl/dt")]

        # Unpack values
        addr, kiez = [a.strip() for a in adresse]

        kalt, sqm, zimmer = maincriteria
        neben = addrcriteria[0]
        total = addrcriteria[1]
        timeframe = addrcriteria[2]
        floor = addrcriteria[3]
        year = addrcriteria[5]

        yield {
            'kalt': kalt.split(" ")[0],
            'neben': neben.split(" ")[0],
            'total': total.split(" ")[0],
            'sqm': sqm.split(" ")[0],
            'floor': floor,
            'zimmer': zimmer,
            'timeframe': timeframe,
            'year': year,
            'addr': addr,
            'kiez': kiez,
            'link': quote(urljoin(base_url, link), safe=":/"),
        }
