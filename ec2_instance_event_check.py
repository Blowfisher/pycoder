#!/usr/bin/env python
#coding:utf-8
import subprocess
import json

def Get_ip_name(ql,kl,ec2_stat,flag=True):
    key_name = kl
    query_list = ql
    if flag:
        temp = query_list.pop()[0]
        if temp[0] in key_name:
#            print temp
            ec2_stat[temp[0]]['IP'] = temp[1]
            temp_meta = temp[2].__str__().replace('[','').replace(']','').replace('{','').replace('}','').replace('Key','').replace(':','').replace("'","").replace('Value','').replace(' ','').replace('uu','').split(',')
#            print(temp_meta)
            try:
                role = temp_meta[temp_meta.index('Name')+1].split('->')[1].split('#')[0].replace('-centos6-ci-hvm','')
            except Exception as e:
                try:
                    role = temp_meta[temp_meta.index('Name')-1].split('->')[1].split('#')[0].replace('-centos6-ci-hvm','')
                except Exception as e:
                    role = None
            ec2_stat[temp[0]]['info'] = ec2_stat[temp[0]]['info']+"""
Role : %s """%role
            kl.pop(kl.index(temp[0]))
        if kl.__len__() > 0:
            Flag = True
            Get_ip_name(query_list,key_name,ec2_stat,Flag)
        else:
            Flag = False

def aws_ec2_check():
    ec2_stat = {}
    p = subprocess.Popen('aws ec2 describe-instance-status',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    data = json.loads(p.stdout.read())
    for i in data['InstanceStatuses']:
# check instancestate
        if  i['InstanceState']['Name'] <> 'running' :
            ec2_stat[i['InstanceId']]={'info' : 'InstanceState miss','area': i['AvailabilityZone']}
#check systemstatus
        elif i['SystemStatus']['Status'] <> 'ok':
            ec2_stat[i['InstanceId']]={'info' : 'Systemstatus miss','area': i['AvailabilityZone']}
#check instancestatus
        elif i['InstanceStatus']['Status'] <> 'ok':
            ec2_stat[i['InstanceId']]={"info" : "Instancestatus miss","area": i['AvailabilityZone']}
        elif i.has_key('Events'):
            if 'Completed' in i['Events'][0]['Description']:
                continue
            info = """"MType: %s
Zone: %s
S_Time:%s (UTC)"""%(i['Events'][0]['Code'],i['AvailabilityZone'],str(i['Events'][0]['NotBefore']).split(":00.000Z")[0])
            ec2_stat[i['InstanceId']]={'info':info}

    if ec2_stat.__len__() != 0:
        p2 = subprocess.Popen("aws ec2 describe-instances --query 'Reservations[*].Instances[*].[InstanceId,PrivateIpAddress,Tags]'",shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        data_ip = json.loads(p2.stdout.read(),encoding='utf-8')
        ec2_key_list = ec2_stat.keys()
        Get_ip_name(data_ip,ec2_key_list,ec2_stat)

    return ec2_stat

if __name__ == '__main__':
    a = aws_ec2_check()
    print u'实例事件:','\n',a
