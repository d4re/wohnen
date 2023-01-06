import re

addr_parser = re.compile("^([a-zäöüß\s\d.,-]+?)?\s*([\d\s]+(?:\s?[-|+/]\s?\d+)?\s*[a-z]?)?[\s,]*(\d{5})\s*(.+)?$")

def parse_plz(addr: str) -> str:
    if match:= addr_parser.match(addr):
        plz = match.groups[2]
        return plz
    else:
        return ""