import paho.mqtt.client as mqtt
import time
import sys
import base64

from time import sleep

HOST = 'xxx.xxx.xxx.xxx'    # 设置成你服务器的IP
PORT = 1883
client_id = 'CCTV-R'
client = mqtt.Client(client_id)

def base64_to_image(image_read):
    imgdata=base64.b64decode(image_read)
    Image = open('Cam1.jpg','wb')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    Image.write(imgdata)
    Image.close() 

def on_message_come_cmd(client, userdata, msg):
    base64_to_image(msg.payload.decode("UTF-8"))
    print("RECEIVE Successfully")

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

def client_connect():
    client.username_pw_set("CCTV_R","8qADTw1m6ilcHg0pVSmh")    # 填MQTT账号密码
    client.on_connect = on_connect
    client.connect(HOST, PORT, 60)
    client.loop_start()
    client.subscribe("Cam1", 1)    # 填订阅主题的名字
    client.on_message = on_message_come_cmd

if __name__ == '__main__':
    client_connect()
    while(True):
        time.sleep(20)
