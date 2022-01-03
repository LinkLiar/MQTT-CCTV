import paho.mqtt.client as mqtt
import time
import sys
import base64
import cv2


HOST = 'xxx.xxx.xxx.xxx'    # 设置成你服务器的IP
PORT = 1883
clientID = 'CCTV-S'
width = 800
height = 600

def ImageToBase64(image_np):
    image = cv2.imencode('.jpg', image_np)[1]
    imageCode = str(base64.b64encode(image))[2:-1]
    return imageCode


def SendingImage():
    cap = cv2.VideoCapture(0)    # 设置成摄像头的ID
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,width);
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height);
    print("Camera initialized successfully...")
    while True:
        ret, frame = cap.read()
        disconnectTime = 0
        while(not ret):
            tic = time.time()
            time.sleep(6)
            cap = cv2.VideoCapture(0)
            cap.set(cv2.CAP_PROP_FRAME_WIDTH,width);
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT,height);
            ret, frame = cap.read()
            toc = time.time()
            disconnectTime += toc-tic
            print("Camera disconnected...for " +
                  f"{disconnectTime:.4f}" + " seconds")

        data = ImageToBase64(frame)

        client.publish('Cam1', data, qos=0, retain=False)    # 填发布主题的名字
        cv2.imshow("Test Frame", frame)
        cv2.waitKey(1)
        time.sleep(6)
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) +
              "   " + f"{height}h {width}w   " + f"size: {len(data)/1024:.4f} kB")


def OnConnect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def ClientConnect():
    client.username_pw_set("CCTV_S", "8qADTw1m6ilcHg0pVSmh")    # 填MQTT账号密码
    client.on_connect = OnConnect
    client.connect(HOST, PORT, 60)
    client.loop_start()


if __name__ == '__main__':
    client = mqtt.Client(clientID)
    ClientConnect()
    SendingImage()
