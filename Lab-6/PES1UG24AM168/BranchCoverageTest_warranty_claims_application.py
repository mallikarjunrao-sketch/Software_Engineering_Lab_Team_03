import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ================= out_of_warranty_charge =================
# plan not in COVERED_MONTHS: True / False
def test_unknown_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_known_plans_valid():
    assert out_of_warranty_charge("basic", 12, "defect", False) == 0
    assert out_of_warranty_charge("standard", 24, "defect", False) == 0
    assert out_of_warranty_charge("premium", 36, "defect", False) == 0


# age_months < 0: True / False
def test_negative_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("basic", -1, "defect", False)


def test_zero_age():
    assert out_of_warranty_charge("basic", 0, "defect", False) == 0


# is_registered and plan != "premium": (T, T), (T, F), (F)
def test_registered_non_premium_adds_six_months():
    assert out_of_warranty_charge("basic", 18, "defect", True) == 0
    assert out_of_warranty_charge("standard", 30, "defect", True) == 0


def test_registered_premium_no_bonus_months():
    assert out_of_warranty_charge("premium", 37, "defect", True) == 100


def test_unregistered_no_bonus_months():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


# excess <= 0: True (negative and 0) / False (> 0)
def test_within_warranty_negative_excess():
    assert out_of_warranty_charge("standard", 10, "defect", False) == 0


def test_boundary_exact_warranty_expiry():
    assert out_of_warranty_charge("basic", 12, "defect", False) == 0


def test_boundary_one_month_excess():
    assert out_of_warranty_charge("basic", 13, "defect", False) == 100


# claim_type == "accidental": True / False (with excess <= 12)
def test_accidental_moderate_excess():
    assert out_of_warranty_charge("basic", 24, "accidental", False) == 2400


def test_defect_moderate_excess():
    assert out_of_warranty_charge("basic", 24, "defect", False) == 1200


# excess > 12: True / False, and nested claim_type == "accidental": True / False
def test_accidental_high_excess_surcharge():
    assert out_of_warranty_charge("basic", 25, "accidental", False) == 3575


def test_defect_high_excess_surcharge():
    assert out_of_warranty_charge("basic", 25, "defect", False) == 1950


# ================= claim_allowed =================
# is_recall: True (claims_filed <= 5 and > 5) / False
def test_recall_within_limit():
    assert claim_allowed(5, 5, True) is True


def test_recall_exceeds_limit():
    assert claim_allowed(60, 6, True) is False


# days_since_last_claim < 30: True / False (boundary 29 and 30)
def test_non_recall_too_soon():
    assert claim_allowed(29, 0, False) is False


def test_non_recall_boundary_30_days_within_limit():
    assert claim_allowed(30, 2, False) is True


def test_non_recall_exceeds_claim_limit():
    assert claim_allowed(60, 3, False) is False


# ================= sla_status =================
# is_hardware: True / False, is_priority: True / False
# hours_left >= cutoff (on_track), >= cutoff - 12 (at_risk), < cutoff - 12 (critical)
def test_sla_hardware_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_sla_hardware_priority_at_risk():
    assert sla_status(60, True, True) == "at_risk"


def test_sla_hardware_priority_critical():
    assert sla_status(59, True, True) == "critical"


def test_sla_hardware_non_priority_on_track():
    assert sla_status(48, True, False) == "on_track"


def test_sla_software_priority_at_risk():
    assert sla_status(36, False, True) == "at_risk"


def test_sla_software_non_priority_on_track():
    assert sla_status(24, False, False) == "on_track"


def test_sla_software_non_priority_at_risk():
    assert sla_status(12, False, False) == "at_risk"


def test_sla_software_non_priority_critical():
    assert sla_status(11, False, False) == "critical"
