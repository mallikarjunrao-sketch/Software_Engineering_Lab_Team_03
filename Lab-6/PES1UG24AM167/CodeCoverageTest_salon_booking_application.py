import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ---------- extra_time_charge ----------
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0


def test_unknown_service():
    with pytest.raises(ValueError):
        extra_time_charge("manicure", 30, "junior", False)


def test_negative_duration():
    with pytest.raises(ValueError):
        extra_time_charge("haircut", -5, "junior", False)


def test_member_gets_extra_15_minutes():
    # haircut 30 + 15 member minutes = 45 included
    assert extra_time_charge("haircut", 40, "junior", True) == 0


def test_junior_extra_time():
    # 20 extra minutes at 10 per minute
    assert extra_time_charge("haircut", 50, "junior", False) == 200


def test_senior_long_overrun():
    # 70 extra minutes at 18 + 8 + 4 = 30 per minute
    assert extra_time_charge("haircut", 100, "senior", False) == 2100


# ---------- can_book ----------
def test_can_book():
    assert can_book(2, 1, False) is True


def test_walk_in_small_party():
    assert can_book(2, 1, True) is True


def test_party_too_large():
    assert can_book(5, 1, False) is False


# ---------- arrival_status ----------
def test_colour_weekend_open():
    assert arrival_status(20, True, True) == "open"


def test_regular_weekday_late():
    assert arrival_status(0, False, False) == "late"


def test_regular_weekday_closed():
    assert arrival_status(-20, False, False) == "closed"
