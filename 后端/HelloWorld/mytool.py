# -*- coding: UTF-8 -*-

import json
import requests, urllib3
import mysql.connector
import time
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header

urllib3.disable_warnings()


def putJson(string,ind=4):
    print(json.dumps(string,sort_keys=True,indent=ind,separators=(',',':')))

def putSize(num):
  sizelist = ["B","KB","MB","GB","TB","PB"]
  thenum = num
  size = 0
  while (int(thenum/1024)>0):
    thenum = 1.0*thenum/1024
    size += 1
  return str(round(thenum,2))+sizelist[size]

def keyindict(diction,keylist):
    thedict = diction
    for key in keylist:
        if key in thedict:
            thedict = thedict[key]
        else:
            return thedict[key]
    return thedict

def myrand(thepeer,thenum):
    flag = True
    if random.random()<0.4:
        flag = False
    peer = thepeer
    while peer>0.1:
        peer /= 10
    num = random.random()
    if num>=0.3 and num<0.6:
        num -= 0.3
    elif num>=0.6 and num<0.8:
        num -= 0.5
    elif num>=0.8 and num<1:
        num -= 0.75
    num += peer
    print("num:"+str(num))
    if flag:
        return 1.0*thenum*(1+num)
    else:
        return 1.0*thenum*(1-num)


'''
    @error_machine_id：错误机器编号，string
    @manager_email_address：管理员邮箱地址
    @error_type：错误类型, string，这个可以是事先定好的错误码，可以用int
    @error_msg：错误内容, string
    返回值为操作码，0为成功，1为错误
    需要服务器配置sendmail
'''
def sendmail(error_machine_id, manager_email_address, error_type, error_msg, flag=True):
    mail_host="smtp.qq.com"  #设置服务器
    mail_user="810625367@qq.com"    #用户名
    mail_pass="knckwabebrocbfge"   #授权码
    
    sender = '810625367@qq.com'     # 代发邮箱地址，可换
    receivers = [manager_email_address]  
    
    message = MIMEText(error_msg, 'plain', 'utf-8')
    message['From'] = Header("A niubility program", 'utf-8')
    message['To'] =  Header("Manager", 'utf-8')
    
    if flag:
      subject = "Your Switch: " + error_machine_id + " has an error, error code: " + error_type
    else:
      subject = "Your Switch: " + error_machine_id + " the error " + error_type + "is end"
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP() 
        smtpObj.connect(mail_host, 25)    # 25 为 SMTP 端口号
        smtpObj.login(mail_user,mail_pass)  
        smtpObj.sendmail(sender, receivers, message.as_string())
        return 0
    except smtplib.SMTPException:
        return 1

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
    response = session.get(myurl,verify=False).json()
    response = response["imdata"][0]
    print(response)
    thedict = keyindict(response,["topSystem","attributes"])
    response = thedict
    mydata = {
        "ip": ip,
        "hostname": (response["name"] if "name" in response else "null"),
        "serial_num": (response["serial"] if "serial" in response else "null"),
        "uptime": (response["systemUpTime"] if "systemUpTime" in response else "null"),
        "modTs": (response["modTs"] if "modTs" in response else "null")
    }

    myurl = "https://"+ip+"/api/class/eqptSupC.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]
    thedict = keyindict(response,["eqptSupC","attributes"])
    response = thedict
    mydata["opentime"] = response["upTs"] if "upTs" in response else "null"
    mydata["model"] = response["model"] if "model" in response else "null"
    mydata["numP"] = response["numP"] if "numP" in response else "null"
    mydata["swVer"] = response["swVer"] if "swVer" in response else "null"
    myurl = "https://"+ip+"/api/class/eqptCPU.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]
    thedict = keyindict(response,["eqptCPU","attributes"])
    response = thedict
    mydata["cpu_type"] = response["descr"] if "descr" in response else (response["model"] if "model" in response else "null")
    mydata["cpu_size"] = response["speed"] if "speed" in response else "null"

    myurl = "https://"+ip+"/api/class/eqptDimm.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]
    thedict = keyindict(response,["eqptDimm","attributes"])
    response = thedict
    mydata["mem_type"] = response["type"] if "type" in response else "null"
    mydata["mem_size"] = response["cap"] if "cap" in response else "null"
    
    return mydata

