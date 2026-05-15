from datetime import date

from nldate import parse


def test_parse_today() -> None:
    assert parse("today", today=date(2025, 12, 1)) == date(2025, 12, 1)

def test_parse_tomorrow() -> None:
    assert parse("tomorrow", today=date(2025, 12, 1)) == date(2025, 12, 2)


def test_parse_yesterday() -> None:
    assert parse("yesterday", today=date(2025, 12, 1)) == date(2025, 11, 30)
