# tests/test_units/test_state_manager.py
import pytest
from datetime import datetime, timedelta
from core.state_manager import ParkingStateManager, CapacityExceededError

@pytest.fixture
def state_manager():
    mgr = ParkingStateManager()
    mgr.state["A1"]["threshold"] = 100
    mgr.state["A1"]["rates"]["sedan"] = 2.5
    return mgr

def test_vehicle_entry_exit(state_manager):
    # Test basic increment/decrement
    state_manager.update_vehicle_count("A1", "ENTER", {"nft_id": "001"})
    assert state_manager.state["A1"]["count"] == 1
    
    state_manager.update_vehicle_count("A1", "EXIT", {"nft_id": "001"})
    assert state_manager.state["A1"]["count"] == 0

def test_capacity_exception(state_manager):
    # Fill parking lot
    for i in range(100):
        state_manager.update_vehicle_count("A1", "ENTER", {"nft_id": str(i)})
    
    with pytest.raises(CapacityExceededError):
        state_manager.update_vehicle_count("A1", "ENTER", {"nft_id": "101"})

@pytest.mark.parametrize("count,expected", [
    (50, 2.5),    # Base rate
    (90, 2.5*(1+0.9**2)), 
    (100, 2.5*(1+1**2))
])
def test_dynamic_pricing(state_manager, count, expected):
    state_manager.state["A1"]["count"] = count
    price = state_manager.dynamic_pricing("A1", "sedan")
    assert price == pytest.approx(expected, rel=0.01)

def test_capacity_history(state_manager):
    test_time = datetime.utcnow()
    with patch('datetime.datetime') as mock_datetime:
        mock_datetime.utcnow.return_value = test_time
        
        state_manager.update_vehicle_count("A1", "ENTER", {"nft_id": "001"})
        assert state_manager.state["A1"]["capacity_history"] == [{
            "timestamp": test_time.isoformat(),
            "count": 1,
            "threshold": 100
        }]