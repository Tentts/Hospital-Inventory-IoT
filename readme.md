# IoT Data Platform for Hospital Inventory Monitoring

## ⚠️ Disclaimer
This project was developed as part of a master's course and is intended for educational purposes only.
It was created several years ago and may not reflect current best practices, security standards, or the latest versions of the technologies used.

---

## 📌 Overview
This project implements an end-to-end IoT data platform designed to simulate and monitor hospital inventory systems such as refrigeration units and sensor-based equipment.

It demonstrates how IoT devices can integrate with context-aware platforms to enable real-time monitoring, data processing, and automated workflows.

---

## 🏗️ Architecture
The platform is composed of the following components:

- **Sensor Simulation**  
  Python scripts simulate IoT devices (e.g., temperature sensors, IR sensors) and generate telemetry data.

- **Messaging Layer**  
  MQTT protocol is used for lightweight communication between devices and the backend, powered by Mosquitto.

- **Context Management (FIWARE)**  
  - **IoT Agent**: Translates MQTT messages into NGSI format  
  - **Orion Context Broker**: Manages context information and entity state

- **Event Processing**  
  Node-RED is used to create event-driven workflows and automate actions based on incoming data.

- **Client Application**  
  A simple Python interface designed to monitor system state and interact with the platform.

![Project scheme image](https://github.com/Tentts/Hospital-Inventory-IoT/blob/master/project_scheme.png)

---

## ⚙️ Technologies Used

- Python
- MQTT (Mosquitto)
- FIWARE IoT Agent
- FIWARE Orion Context Broker (NGSI)
- Node-RED

---

## 🚀 Features

- Simulated IoT sensor data generation
- Real-time data ingestion via MQTT
- Context-aware data modeling using NGSI entities
- Persistent storage and querying
- Event-driven automation workflows
- Basic monitoring client

---

## 📊 Data Flow

1. Python scripts simulate sensor data
2. Data is published to MQTT topics
3. FIWARE IoT Agent consumes and translates messages into NGSI
4. Orion Context Broker manages entity state
5. Data is stored in MongoDB
6. Node-RED processes events and triggers actions
7. Client application visualizes system state

---

## 🧪 Use Case

This project simulates hospital inventory monitoring scenarios such as:

- Detecting temperature anomalies in refrigeration systems
- Monitoring presence/activity via IR sensors
- Triggering alerts or automated workflows based on thresholds

---

## ⚠️ Limitations

- Not production-ready
- Limited security considerations
- Simplified simulation of real-world IoT devices
- No scalability testing

---

## 📚 Learning Objectives

- Understand IoT data pipelines
- Work with FIWARE ecosystem components
- Learn context-based data modeling (NGSI)
- Implement event-driven architectures
- Integrate multiple distributed systems

