#!/usr/bin/env python
#coding:utf8
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib

#             '2305901977@qq.com',
#addr_list=['shengwei.wen@hydmsp.com','345740575@qq.com']
addr_list = ['344575@qq.com',
             'sv3ce@h3sp.com',
             '283400@qq.com',
             'wes34100318@163.com',
             'sh4i.wen@4r.sam44g.com'
             ]

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def mailer(title,body,addr):
    from_addr = 'wangbo1@ha.com'
    password = 'fity2013@'
    smtp_server = 'smtp.261.net'

    to_addr = addr

    msg = MIMEText(body,'plain','utf-8')
    msg['From'] = _format_addr('SVOICE <%s>' % from_addr)
    msg['To'] = _format_addr('Administrator <%s>' % to_addr)
    msg['Subject'] = Header(title,'utf-8').encode()

    server = smtplib.SMTP_SSL(smtp_server,465)
    server.set_debuglevel(0)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

def sendmailer(title,body,args):
    try:
        for i in args:
        #print('Email Address: %s' %i)
            mailer(title,body,i)
    except Exception as e:
        return "SMTP Error,Mail send failure !"


if __name__ == '__main__':
    title = '测试'
    body = 'testing...'
    addr1 = ['booo.wang@aa.com',]
    sendmailer(title,body,addr1)
    print(body)
                    