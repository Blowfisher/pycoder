#!/usr/bin/python env
#coding:utf-8


import os
import sys
import json
import time
import logging
import requests
import random
import matplotlib.pyplot as plt
from multiprocessing import Process,Queue

from datetime import datetime,timedelta

from config import *
from ec2_instance import aws_ec2_check
from msger import Msger

d = {}
s = set()
logger = logging.getLogger('grafana')

class Client():
    config_path = '/mnt/new_alert_client/config.yml' if  os.getenv('GCONFIG') == None else os.getenv('GCONFIG')
    if config_path == None:
        config_path = 'config.yml'
    def __init__(self,Messager):
        try:
            self.config = Filer(Client.config_path).get_yaml_data()
        except Exception as e:
            logger.error('Get config error: {0}'.format(e))
            os.exit(1)
        self.mtime = os.path.getmtime(Client.config_path)
        self.stats = self.config['stats_check']
        self.api = self.config['grafana_api']
        self.auth_obj = {"Accept":"application/json","Content-Type":"application/json","Authorization": "Bearer {0}".format(self.config['grafana_auth'])}
        self.log_file = self.config['alert_log_file']
        self.ec2_day = 0
        self.Messager = Messager
    def config_stats_check(self):
        if self.stats == True and self.mtime != os.path.getmtime(Client.config_path):
            self.mtime = os.path.getmtime(Client.config_path)
            self.config = Filer(Client.config_path).get_yaml_data()

            self.api = self.config['grafana_api']
            self.auth_obj = {"Accept":"application/json","Content-Type":"application/json","Authorization": "Bearer {0}".format(self.config['grafana_auth'])}
            self.log_file = self.config['alert_log_file']


    def gphoto(self,info,d):
        self.gphoto_helper(info)

        title = info['name']
        data = d[info['id']]
        x = [0,1,2,3,4,5]
        y = ('{0},{0},{0},{0},{0},{0}'.format(data['alert_v'])).split(',')
        y = [ x for x in map(lambda x:float(x),y)]

        color = {
        1: 'r',
        2: 'y',
        3: 'b',
        4: 'g',
        5: 'c',
        6: 'k',
        7: 'm',
        }

#        fig,ax = plt.subplots()
        group_labels = set()
        group_labels.add(data['alert_v'])

        for i in data['host'].keys():
            if len(data['host'][i]) < len(x):
                y1 = data['host'][i]
                x1 = x[:len(y)]
            elif len(data['host'][i]) > len(x):
                y1 =  data['host'][i][:len(x)]
                x1 = x
            else:
                y1 = data['host'][i]
                x1 = x
            y1 = [x for x in map(lambda x:float('{:.2f}'.format(x)) if type(x) == float else x,y1)]
            plt.plot(x1,y1,label='{0}'.format(i),color=color[random.randint(2,7)])
            group_labels = group_labels.union(set(y1))

        plt.plot(x,y,label='Alert Condition',color='r',linestyle='--')
        group_labels = list(group_labels)
        grl = list(group_labels)
        grl.sort()
        group_labels = [ j for j in range(0,int(grl[-1]),int(grl[-1]/3))]
        group_labels.append(int(grl[-1]*1.5))

        ax = plt.gca()
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.spines['bottom'].set_position(('data',0))
        ax.spines['left'].set_position(('data',0))
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

        plt.yticks(group_labels,group_labels)
#        plt.xticks(x,x)
        plt.grid(b=True,axis='x')
        plt.xlabel('Time-axis(/min)')
        plt.ylabel('Value-axis')
        plt.title('{0}'.format(title))
        plt.legend()
        plt.savefig('test.png')
        logger.info("gphoto pull data : {0}".format(data))
        logger.info('alert photo writen...')

    def gphoto_helper(self,i):
        start_time = time.time()
        logger.info('Gphoto helper Starting pull data')
        while True:
            time.sleep(60)
            gurl = self.api + '/{0}'.format(i['id']) if self.api[-1] != "/" else self.api + '{0}'.format(i['id'])
            data_info = self.get_content(gurl)
            try:
                for j in data_info['EvalData']:
                    d[i['id']]['host'][j['metric']].append(j['value'])
            except Exception as e:
                logger.info('mailer pull data Error: {0}'.format(e))
                return  False
            if  time.time() - start_time >= 300:
                logger.info('Gphoto Pull data Timeout,return data.')
                return  False


    def get_content(self,gurl):
        header = self.auth_obj
        opener = requests.request(
                'GET',
                gurl,
                headers = header )
        f = json.loads(opener.text)
        return f

    def info_helper(self,i):
        host=[]
        item_v=[]

        alert_time = int(time.time())
        time_around = time.time() - 86400
        gurl = self.api + '/{0}'.format(i['id']) if self.api[-1] != "/" else self.api + '{0}'.format(i['id'])
        logger.info('Gurl: {0}'.format(gurl))
        data_info = self.get_content(gurl)
#        logger.info('DATA info: {0} i is: {1}'.format(data_info,i))

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
            d[i['id']]['host'] = {}
            d[i['id']]['alert_num']=[]
            d[i['id']]['alert_num'].append(alert_time)
            logger.error("grafana select error: {0}".format(e))
    #        print("Exception appended alert time.")
        if data_info['ExecutionError'] != " ":
            item_v = data_info['ExecutionError']
        else:
            for j in data_info['EvalData']:
                if  j['metric'] not in d[i['id']]['host']: d[i['id']]['host'][j['metric']] = []
                d[i['id']]['host'][j['metric']].append(j['value'])

                host.append(j.pop('metric'))
                item_v.append(j.pop('value'))

