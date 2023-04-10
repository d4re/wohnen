from decimal import Decimal

from sites.helpers import parse_number


def test_parse_number():
    tests = {
        "805.1 €": 805.1,
        "1.5 rooms": 1.5,
        " €": 0,
        "12 €": 12,
        123: 123,
        123.23: 123.23,
        "123": 123,
        "123.23": 123.23,
        "1,234.33": 1234.33,
        "1,234234.55": 1234234.55,
        "123,23": 123.23,
        "1.234,34": 1234.34,
        "1.234234,34": 1234234.34,
        "12.34.42,32": 123442.32,
        "13,42,2.32": 13422.32,
    }
    for val, expected in tests.items():
        assert parse_number(val) == expected
