#! /opt/local/bin/python3.7

from ftntlib import FortiManagerJSON
import argparse
import getpass

class AdomUsage:
    def __init__(self, adom=None, api = None):
        self._adom = adom
        self._api = api
        self._adomdb = {}

    def count(self, url_postfix):
        url = 'pm/config/adom/{0}/obj/{1}'.format(self._adom, url_postfix.lstrip('/'))

        api = self._api
        response = api.get(url)

        result = 0
        
        if response[1] is not None:
            objects = response[1]

            for object in objects:
                result = result + 1

        self._adomdb[url_postfix] = result

    def show(self):

        # Find the longest key
        l_result = 0
        r_result = 0        
        for key in self._adomdb:
            len_key = len(key)
            len_value = len(str(self._adomdb[key]))
            if len_key > l_result:
                l_result = len_key
            if len_value > r_result:
                r_result = len_value
        
        total = 0
        print('ADOM Usage for {0}'.format(self._adom))
        string = '{0:' + str(l_result + 3) + '}:{1:' + str(r_result + 3) + '}'
        print('=' * (l_result + r_result + 7))        
        for key in self._adomdb:
            print(string.format(key, self._adomdb[key]))
            total = total + self._adomdb[key]

        print('=' * (l_result + r_result + 7))
        print(string.format('TOTAL', total))

if __name__ == '__main__':
    #ip = '10.210.35.200'
    ip = '10.210.34.241'    
    login = 'admin'
    password = 'fortinet'

    api = FortiManagerJSON()
    api.login(ip, login, password)
    
    adom = "LDL-FR"
    au = AdomUsage(adom, api)

    au.count('/firewall/address')
    au.count('/firewall/address6')    
    au.count('/firewall/addrgrp')
    au.count('/firewall/addrgrp6')    
    au.count('/firewall/vip')
    au.count('/firewall/vipgrp')
    au.count('/firewall/service/custom')
    au.count('/firewall/schedule/onetime')
    au.count('/webfilter/profile')
    au.count('/ips/sensor')
    au.count('/firewall/ippool')
    au.count('/firewall/ippool6')           

    au.show()


    api.logout()
