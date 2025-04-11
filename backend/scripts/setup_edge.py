# scripts/setup_edge.py
import os
import subprocess
from datetime import datetime

EDGE_CONFIG = {
    "mqtt_broker": "10.0.1.100",
    "camera_device": "/dev/video0",
    "model_path": "/opt/visionguard/models"
}

def setup_edge_node():
    print(f"[{datetime.now()}] Starting edge device setup")
    
    # Install dependencies
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "install", "-y", 
                   "python3-pip", "docker.io", "mosquitto"])
    
    # Configure MQTT
    with open("/etc/mosquitto/mosquitto.conf", "a") as f:
        f.write(f"\nlistener 1883 {EDGE_CONFIG['mqtt_broker']}")
    
    # Setup model directory
    os.makedirs(EDGE_CONFIG["model_path"], exist_ok=True)
    
    # Enable camera access
    subprocess.run(["sudo", "usermod", "-aG", "video", os.getenv("USER")])
    
    print(f"[{datetime.now()}] Edge setup completed")

if __name__ == "__main__":
    setup_edge_node()