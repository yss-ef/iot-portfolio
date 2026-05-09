# IoT Labs Collection

A collection of projects and labs focused on Internet of Things (IoT), MQTT communication, and Digital Twin simulations.

## Repository Structure

### Labs
- **[Secure MQTT TLS](./labs/secure-mqtt-tls)**: A lab focused on securing MQTT communication using TLS/SSL certificates (CA, Broker, and Client certificates).
- **[Sensor Simulation](./labs/sensor-simulation)**: Basic MQTT sensor simulators and readers for testing message brokering and connectivity.

### Projects
- **[Industrial Digital Twin](./projects/industrial-digital-twin)**: An Industrial IoT (IIoT) simulation featuring real-time sensor data publishing, stream processing, and an interactive Python dashboard for industrial monitoring.

---

## Getting Started

### Prerequisites
- Python 3.x
- MQTT Broker (e.g., Mosquitto)
- Paho-MQTT library:
  ```bash
  pip install paho-mqtt
  ```

### Running the Digital Twin
1. Start your MQTT broker.
2. Run the sensor simulation:
   ```bash
   python projects/industrial-digital-twin/sensor_sim.py
   ```
3. Run the dashboard client:
   ```bash
   python projects/industrial-digital-twin/dashboard_client.py
   ```
