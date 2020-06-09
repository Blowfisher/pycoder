#!/usr/bin/env python
#coding:utf-8

import requests
import os
import sys
import urllib2
from datetime import datetime,timedelta
import json
import time
from sendmail import addr_list,sendmailer
#from ec2_instance import aws_ec2_check
#from mapr_alert import mapr_alerts


s = set() #used by issue number sum
d = {} #sued by alert times and messages
url = 'https://oapi.dingtalk.com/robot/send?access_token=613340c612643bdc03abce3059d4ab846ceff54372f0ef45e17ac132c8edc1' #钉钉聊天室api
reminders = []
log_file = "/var/log/gra_ding.log"
ec2_day = 0 #datetime.now().day
mon = datetime.now().month
mon_log_name = '/mnt/log/alert/' + str(datetime.now().month) + '_month_alert.log'
Old_mapr_alert_set =set()

# DingDing send messager
def send_msg(url, remiders, msg):
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    data = {
        "msgtype": "text",
        "at": {
            "atMobiles": remiders,
            "isAtAll": True,
        },
        "text": {
            "content": msg,
        }
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    return r.text
#start send message
#send_msg(url,reminders,"Grafana agent has recovered!")

#Track log document
def write_log(file_name,msg):
    with open(file_name,"ab+") as f:
        f.write(msg)
    return

#The alert message init.
reload(sys)
sys.setdefaultencoding('utf-8')
def msg(name,host,alert_id,item_v,dashboard,alert_time):
    msg = """Alarm:  %s
Host(metric): %s
ID: %s
Value: %s
Dashboard: %s
Time: %s (UTC+8)"""%(name,host,alert_id,item_v,dashboard,alert_time)
    return msg

def msg_ding(name,host,alert_id,item_v,dashboard,alert_time,alert_num=None,total_num=0):
    msg = """Alarm:  %s
Host(metric): %s
ID: %s
Value: %s
Dashboard: %s
24h Metric：%s times
Alerting: %s issues
Time: %s """%(name,host,alert_id,item_v,dashboard,alert_num,total_num,alert_time)
    return msg

#Message  处理
#Message  处理
def info_helper(i):
    host=[]
    item_v=[]
    alert_time = int(time.time())
    time_around = time.time() - 86400
    gurl = 'http://127.0.0.1/api/alerts/%s'%(i['id'])
    alert_info = get_content(gurl)
    data_info = json.loads(alert_info.read())

    try:
#        print("Try sentence start: ")
        for j in d[i['id']]['alert_num']:
            if j <= time_around:
#                print("List paramenter delete: ")
                d[i['id']]['alert_num'].pop(d[i['id']]['alert_num'].index(j))
            else:
                break
        d[i['id']]['alert_num'].append(alert_time)
#        print("Appended alert_time ")
    except Exception as e:
#        print("Exception Err happened : ",e)
        d[i['id']] = {}
        d[i['id']]['alert_num']=[]
        d[i['id']]['alert_num'].append(alert_time)
#        print("Exception appended alert time.")
    if data_info['ExecutionError'] <> " ":
        item_v = data_info['ExecutionError']
        d[i['id']]['host'] = host
        d[i['id']]['item_v'] = item_v
    else:
        for j in data_info['EvalData']:
            host.append(j.pop('metric'))
            item_v.append(j.pop('value'))
        d[i['id']]['host'] = host
        d[i['id']]['item_v'] = item_v

    return host,item_v
#提交认证信息 获取所需内容
#提交认证信息 获取所需内容
def get_content(gurl):
    header = ('Authorization','Bearer eyJrIjoiS1c1c0pPUzRKeVI3d36VUduUGpyZzdOWlNDYXlzZlYiLCJuIjoiQ04tU1ZvaWNlIiwiaWQiOjJ9')  #grafana用户信息
    opener = urllib2.build_opener()
    opener.addheaders = [header]
    f = opener.open(gurl)
    return f

#月告警记录统计
def mon_log(log_name,mon):
    if datetime.now().month <> mon:
        log_name = '/mnt/log/alert/' + str(datetime.now().month) + '_month_alert.log'
        mon = datetime.now().month
    if not os.path.exists(log_name):
        write_log(log_name,"name,host(metric),id,value,dashboard,time,r_time\n")
    return log_name,mon
#EC2 check
'''
def ec2_check(url,ec2_day):
    if ec2_day <> datetime.now().day:
        ec2_day = datetime.now().day
        ec2_stat = aws_ec2_check()
        if ec2_stat.__len__() <> 0:
            for i in ec2_stat.keys():
                msg = """Name: EC2 events alert
%s
InstanceId: %s
IP: %s
"""%(ec2_stat[i]['info'].replace('"',''),i,ec2_stat[i]['IP'])
                send_msg(url, reminders, msg)

#        return ec2_day
    return ec2_day

def mapr_check(x):
    for i in Mapr_alerts[x].keys():
        if i not in s:
            s.add(i)
            Old_mapr_alert_set.add(i)
            dt = (datetime.now()+timedelta(hours=8)).ctime().replace("'",'')
            msg = """Alarm: Mapr %s alert
Hosts: %s
Cluster: Mapr_%s
Time: %s
"""%(i,str(Mapr_alerts[x][i]).replace('[','').replace(']','').replace("'",''),x,dt)
            send_msg(url,reminders,msg)
            write_log(mon_log_name,"""%s,%s,%s,%s\n"""%(i,str(Mapr_alerts[x][i]).replace('[','').replace(']','').replace("'",''),x,dt))
'''
while True:
    gurl = 'http://127.0.0.1/api/alerts'
    alert = get_content(gurl)
    data = json.loads(alert.read())
#    ec2_day = ec2_check(url,ec2_day)

#Mapr alert
'''
    Mapr_alerts = mapr_alerts()
    if Mapr_alerts.__len__() > 0:
        map(mapr_check,Mapr_alerts.keys())
    else:
        for i in Old_mapr_alert_set:
            dt = (datetime.now()+timedelta(hours=8)).ctime().replace("'",'')
            msg = """Alarm: Mapr %s alert Recovery !
Time: %s(UTC+8)
"""%(i,dt)
            send_msg(url,reminders,msg)
            s.remove(i)
        Old_mapr_alert_set.clear()
#    print("day :",ec2_day)
'''
    for i in data:
#告警信息
        if i['state'] <> 'ok' and i['state'] <> 'no_data':
            if i['id'] not in s:
                s.add(i['id'])
                dt = (datetime.strptime(i["newStateDate"].strip('Z').replace('T',' '),'%Y-%m-%d %H:%M:%S') + timedelta(hours=8)).ctime()
            #    print(dt,i['id'])
                host_str=str()
                host,item_v = info_helper(i)
                for j in host:host_str= host_str +' '+str(j)
                dashboard = i['dashboardUri'].replace('db/','')
#                print('The dicotionary is: ',d[i['id']])
                if 'HandleRequest' in item_v or item_v.__len__() == 0:
                    write_log(log_file,"""Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"""%(dt,i['name'],host,i['id'],item_v,dashboard))
                else:
                    mon_log_name,mon = mon_log(mon_log_name,mon)
                    recv = sendmailer(i['name'],msg(i['name'],host_str,i['id'],item_v,dashboard,dt),addr_list)
                    if recv <> None:
                        send_msg(url,reminders,recv)

#                    write_log(mon_log_name,"""%s,%s,%s,%s,%s,%s\n"""%(i['name'],host_str,i['id'],reduce(lambda x,y:str(x)+' '+str(y),item_v),dashboard,dt))
                    send_msg(url,reminders,msg_ding(i['name'],host_str,i['id'],item_v,dashboard,dt,d[i['id']]['alert_num'].__len__(),s.__len__()))
                    write_log(log_file,"""Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"""%(dt,i['name'],host,i['id'],item_v,dashboard))

#恢复信息
        if i['id'] in s and i['state'] == 'ok':
            h_str=''
            s.remove(i['id'])
            host = d[i['id']].pop('host')
            for r in host:h_str= h_str +' '+str(r)
            item_v = d[i['id']].pop('item_v')
            name = i['name']+' Recovery !'
            dashboard = i['dashboardUri'].replace('db/','')
            if 'HandleRequest' in item_v or item_v.__len__() == 0:
                write_log(log_file,"Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"%((datetime.now()+timedelta(hours=8)).ctime(),name,host,i['id'],item_v,dashboard))
            else:
                send_msg(url,reminders,msg_ding(name,h_str,i['id'],item_v,dashboard,(datetime.now()+timedelta(hours=8)).ctime(),d[i['id']]['alert_num'].__len__(),s.__len__()))
#                sendmailer(name,msg(name,h_str,i['id'],item_v,dashboard,(datetime.now()+timedelta(hours=8)).ctime()),addr_list)
#                print('The dicotionary is: ',d[i['id']])
                dt = str(datetime.fromtimestamp(d[i['id']]['alert_num'][d[i['id']]['alert_num'].__len__()-1])).split('.')[0]
                r_time = int((time.time()-d[i['id']]['alert_num'][d[i['id']]['alert_num'].__len__()-1]))
                write_log(mon_log_name,"""%s,%s,%s,%s,%s,%s,%s\n"""%(i['name'],host_str,i['id'],reduce(lambda x,y:str(x)+' '+str(y),item_v),dashboard,dt,r_time))
                write_log(log_file,"Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"%((datetime.now()+timedelta(hours=8)).ctime(),name,host,i['id'],item_v,dashboard))
    time.sleep(30)
































