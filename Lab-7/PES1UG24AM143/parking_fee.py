"""Parking fee helper functions for Lab 7 fuzz testing.

Input rules:
- Parking times use 24-hour HH:MM-HH:MM format and refer to the same day.
- Vehicle names are bike, car, or truck (case/outer whitespace ignored).
- Registration plates use the format LLDDLLDDDD (e.g. KA01AB1234).
Invalid input is reported consistently with ValueError.
"""

import re

RATES = {"bike": 10, "car": 30, "truck": 60}

_TIME_RANGE = re.compile(
    r"^(?:[01][0-9]|2[0-3]):[0-5][0-9]-(?:[01][0-9]|2[0-3]):[0-5][0-9]$"
)
_PLATE = re.compile(r"^[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}$")


def minutes_parked(times):
    """Return the number of minutes between two same-day HH:MM times."""
    if not isinstance(times, str) or not _TIME_RANGE.fullmatch(times):
        raise ValueError("time range must be in HH:MM-HH:MM 24-hour format")

    entry, exit_time = times.split("-")
    h1, m1 = map(int, entry.split(":"))
    h2, m2 = map(int, exit_time.split(":"))

    start = h1 * 60 + m1
    end = h2 * 60 + m2
    if end < start:
        raise ValueError("exit time must not be earlier than entry time")

    return end - start


def hourly_rate(vehicle):
    """Return the hourly rate for bike, car, or truck."""
    if not isinstance(vehicle, str):
        raise ValueError("vehicle must be a string")

    normalized = vehicle.strip().lower()
    if normalized not in RATES:
        raise ValueError("unknown vehicle")

    return RATES[normalized]


def format_plate(plate):
    """Validate and format a plate such as ka01ab1234 as KA 01 AB 1234."""
    if not isinstance(plate, str):
        raise ValueError("plate must be a string")

    normalized = plate.strip().upper()
    if not _PLATE.fullmatch(normalized):
        raise ValueError("plate must contain 2 letters, 2 digits, 2 letters, 4 digits")

    return (
        normalized[:2]
        + " "
        + normalized[2:4]
        + " "
        + normalized[4:6]
        + " "
        + normalized[6:10]
    )


def main():
    print("==== Running minutes_parked ====")
    user_input = input("Enter entry and exit time (e.g. 09:30-11:45): ")
    result = minutes_parked(user_input)
    print("Minutes Parked:", result)

    print("\n==== Running hourly_rate ====")
    user_input = input("Enter vehicle type (bike/car/truck): ")
    result = hourly_rate(user_input)
    print("Hourly Rate:", result)

    print("\n==== Running format_plate ====")
    user_input = input("Enter a number plate (e.g. ka01ab1234): ")
    result = format_plate(user_input)
    print("Formatted Plate:", result)


if __name__ == "__main__":
    main()
