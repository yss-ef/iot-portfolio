import time
import random
import json
import datetime
import threading
import ssl
import paho.mqtt.client as mqtt

# --- Configuration Sécurité & Broker ---
BROKER = "localhost"
PORT = 8883
# Utilisation de chemins relatifs propres
CA_CERT = "certificats/ca.crt"
CLIENT_CERT = "certificats/client.crt"
CLIENT_KEY = "certificats/client.key"
BASE_TOPIC = "youssef/iot"


class IoTDevice(threading.Thread):
    """Classe parente gérant l'infrastructure mTLS pour chaque thread."""

    def __init__(self, device_id, device_type):
        super().__init__()
        self.device_id = device_id
        self.device_type = device_type
        # Version 2.x de paho-mqtt nécessite CallbackAPIVersion
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
            client_id=f"{device_type}_{device_id}_{random.randint(100, 999)}"
        )
        self.running = True
        self.topic = f"{BASE_TOPIC}/{device_type}/{device_id}"

    def run(self):
        # Configuration mTLS
        try:
            self.client.tls_set(
                ca_certs=CA_CERT,
                certfile=CLIENT_CERT,
                keyfile=CLIENT_KEY,
                cert_reqs=ssl.CERT_REQUIRED,
                tls_version=ssl.PROTOCOL_TLSv1_2
            )
            # Désactive la vérification du nom d'hôte si vous utilisez 'localhost'
            # mais que le certificat est généré pour un autre nom.
            self.client.tls_insecure_set(True)

            self.client.connect(BROKER, PORT, 60)
            self.client.loop_start()

            while self.running:
                data = self.simulate_sensors()
                payload = {
                    "device_id": self.device_id,
                    "type": self.device_type,
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                    "metrics": data
                }
                self.client.publish(self.topic, json.dumps(payload), qos=1)
                time.sleep(2)

        except Exception as e:
            print(f"[ERREUR] {self.device_id} : {e}")
        finally:
            self.client.loop_stop()
            self.client.disconnect()


class CNCMachine(IoTDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "cnc")
        self.temp = 22.0

    def simulate_sensors(self):
        rpm = 15000 + random.uniform(-150, 150)
        self.temp = min(85.0, self.temp + (rpm / 25000) * random.uniform(0.05, 0.15))
        vib = (rpm / 45000) + random.uniform(0.001, 0.005)
        return {
            "rpm": round(rpm, 2),
            "temp": round(self.temp, 2),
            "vib": round(vib, 4)
        }


class EnvMonitor(IoTDevice):
    def __init__(self, device_id):
        super().__init__(device_id, "env")

    def simulate_sensors(self):
        return {
            "ambient_temp": round(random.uniform(20.0, 25.0), 2),
            "humidity": round(random.uniform(40.0, 50.0), 1),
            "aqi": random.randint(20, 40)
        }


def main():
    devices = []
    # Instanciation dynamique
    for i in range(1, 6): devices.append(CNCMachine(f"CNC-{i:03}"))
    for i in range(1, 4): devices.append(EnvMonitor(f"ENV-{i:03}"))

    print(f"--- Usine active : {len(devices)} simulateurs mTLS ---")

    for d in devices:
        d.daemon = True  # Version moderne de setDaemon
        d.start()

    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt des systèmes...")
        for d in devices:
            d.running = False
            d.join()


if __name__ == "__main__":
    main()