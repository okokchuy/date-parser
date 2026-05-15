from datetime import date
import pytest
from nldate import parse


def test_parse_invalid_input() -> None:
    with pytest.raises(ValueError):
        parse("pizza time")


def test_parse_today() -> None:
    assert parse("today", today=date(2025, 12, 1)) == date(2025, 12, 1)


def test_parse_tomorrow() -> None:
    assert parse("tomorrow", today=date(2025, 12, 1)) == date(2025, 12, 2)


def test_parse_yesterday() -> None:
    assert parse("yesterday", today=date(2025, 12, 1)) == date(2025, 11, 30)


def test_parse_in_days() -> None:
    assert parse("in 3 days", today=date(2025, 12, 1)) == date(2025, 12, 4)


def test_parse_days_ago() -> None:
    assert parse("3 days ago", today=date(2025, 12, 1)) == date(2025, 11, 28)


def test_parse_in_one_day() -> None:
    assert parse("in 1 day", today=date(2025, 12, 1)) == date(2025, 12, 2)


def test_parse_one_day_ago() -> None:
    assert parse("1 day ago", today=date(2025, 12, 1)) == date(2025, 11, 30)


def test_parse_next_tuesday() -> None:
    assert parse("next tuesday", today=date(2025, 12, 1)) == date(2025, 12, 2)


def test_parse_next_monday() -> None:
    assert parse("next monday", today=date(2025, 12, 1)) == date(2025, 12, 8)
