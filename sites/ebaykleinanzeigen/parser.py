# coding: utf-8

import datetime
import json
import logging
import re
import urllib
from urllib.parse import quote, urljoin

from lxml import html

logger = logging.getLogger(__name__)


def parse(html_input):
    """
     <li class="ad-listitem lazyload-item   ">
      <article class="aditem" data-adid="2001221462" data-href="/s-anzeige/2-zimmer-wohnung/2001221462-203-3390">
        <div class="aditem-image">
          <a href="/s-anzeige/2-zimmer-wohnung/2001221462-203-3390">
            <div class="imagebox srpimagebox"
              data-imgsrc="https://i.ebayimg.com/00/s/MTYwMFgxMjAw/z/qggAAOSwck9h6Syg/$_2.JPG"
              data-imgsrcretina="https://i.ebayimg.com/00/s/MTYwMFgxMjAw/z/qggAAOSwck9h6Syg/$_35.JPG 2x"
              data-imgtitle="Möblierte Designer-3-Zimmer-Erdgeschosswohnung mit Garten Berlin - Wilmersdorf Vorschau"
            >
            </div>
          </a>
        </div>
        <div class="aditem-main">
          <div class="aditem-main--top">
            <div class="aditem-main--top--left">
              <i class="icon icon-small icon-pin"></i> 12351 Neukölln (ca. 10 km)
            </div>
            <div class="aditem-main--top--right">
                    <i class="icon icon-small icon-calendar-open"></i> Heute, 22:32
            </div>
          </div>
          <div class="aditem-main--middle">
              <h2 class="text-module-begin">
                  <a class="ellipsis" href="/s-anzeige/2-zimmer-wohnung/2001221462-203-3390">2 Zimmer Wohnung</a>
              </h2>
              <p class="aditem-main--middle--description">Suche Nachmieter für meine Wohnung, alles frisch renoviert, neue Küche neues bad und neuer...</p>
              <p class="aditem-main--middle--price">580 €</p>
          </div>
          <div class="aditem-main--bottom">
              <p class="text-module-end">
                <span class="simpletag tag-small">56 m²</span>
                <span class="simpletag tag-small">2 Zimmer</span>
              </p>
          </div>
        </div>
      </article>
    </li>
    """
    base_url = "https://www.ebay-kleinanzeigen.de/"

    # parse results
    tree = html.fromstring(html_input)
    all_flats = tree.xpath("//article[contains(@class,'aditem')]")

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        flat_dict = {}

        flat_dict["title"] = flat.xpath(".//h2")[0].text_content().strip()
        flat_dict["id"] = flat.xpath("./@data-adid")[0]
        flat_dict["link"] = flat.xpath("./@data-href")[0]
        flat_dict["link"] = quote(urljoin(base_url, flat_dict["link"]), safe=":/")

        # Bild
        image = flat.xpath(".//div[contains(@class,'imagebox')]/@data-imgsrcretina")
        if image:
            flat_dict["image"] = image[0].split(" ")[0]
            flat_dict["image"] = quote(flat_dict["image"], safe=":/")

        # Text module top
        top = flat.xpath(".//div[contains(@class,'aditem-main--top')]")[0]
        flat_dict["addr"] = (
            top.xpath(".//div[contains(@class,'aditem-main--top--left')]")[0]
            .text_content()
            .strip()
        )
        flat_dict["addr"] = re.sub("\n\s+", " ", flat_dict["addr"])

        location_s = re.search("(\d+) (.*) \((.*)\)", flat_dict["addr"])
        if location_s:
            flat_dict["plz"] = location_s.group(1)
            flat_dict["kiez"] = location_s.group(2)
            flat_dict["distance_from_center"] = location_s.group(3)

        flat_dict["date_found"] = (
            top.xpath(".//div[contains(@class,'aditem-main--top--right')]")[0]
            .text_content()
            .strip()
        )
        if len(flat_dict["date_found"]) > 0:
            flat_dict["date_found"] = flat_dict["date_found"].replace(
                "Heute,", datetime.datetime.now().strftime("%d.%m.%Y")
            )
            flat_dict["date_found"] = flat_dict["date_found"].replace(
                "Gestern,",
                (datetime.date.today() - datetime.timedelta(days=1)).strftime(
                    "%d.%m.%Y"
                ),
            )
        else:
            flat_dict["date_found"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        # Eigenschaften
        flat_dict["properties"] = {}

        middle = flat.xpath(".//div[contains(@class,'aditem-main--middle')]")[0]
        flat_dict["properties"]["Miete"] = middle.xpath(
            ".//p[contains(@class,'aditem-main--middle--price')]"
        )[0].text_content()
        flat_dict["properties"]["Miete"] = re.sub(
            "\n\s+", "", flat_dict["properties"]["Miete"]
        )
        flat_dict["properties"]["Beschreibung"] = middle.xpath(
            ".//p[contains(@class,'aditem-main--middle--description')]"
        )[0].text_content()
        flat_dict["properties"]["Eingestellt"] = flat_dict["date_found"]

        # Besonderheiten
        flat_dict["features"] = []
        all_features = flat.xpath(".//span[contains(@class, 'simpletag')]")
        for feature in all_features:
            flat_dict["features"].append(feature.text_content())

        flat_dict["landlord"] = ""

        yield flat_dict
