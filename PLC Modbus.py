
 #!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyModbusTCP.client import ModbusClient
import paho.mqtt.client as paho
import threading
import time

SERVER_HOST = "192.168.0.3"
SERVER_PORT = 502
 
def on_connect(client, userdata, flags, rc):
    if rc == 0 :
        print("Connected to the broker")

    else:
        print("Connection failed")

def on_subscribe(client1, userdata, mid, qos):
    print("Subscribed: " +str(mid))

def on_message(client1, userdata, msg):
    print(msg.topic+" "+ str(msg.payload)) #msg.topic is a string (str) type and msg.payload byte (bytes) type
    #print(type(msg.topic))
    if not c.is_open():
        if not c.open():
            print("unable to connect")
    if c.is_open():
        print("c is open")
        if(msg.topic=='MQTT_Topic/scada/outputstatus1' and msg.payload==b'1'): # switch1
            print("true OUTPUT1 value is recieved")
            c.write_single_coil(8192, 1)
            time.sleep(0.1)
        if(msg.topic=='MQTT_Topic/scada/outputstatus1' and msg.payload==b'0'):
            print("false OUTPUT1 value is recieved")
            c.write_single_coil(8192, 0)
            time.sleep(0.1)

        if(msg.topic=='MQTT_Topic/scada/outputstatus2' and msg.payload==b'1'): # switch2
            print("true OUTPUT2 value is recieved")
            c.write_single_coil(8193, 1)
            time.sleep(0.1)
        if(msg.topic=='MQTT_Topic/scada/outputstatus2' and msg.payload==b'0'):
            print("false OUTPUT2 value is recieved")
            c.write_single_coil(8193, 0)
            time.sleep(0.1)

        if(msg.topic=='MQTT_Topic/scada/outputstatus3' and msg.payload==b'1'): # switch3
            print("true OUTPUT3 value is recieved")
            c.write_single_coil(8194, 1)
            time.sleep(0.1)
        if(msg.topic=='MQTT_Topic/scada/outputstatus3' and msg.payload==b'0'):
            print("false OUTPUT3 value is recieved")
            c.write_single_coil(8194, 0)
            time.sleep(0.1)

        if(msg.topic=='MQTT_Topic/scada/outputstatus4' and msg.payload==b'1'): # switch4
            print("true OUTPUT4 value is recieved")
            c.write_single_coil(8195, 1)
            time.sleep(0.1)
        if(msg.topic=='MQTT_Topic/scada/outputstatus4' and msg.payload==b'0'):
            print("false OUTPUT4 value is recieved")
            c.write_single_coil(8195, 0)
            time.sleep(0.1)
        time.sleep(0.1)

def readValues():
    while True:        
        bits = c.read_holding_registers(0, 1)        
        print("bit ad #0 to 9: "+str(bits) if bits else "read error")
        client.publish("MQTT_Topic/scada/inputstatus5", str(bits), qos=0)

        input_bits = c.read_discrete_inputs(0, 4)
        if(input_bits[0]):
            print("True INPUT1 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus1", "true", qos=0)
        #else: #elif
        if input_bits[0] == False:
            print("False INPUT1 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus1", "false", qos=0)
            
        if(input_bits[1]):
            print("True INPUT2 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus2", "true", qos=0)
        if input_bits[1] == False:
            print("False INPUT2 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus2", "false", qos=0)

        if(input_bits[2]):
            print("True INPUT3 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus3", "true", qos=0)
        if input_bits[2] == False:
            print("False INPUT3 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus3", "false", qos=0)

        if(input_bits[3]):
            print("True INPUT4 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus4", "true", qos=0)
        if input_bits[3] == False:
            print("False INPUT4 value is recieved")
            client.publish("MQTT_Topic/scada/inputstatus4", "false", qos=0)
        time.sleep(0.1)
        time.sleep(1)

c = ModbusClient(host="192.168.0.3", port=502, auto_open=True)

c.host(SERVER_HOST)
c.port(SERVER_PORT)

client1 = paho.Client()
client1.on_subscribe = on_subscribe
client1.on_message = on_message
client1.on_connect=on_connect #("iot.eclipse.org", 1883)
client1.connect("iot.eclipse.org", 1883)
client1.subscribe("MQTT_Topic/scada/outputstatus1", qos=0)
client1.subscribe("MQTT_Topic/scada/outputstatus2", qos=0)
client1.subscribe("MQTT_Topic/scada/outputstatus3", qos=0)
client1.subscribe("MQTT_Topic/scada/outputstatus4", qos=0)

client = paho.Client()
client.connect("iot.eclipse.org", 1883)

client1.loop_start()

thread3 = threading.Thread(target=readValues)
thread3.start()


