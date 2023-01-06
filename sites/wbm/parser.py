import datetime
import json
import logging
import re
import urllib
from urllib.parse import quote, urljoin

from lxml import html

from sites.helpers import parse_plz

logger = logging.getLogger(__name__)

"""
<div class="row openimmo-search-list-item" data-id="51-3109/3/184">
    <div class="col-8 immo-col stretch">
        <article class="teaserBox variation-pt immo-element">
            <div class="imgWrap"
                style="background-image:url(/uploads/tx_openimmo/connection-3/images/67132-0368592d43d9f93dceeba9b3ff9d22c1.jpg)">
                <h2 class="imageTitle">2-Zimmer-Wohnung in Friedrichshain mit WBS140!</h2>
            </div>
        </article>
        <div id="immobilie-list-item-tooltip-67132" style="display:none">
            <p><b>2-Zimmer-Wohnung in Friedrichshain mit WBS140!</b><br> Koppenstraße 60<br> 10243
                Berlin<br></p>
            <p class="btn-holder margin-top"><a class="btn sign" title="Details"
                    href="/wohnungen-berlin/angebote/details/67132/"> Zum Exposé</a></p>
        </div>
    </div>
    <div class="col-4 immo-col stretch">
        <article class="textOnly immo-element">
            <div class="textWrap">
                <p class="category">Friedrichshain</p>
                <p class="address">Koppenstrasse 60,<br>10243 Berlin</p>
                <ul class="main-property-list" data-cols="3">
                    <li class="main-property">
                        <div>Gesamtmiete:</div>
                        <div>531,72 €</div>
                    </li>
                    <li class="main-property">
                        <div>Größe:</div>
                        <div>60,35 m²</div>
                    </li>
                    <li class="main-property">
                        <div>Zimmer:</div>
                        <div>2</div>
                    </li>
                </ul>
                <ul class="check-property-list">
                    <li>Bad mit Dusche</li>
                    <li>Aufzug</li>
                    <li>WBS</li>
                </ul>
                <p class="btn-holder margin-top"><a class="btn sign" title="Details"
                        href="/wohnungen-berlin/angebote/details/67132/"> Weiter</a></p>
            </div>
        </article>
    </div>
</div>
"""


def parse(html_input):
    base_url = "https://www.wbm.de"

    property_map = {
        "Größe": "area",
        "Zimmer": "rooms",
        "Gesamtmiete": "rent_total",
    }

    # parse results
    tree = html.fromstring(html_input)
    all_flats = tree.xpath("//div[contains(@class,'openimmo-search-list-item')]")

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        flat_dict = {}

        flat_dict["title"] = (
            flat.xpath(".//h2[contains(@class,'imageTitle')]")[0].text_content().strip()
        )
        flat_dict["id"] = flat.xpath("./@data-id")[0]
        flat_dict["link"] = flat.xpath(".//a[contains(@class,'btn')]/@href")[0]
        flat_dict["link"] = quote(urljoin(base_url, flat_dict["link"]), safe=":/")

        flat_dict["addr"] = (
            flat.xpath(".//p[contains(@class,'address')]")[0].text_content().strip()
        )
        flat_dict["addr"] = re.sub("\n\s+", " ", flat_dict["addr"])
        flat_dict["addr"] = flat_dict["addr"].replace(",", ", ")

        flat_dict["plz"] = parse_plz(flat_dict["addr"])

        flat_dict["kiez"] = (
            flat.xpath(".//p[contains(@class,'category')]")[0].text_content().strip()
        )

        flat_dict["date_found"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        # Eigenschaften
        flat_dict["properties"] = {}

        props = flat.xpath(".//ul[contains(@class,'main-property-list')][1]/li")
        for prop in props:
            kv = prop.xpath("./div")
            key = kv[0].text_content().replace(":", "")
            key = property_map.get(key, key)
            value = kv[1].text_content()
            flat_dict["properties"][key] = value

        # Besonderheiten
        flat_dict["features"] = []
        all_features = flat.xpath(".//ul[contains(@class,'check-property-list')][1]/li")
        for feature in all_features:
            flat_dict["features"].append(feature.text_content())

        flat_dict["landlord"] = "WBM"

        yield flat_dict
