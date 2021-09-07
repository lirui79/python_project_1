#!/usr/bin/python
 
import json
import sys
import time
import datetime
import threading
import socket, sys

import paho.mqtt.client as mqtt

 
#======================================================
def on_connect(mqttc, obj, flags, rc):
    print("OnConnetc, rc: "+str(rc))
 
def on_publish(mqttc, obj, mid):
    print("OnPublish, mid: "+str(mid))
 
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
 
def on_log(mqttc, obj, level, string):
    print("Log:"+string)
 
def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    payload = json.loads(msg.payload.decode('utf-8'))
    print(strcurtime + ": " + msg.topic+" "+str(msg.qos))
    print(payload)

def on_mqtt_publisher(address, port, token, topic, msg):
    mqttc = mqtt.Client(token)
    #mqttc = mqtt.Client(str("provision"))
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe
    mqttc.on_log = on_log
 
    # 设置账号密码（如果需要的话）
    # 用户名
    #username = 'admin'
    # 密码
    #password = 'password'
    #mqttc.username_pw_set(username, password=password)
    #broker  port
    #port = int(argv[2]);
    mqttc.connect(address, port, 60)
    time.sleep(1)
    #mqttc.loop_start()
    #topic = "/provision/request"
    #mqttc.subscribe([("/provision/request", 1),("/provision/response",2)])
    #time.sleep(1)
    #payload = "{deviceName:gcc_device,provisionDeviceKey:q4rmjrkm76m753ga752l,provisionDeviceSecret:08xu4filusqc8j8bodp9}"
    #payload = "{deviceName:device0,provisionDeviceKey:q4rmjrkm76m753ga752l,provisionDeviceSecret:08xu4filusqc8j8bodp9}"
    #mqttc.publish(topic, payload)
    #time.sleep(3)
    #mqttc.loop_forever()

    i = 0
    while 1:
        time_now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
        payload = {"index": "%s" % i, "time": "%s" % time_now, "msg": "%s" % msg}
        # publish(主题：Topic; 消息内容)
        mqttc.publish(topic, payload = json.dumps(payload, ensure_ascii=False))
        print(token + ": send message to server!")
        i += 1
        time.sleep(1)



def on_mqtt_threadRun(argv):
    del argv[0]
    address = argv[0]
    port = int(argv[1])
    device = argv[2]
    topic = argv[3]
    msg = argv[4]
    min = int(argv[5])
    max = int(argv[6])
    print("address:" + address + " port:" + str(port) + "device:" + device + " topic:" + topic + "msg:" + msg)
    print("[min, max)->(" + str(min) + ", " + str(max) + ")")
    threadList = []
    for i in range(min,max,1):
        token = device + str(i)
        thread = threading.Thread(target=on_mqtt_publisher,args=(address, port, token, topic, msg,))
        threadList.append(thread)
        thread.start()
    
    for thread in threadList:
        thread.join()
    print("mqtt publish test over")


#=====================================================
if __name__ == '__main__':
   on_mqtt_threadRun(sys.argv)