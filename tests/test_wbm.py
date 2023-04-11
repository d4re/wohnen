from numbers import Number
from sites.helpers import NUMBER_TYPES
from sites.wbm import parser, scraper


def test_parser():
    with open("tests/samples/wbm.html") as f:
        sample_html = f.read()
    flats = list(parser.parse(sample_html))
    for flat in flats:
        properties = flat["properties"]
        for prop in NUMBER_TYPES:
            assert prop in properties
            assert isinstance(properties[prop], Number)