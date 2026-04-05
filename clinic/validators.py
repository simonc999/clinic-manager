from __future__ import annotations

from datetime import datetime


DATE_FORMAT = "%Y-%m-%d"


def is_valid_date(value: str) -> bool:
    try:
        datetime.strptime(value, DATE_FORMAT)
        return True
    except ValueError:
        return False


def require_valid_date(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if is_valid_date(value):
            return value
        print("Invalid date. Use the YYYY-MM-DD format.")


def require_positive_integer(prompt: str) -> int:
    while True:
        raw_value = input(prompt).strip()
        if raw_value.isdigit() and int(raw_value) > 0:
            return int(raw_value)
        print("Please enter a positive integer.")
