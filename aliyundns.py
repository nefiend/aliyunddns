#!/usr/bin/env python3
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalidns.request.v20150109.DescribeDomainRecordInfoRequest import DescribeDomainRecordInfoRequest
from aliyunsdkalidns.request.v20150109.UpdateDomainRecordRequest import UpdateDomainRecordRequest
import json
import requests

class DDNS():
    with open('./config.json') as s:
        config = json.load(s)
    client = AcsClient(config['KeyId'], config['KeySec'], 'cn-hangzhou')

    def getDnsIp(self):
        request = DescribeDomainRecordInfoRequest()
        request.set_accept_format('json')

        request.set_RecordId(self.config['RecordId'])

        response = self.client.do_action_with_exception(request)
        string = str(response, encoding='utf-8')

        a = json.loads(string)
        ip = a['Value']
        return ip

    def getRouterIp(self):
        response = requests.get("http://members.3322.org/dyndns/getip")
        return response.text.strip('\n') 
    
    def setDnsRecord(self, ip):
        request = UpdateDomainRecordRequest()
        request.set_accept_format('json')

        request.set_Type(self.config['Type'])
        request.set_Value(ip)
        request.set_RR(self.config['RR'])
        request.set_RecordId(self.config['RecordId'])

        response = self.client.do_action_with_exception(request)
        # python2:  print(response) 
        print(str(response, encoding='utf-8'))

    
if __name__ == '__main__':
    ddns = DDNS()
    DnsIp = ddns.getDnsIp()
    print(DnsIp)
    RouterIp = ddns.getRouterIp()
    print(RouterIp)
    if (DnsIp != RouterIp):
        ddns.setDnsRecord(RouterIp)
