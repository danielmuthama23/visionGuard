# iot_control/edge_processing/vehicle_frame_processor.py
import cv2
import onnxruntime as ort
import numpy as np

class VehicleFrameProcessor:
    def __init__(self, model_path="models/edge_vehicle_detection.onnx"):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name

    def preprocess(self, frame):
        """Prepare frame for model input"""
        blob = cv2.dnn.blobFromImage(
            frame, 
            1/255.0, 
            (640, 640), 
            swapRB=True
        )
        return blob.astype(np.float32)

    def analyze_frame(self, frame):
        """Run vehicle detection model"""
        processed = self.preprocess(frame)
        outputs = self.session.run(None, {self.input_name: processed})
        
        # Process model outputs
        count = self._count_vehicles(outputs[0])
        anomaly = self._detect_anomalies(outputs[1])
        
        return {
            "count": count,
            "anomaly": anomaly
        }

    def _count_vehicles(self, output):
        # Implementation depends on model output format
        return np.count_nonzero(output[0][:, 4] > 0.5)

    def _detect_anomalies(self, output):
        # Implement anomaly detection logic
        return any(output > 0.7)