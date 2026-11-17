"""Property-based Hypothesis fuzz tests for the Lab 7 warranty-claims module."""

import math
from hypothesis import given, strategies as st
from warranty_claims import parse_claim, age_average, payable_charge


# Fuzz tests from starter scaffold: arbitrary strings and None must not crash.
@given(st.text() | st.none())
def test_parse_claim_no_crash(s):
    result = parse_claim(s)
    assert result is None or (
        isinstance(result, tuple)
        and len(result) == 2
        and isinstance(result[0], str)
        and len(result[0]) > 0
        and isinstance(result[1], float)
        and math.isfinite(result[1])
        and result[1] >= 0
    )


@given(st.text() | st.none())
def test_age_average_no_crash(s):
    result = age_average(s)
    assert result is None or (isinstance(result, int) and result >= 0)


@given(st.text() | st.none())
def test_payable_charge_no_crash(s):
    result = payable_charge(s)
    assert result is None or (
        isinstance(result, (int, float))
        and math.isfinite(result)
        and result >= 0
    )


# Property tests for valid generated inputs.
@given(
    st.sampled_from(["basic", "standard", "premium", "  standard ", "BASIC"]),
    st.integers(min_value=0, max_value=240),
)
def test_parse_claim_valid_inputs(plan, months):
    result = parse_claim(f"{plan}:{months}")
    assert result == (plan.strip().title(), float(months))


@given(st.lists(st.integers(min_value=0, max_value=1200), min_size=1, max_size=25))
def test_age_average_valid_integer_lists(values):
    csv_text = ",".join(str(v) for v in values)
    assert age_average(csv_text) == sum(values) // len(values)


@given(
    st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False),
    st.floats(min_value=0, max_value=1e6, allow_nan=False, allow_infinity=False),
)
def test_payable_charge_valid_inputs(charge, discount):
    text = f"{charge}|{discount}"
    result = payable_charge(text)
    expected = max(float(f"{charge}") * 1.18 - float(f"{discount}"), 0.0)
    assert result == expected