def getOCC(ip,session):
    myurl = "https://"+ip+"/api/class/procSysCpuSummary.json"
    myurl2 = "https://"+ip+"/api/class/procSysMem.json"
    response = session.get(myurl,verify=False).json()["imdata"][0]
    thedict = keyindict(response,["procSysCpuSummary","attributes"])
    response = thedict
    response2 = session.get(myurl2,verify=False).json()["imdata"][0]
    thedict = keyindict(response2,["procSysMem","attributes"])
    response2 = thedict
    kernel = float(response["kernel"] if "kernel" in response else 0)
    user = float(response["user"] if "user" in response else 0)
    used = float(response2["used"] if "used" in response2 else 0)
    total = float(response2["total"] if "total" in response2 else (used+1))
    mydata = {
        "cpu_occ": kernel+user,
        "mem_occ": 100.0*used/total,
        "time": int(time.time())
    }
    return mydata

def getProc(ip,username,password):
  myurl = "https://"+ip+"/ins"
  myheaders = {'content-type':'application/json'}
  payload = {
    "ins_api": {
      "version": "1.0",
      "type": "cli_show",
      "chunk": "0",
      "sid": "1",
      "input": "show processes memory",
      "output_format": "json"
    }
  }
  
  response = requests.post(myurl,data=json.dumps(payload),headers=myheaders,auth=(username,password),verify=False).json()
  thedict = keyindict(response,["ins_api","outputs","output","body","TABLE_process_memory","ROW_process_memory"])
  response = thedict
  thedata = {}
  for item in response:
    myproc = {
      "name":(item["process"] if "process" in item else "null"),
      "mem_pid":(item["mem_pid"] if "mem_pid" in item else "null"),
      "mem_alloc": putSize(int(item["mem_alloc"]) if "mem_alloc" in item else 0)
    }
    thedata[item["process"]] = myproc
  payload["ins_api"]["input"] = "show processes cpu"
  response = requests.post(myurl,data=json.dumps(payload),headers=myheaders,auth=(username,password),verify=False).json()
  thedict = keyindict(response,["ins_api","outputs","output","body","TABLE_process_cpu","ROW_process_cpu"])
  response = thedict
  for item in response: 
    myproc = thedata[item["process"]]
    myproc["pid"] = (item["pid"] if "pid" in item else "null")
    myproc["onesec"] = (item["onesec"] if "onesec" in item else "null")
  mydata = []
  for key in thedata.keys():
    mydata.append(thedata[key])

  return mydata

def initdatabase():
    mydatabase = mysql.connector.connect(
        user='root', 
        password='306812',
        host='129.204.19.52',
        database='sdn_database'
    )
    return mydatabase

def initsystem(mydatabase):
    mysystem = {}
    mycursor = mydatabase.cursor()
    mycursor.execute("SELECT * FROM device_message")
    d=mycursor.fetchall()
    mydatabase.commit()
    mycursor.close()

    for item in d:
        mydata = {}
        mydata["id"] = str(item[0])
        mydata["ip"] = str(item[1])
        mydata["username"] = str(item[2])
        mydata["password"] = str(item[3])
        mysystem[mydata["id"]] = mydata
    return mysystem

def initsession(mysystem):
    for key in mysystem.keys():
        ip = mysystem[key]["ip"]
        username = mysystem[key]["username"]
        password = mysystem[key]["password"]
        mysystem[key]["session"] = aaa_login(username,password,ip)
        mydata = getDevice(ip,mysystem[key]["session"])
        mysystem[key]["device"] = mydata

def inituserconfig(userconfig,mysystem,mydatabase):
  mycursor = mydatabase.cursor()
  newuserconfig = {}
  for key in mysystem.keys():
    bid = mysystem[key]["id"]
    mycursor.execute("SELECT * FROM user_config where BID="+bid)
    d=mycursor.fetchall()
    mydatabase.commit()
    if key not in userconfig:
      userconfig[key] = {}
    configs = userconfig[key]
    newconfigs = {}
    for item in d:
      rid = str(item[0])
      config = eval(str(item[2]))
      email = str(item[3])
      name = str(item[4]).decode('utf-8')
      text = str(item[5]).decode('utf-8')
      if rid in configs:
        newconfig = configs[rid]
        newconfig["email"] = email
        newconfig["name"] = name
        newconfig["text"] = text
      else:
        newconfig = {
          "config": {},
          "email": email,
          "name": name,
          "text": text
        }
      for element in config:
        if "type" in element and "value" in element:
            newconfig["config"][element["type"]] = element["value"]
      newconfigs[rid] = newconfig 
    newuserconfig[key] = newconfigs
  mycursor.close()

  print(newuserconfig)
  return newuserconfig


