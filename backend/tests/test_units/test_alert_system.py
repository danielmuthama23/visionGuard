# tests/test_units/test_alert_system.py
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from core.alert_system import MultiChannelAlertSystem

@pytest.fixture
def alert_system():
    with patch('paho.mqtt.client.Client'), \
         patch('azure.communication.email.EmailClient'):
        system = MultiChannelAlertSystem()
        system.sio = AsyncMock()
        return system

@pytest.mark.asyncio
async def test_multi_channel_alert(alert_system):
    test_data = {"lot_id": "A1", "count": 100}
    
    await alert_system.send_alert("capacity.full", test_data)
    
    # Verify MQTT
    alert_system.mqtt_client.publish.assert_called_with(
        "parking/A1/alerts",
        '{"type": "capacity.full", "lot_id": "A1", "count": 100}'
    )
    
    # Verify WebSocket
    alert_system.sio.emit.assert_awaited_with("parking_alert", {
        "type": "capacity.full",
        "data": test_data,
        "timestamp": pytest.any(str)
    })
    
    # Verify Email
    alert_system.email_client.send_email.assert_called_once()

@pytest.mark.asyncio
async def test_alert_acknowledgement(alert_system):
    test_data = {"alert_id": "12345"}
    await alert_system.handle_acknowledgement(test_data)
    assert "12345" in alert_system.acknowledged_alerts