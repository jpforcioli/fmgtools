#! /opt/local/bin/python2.7

import re
from ftntlib import FortiManagerJSON

class WebUrlFilter:
    def __init__(self):
        self.data = {}

    def getIdFromUrlFilterName(self, fmg, adom, urlf_name):
        url = '/pm/config/adom/{0}/obj/webfilter/urlfilter/'.format(adom)
        data = {
            'fields': ['id', 'name'],
            'loadsub': 0,
        }
        fmg.debug('on')
        fmg.get(url, data)
        fmg.debug('off')        

    def loadFrom(self, fmg, adom, urlf_name):
        id = self.getIdFromUrlFilterName(fmg, adom, urlf_name)
        pass

class Entry:
    def __init__(self, csvline=None):
        if csvline:
            self.setWithCsvLine(csvline)
        else:
            self.data = {}

    def __str__(self):
        return str(self.data)

    def __cmp__(self, other):
        return cmp(self.data['url'], other.data['url'])

    def setWithCsvLine(self, csvline):
        # To remove all whitespace from csvline
        l = ''.join(csvline.split())

        l = l.split(',')
        self.data = {
            "url": l[0],
            "type": l[1], 
            "action": l[2],
            "status": l[3],
            "referrer-host": l[4]
          }        

if __name__ == '__main__':
    ip = '192.168.244.200'
    login = 'admin'
    password = 'fortinet'
    
    fmg = FortiManagerJSON()
    fmg.verbose('on')
    fmg.skip('off')

    f = open('data.csv')

    for line in f:
        line = line.strip()
        if re.match('^#.*$', line):
            next
        else:
            entry = Entry(line)
            print entry
    

    adom = 'CM-LAB-003'
    fmg.login(ip, login, password)
    wuf = WebUrlFilter()
    wuf.getIdFromUrlFilterName(fmg, adom, 'web-filter-profile-001')
    fmg.logout()

