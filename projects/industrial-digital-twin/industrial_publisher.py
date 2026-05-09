import time
import random
import json
import datetime
import threading
import ssl
import paho.mqtt.client as mqtt

# --- Configuration ---
BROKER = "localhost"
PORT = 8883
CA_CERT = "certificats/ca.crt"
CLIENT_CERT = "certificats/client.crt"
CLIENT_KEY = "certificats/client.key"
BASE_TOPIC = "youssef/iot"


class IoTDevice(threading.Thread):
    def __init__(self, device_id, device_type):
        super().__init__()
        self.device_id = device_id
        self.device_type = device_type
        self.client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
                                  client_id=f"{device_type}_{device_id}")
        self.running = True
        self.topic = f"{BASE_TOPIC}/{device_type}/{device_id}"

    def run(self):
        self.client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY,
                            cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2)
        self.client.tls_insecure_set(True)

        try:
            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while self.running:
                metrics = self.simulate_sensors()
                payload = {
                    "device_id": self.device_id,
                    "type": self.device_type,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "metrics": metrics
                }

                # Publication
                self.client.publish(self.topic, json.dumps(payload), qos=1)

                # AFFICHAGE CONSOLE (Visual Feedback)
                timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] [SENT] {self.device_id:<8} | Data: {metrics}")

                time.sleep(random.uniform(2.0, 4.0))  # Fréquence légèrement aléatoire pour le réalisme

        except Exception as e:
            print(f"\n[!] ERREUR CRITIQUE {self.device_id}: {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


class CNCMachine(IoTDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "cnc")
        self.temp = 22.0

    def simulate_sensors(self):
        rpm = random.uniform(12000, 15000)
        self.temp = min(85.0, self.temp + (rpm / 35000) * random.uniform(0.1, 0.25))
        return {"rpm": round(rpm, 1), "temp": round(self.temp, 2)}


class EnvMonitor(IoTDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "env")

    def simulate_sensors(self):
        return {"aqi": random.randint(20, 45), "hum": round(random.uniform(40, 55), 1)}


def main():
    devices = []
    for i in range(1, 6): devices.append(CNCMachine(f"CNC-{i:03}"))
    for i in range(1, 4): devices.append(EnvMonitor(f"ENV-{i:03}"))

    print("=" * 60)
    print(f" DÉMARRAGE DE L'USINE CONNECTÉE (mTLS) - {len(devices)} APPAREILS")
    print("=" * 60)

    for d in devices:
        d.daemon = True
        d.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[STOP] Fermeture sécurisée de l'usine...")
        for d in devices:
            d.running = False
            d.join()


if __name__ == "__main__":
    main()