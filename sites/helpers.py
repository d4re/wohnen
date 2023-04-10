import logging
import re
import numbers
import re
from decimal import Decimal
from typing import Union

addr_parser = re.compile("^([a-zäöüß\s\d.,-]+?)?\s*([\d\s]+(?:\s?[-|+/]\s?\d+)?\s*[a-z]?)?[\s,]*(\d{5})\s*(.+)?$")

def parse_plz(addr: str) -> str:
    addr = addr.lower()
    if match:= addr_parser.match(addr):
        plz = match.groups()[2]
        return plz
    else:
        return ""
    
NUMBER_TYPES = ["rooms", "area", "rent_total"]

def parse_number(number_str: Union[str, int]) -> float:
    if isinstance(number_str, numbers.Number):
        return float(number_str)
    else:
        # lets try to be localization independent
        # first only get the numbers part containing at most , and .
        number_str_stripped = re.sub(r"[^(\d.,)]", "", number_str)
        # since we are working with currencies or room count there are two options,
        # either it is a whole number, or the second or third sign from the right is either a period or a comma
        # (or it was written very strangely in which case I guess we will fail)
        if len(number_str_stripped) >= 3 and (number_str_stripped[-3] == "." or number_str_stripped[-2] == "."):
            # us format, just remove "," to allow for parsing
            number_str_clean = number_str_stripped.replace(",", "")
        elif len(number_str_stripped) >= 3 and (number_str_stripped[-3] == "," or number_str_stripped[-2] == ","):
            # german format, remove "." and then convert the "," to "."
            number_str_clean = number_str_stripped.replace(".", "").replace(",", ".")
        else:
            # whole number, remove everything that's not a number
            number_str_clean = number_str_stripped.replace(".", "").replace(",", "")
        try:
            return float(number_str_clean)
        except:
            logging.exception(f"Error parsing {number_str}")
            return float(0)
