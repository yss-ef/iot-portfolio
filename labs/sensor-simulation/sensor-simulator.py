import time
import random
import json
import datetime
import paho.mqtt.client as mqtt

# --- Configuration ---
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "youssef/home/sensors/temperature"
SENSOR_ID = "temp_sensor_01"

# --- Simulation Parameters ---
BASE_TEMP = 22.0
FLUCTUATION_RANGE = 2.5
INTERVAL = 5


def on_connect(client, userdata, flags, rc):
    """Callback triggered upon connection to the broker."""
    if rc == 0:
        print(f"[INFO] Connected to broker {BROKER}")
    else:
        print(f"[ERROR] Connection failed with code {rc}")


def generate_temperature(base_temp, fluctuation):
    """Generates a realistic temperature variation."""
    # Adds a random float between -fluctuation and +fluctuation
    variance = random.uniform(-fluctuation, fluctuation)
    return round(base_temp + variance, 2)


def main():
    # Initialize MQTT Client
    client = mqtt.Client(client_id=f"{SENSOR_ID}_{random.randint(1000, 9999)}")
    client.on_connect = on_connect

    # Connect to the broker
    print(f"[INFO] Attempting connection to {BROKER}...")
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # Start network loop in a background thread

    try:
        print("[INFO] Starting temperature simulation. Press Ctrl+C to exit.")
        while True:
            # Generate simulated data
            current_temp = generate_temperature(BASE_TEMP, FLUCTUATION_RANGE)
            timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

            # Construct payload
            payload = {
                "sensor_id": SENSOR_ID,
                "temperature_celsius": current_temp,
                "timestamp": timestamp
            }

            # Convert payload to JSON and publish
            json_payload = json.dumps(payload)
            client.publish(TOPIC, json_payload)

            print(f"[PUBLISHED] {TOPIC} -> {json_payload}")

            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        print("\n[INFO] Simulation terminated by user.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[INFO] Disconnected from broker.")


if __name__ == "__main__":
    main()