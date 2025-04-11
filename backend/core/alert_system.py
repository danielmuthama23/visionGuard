# core/alert_system.py
import paho.mqtt.client as mqtt
from azure.communication.email import EmailClient
import socketio

class MultiChannelAlertSystem:
    def __init__(self):
        self.mqtt_client = mqtt.Client(client_id="alert-system")
        self.sio = socketio.AsyncClient()
        self.email_client = EmailClient.from_connection_string(
            os.getenv("EMAIL_CONN_STR"))
        
        # Configure transports
        self._configure_mqtt()
        self._configure_websockets()

    def _configure_mqtt(self):
        self.mqtt_client.connect(
            os.getenv("MQTT_BROKER", "localhost"),
            int(os.getenv("MQTT_PORT", 1883))
        self.mqtt_client.loop_start()

    async def _configure_websockets(self):
        await self.sio.connect(os.getenv("WS_SERVER"))
        self.sio.on("alert_ack", self.handle_acknowledgement)

    async def send_alert(self, alert_type, data):
        """Multi-channel alert distribution"""
        # MQTT for IoT devices
        self.mqtt_client.publish(
            f"parking/{data['lot_id']}/alerts",
            json.dumps({"type": alert_type, **data})
            
        # WebSocket for real-time dashboard
        await self.sio.emit("parking_alert", {
            "type": alert_type,
            "data": data,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Email for staff notifications
        if alert_type in ["capacity.full", "security.breach"]:
            await self.email_client.send_email(
                from_address="alerts@visionguard.com",
                to_addresses=os.getenv("STAFF_EMAILS").split(","),
                subject=f"Parking Alert: {alert_type}",
                html_content=f"""
                <h1>{alert_type} Alert</h1>
                <p>Parking lot {data['lot_id']} requires attention</p>
                <pre>{json.dumps(data, indent=2)}</pre>
                """
            )

    async def handle_acknowledgement(self, data):
        logger.info(f"Alert acknowledged: {data['alert_id']}")

    async def shutdown(self):
        self.mqtt_client.loop_stop()
        await self.sio.disconnect()

class CapacityExceededError(Exception):
    def __init__(self, lot_id):
        super().__init__(f"Capacity exceeded in lot {lot_id}")
        self.lot_id = lot_id