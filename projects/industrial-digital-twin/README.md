# Secure Industrial IoT Framework: CNC Digital Twin & Environmental Monitoring

An advanced Python-based simulation of an **Industry 4.0** ecosystem. This project demonstrates the orchestration of multiple industrial assets (CNC machines and environmental sensors) using a hardened **MQTT** infrastructure with **mTLS** encryption.

## 🔬 Core IoT Concepts & Theory

### 1. The MQTT Protocol (Message Queuing Telemetry Transport)

MQTT is a lightweight, broker-based publish/subscribe messaging protocol. It is designed for high-latency, low-bandwidth, or unreliable networks.

* **Pub/Sub Decoupling**: Unlike REST (Client-Server), MQTT decouples the producer and consumer in **space** (they don't need to know each other's IP), **time** (they don't need to be connected at the same time), and **synchronization** (the publisher isn't blocked while sending).
* **Topic Hierarchy**: Uses a UTF-8 string structure (e.g., `factory/floor1/cnc/01/temp`). This allows for granular data routing.

### 2. Deep Dive: Quality of Service (QoS)

QoS levels define the "guarantee of delivery" for a specific message. Choosing the right level is a trade-off between **reliability** and **network overhead**.

| Level | Logic | Mechanism | Use Case |
| --- | --- | --- | --- |
| **QoS 0** | At most once | "Fire and Forget." The message is sent without an acknowledgment. | Non-critical streaming (e.g., ambient light levels). |
| **QoS 1** | At least once | **Used in this project.** The broker sends a `PUBACK`. If the publisher doesn't receive it, it re-sends. Duplicate messages are possible. | **Critical telemetry** (e.g., CNC Spindle Overheat alerts). |
| **QoS 2** | Exactly once | A 4-step handshake (`PUBLISH`, `PUBREC`, `PUBREL`, `PUBCOMP`). Ensures the message is received once and only once. | Financial transactions or precision robotic commands. |

### 3. Advanced Reliability Features (Theory)

While not all are implemented in every script, these are vital for Industrial IoT:

* **Last Will and Testament (LWT)**: A message stored by the broker and sent automatically if a client disconnects unexpectedly. It acts as a "death notification" for remote monitoring.
* **Retained Messages**: The broker stores the last "good" value of a topic. New subscribers receive this value immediately upon joining, without waiting for the next sensor update.
* **Keep Alive & PING**: A heartbeat mechanism to detect "half-open" TCP connections where the cable is cut but the socket remains open.

---

## 🔐 Cybersecurity: Mutual TLS (mTLS)

In industrial settings, security is non-negotiable. This project bypasses simple passwords in favor of **mTLS**.

* **Asymmetric Encryption**: Uses RSA/ECC key pairs.
* **The Trust Chain**: Both the Client and the Broker must present a certificate signed by a trusted **Certificate Authority (CA)**.
* **The Handshake**:
1. **Server Authentication**: Client verifies the Broker's certificate against the `ca.crt`.
2. **Client Authentication**: Broker verifies the Client's certificate.
3. **Key Exchange**: A temporary symmetric key is generated for the session, ensuring **Perfect Forward Secrecy (PFS)**.



---

## 🛠 Digital Twin Simulation Logic

The simulation uses **Object-Oriented Programming (OOP)** to create a "Digital Twin" of each asset:

* **CNC Assets**: Implements a thermal inertia model. Spindle temperature ($T$) is calculated as a function of RPM ($R$) over time ($t$):

$$\Delta T \propto \frac{R}{R_{max}} \cdot \text{friction\_coeff}$$


* **Environmental Assets**: Simulates Gaussian noise around a base atmospheric value to mimic real-world sensor fluctuations.

---

## 📂 Project Structure

* `industrial_publisher.py`: Multi-threaded engine managing 8 concurrent IoT threads.
* `dashboard_client.py`: Real-time telemetry consumer using **Wildcard Subscriptions** (`#`).
* `certificats/`: Infrastructure for X.509 certificates.

---

## 🚀 Getting Started on Fedora 43

1. **Install Mosquitto**: `sudo dnf install mosquitto`
2. **Configure SSL**: Update `mosquitto.conf` to point to your `ca.crt`, `server.crt`, and `server.key`.
3. **Run Simulation**:
```bash
python industrial_publisher.py

```

---

*Authored by Youssef Fellah.*

*Developed as part of an internship - Broker immobilier.*
