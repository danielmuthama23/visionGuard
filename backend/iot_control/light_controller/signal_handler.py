# iot_control/light_controller/signal_handler.py
import paho.mqtt.client as mqtt
import json
import logging
from .led_simulator import LEDController

logger = logging.getLogger(__name__)

class LightSignalHandler:
    def __init__(self, broker_address, port=1883):
        self.broker = broker_address
        self.port = port
        self.client = mqtt.Client(client_id="parking_light_controller")
        self.led = LEDController()
        
        # Configure callbacks
        self.client.on_connect = self._on_connect
        self.client.on_message = self._on_message

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info("Connected to MQTT Broker")
            self.client.subscribe("parking/+/status")
        else:
            logger.error(f"Connection failed with code {rc}")

    def _on_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode())
            lot_id = msg.topic.split('/')[1]
            
            if payload['status'] == "FULL":
                self.led.set_red(lot_id)
            elif payload['status'] == "AVAILABLE":
                self.led.set_green(lot_id)
                
            self._update_counter_display(payload['count'])
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")

    def _update_counter_display(self, count):
        """Update 7-segment display or digital counter"""
        # Implementation depends on hardware
        logger.info(f"Updated parking counter to: {count}")

    def start(self):
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        self.led.cleanup()