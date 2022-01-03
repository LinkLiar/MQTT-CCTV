# coding:utf-8
import paho.mqtt.client as mqtt
import time
import sys
import base64
import webbrowser
from time import sleep

HOST = 'xxx.xxx.xxx.xxx'
PORT = 1883
client_id = 'CCTV-R'
client = mqtt.Client(client_id)

# 命名生成的html
GEN_HTML = "index.html"
message = """
<!DOCTYPE > 
<html xmlns="http://www.w3.org/1999/xhtml"> 
<head> 
<meta charset="utf-8" /> 
<title>监控中......</title> 
        <script language="JavaScript">
            function startTime()   
            {   
                var today=new Date();//定义日期对象   
                var yyyy = today.getFullYear();//通过日期对象的getFullYear()方法返回年    
                var MM = today.getMonth()+1;//通过日期对象的getMonth()方法返回年    
                var dd = today.getDate();//通过日期对象的getDate()方法返回年     
                var hh=today.getHours();//通过日期对象的getHours方法返回小时   
                var mm=today.getMinutes();//通过日期对象的getMinutes方法返回分钟   
                var ss=today.getSeconds();//通过日期对象的getSeconds方法返回秒   
                // 如果分钟或小时的值小于10，则在其值前加0，比如如果时间是下午3点20分9秒的话，则显示15：20：09   
                MM=checkTime(MM);
                dd=checkTime(dd);
                hh=checkTime(hh);
                mm=checkTime(mm);   
                ss=checkTime(ss);    
                var day; //用于保存星期（getDay()方法得到星期编号）
                if(today.getDay()==0)   day   =   "星期日 " 
                if(today.getDay()==1)   day   =   "星期一 " 
                if(today.getDay()==2)   day   =   "星期二 " 
                if(today.getDay()==3)   day   =   "星期三 " 
                if(today.getDay()==4)   day   =   "星期四 " 
                if(today.getDay()==5)   day   =   "星期五 " 
                if(today.getDay()==6)   day   =   "星期六 " 
                document.getElementById('nowDateTimeSpan').innerHTML=yyyy+"-"+MM +"-"+ dd +" " + hh+":"+mm+":"+ss+"   " + day;   
                setTimeout('startTime()',1000);//每一秒中重新加载startTime()方法 
            }   
             
            function checkTime(i)   
            {   
                if (i<10){
                    i="0" + i;
                }   
                  return i;
            }  
        </script>
<style> 
.divcss5{text-align:center} 
</style> 
</head> 
<body> 
<div class="divcss5"><img src="Cam1.jpg" /></div> 
<body onload="startTime()">
	   <center>该帧时间：<font color="#000000">%s</font> </center>
        <center>当前时间：<font color="#000000"><span id="nowDateTimeSpan"></span></font> </center>
</body>
</body> 
</html> 
"""


def Base64ToImage(imageRec):
    imgData = base64.b64decode(imageRec)
    imageHandle = open('Cam1.jpg', 'wb')
    RealTime = time.localtime(time.time() + 28800)    # 与北京时间的偏移
    print(time.strftime("%Y-%m-%d %H:%M:%S", RealTime))
    imageHandle.write(imgData)
    imageHandle.close()

    # 打开文件，准备写入
    f = open(GEN_HTML, 'w')
    DayNumber = time.strftime("%w", RealTime)
    if(DayNumber == '0'):
        day = "星期日"
    if(DayNumber == '1'):
        day = "星期一"
    if(DayNumber == '2'):
        day = "星期二"
    if(DayNumber == '3'):
        day = "星期三"
    if(DayNumber == '4'):
        day = "星期四"
    if(DayNumber == '5'):
        day = "星期五"
    if(DayNumber == '6'):
        day = "星期六"
    text = time.strftime("%Y-%m-%d %H:%M:%S", RealTime) + ' ' + day


    f.write(message % text)    # 写入文件
    f.close()    # 关闭文件
    webbrowser.open(GEN_HTML, new=1)


def OnMessageComeCmd(client, userdata, msg):
    Base64ToImage(msg.payload.decode("UTF-8"))
    print("RECEIVE Successfully")


def OnConnect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))


def client_connect():
    client.username_pw_set("CCTV_R", "8qADTw1m6ilcHg0pVSmh")
    client.on_connect = OnConnect
    client.connect(HOST, PORT, 60)
    client.loop_start()
    client.subscribe("Cam1", 1)
    client.on_message = OnMessageComeCmd


if __name__ == '__main__':
    client_connect()
    while(True):
        time.sleep(20)
