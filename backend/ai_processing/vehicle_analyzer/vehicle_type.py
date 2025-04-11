# ai_processing/vehicle_analyzer/vehicle_type.py
import onnxruntime as ort
import numpy as np
from PIL import Image

class VehicleTypeClassifier:
    def __init__(self, model_path="models/vehicle_type.onnx"):
        self.session = ort.InferenceSession(model_path)
        self.classes = [
            'sedan', 'suv', 'truck', 
            'motorcycle', 'van', 'bus'
        ]

    def preprocess(self, image):
        """Prepare image for type classification"""
        img = image.resize((256, 256))
        img = img.convert('RGB')
        img_array = np.array(img).astype(np.float32)
        img_array = np.transpose(img_array, (2, 0, 1))
        img_array = (img_array / 255.0 - 0.5) / 0.5
        return np.expand_dims(img_array, axis=0)

    def classify_type(self, image):
        """Predict vehicle type from image"""
        preprocessed = self.preprocess(image)
        outputs = self.session.run(None, {'input': preprocessed})
        return self.classes[np.argmax(outputs[0])]