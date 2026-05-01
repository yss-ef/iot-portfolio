# Secure Industrial IoT: CNC Digital Twin & Telemetry

A high-performance Industry 4.0 ecosystem simulation engineered to bridge the gap between physical thermal modeling and secure cloud telemetry. This framework implements a hardened MQTT infrastructure secured with mTLS encryption to orchestrate Digital Twins of industrial assets.

## Technical Architecture

The system is designed as a three-tier observability framework, ensuring data integrity and service reliability in a simulated factory environment:

1.  **Physical Simulation Tier**: Multi-threaded Python engines modeling the physics of industrial hardware (RPM, thermal inertia, atmospheric noise).
2.  **Transport Tier**: A hardened Mosquitto broker managing secure, decoupled data distribution.
3.  **Supervision Tier**: Real-time telemetry consumers utilizing high-level wildcard subscriptions for factory-wide oversight.

---

## Technical Stack

*   **Language**: Python 3.10+ (Multi-threading, OOP)
*   **Protocol**: MQTT (Paho-MQTT)
*   **Security**: Mutual TLS (mTLS) / X.509 Certificates
*   **Broker**: Eclipse Mosquitto
*   **Modeling**: Numerical physics simulation (Thermal Inertia)
*   **Build Tool**: Pip / Virtualenv

---

## Core Implementations

### 1. Hardened Messaging Logic
*   **QoS 1 (At Least Once)**: Implementation of acknowledgment handshakes (`PUBACK`) to ensure critical alerts—such as Spindle Overheat—survive transient network failures.
*   **Reliability Patterns**: Integration of **Last Will and Testament (LWT)** for unexpected disconnect notifications and **Retained Messages** for immediate state recovery.
*   **Decoupled Pub/Sub**: Spatial and temporal decoupling to ensure the system remains non-blocking under high-frequency telemetry loads.

### 2. Cybersecurity & mTLS
*   **Dual Handshake**: Moving beyond password-based security to a certificate-based trust chain.
*   **Asymmetric Encryption**: Client and Broker validation using a trusted Certificate Authority (CA).
*   **Data Privacy**: Generation of symmetric session keys to ensure Perfect Forward Secrecy (PFS) for industrial data streams.

### 3. Digital Twin Physics Modeling
*   **Thermal Dynamics**: Mathematical modeling of spindle temperature as a function of rotational speed ($RPM$) and friction over time ($t$).
*   **Environmental Simulation**: Stochastic modeling of atmospheric sensors using Gaussian noise to simulate real-world data fluctuations.

---

## Project Structure

```text
├── industrial_publisher.py # Multi-threaded engine for 8+ industrial assets
├── dashboard_client.py     # Real-time telemetry consumer & visualizer
├── sensor_sim.py          # Physics-based Digital Twin definitions
└── README.md              # System documentation
```

---

## Deployment & Setup

### Prerequisites
*   Python 3.10+
*   Eclipse Mosquitto (configured for SSL/TLS on port 8883)

### Execution Sequence
1.  **Initialize Environment**:
    ```bash
    pip install paho-mqtt pandas
    ```
2.  **Configure Trust Chain**:
    Ensure your `ca.crt`, `client.crt`, and `client.key` are present in the certificates directory.
3.  **Launch Simulation**:
    ```bash
    python industrial_publisher.py
    ```

---

*Authored by Youssef Fellah.*

*Developed during professional internship - Industrial IoT Deep-Dive.*
