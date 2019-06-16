# -*- coding: UTF-8 -*-

import mysql.connector
import mysql.connector
import time, datetime
import requests
import os, sys

mypath = os.path.join(os.path.dirname(os.path.abspath(__file__)),'HelloWorld')
sys.path.append(mypath)
import mytool

mydatabase = mytool.initdatabase()
mysystem = mytool.initsystem(mydatabase)
mytool.initsession(mysystem)
userconfig = {}
userconfig = mytool.inituserconfig(userconfig,mysystem,mydatabase)

def senderror(text,nowdata):
  error_machine_id = nowdata["hostname"]
  manager_email_address = text["email"]
  error_type = text["name"]
  error_msg = "nowtime: "+time.strftime("%Y--%m--%d %H:%M:%S",time.localtime(nowdata["time"]))
  error_msg += "\ncpu_occ: "+(str(nowdata["cpu_occ"]) if "cpu_occ" in nowdata else "null")
  error_msg += "\nmem_occ: "+(str(nowdata["mem_occ"]) if "mem_occ" in nowdata else "null")
  error_msg += "\ntext: " + text["text"]+"\n"
  a = mytool.sendmail(error_machine_id, manager_email_address, error_type, error_msg)
  if not a:
    print("报错邮件发送成功！")
  else:
    print("报错邮件发送失败！")

def sendnormal(text,nowdata):
  error_machine_id = nowdata["hostname"]
  manager_email_address = text["email"]
  error_type = text["name"]
  error_msg = "nowtime: "+time.strftime("%Y--%m--%d %H:%M:%S",time.localtime(nowdata["time"]))
  error_msg += "\nerrtime: "+time.strftime("%Y--%m--%d %H:%M:%S",time.localtime(text["time"]))
  error_msg += "\ncpu_occ: "+(str(nowdata["cpu_occ"]) if "cpu_occ" in nowdata else "null")
  error_msg += "\nmem_occ: "+(str(nowdata["mem_occ"]) if "mem_occ" in nowdata else "null")
  error_msg += "\ntext: " + text["text"]+"\n"
  a = mytool.sendmail(error_machine_id, manager_email_address, error_type, error_msg,False)
  if not a:
    print("返回正常邮件发送成功！")
  else:
    print("返回正常邮件发送失败！")
  pass

mycursor = mydatabase.cursor()
data = []
while True:
  try:
    for key in mysystem.keys():
      ip = mysystem[key]["ip"]
      session = mysystem[key]["session"]
      mydata = mytool.getOCC(ip,session)
      print(mydata)
      configs = userconfig[key]
      
      for thekey in configs.keys():
        item = configs[thekey]
        item["Eflag"] = False # 假设设备正常
        nowdata = {
          "hostname": mysystem[key]["device"]["hostname"],
          "ip": ip,
          "time": mydata["time"]
        }
        config = item["config"]
        if "cpu" in config and "mem" not in config:
          if mydata["cpu_occ"]>=float(config["cpu"]):
            nowdata["cpu_occ"] = mydata["cpu_occ"]
            item["Eflag"] = True
        elif "cpu" not in config and "mem" in config:
          if mydata["mem_occ"]>=float(config["mem"]):
            nowdata["mem_occ"] = mydata["mem_occ"]
            item["Eflag"] = True
        elif "cpu" in config and "mem" in config:
          if mydata["cpu_occ"]>=float(config["cpu"]) and mydata["mem_occ"]>=float(config["mem"]):
            nowdata["cpu_occ"] = mydata["cpu_occ"]
            nowdata["mem_occ"] = mydata["mem_occ"]
            item["Eflag"] = True
            
        # if "cpu" in config and mydata["cpu_occ"]>=float(config["cpu"]):
        #   nowdata["cpu_occ"] = mydata["cpu_occ"]
        #   item["Eflag"] = True
        # if "mem" in config and mydata["mem_occ"]>=float(config["mem"]):
        #   nowdata["mem_occ"] = mydata["mem_occ"]
        #   item["Eflag"] = True
        if item["Eflag"] and "Yflag" not in item:
          print(1)
          item["time"] = mydata["time"]
          senderror(item,nowdata)
          item["Yflag"] = True
        elif item["Eflag"] and not item["Yflag"]:
          print(2) 
          item["time"] = mydata["time"]
          senderror(item,nowdata)
          item["Yflag"] = True
        elif item["Eflag"] and item["Yflag"]:
          print(3) 
          pass
        elif not item["Eflag"] and "Yflag" not in item:
          print(4) 
          pass
        elif not item["Eflag"] and not item["Yflag"]:
          print(5) 
          pass
        elif not item["Eflag"] and item["Yflag"]:
          print(6) 
          sendnormal(item,nowdata)
          item["Yflag"] = False
        else:
          print(7) 

      mydata["bid"] = mysystem[key]["id"]
      sql = "INSERT INTO device_status (BID,CPUOCC,MEMOCC,nowtime) VALUES (%s,%s,%s,%s)"
      val = (mydata["bid"],mydata["cpu_occ"],mydata["mem_occ"],mydata["time"])
      mycursor.execute(sql, val)
      mydatabase.commit()
      data.append(mydata)
      print(mydata)
    userconfig = mytool.inituserconfig(userconfig,mysystem,mydatabase)
    time.sleep(5)
  except:
    continue