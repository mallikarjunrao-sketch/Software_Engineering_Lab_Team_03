import pytest
import vending_machine
from vending_machine import select_item, make_change, purchase

def test_select_item_all_outcomes():
    assert select_item("water", {}, 100) == "invalid"
    assert select_item("cola", {"cola": 0}, 200) == "sold_out"
    assert select_item("cola", {"cola": 1}, 149) == "insufficient"
    assert select_item("cola", {"cola": 1}, 150) == "ok"

def test_make_change_negative_and_all_coin_loops():
    with pytest.raises(ValueError, match="negative amount"):
        make_change(-1)
    assert make_change(0) == []
    assert make_change(190) == [100, 50, 25, 10, 5]
    assert make_change(1) is None

def test_purchase_rejected():
    stock = {"cola": 0}
    assert purchase("cola", stock, 200) == ("sold_out", [])
    assert stock["cola"] == 0

def test_purchase_dispenses_and_decrements_stock():
    stock = {"cola": 2}
    assert purchase("cola", stock, 200) == ("dispensed", [50])
    assert stock["cola"] == 1

def test_purchase_no_exact_change_branch(monkeypatch):
    monkeypatch.setattr(vending_machine, "make_change", lambda amount: None)
    stock = {"candy": 2}
    assert purchase("candy", stock, 100) == ("no_exact_change", [])
    assert stock["candy"] == 2
