import logging

import config

logger = logging.getLogger(__name__)


def filter_list(flats, search_config: config.Search):
    flat_list = []

    for flat in flats:
        skip = False
        keep = False

        # first check, if we pick the flat due to match words (block list won't be considered)
        filter = search_config.filter

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
            text = get_field(flat, field)

            for word in words:
                if word in text:
                    logging.info(
                        f"Skipped entry \"{flat['title']}\" due to \"{word}\" in {field}"
                    )
                    skip = True

        # now check the required list (the value of field should be one of the required values for the field)
        for field, words in filter.require.items():
            text = get_field(flat, field)

            if text:
                if not text in words:
                    logging.info(
                        f"Skipped entry \"{flat['title']}\" since \"{text}\" in {field} is not in required list"
                    )
                    skip = True

        if skip:
            continue

        # now use the configured filter values as they were not necessarily applied correctly in the site scraper
        restrictions = search_config.flat_params
        props = flat["properties"]
        if area := props.get("area"):
            if area < restrictions.area_min:
                logger.info(
                    f"Skipped appartment {flat['title']} due to area: {area}"
                )
                continue

        if rooms := props.get("rooms"):
            if rooms < restrictions.rooms_min or rooms > restrictions.rooms_max:
                logger.info(
                    f"Skipped appartment {flat['title']} due to rooms: {rooms}"
                )
                continue

        if rent := props.get("rent_total"):
            if restrictions.rent_base_min > rent > restrictions.rent_total_max:
                logger.info(
                    f"Skipped appartment {flat['title']} due to rent: {rent}"
                )
                continue

        flat_list.append(flat)

    return flat_list


def get_field(flat, field):
    text = ""
    if field in flat:  # try direct fields
        text = flat[field].lower()
    elif field in flat["properties"]:  # try also properties
        text = flat["properties"][field].lower()
    return text
