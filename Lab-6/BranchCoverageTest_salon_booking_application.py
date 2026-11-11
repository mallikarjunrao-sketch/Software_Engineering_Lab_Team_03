import pytest
from salon_booking import extra_time_charge, can_book, arrival_status


# ================= extra_time_charge =================
# service not in INCLUDED_MIN: True / False
def test_unknown_service():
    with pytest.raises(ValueError):
        extra_time_charge("manicure", 30, "junior", False)


def test_known_services_valid():
    assert extra_time_charge("haircut", 30, "junior", False) == 0
    assert extra_time_charge("colour", 60, "junior", False) == 0
    assert extra_time_charge("spa", 90, "junior", False) == 0


# duration_min < 0: True / False
def test_negative_duration():
    with pytest.raises(ValueError):
        extra_time_charge("haircut", -1, "junior", False)


def test_zero_duration():
    assert extra_time_charge("haircut", 0, "junior", False) == 0


# is_member and service != "spa": (T, T), (T, F), (F)
def test_member_non_spa_gets_15_extra_minutes():
    assert extra_time_charge("haircut", 45, "junior", True) == 0
    assert extra_time_charge("colour", 75, "junior", True) == 0


def test_member_spa_no_extra_minutes():
    # spa stays at 90 included minutes even for members
    assert extra_time_charge("spa", 91, "junior", True) == 10


def test_non_member_no_extra_minutes():
    assert extra_time_charge("haircut", 31, "junior", False) == 10


# extra <= 0: True (negative and 0) / False (> 0)
def test_negative_extra():
    assert extra_time_charge("colour", 40, "junior", False) == 0


def test_boundary_exactly_included_time():
    assert extra_time_charge("haircut", 30, "junior", False) == 0


def test_boundary_one_extra_minute():
    assert extra_time_charge("haircut", 31, "junior", False) == 10


# stylist_level == "junior": True / False (with extra <= 60)
def test_junior_rate():
    assert extra_time_charge("haircut", 50, "junior", False) == 200


def test_non_junior_rate():
    assert extra_time_charge("haircut", 50, "senior", False) == 360


# extra > 60: True / False (boundary 60 and 61)
def test_boundary_extra_60_no_surcharge():
    assert extra_time_charge("haircut", 90, "junior", False) == 600


def test_boundary_extra_61_surcharge():
    # junior: 10 + 8 = 18 per minute
    assert extra_time_charge("haircut", 91, "junior", False) == 1098


# nested stylist_level == "senior" inside extra > 60: True / False
def test_senior_long_overrun():
    # 18 + 8 + 4 = 30 per minute
    assert extra_time_charge("haircut", 100, "senior", False) == 2100


def test_mid_level_long_overrun():
    # not junior, not senior: 18 + 8 = 26 per minute
    assert extra_time_charge("haircut", 100, "mid", False) == 1820


# ================= can_book =================
# is_walk_in: True (party <= 2 and > 2) / False
def test_walk_in_within_limit():
    assert can_book(2, 1, True) is True


def test_walk_in_exceeds_limit():
    assert can_book(3, 1, True) is False


# party_size > 4: True / False (boundary 4 and 5)
def test_booking_party_too_large():
    assert can_book(5, 1, False) is False


def test_booking_boundary_party_4_services_2():
    assert can_book(4, 2, False) is True


def test_booking_too_many_services():
    assert can_book(4, 3, False) is False


# ================= arrival_status =================
# is_colour: True / False, is_weekend: True / False
# minutes_early >= cutoff (open), >= cutoff - 15 (late), below (closed)
def test_colour_weekday_open():
    assert arrival_status(10, True, False) == "open"


def test_colour_weekday_late():
    assert arrival_status(-5, True, False) == "late"


def test_colour_weekday_closed():
    assert arrival_status(-6, True, False) == "closed"


def test_colour_weekend_open():
    assert arrival_status(20, True, True) == "open"


def test_colour_weekend_late():
    assert arrival_status(5, True, True) == "late"


def test_colour_weekend_closed():
    assert arrival_status(4, True, True) == "closed"


def test_regular_weekday_open():
    assert arrival_status(5, False, False) == "open"


def test_regular_weekday_late():
    assert arrival_status(4, False, False) == "late"


def test_regular_weekday_closed():
    assert arrival_status(-11, False, False) == "closed"


def test_regular_weekend_open():
    assert arrival_status(15, False, True) == "open"


def test_regular_weekend_late():
    assert arrival_status(0, False, True) == "late"


def test_regular_weekend_closed():
    assert arrival_status(-1, False, True) == "closed"
