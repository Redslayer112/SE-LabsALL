import pytest
from parking_fee import parking_fee, find_slot, monthly_pass

#Example test cases:
def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0

def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"

def test_unknown_vehicle():
    with pytest.raises(ValueError):
        parking_fee("bus", 60, False, False)

def test_negative_minutes():
    with pytest.raises(ValueError):
        parking_fee("car", -5, False, False)

def test_ev_partial_hour_lost_ticket():
    assert parking_fee("car", 90, True, True) == 230

def test_slot_full():
    assert find_slot("car", 0, False) == "full"

def test_slot_disabled():
    assert find_slot("car", 3, True) == "ground floor"

def test_slot_truck():
    assert find_slot("truck", 3, False) == "basement"

def test_pass_bike_resident():
    assert monthly_pass("bike", True) == 400

def test_pass_car():
    assert monthly_pass("car", False) == 1500

def test_pass_truck():
    with pytest.raises(ValueError):
        monthly_pass("truck", False)
