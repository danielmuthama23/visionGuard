# core/state_manager.py
import threading
from azure.cosmos import CosmosClient
from azure.eventhub import EventHubProducerClient
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class ParkingStateManager:
    def __init__(self):
        self.lock = threading.Lock()
        self.state = defaultdict(lambda: {
            'count': 0,
            'threshold': 100,
            'vehicles': {},
            'rates': defaultdict(float),
            'capacity_history': []
        })
        self._init_cosmos()
        self._init_event_hub()

    def _init_cosmos(self):
        self.cosmos_client = CosmosClient.from_connection_string(
            os.getenv("COSMOS_DB_CONN_STR"))
        self.database = self.cosmos_client.get_database_client("ParkingDB")
        self.container = self.database.get_container_client("RealTimeState")

    def _init_event_hub(self):
        self.eventhub_client = EventHubProducerClient.from_connection_string(
            os.getenv("EVENT_HUB_CONN_STR"),
            eventhub_name="parking-alerts"
        )

    def update_vehicle_count(self, lot_id: str, action: str, vehicle_data: dict):
        with self.lock:
            current_state = self.state[lot_id]
            
            if action == "ENTER":
                if current_state['count'] >= current_state['threshold']:
                    raise CapacityExceededError(lot_id)
                
                current_state['count'] += 1
                current_state['vehicles'][vehicle_data['nft_id']] = vehicle_data
                self._log_capacity(lot_id)
                self._check_thresholds(lot_id)

            elif action == "EXIT":
                current_state['count'] = max(0, current_state['count'] - 1)
                if vehicle_data['nft_id'] in current_state['vehicles']:
                    del current_state['vehicles'][vehicle_data['nft_id']]
                
                self._log_capacity(lot_id)

            self._sync_cosmos(lot_id)

    def _log_capacity(self, lot_id):
        self.state[lot_id]['capacity_history'].append({
            "timestamp": datetime.utcnow().isoformat(),
            "count": self.state[lot_id]['count'],
            "threshold": self.state[lot_id]['threshold']
        })
        
    def _check_thresholds(self, lot_id):
        current = self.state[lot_id]
        event_data = {
            "lot_id": lot_id,
            "count": current['count'],
            "threshold": current['threshold'],
            "timestamp": datetime.utcnow().isoformat()
        }

        if current['count'] >= current['threshold']:
            self._send_alert("capacity.full", event_data)
        elif current['count'] >= current['threshold'] * 0.9:
            self._send_alert("capacity.warning", event_data)

    def _send_alert(self, alert_type, data):
        event_data_batch = self.eventhub_client.create_batch()
        event_data_batch.add(EventData(json.dumps({
            "type": alert_type,
            "data": data
        })))
        self.eventhub_client.send_batch(event_data_batch)

    def _sync_cosmos(self, lot_id):
        self.container.upsert_item({
            "id": f"state_{lot_id}",
            "partitionKey": lot_id,
            **self.state[lot_id]
        })

    def dynamic_pricing(self, lot_id, vehicle_type):
        base_rate = self.state[lot_id]['rates'][vehicle_type]
        demand_factor = self.state[lot_id]['count'] / self.state[lot_id]['threshold']
        return base_rate * (1 + demand_factor ** 2)