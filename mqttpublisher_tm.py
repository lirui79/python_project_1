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
    if (mid % 1000) == 0:
        print("OnPublish, mid: "+str(mid))
 
def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

k = 0
def on_log(mqttc, obj, level, string):
    if (k % 1000) == 0:
        print("Log:"+string)
    k += 1

 
def on_message(mqttc, obj, msg):
    curtime = datetime.datetime.now()
    strcurtime = curtime.strftime("%Y-%m-%d %H:%M:%S")
    payload = json.loads(msg.payload.decode('utf-8'))
    print(strcurtime + ": " + msg.topic+" "+str(msg.qos))
    print(payload)

def on_mqtt_publisher(address, port, token, topic, msg, min, step):
    mqttlist = []
    devid = min
    for i in range(0,step,1):
        device = token + str(devid)
        mqttc = mqtt.Client(device)
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
        mqttlist.append(mqttc)
        devid += 1
        #time.sleep(1)
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
    n = 0
    while 1:
        devid = min
        for mqttc in mqttlist:
            device = token + str(devid)
            time_now = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
            payload = {"index": "%s" % i, "time": "%s" % time_now, "msg": "%s" % msg}
            # publish(主题：Topic; 消息内容)
            mqttc.publish(topic, payload = json.dumps(payload, ensure_ascii=False))

            if (n % 1000) == 0:
                print(time_now + " " + device + ": send message to server!")
            devid += 1
            n += 1
        i += 1
        time.sleep(10)



def on_mqtt_threadRun(argv):
    del argv[0]
    address = argv[0]
    port = int(argv[1])
    token = argv[2]
    topic = argv[3]
    msg = argv[4]
    min = int(argv[5])
    max = int(argv[6])
    print("address:" + address + " port:" + str(port) + "token:" + token + " topic:" + topic + "msg:" + msg)
    print("[min, max)->(" + str(min) + ", " + str(max) + ")")
    threadList = []
    step = 100
    for i in range(min,max,step):
        #token = device + str(i)
        if (i + step) > max:
           step = max - i
        thread = threading.Thread(target=on_mqtt_publisher,args=(address, port, token, topic, msg,i, step,))
        threadList.append(thread)
        thread.start()
        print("thread ========")
    
    for thread in threadList:
        thread.join()
    print("mqtt publish test over")


#=====================================================
if __name__ == '__main__':
   on_mqtt_threadRun(sys.argv)