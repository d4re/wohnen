import datetime
import logging
import re
from urllib.parse import quote, urljoin

from lxml import html

logger = logging.getLogger(__name__)

"""
<div id="liste-details-ad-8457387" class="col-sm-6 offer_list_item" data-id="8457387">
    <div class="panel panel-default ">
        <div class="panel-heading" style="padding:0;">
            <div class="gallery-list-fav-button asset_favourite" data-ad_id="8457387" data-ad_type="0" data-favourite_status="0">
                <span id="to-fav-8457387" class="fav-button-8457387 mdi mdi-22px mdi-heart-outline icon-fav-empty icon-fav-list" style="margin-left: 2px;" aria-hidden="true"></span>
            </div>

            <div class="gallery-view-img-wrapper">
                <a class="detailansicht" href="wohnungen-in-Berlin-Hermsdorf.8457387.html">
                    <img class="img-responsive center-block image_responsive_contained" src="https://img.wg-gesucht.de/media/up/2021/12/5894a9bcf618f03318c8f7b2c638a279c8f09437892a3a77a7c11ceafed17467_IMG_20160129_00671__1_.small.jpg" data-src="https://img.wg-gesucht.de/media/up/2021/12/5894a9bcf618f03318c8f7b2c638a279c8f09437892a3a77a7c11ceafed17467_IMG_20160129_00671__1_.small.jpg" alt="" style="max-height: 240px;" data-cmp-info="9">
                </a>
            </div>
        </div>
        <div class="panel-body noprint" style="padding-top: 0; height: 100px;">
            <h3 class="headline headline-list-view headline-gallery truncate_title" title="Möbliertes Gartenhaus nahe S-Bahnhof Hermsdorf">
                <a href="wohnungen-in-Berlin-Hermsdorf.8457387.html" class="detailansicht">
                    Möbliertes Gartenhaus nahe S-Bahnhof Hermsdorf
                </a>
            </h3>
            62m² - 890€
        </div>

        <div class="panel-body printonly" style="padding: 0 10px;">
            <h3 class="headline headline-list-view headline-gallery truncate_title" title="Möbliertes Gartenhaus nahe S-Bahnhof Hermsdorf">
                <a class="detailansicht" href="wohnungen-in-Berlin-Hermsdorf.8457387.html">
                    Möbliertes Gartenhaus nahe S-Bahnhof Hermsdorf
                </a>
            </h3>
        </div>
        
        <div class="printonly">
            <br>
            <i>Diese Anzeige ist erreichbar unter:</i> https://www.wg-gesucht.de/8457387.html
            <br><br><br>

            <div style="border-top: 2px solid #ddd; margin-bottom:10px"></div>
            <br>
        </div>
    </div>
</div>
"""


def parse(html_input):

    if isinstance(html, bytes):
        html_input = html_input.decode("utf-8")

    base_url = "https://www.wg-gesucht.de/"

    # parse results
    tree = html.fromstring(html_input)
    all_flats = tree.xpath("//div[contains(@class,'offer_list_item')]")

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        flat_dict = {}

        headline = flat.xpath(".//h3[contains(@class,'headline-list-view')]/a")[0]
        flat_dict["title"] = headline.text_content().strip()
        flat_dict["id"] = flat.attrib["data-id"]
        flat_dict["link"] = headline.attrib["href"]
        flat_dict["link"] = quote(urljoin(base_url, flat_dict["link"]), safe=":/")

        # Bild
        image = flat.xpath(".//img[contains(@class,'img-responsive')]/@data-src")
        if image:
            flat_dict["image"] = quote(image[0], safe=":/")

        # panel-body
        panel = flat.xpath(".//div[contains(@class,'panel-body')]/text()")
        area_price = ("".join(panel)).strip().split("-")
        flat_dict["properties"] = {
            "Fläche": area_price[0].strip(),
            "Warmmiete": area_price[1].strip(),
        }

        # empty defaults
        flat_dict["addr"] = ""
        flat_dict["kiez"] = ""

        kiez_s = re.search("wohnungen-in-Berlin-(.*)\.\d+.html", flat_dict["link"])
        if kiez_s:
            flat_dict["kiez"] = kiez_s.group(1)
        # umlauts
        flat_dict["kiez"] = flat_dict["kiez"].replace("oe", "ö")

        flat_dict["date_found"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

        # Besonderheiten
        flat_dict["features"] = []
        flat_dict["landlord"] = ""

        yield flat_dict
