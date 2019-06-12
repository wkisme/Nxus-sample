
#coding:utf-8
import json
import requests, urllib3
from django.shortcuts import render
import mysql.connector
from django.http import JsonResponse,HttpResponse

urllib3.disable_warnings()

def putJson(string,ind=4):
    print(json.dumps(string,sort_keys=True,indent=ind,separators=(',',':')))

def aaa_login(username,password,ip):
    session = requests.Session()
    myurl = "https://"+ip+"/api/aaaLogin.json"
    mydata = {
    "aaaUser": {
      "attributes": {
        "name": username,
        "pwd": password
    }}}
    session.post(myurl,json=mydata,verify=False)
    return session

def getDevice(ip,session):
    myurl = "https://"+ip+"/api/mo/sys.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]["topSystem"]["attributes"]

    mydata = {
        "ip": ip,
        "hostname": (response["name"] if response["name"] else "null"),
        "serial_num": (response["serial"] if response["serial"] else "null"),
        "uptime": (response["systemUpTime"] if response["systemUpTime"] else "null"),
        "modTs": (response["modTs"] if response["modTs"] else "null")
    }

    myurl = "https://"+ip+"/api/class/eqptSupC.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]["eqptSupC"]["attributes"]
    mydata["opentime"] = response["upTs"] if response["upTs"] else "null"
    mydata["model"] = response["model"] if response["model"] else "null"
    mydata["numP"] = response["numP"] if response["numP"] else "null"
    mydata["swVer"] = response["swVer"] if response["swVer"] else "null"
    myurl = "https://"+ip+"/api/class/eqptCPU.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]["eqptCPU"]["attributes"]
    mydata["cpu_type"] = response["descr"] if response["descr"] else (response["model"] if response["model"] else "null")
    mydata["cpu_size"] = response["speed"] if response["speed"] else "null"

    myurl = "https://"+ip+"/api/class/eqptDimm.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]["eqptDimm"]["attributes"]
    mydata["mem_type"] = response["type"] if response["type"] else "null"
    mydata["mem_size"] = response["cap"] if response["cap"] else "null"
    return mydata

def alldevice(request):
    

    mydb = mysql.connector.connect(
    user='root', password='root',
    host='127.0.0.1',
    database='123'
    )
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM device_message")
    d=mycursor.fetchall()
    data = []
    for item in d:
        mydata = {}
        mydata["id"] = item[0]
        mydata["ip"] = item[1]
        mydata["username"] = item[2]
        mydata["password"] = item[3]
        data.append(mydata)
    device = []
    print(data)
    for item in data:
        print()
        print(item)
        session = aaa_login(item["username"],item["password"],item["ip"])
        mydata = getDevice(item["ip"],session)
        mydata["id"] = item["id"]
        device.append(mydata)
    return render(request, 'hello.html', {
        'hello': json.dumps(device),
    })

    
def readcpu(request):
    request.encoding='utf-8'
    print(request.GET)
    start = request.GET["start"]
    end = request.GET["end"]
    bid = request.GET["bid"]
    mydb = mysql.connector.connect(
    user='root', password='root',
    host='127.0.0.1',
    database='123'
    )
    print(123)
    mycursor = mydb.cursor()
    sql = "select * from device_status where BID=%s and nowtime>= %s and nowtime<=%s" 
    na=(bid,start,end)
    mycursor.execute(sql,na)
    d=mycursor.fetchall()
    data = []
    i=0
    for item in d:
        mydata1 = {}
        mydata1["ID"] = str(item[0])
        mydata1["BID"] = str(item[1])
        mydata1["CPUOCC"] = str(item[2])
        mydata1["MEMOCC"] = str(item[3])
        mydata1["nowtime"] = str(item[4])
        data.append(mydata1)
        i+=1
    print(i)
    
    return HttpResponse(json.dumps(data), content_type="application/json")



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    