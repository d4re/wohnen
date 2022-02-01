import logging
import config

logger = logging.getLogger(__name__)

def filter_list(flats):
    flat_list = []

    for flat in flats:
        skip = False
        keep = False

        # first check, if we pick the flat due to match words (block list won't be considered)
        for field in config.filter['allow']:
            for word in config.filter['allow'][field]:
                if word in flat[field].lower():
                    logging.info(f"Picked entry \"{flat['title']}\" due to \"{word}\" in {field}")
                    keep = True
        if keep:
            flat_list.append(flat)
            continue
        
        # now check the block list
        for field in config.filter['block']:
            if field in flat:                 # try direct fields
                string = flat[field].lower()
            elif field in flat['properties']: # try also properties
                string = flat['properties'][field].lower()

            for word in config.filter['block'][field]:
                if word in string:
                    logging.info(f"Skipped entry \"{flat['title']}\" due to \"{word}\" in {field}")
                    skip = True
        if not skip:
            flat_list.append(flat)

    return flat_list