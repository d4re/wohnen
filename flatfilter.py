import logging
import numbers
import re
from decimal import Decimal

import config

logger = logging.getLogger(__name__)


def filter_list(flats):
    flat_list = []

    for flat in flats:
        skip = False
        keep = False

        # first check, if we pick the flat due to match words (block list won't be considered)
        filter = config.search.filter

        for field, words in filter.allow.items():
            for word in words:
                if word in flat[field].lower():
                    logging.info(
                        f"Picked entry \"{flat['title']}\" due to \"{word}\" in {field}"
                    )
                    keep = True

        if keep:
            flat_list.append(flat)
            continue

        # now check the block list
        for field, words in filter.block.items():
            text = ""
            if field in flat:  # try direct fields
                text = flat[field].lower()
            elif field in flat["properties"]:  # try also properties
                text = flat["properties"][field].lower()

            for word in words:
                if word in text:
                    logging.info(
                        f"Skipped entry \"{flat['title']}\" due to \"{word}\" in {field}"
                    )
                    skip = True

        if skip:
            continue

        # now use the configured filter values as they were not necessarily applied correctly in the site scraper
        restrictions = config.search.flat_params
        props = flat["properties"]
        if area_str := props.get("area"):
            area = parse_number(area_str)
            if area < restrictions.area_min:
                logger.info(
                    f"Skipped appartment {flat['title']} due to area: {area_str}"
                )
                continue

        if rooms_str := props.get("rooms"):
            rooms = parse_number(rooms_str)
            if rooms < restrictions.rooms_min or rooms > restrictions.rooms_max:
                logger.info(
                    f"Skipped appartment {flat['title']} due to rooms: {rooms_str}"
                )
                continue

        if rent_str := props.get("rent_total"):
            rent = parse_number(rent_str)
            if rent > restrictions.rent_total_max:
                logger.info(
                    f"Skipped appartment {flat['title']} due to rent: {rent_str}"
                )
                continue

        flat_list.append(flat)

    return flat_list


def parse_number(number_str: str | int) -> Decimal:
    if isinstance(number_str, numbers.Number):
        return Decimal(f"{number_str:2}")
    else:
        # lets try to be localization independent
        # first only get the numbers part containing at most , and .
        number_str_stripped = re.sub(r"[^(\d.,)]", "", number_str)
        # since we are working with currencies there are two options,
        # either it is a whole number, or the third sign from the right is either a period or a comma
        # (or it was written very strangely in which case I guess we will fail)
        if len(number_str_stripped) > 3 and number_str_stripped[-3] == ".":
            # us format, just remove "," to allow for parsing
            number_str_clean = number_str_stripped.replace(",", "")
        elif len(number_str_stripped) > 3 and number_str_stripped[-3] == ",":
            # german format, remove "." and then convert the "," to "."
            number_str_clean = number_str_stripped.replace(".", "").replace(",", ".")
        else:
            # whole number, remove everything that's not a number
            number_str_clean = number_str_stripped.replace(".", "").replace(",", "")
        try:
            return Decimal(number_str_clean)
        except:
            logger.exception(f"Error parsing {number_str}")
            return Decimal(0)
