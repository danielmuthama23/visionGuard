# tests/test_units/test_vision_processing.py
import pytest
import numpy as np
from unittest.mock import MagicMock, patch
from ai_processing.vehicle_analyzer.plate_detection import PlateDetector
from ai_processing.vehicle_analyzer.color_classifier import ColorClassifier

@pytest.fixture
def mock_vision_client():
    client = MagicMock()
    client.analyze.return_value = MagicMock(
        read=MagicMock(
            blocks=[MagicMock(text="KAA123X", kind="licensePlate")]
        )
    )
    return client

def test_plate_detection(mock_vision_client):
    detector = PlateDetector(cloud_client=mock_vision_client)
    plates = detector.detect_cloud("http://test.image")
    assert plates == ["KAA123X"]
    mock_vision_client.analyze.assert_called_once()

def test_color_classification():
    classifier = ColorClassifier()
    with patch('onnxruntime.InferenceSession') as mock_session:
        mock_output = [[0.1, 0.8, 0.1]]  # Simulate color probabilities
        mock_session.run.return_value = [np.array(mock_output)]
        
        color = classifier.classify_color(MagicMock())
        assert color == "black"

def test_edge_case_handling():
    detector = PlateDetector()
    with patch('cv2.dnn.blobFromImage') as mock_blob:
        mock_blob.return_value = np.random.rand(1,3,640,640).astype(np.float32)
        results = detector.detect_edge("invalid.jpg")
        assert isinstance(results, list)