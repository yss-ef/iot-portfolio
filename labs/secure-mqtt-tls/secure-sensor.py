import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import ssl
import time

# --- Chemins vers les certificats ---
CA_CERT = "./certificates/ca/ca.crt"
CLIENT_CERT = "./certificates/client/client.crt"
CLIENT_KEY = "./certificates/client/client.key"
BROKER = "localhost"
PORT = 8883

# 1. Utilisation de la nouvelle API (v2) pour éviter le DeprecationWarning
client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2, client_id="sensor_1")

# 2. Last Will and Testament
client.will_set(topic="status/sensor_1", payload="Offline unexpectedly", qos=1, retain=True)

# 3. Configuration TLS
client.tls_set(
    ca_certs=CA_CERT,
    certfile=CLIENT_CERT,
    keyfile=CLIENT_KEY,
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2
)

try:
    print(f"Tentative de connexion à {BROKER}:{PORT}...")
    client.connect(BROKER, PORT)
    client.loop_start()

    for i in range(5):
        client.publish("secure/topic", f"Data point {i}", qos=1)
        print(f"Envoyé : Data point {i}")
        time.sleep(2)

    client.loop_stop()
    client.disconnect()
    print("Déconnexion propre.")
except Exception as e:
    print(f"Erreur : {e}")