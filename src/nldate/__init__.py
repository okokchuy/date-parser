from datetime import date, timedelta
import re


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    if s == "today":
        return today

    if s == "tomorrow":
        return today + timedelta(days=1)

    if s == "yesterday":
        return today - timedelta(days=1)

    match = re.fullmatch(r"in (\d+) days", s)
    if match is not None:
        num_days = int(match.group(1))
        return today + timedelta(days=num_days)

    match = re.fullmatch(r"(\d+) days ago", s)
    if match is not None:
        num_days = int(match.group(1))
        return today - timedelta(days=num_days)

    raise ValueError(f"Could not parse date: {s}")
