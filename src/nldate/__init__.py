from datetime import date, timedelta
import re


WEEKDAYS = {
    "monday": 0,
    "tuesday": 1,
    "wednesday": 2,
    "thursday": 3,
    "friday": 4,
    "saturday": 5,
    "sunday": 6,
}


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    if s == "today":
        return today

    if s == "tomorrow":
        return today + timedelta(days=1)

    if s == "yesterday":
        return today - timedelta(days=1)

    match = re.fullmatch(r"in (\d+) days?", s)
    if match is not None:
        num_days = int(match.group(1))
        return today + timedelta(days=num_days)

    match = re.fullmatch(r"(\d+) days? ago", s)
    if match is not None:
        num_days = int(match.group(1))
        return today - timedelta(days=num_days)

    match = re.fullmatch(r"next (\w+)", s)
    if match is not None:
        weekday_name = match.group(1)
        target_weekday = WEEKDAYS[weekday_name]
        days_until = (target_weekday - today.weekday()) % 7

        if days_until == 0:
            days_until = 7

        return today + timedelta(days=days_until)

    raise ValueError(f"Could not parse date: {s}")
