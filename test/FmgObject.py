#! /opt/local/bin/python2.7

from ftntlib import FortiManagerJSON

class FmgObject:
    def __init__(self):
        pass
    
if __name__ == '__main__':

    ip = '192.168.244.200'
    login = 'admin'
    password = 'fortinet'
    
    fmg = FortiManagerJSON()
    fmg.verbose('on')
    fmg.login(ip, login, password)

    adom = 'CM-LAB-001'

    path = 'pm/config/adom/{0}/obj/firewall/address'.format(adom)
    payload = {
    }

    response = fmg.get(path, payload)

    data = response[1]

    if type(data) is list:
        print "coucou"
        for item in data:
            print item

    fmg.logout()

