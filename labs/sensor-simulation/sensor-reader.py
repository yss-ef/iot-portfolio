import paho.mqtt.client as mqtt
import json

# --- Configuration ---
BROKER = "broker.hivemq.com"
TOPIC = "youssef/home/sensors/temperature"


def on_connect(client, userdata, flags, reason_code, properties):
    """Callback triggered upon connection to the broker."""
    if reason_code.is_failure:
        print(f"[ERROR] Connection failed: {reason_code}")
    else:
        print(f"[INFO] Connected to broker successfully.")
        # The moment we connect, we tell the broker which channel we want to listen to
        client.subscribe(TOPIC)
        print(f"[INFO] Subscribed to topic: {TOPIC}")


def on_message(client, userdata, msg):
    """Callback triggered every time a message is received on a subscribed topic."""
    # The payload arrives as raw bytes. We must decode it into a standard text string.
    raw_payload = msg.payload.decode('utf-8')

    print(f"\n[RECEIVED] Topic: {msg.topic}")
    print(f"[RAW DATA] {raw_payload}")


def main():
    # 1. Initialize the client using the modern Version 2 API
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)

    # 2. Attach our callback instructions
    client.on_connect = on_connect
    client.on_message = on_message

    # 3. Connect to the broker
    print(f"[INFO] Attempting connection to {BROKER}...")
    client.connect(BROKER, 1883, 60)

    # 4. Start the infinite listening loop
    try:
        print("[INFO] Waiting for messages. Press Ctrl+C to exit.")
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Terminated by user.")
    finally:
        client.disconnect()
        print("[INFO] Disconnected.")


if __name__ == "__main__":
    main()