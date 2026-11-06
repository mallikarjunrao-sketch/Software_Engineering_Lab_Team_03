import pytest
from parking_fee import parking_fee, find_slot, monthly_pass


# ================= parking_fee =================
# vehicle in HOURLY_RATE: False / True
def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)


def test_known_vehicle_valid():
    assert parking_fee("bike", 60, False, False) == 10


# minutes < 0: True / False
def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -1, False, False)


# minutes <= 30: True / False (boundary 30 and 31)
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_boundary_30_minutes_free():
    assert parking_fee("car", 30, False, False) == 0


def test_boundary_31_minutes_charged():
    assert parking_fee("car", 31, False, False) == 30


def test_zero_minutes():
    assert parking_fee("car", 0, False, False) == 0


# minutes % 60 != 0: True / False
def test_exact_hours_no_rounding():
    assert parking_fee("car", 120, False, False) == 60


def test_partial_hour_rounds_up():
    assert parking_fee("truck", 61, False, False) == 120


# is_ev and vehicle != "truck": (F), (T,F), (T,T)
def test_not_ev():
    assert parking_fee("car", 120, False, False) == 60


def test_ev_truck_no_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_ev_car_half_fee():
    assert parking_fee("car", 120, True, False) == 30


def test_ev_bike_half_fee():
    assert parking_fee("bike", 60, True, False) == 5


# lost_ticket: True / False
def test_lost_ticket_penalty():
    assert parking_fee("car", 120, False, True) == 260


def test_lost_ticket_with_free_stay():
    assert parking_fee("car", 10, False, True) == 200


def test_ev_and_lost_ticket_combined():
    assert parking_fee("car", 120, True, True) == 230


# ================= find_slot =================
# free_slots <= 0: True / False (boundary 0, 1, negative)
def test_slot_full_zero():
    assert find_slot("car", 0, False) == "full"


def test_slot_full_negative():
    assert find_slot("car", -3, False) == "full"


def test_slot_one_left():
    assert find_slot("car", 1, False) == "any floor"


# is_disabled: True / False
def test_slot_disabled():
    assert find_slot("car", 5, True) == "ground floor"


def test_slot_disabled_truck_priority():
    assert find_slot("truck", 5, True) == "ground floor"


def test_slot_full_beats_disabled():
    assert find_slot("car", 0, True) == "full"


# vehicle == "truck": True / False
def test_slot_truck_basement():
    assert find_slot("truck", 5, False) == "basement"


def test_slot_bike_any_floor():
    assert find_slot("bike", 5, False) == "any floor"


# ================= monthly_pass =================
# bike / car / else, and is_resident True / False
def test_pass_bike_non_resident():
    assert monthly_pass("bike", False) == 500


def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400


def test_pass_car_non_resident():
    assert monthly_pass("car", False) == 1500


def test_pass_car_resident():
    assert monthly_pass("car", True) == 1200


def test_pass_truck_invalid():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)


def test_pass_unknown_invalid():
    with pytest.raises(ValueError):
        monthly_pass("bus", True)
