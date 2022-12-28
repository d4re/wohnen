from decimal import Decimal
import flatfilter


def test_parse_number():
    tests = {
        " €": Decimal("0"),
        "12 €": Decimal("12"),
        123: Decimal("123"),
        123.23: Decimal("123.23"),
        "123": Decimal("123"),
        "123.23": Decimal("123.23"),
        "1,234.33": Decimal("1234.33"),
        "1,234234.55": Decimal("1234234.55"),
        "123,23": Decimal("123.23"),
        "1.234,34": Decimal("1234.34"),
        "1.234234,34": Decimal("1234234.34"),
        "12.34.42,32": Decimal("123442.32"),
        "13,42,2.32": Decimal("13422.32"),
    }
    for val, expected in tests.items():
        assert flatfilter.parse_number(val) == expected
