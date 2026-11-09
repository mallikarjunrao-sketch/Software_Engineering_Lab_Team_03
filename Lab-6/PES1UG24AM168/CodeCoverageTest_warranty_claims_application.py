import pytest
from warranty_claims import out_of_warranty_charge, claim_allowed, sla_status


# ---------- out_of_warranty_charge ----------
def test_within_warranty():
    assert out_of_warranty_charge("standard", 20, "defect", False) == 0


def test_unknown_plan():
    with pytest.raises(ValueError):
        out_of_warranty_charge("gold", 10, "defect", False)


def test_negative_age():
    with pytest.raises(ValueError):
        out_of_warranty_charge("basic", -3, "defect", False)


def test_registered_bonus_months():
    assert out_of_warranty_charge("basic", 16, "defect", True) == 0


def test_defect_out_of_warranty():
    assert out_of_warranty_charge("basic", 15, "defect", False) == 300


def test_accidental_high_excess():
    assert out_of_warranty_charge("basic", 30, "accidental", False) == 4950


# ---------- claim_allowed ----------
def test_claim_recall():
    assert claim_allowed(10, 4, True) is True


def test_claim_too_recent():
    assert claim_allowed(15, 1, False) is False


def test_claim_allowed_standard():
    assert claim_allowed(60, 1, False) is True


# ---------- sla_status ----------
def test_sla_hardware_priority_on_track():
    assert sla_status(72, True, True) == "on_track"


def test_sla_software_at_risk():
    assert sla_status(18, False, False) == "at_risk"


def test_sla_software_critical():
    assert sla_status(5, False, False) == "critical"
