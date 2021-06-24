import paho.mqtt.client as paho
import json
import os
import random
from time import sleep, time

# functions
def current_milli_time():
    """
    This function is used to get current time in milliseconds
    """
    return round(time() * 1000)

def save_log(json_data):
    """
    This function is used to record sensor data into a log file
    """
    path_output = 'output/logs.json'
    file_exists = os.path.isfile(path_output)
    if file_exists == True:
        with open(path_output,'r+') as file:            
            file_data = json.load(file)
            # get last id
            last_id = file_data["logs"][-1]["id"]
            json_data["id"] = last_id+1
            # append new data 
            file_data["logs"].append(json_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent=4)
    else:            
        with open(path_output, 'w+') as file:
            logs = {}
            logs["logs"] = [json_data]
            json.dump(logs, file, indent=4)

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    """
    This function is used when connecting to broker mqtt broker
    """
    if rc==0:
		# subscribe to topic wildcard
        client.subscribe("sensor/#", 1)
        print("connected OK Returned code=",rc)
    else:
        print("Bad connection Returned code=",rc)

def on_subscribe(client, userdata, mid, granted_qos):   #create function for callback
    """
    This function is used when subscribing to a topic
    """
    print("subscribed with qos",granted_qos, "\n")

def on_message(client, userdata, message):
    """
    This function is used when there is an incoming message
    """	        
    get_topic = message.topic
    get_msg = message.payload.decode("utf-8")
    # convert string to dict
    data = eval(get_msg)    
    temp = data["temp"]
    hum = data["hum"]
    room = get_topic.split("/")[1]
    timestamp = current_milli_time()           
    sensor_dict = {
        "id": 1,
        "temperature": temp,
        "humidity": hum,
        "roomArea": room,      
        "timestamp": timestamp
    }
    save_log(sensor_dict)
    
def on_publish(client,userdata,mid):   #create function for callback
    """
    This function is used when publishing message
    """
    print("data published mid=",mid, "\n")

def on_disconnect(client, userdata, rc):
    """
    This function is used when the connection is lost
    """
    print("client disconnected ok")
    client.connected_flag=False
    client.disconnect_flag=True	

def main(): 
    # publish dummy sensor data every 2 minutes      
    random_room = random.randint(1, 10)
    random_temp = random.uniform(20.0, 40.0)
    random_hum = random.uniform(70.0, 90.0)
    data = {"temp": random_temp, "hum": random_hum}
    json_data = json.dumps(data)
    client.publish(f"sensor/room{random_room}", json_data, 1)
    
# start mqtt connection and streaming process
broker="localhost"
port= 1883
client= paho.Client("client-sub")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_publish = on_publish
client.on_message = on_message
client.on_disconnect = on_disconnect
print("connecting to broker ",broker,"on port ",port)
client.connect(broker,port)
client.loop_start()

if __name__ == "__main__":
    while True:
        sleep(120)
        main()
        
