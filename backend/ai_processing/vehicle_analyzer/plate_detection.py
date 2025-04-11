# ai_processing/vehicle_analyzer/plate_detection.py
import cv2
import numpy as np
from azure.ai.vision import ImageAnalysisClient
from azure.ai.vision.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class PlateDetector:
    def __init__(self, vision_endpoint, vision_key):
        self.cloud_client = ImageAnalysisClient(
            endpoint=vision_endpoint,
            credential=AzureKeyCredential(vision_key))
        self.edge_model = cv2.dnn.readNetFromONNX("models/plate_detection.onnx")
        
    def detect_cloud(self, image_url):
        """Use Azure Computer Vision for plate detection"""
        try:
            result = self.cloud_client.analyze(
                image_url=image_url,
                visual_features=[VisualFeatures.READ]
            )
            return [line.text for line in result.read.blocks if line.kind == "licensePlate"]
        except AzureError as e:
            logger.error(f"Cloud detection failed: {str(e)}")
            return None

    def detect_edge(self, image_path):
        """Local plate detection using ONNX model"""
        img = cv2.imread(image_path)
        blob = cv2.dnn.blobFromImage(img, 1/255.0, (640, 640), swapRB=True)
        self.edge_model.setInput(blob)
        outputs = self.edge_model.forward()
        return self._process_output(outputs, img.shape)

    def _process_output(self, outputs, shape):
        boxes = []
        conf_threshold = 0.5
        height, width = shape[:2]
        
        for detection in outputs[0, 0, :, :]:
            confidence = detection[2]
            if confidence > conf_threshold:
                x1 = int(detection[3] * width)
                y1 = int(detection[4] * height)
                x2 = int(detection[5] * width)
                y2 = int(detection[6] * height)
                boxes.append((x1, y1, x2, y2))
                
        return boxes