#            d[i['id']]['host'] = host
            d[i['id']]['item_v'] = item_v
            d[i['id']]['alert_v'] = data_info['Settings']['conditions'][0]['evaluator']['params'][0]
            d[i['id']]['alert_type'] = " less than " if data_info['Settings']['conditions'][0]['evaluator']['type'] == 'lt' else " greater than  "
            d[i['id']]['alert_time'] = data_info['Settings']['conditions'][0]['query']['params'][1]
#            logger.info('alert info : {0}'.format(d))

        return host,item_v



    def check(self):
        self.ec2_check()
        self.Messager.config_stats_check()
        self.config_stats_check()
        mon_log_name = '/mnt/log/alert' + str(datetime.now().month) + '_month_alert.log'

        data = self.get_content(self.api)


        for i in data:
    #告警信息
            if i['state'] != 'ok' and i['state'] != 'no_data':
                if i['id'] not in s:
                    s.add(i['id'])
                    dt = (datetime.strptime(i["newStateDate"].strip('Z').replace('T',' '),'%Y-%m-%d %H:%M:%S') + timedelta(hours=8)).ctime()
                #    print(dt,i['id'])

                    host_str=str()
                    host,item_v = self.info_helper(i)
                    name = i['name']
                    for j in host:host_str= host_str +' '+str(j)
                    dashboard = i['dashboardUri'].replace('db/','')
    #                print('The dicotionary is: ',d[i['id']])
                    if 'HandleRequest' in item_v or item_v.__len__() == 0:
                        self.Messager.write_log(self.log_file,bytes("""Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"""%(dt,i['name'],host,i['id'],item_v,dashboard),'utf-8'))
                    else:
                        mon_log_name = self.Messager.mon_log()
                        logger.info("Month log name: {0}".format(mon_log_name))
                        self.Messager.send(self.Messager.msg_ding(name ,host_str,i['id'],item_v,dashboard,dt,d[i['id']]['alert_num'].__len__(),s.__len__()))

                        P = Process(target=self.email_handler,args=(i,d,name,host_str,item_v,dashboard,dt))
                        P.start()
#                        recv = self.Messager.emailer(name ,self.Messager.msg_mail(name ,host_str,i['id'],item_v, d[i['id']]['alert_type'],d[i['id']]['alert_v'],d[i['id']]['alert_time'],dashboard,dt))
#                        if recv == False:
#                            self.Messager.send('SMTP ERROR')

    #                    write_log(mon_log_name,"""%s,%s,%s,%s,%s,%s\n"""%(i['name'],host_str,i['id'],reduce(lambda x,y:str(x)+' '+str(y),item_v),dashboard,dt))
                        self.Messager.write_log(self.log_file,bytes("""Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"""%(dt,i['name'],host,i['id'],item_v,dashboard),'utf-8'))

    #恢复信息
            if i['id'] in s and i['state'] == 'ok':
                h_str=''
                s.remove(i['id'])
                host_info = list(d[i['id']]['host'].keys())
                for r in host_info:h_str= h_str +' '+str(r)
                item_v = d[i['id']].pop('item_v')
                name = i['name'] +' Recovery !'
                dashboard = i['dashboardUri'].replace('db/','')
                if 'HandleRequest' in item_v or item_v.__len__() == 0:
                    self.Messager.write_log(self.log_file,bytes("Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"%((datetime.now()+timedelta(hours=8)).ctime(),name,host,i['id'],item_v,dashboard),'utf-8'))
                else:
                    self.Messager.send(self.Messager.msg_ding(name,h_str,i['id'],item_v,dashboard,(datetime.now()+timedelta(hours=8)).ctime(),d[i['id']]['alert_num'].__len__(),s.__len__()))
                    dt = str(datetime.fromtimestamp(d[i['id']]['alert_num'][d[i['id']]['alert_num'].__len__()-1])).split('.')[0]
                    r_time = int((time.time()-d[i['id']]['alert_num'][d[i['id']]['alert_num'].__len__()-1]))
                    logger.info("Recovery messager mon log name :{0}".format(mon_log_name))
                    self.Messager.write_log(mon_log_name,bytes("""%s,%s,%s,%s,%s,%s,%s\n"""%(i['name'],host_str,i['id'],reduce(lambda x,y:str(x)+' '+str(y),item_v),dashboard,dt,r_time),'utf-8'))
                    self.Messager.write_log(self.log_file,bytes("Time: %s    \nAlert Name :%s  Host/IP :%s  Id : %s Item : %s  Dashboard : %s \n"%((datetime.now()+timedelta(hours=8)).ctime(),name,host,i['id'],item_v,dashboard),'utf-8'))
        time.sleep(30)

    def email_handler(self,info,d,name,host_str,item_v,dashboard,dt):
        logger.info('Email handler start...')
        self.gphoto(info,d)
        recv = self.Messager.emailer(name ,self.Messager.msg_mail(name ,host_str,info['id'],item_v, d[info['id']]['alert_type'],d[info['id']]['alert_v'],d[info['id']]['alert_time'],dashboard,dt))
        if recv == False:
            self.Messager.send('SMTP ERROR')

    def ec2_check(self):
        if self.ec2_day != datetime.now().day:
            logger.info("The old ec2 events check day : {0}".format(self.ec2_day))
            self.ec2_day = datetime.now().day
            ec2_stat = aws_ec2_check()
            if ec2_stat.__len__() != 0:
                for i in ec2_stat.keys():
                    msg = """Name: EC2 events alert
    %s
    InstanceId: %s
    IP: %s
    """%(ec2_stat[i]['info'].replace('"',''),i,ec2_stat[i]['IP'])
                    self.Messager.send(msg)

    #        return ec2_day
        return


if __name__ == '__main__':
    msger = Msger()
    client = Client(msger)
    while True:
        client.check()
