import datetime
import json
import logging
import re
from urllib.parse import quote, urljoin

from lxml import html

logger = logging.getLogger(__name__)

feature_map = {
    "AVAILABLE_FOR_RENT": "Sofort verfügbar",
    "BECOMING_AVAILABLE_FOR_RENT": "Demnächst verfügbar",
    "FULLY_RENOVATED": "Komplett renoviert",
    "FULLY_RESTRUCTURED": "Komplett umgebaut",
    "PASSENGER_LIFT": "Aufzug",
    "BALCONY": "Balkon",
    "LOGGIA": "Loggia",
    "TERRACE": "Terasse",
    "GARAGE": "Garage",
    "GARDEN": "Garten",
    "GARDEN_SHARED": "Garten zum Mitbenutzen",
    "UNDERGROUND_PARKING": "Tiefgarage",
    "PARKING_AREA": "Stellplatz",
    "BATH_WITH_WINDOW": "Bad mit Fenster",
    "BATH_WITH_TUB": "Bad mit Wanne",
    "FITTED_KITCHEN": "Einbauküche",
    "CELLAR_SHARE": "Kellerabteil",
    "NEW_BUILDING": "Neubau",
    "NEW_BUILDING_STANDARD": "Neubaustandard",
    "OLD_BUILDING": "Altbau",
    "BARRIER_FREE": "Barrierefrei",
    "GROUND_FLOOR": "Erdgeschoss",
    "PETS_ALLOWED": "Haustiere erlaubt",
    "FLAT_SHARE_POSSIBLE": "WG tauglich",
    "WHEELCHAIR_ACCESSIBLE": "Rollstuhlgerecht",
    "PARTLY_FURNISHED": "Teilmöbliert",
    "FULLY_FURNISHED": "Möbliert",
}

price_type_map = {
    "RENT_INCLUDING_HEATING": "rent_total",
    "COLD_RENT": "Kaltmiete",
    "NET_COLD_RENT": "Nettokaltmiete",
    "SQUARE_METER_PRICE": "Euro/m²",
}


def parse(html_input):

    object_url = "https://www.immowelt.de/expose/"

    if isinstance(html, bytes):
        html_input = html_input.decode("utf-8")

    result = None
    for line in html_input.split("\n"):
        if '<script type="application/json" data-hypernova-key="searchui"' in line:
            json_s = re.search("<!--(.*)-->", line)
            if json_s:
                result = json.loads(json_s.group(1))
            break

    all_flats = result["initialState"]["estateSearch"]["data"]["estates"]

    logger.info("Will parse {} flats".format(len(all_flats)))

    for flat in all_flats:
        flat_dict = {}

        flat_dict["title"] = flat["title"]
        flat_dict["id"] = flat["id"]

        flat_dict["pos"] = {
            "long": flat["place"]["point"]["lon"],
            "lat": flat["place"]["point"]["lat"],
        }

        addr = ""
        if "street" in flat["place"]:
            addr += flat["place"]["street"]
        if "houseNumber" in flat["place"]:
            addr += f" {flat['place']['houseNumber']}, "
        flat_dict["addr"] = f"{addr}{flat['place']['postcode']} {flat['place']['city']}"
        flat_dict["plz"] = flat['place']['postcode']
        flat_dict["kiez"] = ""
        if "district" in flat["place"]:
            flat_dict["kiez"] = flat["place"]["district"]

        flat_dict["link"] = quote(urljoin(object_url, flat["onlineId"]), safe=":/")

        # Bild
        if "pictures" in flat and len(flat["pictures"]) > 0:
            flat_dict["image"] = quote(flat["pictures"][0]["imageUri"], safe=":/")

        flat_dict["date_found"] = datetime.datetime.fromisoformat(
            flat["timestamp"].replace("Z", "+00:00")
        ).strftime("%d.%m.%Y %H:%M")

        flat_dict["properties"] = {
            "rooms": flat["roomsMin"],
            "area": f"{flat['primaryArea']['sizeMin']} m²",
        }
        if "contructionYear" in flat:
            flat_dict["properties"]["Baujahr"] = flat["constructionYear"]
        for price in flat["prices"]:
            if "type" not in price:
                continue
            # special case: omit duplicate if cold rent is already a property
            if (
                price["type"] == "NET_COLD_RENT"
                and "Kaltmiete" in flat_dict["properties"]
            ):
                continue
            if price["type"] in price_type_map:
                name = price_type_map[price["type"]]
            else:
                name = price["type"]
            flat_dict["properties"][name] = f"{price['amountMin']} €"

        flat_dict["features"] = []
        for feature in flat["features"]:
            if feature in feature_map:
                flat_dict["features"].append(feature_map[feature])
            else:
                flat_dict["features"].append(feature)

        flat_dict["landlord"] = ""
        if (
            "companyName" in flat["broker"]
            and flat["broker"]["companyName"] is not None
            and len(flat["broker"]["companyName"]) > 0
        ):
            flat_dict["landlord"] = flat["broker"]["companyName"]

        yield flat_dict
