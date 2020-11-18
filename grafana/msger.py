#!/usr/bin/python env
#coding:utf-8


import os
import json
import logging
import smtplib
import requests

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr
from datetime import datetime

from config import *

Logger()
logger = logging.getLogger('grafana')


class Msger(object):
    reminders = [] # reminders list
    config_path = '/mnt/new_alert_client/config.yml' if  os.getenv('GCONFIG') == None  else os.getenv('GCONFIG')
    if config_path == None:
        config_path = 'config.yml'
    def __init__(self):
        try:
            self.config = Filer(Msger.config_path).get_yaml_data()
        except Exception as e:
            logger.error('Get config error: {0}'.format(e))
            exit(1)
        self.mtime = os.path.getmtime(Msger.config_path)

        self.uri = self.config['dingding_chat_api']
        self.mon = datetime.now().month
        self.mon_log_name = '/mnt/log/alert/' + str(datetime.now().month) + '_month_alert.log'
        self.to_addr = self.config['email_notification']

        self.__from_addr   = self.config['smtp_server']['user_name']
        self.__password    = self.config['smtp_server']['password']
        self.__smtp_server = self.config['smtp_server']['smtp_addr']
        self.smtp_start = self.config['smtp_server']['start_time']
        self.smtp_end = self.config['smtp_server']['end_time']
        self.dingding_sender = self.config['dingding_sender']

        self.stats = self.config['stats_check']
#        self.from_addr = 'svoice@samsung.com'
    def config_stats_check(self):
        if self.stats == True and self.mtime != os.path.getmtime(Msger.config_path):
            logger.info('Found configuration stats changed....')
            self.mtime = os.path.getmtime(Msger.config_path)
            self.config = Filer(Msger.config_path).get_yaml_data()

            self.uri = self.config['dingding_chat_api']
            self.to_addr = self.config['email_notification']
            self.smtp_start = self.config['smtp_server']['start_time']
            self.smtp_end = self.config['smtp_server']['end_time']
            self.dingding_sender = self.config['dingding_sender']
            if type(self.smtp_start) != int or type(self.smtp_end) != int:
                logger.error('Configuration key value error. Please check your configuration config.yaml')
                raise BaseException('{0} Key value error'.format(Msger.config_parth))

    def mon_log(self):
        if datetime.now().month != self.mon:
            self.mon_log_name = '/mnt/log/alert' + str(datetime.now().month) + '_month_alert.log'
            self.mon = datetime.now().month
        if not os.path.exists(self.mon_log_name):
            Msger.write_log(self.mon_log_name,"name,host(metric),id,value,dashboard,time,r_time\n")
        logger.info("Messager mon log name : {0}".format(self.mon_log_name))
        return  self.mon_log_name

    @staticmethod
    def write_log(file_name,msg):
        with open(file_name,"ab+") as f:
            f.write(msg)
        return

    @classmethod
    def msg_mail(cls,name,host,alert_id,item_v,alert_type,alert_v,alert_time,dashboard,alert_start_time):
        msg = """

<p><img src=\"cid:image1\"></p>

<p>Alarm:  %s </p>
<p>Host(metric): %s </p>
<p>Value: %s </p>
<p>Detail: %s </p>
<p>Dashboard: %s </p>
<p>Time: %s (UTC+8) </p>"""%(name,host,item_v,name.replace('alert',alert_type + str(alert_v) + ' Alert. it maybe continue {0} .'.format(alert_time)),dashboard,alert_start_time)
        return msg

    @classmethod
    def msg_ding(cls,name,host,alert_id,item_v,dashboard,alert_time,alert_num=None,total_num=0):
        msg = """Alarm:  %s
Host(metric): %s
ID: %s
Value: %s
Dashboard: %s
24h Metric：%s times
Alerting: %s issues
Time: %s """%(name,host,alert_id,item_v,dashboard,alert_num,total_num,alert_time)
        return msg



    def __format_addr(self,s):
        name, addr = parseaddr(s)
        return formataddr((Header(name,'utf-8').encode(),addr))

    def emailer(self,title,body):
        if self.smtp_start < self.smtp_end:
            alert_time = set([x for x in range(self.smtp_end)]).difference(set([x for x in range(self.smtp_start)]))
        elif self.smtp_start > self.smtp_end:
            alert_time = set([x for x in range(24)]).difference(set([x for x in range(self.smtp_start)])).union(set([x for x in range(self.smtp_end)]))
        elif self.smtp_start == self.smtp_end:
            return False
        if datetime.now().hour not in alert_time:
            logger.info('Base your mail plan the Emailer not send email')
            return False

        ret = True
        msgRoot = MIMEMultipart('related')
        msgRoot['From'] = self.__format_addr('SVOICE <%s>' % self.__from_addr)
        msgRoot['To'] = self.__format_addr('Administrator <%s>' % self.to_addr)
        msgRoot['Subject'] = Header(title,'utf-8').encode()

        msgAlternative = MIMEMultipart('alternative')
        msgRoot.attach(msgAlternative)
        mail_msg = body
        msgAlternative.attach(MIMEText(mail_msg,'html','utf-8'))
#指定图片为当前目录
        with open('test.png','rb') as f:
            msgImage = MIMEImage(f.read())
            msgImage.add_header('Content-ID','<image1>')
            msgRoot.attach(msgImage)

#        msg = MIMEText(body,'plain','utf-8')
        try:
            server = smtplib.SMTP_SSL(self.__smtp_server,465)
            server.set_debuglevel(0)
            server.login(self.__from_addr,self.__password)
            server.sendmail(self.__from_addr, self.to_addr, msgRoot.as_string())
            server.quit()
        except Exception as e:
            ret = False
            logger.error('SMTP ERROR: {0}'.format(e))
        return ret


    def send(self,msg):
        if not self.dingding_sender:
            return  False
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        data = {
             "msgtype": "text",
             "at": {
                 "atMobiles": Msger.reminders,
                 "isAtAll": True,
              },
             "text":{
                 "content": msg,
             }
        }
        r = requests.post(self.uri,data=json.dumps(data),headers=headers)
        logger.info('DingDing message send status: {0}'.format(r.text))
        return r.text



if __name__ == '__main__':
    print('Start....')
