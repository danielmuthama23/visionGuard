## VisionGuard: Smart City Parking Managem# VisionGuard: Smart City Parking Management System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Azure](https://img.shields.io/badge/Azure-%230072C6.svg?logo=microsoft-azure)](https://azure.microsoft.com)
[![React](https://img.shields.io/badge/React-20232a?logo=react)](https://reactjs.org/)

<div align="center">
  <img src="/images/x4.png" alt="VisionGuard Dashboard Preview" width="800">
  <h3>AI-Powered Parking Management with Blockchain Integration</h3>
</div>

## 📖 Table of Contents
- [Problem Statement](#-problem-statement)
- [Solution Overview](#-solution-overview)
- [Key Features](#-key-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [License](#-license)
- [Contact](#-contact)

## 🎯 Problem Statement

Urban centers face critical parking challenges:
- 30% traffic congestion from parking searches
- Manual verification errors
- Static pricing models
- Fraud vulnerabilities
- Fragmented data systems

## 💡 Solution Overview

VisionGuard transforms urban mobility through:
- **Azure Percept Edge AI**: Real-time license plate recognition
- **Hedera Hashgraph DLT**: Immutable transaction auditing
- **Semantic Kernel**: Dynamic pricing models
- **Multi-Chain NFT Framework**: Hybrid payment system

<div align="center">
  <img src="/images/visionguardo.drawio.png" alt="System Architecture" width="800">
</div>

## ✨ Key Features

### 🚗 Real-Time Monitoring
- Live vehicle detection & classification
- IoT sensor integration
- Anomaly detection

### 🔗 Blockchain Integration
- NFT-based parking tickets
- Smart contract enforcement
- Carbon credit tracking

### 📈 Smart Analytics
- Predictive demand forecasting
- Dynamic pricing engine
- Historical trend analysis

### ⚡ IoT Control
- MQTT-based light control
- Edge AI processing
- Real-time alert system

## 🛠 Tech Stack

### Frontend
![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)
![TypeScript](https://img.shields.io/badge/TypeScript-5.3-3178C6?logo=typescript)
![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.4-06B6D4?logo=tailwind-css)

### Backend
![Node.js](https://img.shields.io/badge/Node.js-20-339933?logo=node.js)
![Azure Functions](https://img.shields.io/badge/Azure_Functions-4.0-0089D6)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi)

### AI/ML
![Azure Cognitive Services](https://img.shields.io/badge/Azure_AI-2023-0089D6)
![PyTorch](https://img.shields.io/badge/PyTorch-2.1-EE4C2C?logo=pytorch)

### Blockchain
![Hedera Hashgraph](https://img.shields.io/badge/Hedera-2.6-000?logo=hedera)

## 📦 Installation

### Prerequisites
- Node.js 20.x
- Python 3.10+
- Azure CLI 2.53+
- Docker 24.0+

### Repo:

    git clone https://github.com/danielmuthama23/visionguard.git 
    cd visionguard

# Frontend setup
    cd frontend && npm install

# Backend setup
    cd ../backend && pip install -r requirements.txt

### Run AI processing

    # Start vehicle analysis
    python -m ai_processing.vehicle_analyzer.plate_detection &
    python -m ai_processing.vehicle_analyzer.color_classifier &
    python -m ai_processing.vehicle_analyzer.vehicle_type &

    # Initialize RAG system
    python -m ai_processing.rag_system.vector_store create-index

### Run Blockchain

    # Testnet setup
    python -m blockchain.hashgraph_client.testnet_connector setup

    # NFT Minting Service
    python -m blockchain.nft_minting.hts_nft create-collection &
    python -m blockchain.nft_minting.payment_verifier &

### Launch IOT

# MQTT Broker
    mosquitto -c /etc/mosquitto/mosquitto.conf -v &

    # Light controller
    python -m iot_control.light_controller.signal_handler &

    # Edge processing
    python -m iot_control.edge_processing.camera_adapter &

### Initialize Core System

    # State management
    python -m core.state_manager &

    # Payment orchestration
    python -m core.payment_orchestrator &

    # Alert system
    python -m core.alert_system &

### Infrastructure Deployment

    # Azure deployment
    az login
    az deployment group create \
    --template-file infrastructure/main.bicep \
    --resource-group VisionGuard-RG

    # Docker setup
    docker-compose -f infrastructure/docker-compose.yml up -d

    # Kubernetes deployment (if using)
    helm install visionguard infrastructure/helm-charts/

### System Integration

    Data Flow:
    1. IoT Camera → Edge Processing → AI Analysis
    2. AI Results → Core State Manager
    3. State Changes → Blockchain NFT Minting
    4. Updates → Frontend via WebSocket/API

    API Endpoints:
    - POST /api/parking/entry
    - GET /api/analytics
    - GET /api/nfts

### Test

    # Run integration tests
    pytest tests/test_integration.py

    # Check system status
    curl http://localhost:8000/health

    # Test NFT creation
    python -m tests.test_blockchain

### Set up environment variables

    cp .env.example .env

## 🔧 Configuration

### Frontend

    VITE_API_URL=""

    VITE_HEDERA_ACCOUNT_ID=0.0.1234

    VITE_MQTT_BROKER=mqtts://iot.visionguard.io

    <div align="center">
  <img src="/images/x.png" alt="VisionGuard Dashboard Preview" width="800">
  <h3>Frontend Loading... Page</h3>
</div>

<div align="center">
  <img src="/images/x3.png" alt="VisionGuard Dashboard Preview" width="800">
  <h3>Frontend Light View</h3>
</div>

<div align="center">
  <img src="/images/x2.png" alt="VisionGuard Dashboard Preview" width="800">
  <h3>Frontend Dark View</h3>
</div>

### Backend

    AZURE_CV_KEY=your_azure_cv_key

    HEDERA_PRIVATE_KEY=your_hedera_key

    COSMOS_DB_CONN_STR=your_cosmos_conn_str

## 🖥️ Usage

### Start development servers

    cd frontend && npm run dev

    cd backend && uvicorn main:app --reload

### Run production build

    docker-compose -f docker-compose.prod.yml up --build

## 🌐 Access Interfaces

- **Web Dashboard**: [http://localhost:5173](http://localhost:5173)
- **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Admin Portal**: [http://localhost:5173/admin](http://localhost:5173/admin)


## 📄 License

Distributed under the MIT License.
See LICENSE for more information.

## 📧 Contact

    Daniel Muthama: - +254746815371

    Twitter: @dti_kenya01

    Email: danielmuthama23@gmail.com

**Project Link:** https://github.com/danielmuthama23/visionguard

### 🚀 Happy Coding!

Thank you for considering contributing to VisionGuard!