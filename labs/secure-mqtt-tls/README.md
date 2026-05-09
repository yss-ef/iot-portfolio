# Secure MQTT TLS Lab

This repository explores the security aspects of the MQTT protocol, specifically focusing on **Mutual TLS (mTLS)** and the **Last Will and Testament (LWT)** feature.

## Features
- **TLS/SSL Encryption**: Secures the communication between the client and the broker using certificates.
- **Mutual Authentication**: Both the client and the broker verify each other's identities using certificates (mTLS).
- **Last Will and Testament (LWT)**: Ensures the broker publishes a "status" message if the sensor disconnects unexpectedly.
- **Mosquitto Configuration**: Includes a custom configuration for a local Mosquitto broker with TLS enabled.

## Security Configuration
The project uses the following certificate structure (located in the `Certificate` directory):
- `ca/ca.crt`: Root Certificate Authority.
- `client/client.crt` & `client/client.key`: Client-side certificates for authentication.
- `broker/broker.crt` & `broker/broker.key`: Broker-side certificates.

## Prerequisites
- Python 3.x
- `paho-mqtt` library (v2.x)
- Mosquitto MQTT Broker (installed locally)

## Installation
```bash
pip install paho-mqtt
```

## Setup & Usage
1. **Broker Setup**:
   Configure your Mosquitto broker to use the provided `mosquitto-tls.conf` and the certificates in the `Certificate` folder.
2. **Run the Secure Sensor**:
   ```bash
   python secure-sensor.py
   ```

## License
MIT
