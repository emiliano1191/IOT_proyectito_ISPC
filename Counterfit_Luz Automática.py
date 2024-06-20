from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_light_sensor_v1_2 import GroveLightSensor
from counterfit_shims_grove.grove_led import GroveLed
import paho.mqtt.client as mqtt
import json
import time

# Initialize the CounterFit connection
CounterFitConnection.init("localhost", 5000)

# Create sensor and LED objects
sensor_de_luz = GroveLightSensor(0)
faro_led = GroveLed(1)

# MQTT client setup
id = "19602254-4be3-4494-aadb-87d289ded60a"  # Provide your MQTT ID here
nombre_cliente = id + "LuzAutomatica"
mqtt_cliente = mqtt.Client(client_id=nombre_cliente, protocol=mqtt.MQTTv311)

# Connect to the MQTT broker
mqtt_cliente.connect("localhost")
mqtt_cliente.loop_start()

# Check connection
if mqtt_cliente.is_connected():
    print("Conectado al servidor")
else:
    print("Hubo un problema al conectarse")

# Define MQTT topics
cliente_telemetria_topico = id + "/luzpatio"
cliente_telemetria_comando = id + "/apagar"

# Callback for received messages
def cuando_entra_un_mensaje(cliente, datos_de_usuario, msj):
    msj = json.loads(msj.payload.decode())
    print("Comando recibido: ", msj)
    if msj.get("apagar"):
        faro_led.off()
    else:
        faro_led.on()

# Setup message handling and subscription
mqtt_cliente.on_message = cuando_entra_un_mensaje
mqtt_cliente.subscribe(cliente_telemetria_comando, qos=1)

# Main loop to publish sensor data
while True:
    lumenes_sensor1 = sensor_de_luz.light
    telemetria = json.dumps({"Luz": lumenes_sensor1})
    print(f"Enviando valor del sensor de luz 1: {telemetria}")
    mqtt_cliente.publish(cliente_telemetria_topico, telemetria)
    time.sleep(5)
