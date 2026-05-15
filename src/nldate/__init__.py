from datetime import date, timedelta


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    if s == "today":
        return today

    if s == "tomorrow":
        return today + timedelta(days=1)

    if s == "yesterday":
        return today - timedelta(days=1)

    raise ValueError(f"Could not parse date: {s}")
