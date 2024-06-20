import paho.mqtt.client as mqtt
import json

# MQTT client setup
id = "19602254-4be3-4494-aadb-87d289ded60a"  # Provide your MQTT ID here
nombre_cliente = id + "LuzAutomatica2"
cliente_telemetria_comando = id + "/apagar"

servidor = mqtt.Client(client_id=nombre_cliente, protocol=mqtt.MQTTv311)
servidor.connect("localhost")

# Callback for received messages
def cuando_entra_un_mensaje(cliente, datos_de_usuario, msj):
    print("Mensaje recibido:", str(msj.payload.decode("utf-8")))

# Setup message handling and subscription
servidor.on_message = cuando_entra_un_mensaje
servidor.subscribe(id + "/luzpatio", qos=1)

# Publish command to turn off the LED
servidor.publish(cliente_telemetria_comando, json.dumps({"apagar": True}))

# Start the loop to process received messages
servidor.loop_forever()
