import pytest
from vending_machine import select_item, make_change, purchase

def test_invalid_item():
    assert select_item("water", {}, 100) == "invalid"

def test_sold_out_item():
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"

def test_insufficient_credit():
    assert select_item("cola", {"cola": 2}, 149) == "insufficient"

def test_valid_selection():
    assert select_item("cola", {"cola": 2}, 150) == "ok"

def test_no_change_needed():
    assert make_change(0) == []

def test_make_change_exact():
    assert make_change(185) == [100, 50, 25, 10]

def test_make_change_unrepresentable():
    assert make_change(1) is None

def test_negative_change_raises():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)

def test_purchase_rejected_selection():
    assert purchase("cola", {"cola": 0}, 200) == ("sold_out", [])

def test_successful_purchase_updates_stock():
    stock = {"chips": 2}
    assert purchase("chips", stock, 125) == ("dispensed", [25])
    assert stock["chips"] == 1

def test_purchase_no_exact_change(monkeypatch):
    import vending_machine
    monkeypatch.setattr(vending_machine, "make_change", lambda amount: None)
    stock = {"cola": 1}
    assert purchase("cola", stock, 200) == ("no_exact_change", [])
    assert stock["cola"] == 1
