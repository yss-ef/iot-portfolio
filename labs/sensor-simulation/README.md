# MQTT sensor simulation lab

This project demonstrates a foundational IoT architecture using the MQTT
protocol. It includes a sensor simulator that publishes temperature data and a
reader that subscribes to updates in real-time.

## Features

- Sensor simulator: Generates and publishes random temperature data with
  realistic fluctuations.
- Sensor reader: Subscribes to the MQTT topic and processes incoming data.
- Cloud broker: Uses `broker.hivemq.com` for testing without local
  infrastructure.
- JSON format: Exchanges data using the JSON format for structured information.

## Architecture

- Protocol: MQTT (Message Queuing Telemetry Transport)
- Broker: `broker.hivemq.com`
- Topic: `youssef/home/sensors/temperature`
- Publisher: `sensor-simulator.py`
- Subscriber: `sensor-reader.py`

## Prerequisites

- Python 3.x
- `paho-mqtt` library

## Installation

```bash
pip install paho-mqtt
```

## Usage

Follow these steps to run the simulation:

1. Start the reader to begin listening for messages:
   ```bash
   python sensor-reader.py
   ```
2. In a separate terminal, start the simulator:
   ```bash
   python sensor-simulator.py
   ```

## License

This project is licensed under the MIT License.

Authored by Youssef Fellah.
Developed for the Engineering Cycle at Mundiapolis University.
