# MQTT Sensor Simulation Lab

This project demonstrates a basic IoT architecture using the MQTT protocol. It includes a sensor simulator that publishes temperature data and a reader that subscribes to these updates in real-time.

## Features
- **Sensor Simulator**: Generates and publishes random temperature data with realistic fluctuations.
- **Sensor Reader**: Subscribes to the MQTT topic and processes incoming data.
- **Cloud Broker**: Uses `broker.hivemq.com` for easy testing without local infrastructure.
- **JSON Format**: Data is exchanged using the JSON format for structured information.

## Architecture
- **Protocol**: MQTT (Message Queuing Telemetry Transport)
- **Broker**: `broker.hivemq.com`
- **Topic**: `youssef/home/sensors/temperature`
- **Publisher**: `sensor-simulator.py`
- **Subscriber**: `sensor-reader.py`

## Prerequisites
- Python 3.x
- `paho-mqtt` library

## Installation
```bash
pip install paho-mqtt
```

## Usage
1. Start the reader to begin listening for messages:
   ```bash
   python sensor-reader.py
   ```
2. In a separate terminal, start the simulator:
   ```bash
   python sensor-simulator.py
   ```

## License
MIT

Authored by Youssef Fellah.  
Developed for the Engineering Cycle - Mundiapolis University.
