import paho.mqtt.client as mqtt
import time
import sys
import base64
import cv2

from time import sleep

HOST = 'xxx.xxx.xxx.xxx'    # 设置成你服务器的IP
PORT = 1883
client_id = 'CCTV-S'
client = mqtt.Client(client_id)

def image_to_base64(image_np):
    image = cv2.imencode('.jpg',image_np)[1]
    image_code = str(base64.b64encode(image))[2:-1]
    return image_code

def Send_Cmd():
    vc = cv2.VideoCapture(1)
    while True:
        rval, frame = vc.read()
        # cv2.imshow("dd",frame)
        cv2.waitKey(1)
        data = image_to_base64(frame)
        client.publish('Cam1',data,qos=0,retain=False)    # 填发布主题的名字
        sleep(4)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

def on_connect(client, userdata, flags, rc):
  print("Connected with result code "+str(rc))

def client_connect():
    client.username_pw_set("CCTV_S","8qADTw1m6ilcHg0pVSmh")    # 填MQTT账号密码
    client.on_connect = on_connect
    client.connect(HOST, PORT, 60)
    client.loop_start()

if __name__ == '__main__':
    client_connect()
    Send_Cmd()
