"""Property-based fuzz tests for the vending-machine functions."""
from hypothesis import given, strategies as st

from vending_machine import parse_coins, slot_position, change_due


# Fuzz tests: arbitrary strings and None must not cause uncaught exceptions.
arbitrary_input = st.one_of(st.text(), st.none())


@given(arbitrary_input)
def test_parse_coins_no_crash(value):
    result = parse_coins(value)
    assert isinstance(result, list)


@given(arbitrary_input)
def test_slot_position_no_crash(value):
    result = slot_position(value)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and all(isinstance(part, int) for part in result)
    )


@given(arbitrary_input)
def test_change_due_no_crash(value):
    result = change_due(value)
    assert result is None or isinstance(result, str)


# Valid-input behavior checks.
@given(st.lists(st.integers(), min_size=1, max_size=20))
def test_parse_coins_valid_integer_lists(values):
    csv_value = ",".join(str(value) for value in values)
    assert parse_coins(csv_value) == values


@given(
    st.integers(min_value=0, max_value=25),
    st.integers(min_value=1, max_value=999),
)
def test_slot_position_valid_codes(row, column):
    code = chr(ord("A") + row) + str(column)
    assert slot_position(code) == (row, column - 1)


@given(
    st.integers(min_value=0, max_value=100000),
    st.integers(min_value=0, max_value=100000),
)
def test_change_due_valid_payments(extra, price):
    paid = price + extra
    expected = f"{extra // 5} five-coins"
    assert change_due(f"{paid}/{price}") == expected
