import machine
import network
import ssl
import time
import ubinascii
from simple import MQTTClient

# =============== CONFIGURATION ===============
SSID = "*"
WIFI_PASSWORD = "*"

MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_CLIENT_KEY = "*-private.pem.key"
MQTT_CLIENT_CERT = "*-certificate.pem.crt"
MQTT_BROKER = "*.amazonaws.com"
MQTT_BROKER_CA = "AmazonRootCA1.pem"
MQTT_TOPIC = "/test"


# ================= FUNCTIONS =================
def read_pem(file):
    """
    Function that reads PEM file and return byte array of data
    """
    with open(file, "r") as input:
        text = input.read().strip()
        split_text = text.split("\n")
        base64_text = "".join(split_text[1:-1])
        return ubinascii.a2b_base64(base64_text)


def connect_internet(ssid, wifi_password):
    """
    Function that connects to the internet
    """
    try:
        sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        sta_if.connect(ssid, wifi_password)

        for i in range(0, 10):
            if not sta_if.isconnected():
                time.sleep(1)
        print("Connected to Wi-Fi")
    except Exception as e:
        print('There was an issue connecting to WIFI')
        print(e)


# ==================== MAIN ====================
# Connect to the internet
connect_internet(SSID, WIFI_PASSWORD)

# Read the data in the private key, public certificate, and root CA file
key = read_pem(MQTT_CLIENT_KEY)
cert = read_pem(MQTT_CLIENT_CERT)
ca = read_pem(MQTT_BROKER_CA)

# Create MQTT client that use TLS/SSL for a secure connection
client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    keepalive=60,
    ssl=True,
    ssl_params={
        "key": key,
        "cert": cert,
        "server_hostname": MQTT_BROKER,
        "cert_reqs": ssl.CERT_REQUIRED,
        "cadata": ca,
    },
)

# Connect to the MQTT broker
print(f"Connecting to MQTT broker")
client.connect()
print("Connection established")

# Main loop, continuously publish messages to topic
while True:
    try:
        msg = input("Enter a message >> ").strip()
        if msg:
            client.publish(TOPIC_PUB, msg)
            print(f"Message published in {TOPIC_PUB}")
    except KeyboardInterrupt:
        print("\nClossing conection.")
        client.disconnect()
        break

