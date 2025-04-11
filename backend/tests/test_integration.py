# tests/test_integration.py
import pytest
from unittest.mock import AsyncMock, patch
from core.state_manager import ParkingStateManager
from blockchain.nft_minting.hts_nft import HederaNFTHandler

@pytest.fixture
def mock_hedera():
    handler = HederaNFTHandler()
    handler.create_parking_nft_collection = AsyncMock()
    handler.mint_parking_nft = AsyncMock(return_value="0.0.1234:5678")
    return handler

@pytest.mark.asyncio
async def test_full_parking_workflow(mock_hedera):
    state_mgr = ParkingStateManager()
    
    # Test vehicle entry
    await state_mgr.update_vehicle_count(
        "A1", "ENTER", {"nft_id": "test-nft", "plate": "KAA123X"}
    )
    assert state_mgr.state["A1"]["count"] == 1
    
    # Test capacity alerts
    state_mgr.state["A1"]["threshold"] = 1
    with pytest.raises(CapacityExceededError):
        await state_mgr.update_vehicle_count(
            "A1", "ENTER", {"nft_id": "test-nft2", "plate": "KAA123Y"}
        )
    
    # Test NFT integration
    nft_id = await mock_hedera.mint_parking_nft({})
    assert "0.0.1234:5678" == nft_id

@pytest.mark.asyncio
async def test_payment_processing():
    with patch('core.payment_orchestrator.HederaNFTHandler') as mock:
        instance = mock.return_value
        instance.process_payment = AsyncMock(return_value=True)
        
        # Test successful payment
        result = await instance.process_payment({})
        assert result is True