# -*- coding: UTF-8 -*-

import json
import requests, urllib3
from django.shortcuts import render
import mysql.connector
from django.http import JsonResponse,HttpResponse
import random
from . import mytool

urllib3.disable_warnings()

mydatabase = mytool.initdatabase()
mysystem = mytool.initsystem(mydatabase)
mytool.initsession(mysystem)
# print(mydatabase)
# print(mysystem.keys())
# print(mysystem)

def alldevice(request):
    device = []

    for key in mysystem.keys():
        ip = mysystem[key]["ip"]
        session = mysystem[key]["session"]
        mydata = mytool.getDevice(ip,session)
        mydata["id"] = mysystem[key]["id"]
        device.append(mydata)
        
    return HttpResponse(json.dumps(device), content_type="application/json")
    
def readcpu(request):
    request.encoding='utf-8'
    start = request.GET["start"]
    end = request.GET["end"]
    bid = request.GET["bid"]
    mycursor = mydatabase.cursor()
    sql = "select * from device_status where BID=%s and nowtime>= %s and nowtime<=%s" 
    val=(bid,start,end)
    mycursor.execute(sql,val)
    d=mycursor.fetchall()
    mydatabase.commit()
    mycursor.close()
    
    data = []
    for item in d:
        mydata = {}
        mydata["ID"] = str(item[0])
        mydata["BID"] = str(item[1])
        mydata["CPUOCC"] = str(item[2])
        mydata["MEMOCC"] = str(item[3])
        mydata["nowtime"] = str(item[4])
        data.append(mydata)

    return HttpResponse(json.dumps(data), content_type="application/json")

def readflow(request):
    request.encoding='utf-8'
    bid = request.GET["bid"]
    pid = request.GET["pid"]
    start = request.GET["start"]
    end = request.GET["end"]
    peer = int(bid)+int(pid)
    mycursor = mydatabase.cursor()
    sql = "select * from device_status where BID=%s and nowtime>= %s and nowtime<=%s" 
    val=(bid,start,end)
    mycursor.execute(sql,val)
    d=mycursor.fetchall()
    mydatabase.commit()
    mycursor.close()

    data = []
    for item in d:
        mydata = {}
        cpu_occ = float(item[2])
        mem_occ = float(item[3])
        thenum = cpu_occ+mem_occ
        mydata["num"] = mytool.myrand(peer,thenum)
        data.append(mydata)
        
    return HttpResponse(json.dumps(data), content_type="application/json")



def setconfig(request):
    request.encoding='utf-8'
    bid = request.GET["bid"]
    config = request.GET["config"]
    email = request.GET["email"]
    name = request.GET["name"]
    text = request.GET["text"]
    # data = {}
    # data["bid"] = bid
    # data["config"] = config
    # data["email"] = email
    
    mycursor = mydatabase.cursor()
    sql = "INSERT INTO user_config (BID,config,email,name,text) VALUES (%s,%s,%s,%s,%s)"
    val = (bid,config,email,name,text)
    
    mycursor.execute(sql, val)
    mydatabase.commit()
    mycursor.close()

    return HttpResponse(json.dumps({"status":"OK"}), content_type="application/json")

def getconfig(request):
    request.encoding='utf-8'
    # bid = request.GET["bid"]
    mycursor = mydatabase.cursor()
    # sql = "select * from user_config where BID="+bid
    sql = "select * from user_config"
    mycursor.execute(sql)
    d=mycursor.fetchall()
    mydatabase.commit()
    mycursor.close()

    configs = []
    for item in d:
        mydata = {}
        mydata["id"] = str(item[0]) 
        mydata["bid"] = int(item[1])
        mydata["config"] = str(item[2])
        mydata["email"] = str(item[3])
        mydata["name"] = str(item[4]).decode('utf-8')
        mydata["text"] = str(item[5]).decode('utf-8')
        configs.append(mydata)

    return HttpResponse(json.dumps(configs), content_type="application/json")

def deleteconfig(request):
    request.encoding='utf-8'
    rid = request.GET["rid"]
    print(rid)
    mycursor = mydatabase.cursor()
    sql = "delete from user_config where id="+str(rid)
    mycursor.execute(sql)
    mydatabase.commit()
    mycursor.close()
    
    return HttpResponse(json.dumps({"status":"OK"}), content_type="application/json")

def getproc(request):
    request.encoding='utf-8'
    bid = request.GET["bid"]
    ip = mysystem[bid]["ip"]
    username = mysystem[bid]["username"]
    password = mysystem[bid]["password"]
    mydata = mytool.getProc(ip,username,password)
    return HttpResponse(json.dumps(mydata), content_type="application/json")



    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    