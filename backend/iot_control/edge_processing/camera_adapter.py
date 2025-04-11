# iot_control/edge_processing/camera_adapter.py
import cv2
import os
import json
from azure.iot.device import IoTHubModuleClient
from azure.iot.device import Message

class EdgeCameraAdapter:
    def __init__(self):
        self.client = IoTHubModuleClient.create_from_edge_environment()
        self.camera = cv2.VideoCapture(0)
        self.frame_count = 0
        self.processor = VehicleFrameProcessor()
        
        # Load edge configuration
        self.config = self._load_twin_configuration()

    def _load_twin_configuration(self):
        twin = self.client.get_twin()
        return twin.get('desired', {}).get('cameraConfig', {})

    def process_frame(self, frame):
        """Edge processing pipeline"""
        # Step 1: Preprocessing
        resized = cv2.resize(frame, (640, 480))
        
        # Step 2: Run local ML model
        results = self.processor.analyze_frame(resized)
        
        # Step 3: Create message
        message = {
            "cameraId": self.config.get("cameraId", "default"),
            "timestamp": datetime.utcnow().isoformat(),
            "vehicleCount": results['count'],
            "anomalyDetected": results['anomaly'],
            "frameId": self.frame_count
        }
        
        return message

    def send_to_cloud(self, message):
        msg = Message(json.dumps(message))
        msg.content_encoding = "utf-8"
        msg.content_type = "application/json"
        self.client.send_message_to_output(msg, "cloudOutput")

    def run(self):
        try:
            while True:
                ret, frame = self.camera.read()
                if not ret:
                    logger.error("Failed to capture frame")
                    continue
                
                processed = self.process_frame(frame)
                self.send_to_cloud(processed)
                self.frame_count += 1
                
                # Check for config updates
                if self.frame_count % 100 == 0:
                    self.config = self._load_twin_configuration()
                    
        except KeyboardInterrupt:
            self.camera.release()
            self.client.disconnect()