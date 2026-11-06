import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ---------- parking_fee ----------
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -5, False, False)


def test_exact_hours_no_rounding():
    assert parking_fee("car", 120, False, False) == 60


def test_partial_hour_rounds_up():
    assert parking_fee("car", 90, False, False) == 60


def test_ev_car_half_fee():
    assert parking_fee("car", 120, True, False) == 30


def test_lost_ticket_penalty():
    assert parking_fee("car", 120, False, True) == 260


# ---------- find_slot ----------
def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_slot_full():
    assert find_slot("car", 0, False) == "full"


def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_truck_basement():
    assert find_slot("truck", 5, False) == "basement"


# ---------- monthly_pass ----------
def test_pass_bike():
    assert monthly_pass("bike", False) == 500


def test_pass_car_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_invalid_vehicle():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
