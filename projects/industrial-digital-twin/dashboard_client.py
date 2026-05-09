import paho.mqtt.client as mqtt
import json
import ssl
import os

# --- Configuration (Identique aux simulateurs) ---
BROKER = "localhost"
PORT = 8883
CA_CERT = "certificats/ca.crt"
CLIENT_CERT = "certificats/client.crt"
CLIENT_KEY = "certificats/client.key"
TOPIC = "youssef/iot/#"  # S'abonne à tout sous cette racine


def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print(f"[DASHBOARD] Connecté avec succès. Écoute sur {TOPIC}...")
        client.subscribe(TOPIC)
    else:
        print(f"[ERREUR] Échec de connexion, code : {rc}")


def on_message(client, userdata, msg):
    """Callback déclenché à chaque réception de message."""
    try:
        # Décodage du JSON
        payload = json.loads(msg.payload.decode())
        device_id = payload.get("device_id", "Unknown")
        device_type = payload.get("type", "Unknown")
        metrics = payload.get("metrics", {})

        # Formatage de l'affichage
        timestamp = payload.get("timestamp", "").split("T")[1][:8]  # On garde juste l'heure

        if device_type == "cnc":
            print(f"[{timestamp}] [MACHINE] {device_id} | RPM: {metrics['rpm']} | Temp: {metrics['temp']}°C")
        elif device_type == "env":
            print(f"[{timestamp}] [ENVIRON] {device_id} | AQI: {metrics['aqi']} | Hum: {metrics['humidity']}%")

    except Exception as e:
        print(f"[ERREUR DECODAGE] : {e}")


def main():
    # Initialisation du client (Version 2.x de Paho)
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    # Configuration mTLS
    client.tls_set(
        ca_certs=CA_CERT,
        certfile=CLIENT_CERT,
        keyfile=CLIENT_KEY,
        cert_reqs=ssl.CERT_REQUIRED,
        tls_version=ssl.PROTOCOL_TLSv1_2
    )
    client.tls_insecure_set(True)

    try:
        print("[INFO] Lancement du Dashboard sécurisé...")
        client.connect(BROKER, PORT, 60)
        # loop_forever est bloquant, idéal pour un client qui ne fait qu'écouter
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[INFO] Fermeture du Dashboard.")
        client.disconnect()


if __name__ == "__main__":
    main()