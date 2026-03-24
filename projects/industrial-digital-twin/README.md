# 🔄 Secure Industrial IoT: CNC Digital Twin & Monitoring

> **Industrial Internship Project Report**
> This repository features an advanced **Industry 4.0** ecosystem simulation. It demonstrates the orchestration of industrial assets—specifically CNC machines and environmental sensors—utilizing a hardened **MQTT** infrastructure secured with **mTLS** encryption. The project bridges the gap between physical thermal modeling and secure cloud telemetry.

## 📑 Table of Contents

  * [System Overview](https://www.google.com/search?q=%23-system-overview)
  * [Core IoT Concepts](https://www.google.com/search?q=%23-core-iot-concepts)
  * [Cybersecurity Architecture](https://www.google.com/search?q=%23-cybersecurity-architecture)
  * [Digital Twin Logic](https://www.google.com/search?q=%23-digital-twin-logic)
  * [Local Setup (Fedora)](https://www.google.com/search?q=%23-local-setup-fedora)
  * [Conclusion & Takeaways](https://www.google.com/search?q=%23-conclusion--takeaways)

## 📋 System Overview

The objective of this project was to simulate a real-world factory environment where data integrity and service reliability are paramount. The system is divided into three functional layers:

1.  **Physical Simulation Layer**: Python-based "Digital Twins" that model the physics of industrial hardware (RPM, temperature, atmospheric noise).
2.  **Transport Layer**: A hardened MQTT broker (Mosquitto) managing secure data distribution.
3.  **Supervision Layer**: A real-time dashboard consuming telemetry via high-level wildcard subscriptions.

## 🏗️ Core IoT Concepts

To ensure industrial-grade performance, the framework implements several advanced messaging patterns:

### 1\. MQTT Publish/Subscribe Decoupling

Unlike traditional REST architectures, this system decouples producers and consumers in **space** (IP anonymity), **time** (asynchronous connectivity), and **synchronization** (non-blocking updates).

### 2\. Quality of Service (QoS) Implementation

The project specifically utilizes **QoS Level 1 (At least once)** for critical telemetry.

  * **Mechanism**: The broker issues a `PUBACK` for every message.
  * **Use Case**: Ensuring that high-priority alerts, such as **CNC Spindle Overheat**, are never lost due to transient network failures.

### 3\. Reliability Mechanisms

  * **Last Will and Testament (LWT)**: Acts as a "death notification" if a sensor disconnects unexpectedly.
  * **Retained Messages**: Ensures new monitoring clients immediately receive the last known "good" state of the factory floor.

## 🔐 Cybersecurity Architecture: mTLS

Security is implemented via **Mutual TLS (mTLS)**, moving beyond simple password authentication to a robust X.509 certificate trust chain.

  * **Server Authentication**: The Python clients verify the Broker's identity using a root `ca.crt`.
  * **Client Authentication**: The Broker challenges the client to present a valid certificate before allowing data publication.
  * **Encryption**: A symmetric session key is generated after the dual-handshake, providing **Perfect Forward Secrecy (PFS)** for industrial data.

## ⚙️ Digital Twin Logic

The simulation uses **Object-Oriented Programming (OOP)** to represent physical assets through mathematical models:

**CNC Spindle Thermal Model**
The temperature ($T$) of the spindle is not random; it is a dynamic function of the rotation speed (RPM) and friction over time ($t$):
$$\Delta T \propto \frac{R}{R_{max}} \cdot \text{friction\_coeff}$$

**Environmental Monitoring**
Atmospheric sensors simulate real-world Gaussian noise around base values to test the dashboard's ability to handle fluctuating data streams.

## 💻 Local Setup

To deploy this simulation on a Fedora environment (tested on Fedora 43):

```bash
# 1. Install the MQTT Broker
sudo dnf install mosquitto

# 2. Configure mTLS
# Copy your ca.crt, server.crt, and server.key to /etc/mosquitto/certs/
# Update mosquitto.conf to enable port 8883 with SSL requirements

# 3. Initialize the Python environment
pip install paho-mqtt pandas

# 4. Run the Industrial Engine (8 concurrent asset threads)
python industrial_publisher.py
```

## 🎯 Conclusion & Takeaways

This project successfully demonstrates the complexity of securing the **Industrial Internet of Things (IIoT)**.

By implementing mTLS, the framework mitigates common risks like "man-in-the-middle" attacks or unauthorized device injection. Furthermore, the transition from simple data scripts to a multi-threaded "Digital Twin" approach highlights the importance of accurate physical modeling in predictive maintenance. The use of MQTT's QoS 1 ensures that in a high-stakes industrial environment, critical data always reaches its destination, providing a reliable foundation for real-time factory supervision.

-----

*Authored by Youssef Fellah.*

*Developed as part of an internship - Real Estate Brokerage CRM context.*
