"""Hypothesis fuzz tests for the Lab 7 parking-fee application."""

import re
import string

import pytest
from hypothesis import given, strategies as st

from parking_fee import RATES, format_plate, hourly_rate, minutes_parked


@st.composite
def valid_time_ranges(draw):
    start = draw(st.integers(min_value=0, max_value=23 * 60 + 59))
    end = draw(st.integers(min_value=start, max_value=23 * 60 + 59))

    def clock(value):
        return f"{value // 60:02d}:{value % 60:02d}"

    return f"{clock(start)}-{clock(end)}"


@st.composite
def valid_plates(draw):
    first_letters = draw(st.text(alphabet=string.ascii_letters, min_size=2, max_size=2))
    first_digits = draw(st.text(alphabet=string.digits, min_size=2, max_size=2))
    second_letters = draw(st.text(alphabet=string.ascii_letters, min_size=2, max_size=2))
    last_digits = draw(st.text(alphabet=string.digits, min_size=4, max_size=4))
    return first_letters + first_digits + second_letters + last_digits


# Fuzz tests based on the supplied starter scaffold. Arbitrary text and None
# must either be handled correctly or rejected cleanly with ValueError.
@given(st.text() | st.none())
def test_minutes_parked_no_crash(value):
    try:
        result = minutes_parked(value)
    except ValueError:
        return
    assert isinstance(result, int)
    assert result >= 0


@given(st.text() | st.none())
def test_hourly_rate_no_crash(value):
    try:
        result = hourly_rate(value)
    except ValueError:
        return
    assert isinstance(value, str)
    normalized = value.strip().lower()
    assert normalized in RATES
    assert result == RATES[normalized]


@given(st.text() | st.none())
def test_format_plate_no_crash(value):
    try:
        result = format_plate(value)
    except ValueError:
        return
    assert isinstance(value, str)
    normalized = value.strip().upper()
    assert re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{2}[0-9]{4}", normalized)
    assert result == (
        normalized[:2] + " " + normalized[2:4] + " "
        + normalized[4:6] + " " + normalized[6:10]
    )


# Properties for valid generated inputs.
@given(valid_time_ranges())
def test_minutes_parked_matches_time_difference(times):
    entry, exit_time = times.split("-")
    start_h, start_m = map(int, entry.split(":"))
    end_h, end_m = map(int, exit_time.split(":"))
    expected = (end_h * 60 + end_m) - (start_h * 60 + start_m)
    assert minutes_parked(times) == expected


@given(
    st.sampled_from(["bike", "car", "truck"]),
    st.sampled_from(["", " ", "  ", "\t"]),
)
def test_hourly_rate_is_case_and_whitespace_insensitive(vehicle, padding):
    assert hourly_rate(padding + vehicle.upper() + padding) == RATES[vehicle]


@given(valid_plates())
def test_format_plate_formats_valid_generated_plates(plate):
    normalized = plate.upper()
    expected = (
        normalized[:2] + " " + normalized[2:4] + " "
        + normalized[4:6] + " " + normalized[6:10]
    )
    assert format_plate(plate) == expected


@pytest.mark.parametrize(
    "times",
    ["", "9:30-10:30", "24:00-25:00", "10:60-11:00", "11:00-10:00", "10:00/11:00"],
)
def test_minutes_parked_rejects_invalid_times(times):
    with pytest.raises(ValueError):
        minutes_parked(times)


@pytest.mark.parametrize("vehicle", ["", "plane", "car1"])
def test_hourly_rate_rejects_unknown_vehicles(vehicle):
    with pytest.raises(ValueError):
        hourly_rate(vehicle)


@pytest.mark.parametrize(
    "plate",
    ["", "KA01AB123", "KA01AB12345", "KA01-A1234", "1234567890"],
)
def test_format_plate_rejects_invalid_plates(plate):
    with pytest.raises(ValueError):
        format_plate(plate)
