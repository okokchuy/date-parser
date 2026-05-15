from datetime import date, timedelta
import calendar
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

MONTHS = {
    "january": 1,
    "jan": 1,
    "february": 2,
    "feb": 2,
    "march": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "may": 5,
    "june": 6,
    "jun": 6,
    "july": 7,
    "jul": 7,
    "august": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "october": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "december": 12,
    "dec": 12,
}

NUMBERS = {
    "a": 1,
    "an": 1,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
}


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()

    text = s.strip().lower()
    text = re.sub(r"\s+", " ", text)

    direct = _parse_direct_date(text)
    if direct is not None:
        return direct

    if text == "today":
        return today

    if text == "now":
        return today

    if text == "tomorrow":
        return today + timedelta(days=1)

    if text == "yesterday":
        return today - timedelta(days=1)

    if text == "the day after tomorrow":
        return today + timedelta(days=2)

    if text == "the day before yesterday":
        return today - timedelta(days=2)

    match = re.fullmatch(r"next (\w+)", text)
    if match is not None:
        weekday_name = match.group(1)
        if weekday_name not in WEEKDAYS:
            raise ValueError(f"Could not parse date: {s}")
        days_until = (WEEKDAYS[weekday_name] - today.weekday()) % 7
        if days_until == 0:
            days_until = 7
        return today + timedelta(days=days_until)

    match = re.fullmatch(r"last (\w+)", text)
    if match is not None:
        weekday_name = match.group(1)
        if weekday_name not in WEEKDAYS:
            raise ValueError(f"Could not parse date: {s}")
        days_ago = (today.weekday() - WEEKDAYS[weekday_name]) % 7
        if days_ago == 0:
            days_ago = 7
        return today - timedelta(days=days_ago)

    match = re.fullmatch(r"in (.+)", text)
    if match is not None:
        return _apply_duration(today, match.group(1), 1)

    match = re.fullmatch(r"(.+) ago", text)
    if match is not None:
        return _apply_duration(today, match.group(1), -1)

    match = re.fullmatch(r"(.+) (after|from) (.+)", text)
    if match is not None:
        base = parse(match.group(3), today=today)
        return _apply_duration(base, match.group(1), 1)

    match = re.fullmatch(r"(.+) before (.+)", text)
    if match is not None:
        base = parse(match.group(2), today=today)
        return _apply_duration(base, match.group(1), -1)

    raise ValueError(f"Could not parse date: {s}")


def _parse_direct_date(text: str) -> date | None:
    try:
        return date.fromisoformat(text)
    except ValueError:
        pass

    cleaned = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", text)
    cleaned = cleaned.replace(".", "")

    match = re.fullmatch(r"(\w+) (\d{1,2}),? (\d{4})", cleaned)
    if match is not None:
        month_name, day_text, year_text = match.groups()
        if month_name not in MONTHS:
            return None
        return date(int(year_text), MONTHS[month_name], int(day_text))

    match = re.fullmatch(r"(\d{4})/(\d{1,2})/(\d{1,2})", cleaned)
    if match is not None:
        year_text, month_text, day_text = match.groups()
        return date(int(year_text), int(month_text), int(day_text))

    match = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", cleaned)
    if match is not None:
        month_text, day_text, year_text = match.groups()
        return date(int(year_text), int(month_text), int(day_text))

    return None


def _apply_duration(base: date, duration: str, sign: int) -> date:
    years = 0
    months = 0
    days = 0

    parts = re.findall(r"(\d+|[a-z]+) (days?|weeks?|months?|years?)", duration)
    if not parts:
        raise ValueError(f"Could not parse duration: {duration}")

    for amount_text, unit in parts:
        amount = _parse_number(amount_text)
        if unit.startswith("day"):
            days += amount
        elif unit.startswith("week"):
            days += amount * 7
        elif unit.startswith("month"):
            months += amount
        elif unit.startswith("year"):
            years += amount

    result = _add_months(base, sign * (years * 12 + months))
    return result + timedelta(days=sign * days)


def _parse_number(text: str) -> int:
    if text.isdigit():
        return int(text)
    if text in NUMBERS:
        return NUMBERS[text]
    raise ValueError(f"Could not parse number: {text}")


def _add_months(base: date, months: int) -> date:
    month_index = base.month - 1 + months
    year = base.year + month_index // 12
    month = month_index % 12 + 1
    last_day = calendar.monthrange(year, month)[1]
    day = min(base.day, last_day)
    return date(year, month, day)
