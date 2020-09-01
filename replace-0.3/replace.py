#! /opt/local/bin/python2.7

from ftntlib import FortiManagerJSON
from termcolor import colored
import time
import argparse
import getpass

__version__ = 0.2

def check_response(response):
    code_str = colored('OK', 'green', attrs=['bold'])
    message = ''
    result = True
    
    if len(response) == 2:
        code = response[0]['code']
        if code != 0:
            code_str = colored('FAILED', 'red', attrs=['bold'])
            message = response[0]['message']
            print '[{}] {} ({})'.format(code_str, message, code)
            result = False
        if code == 0:
            print '[{}]'.format(code_str)

    return result

def my_print(topic, message, newline=True):

    t = colored(time.ctime(), 'blue', attrs=['bold'])
    topic = colored(topic, 'yellow', attrs=['bold'])
    string = ''

    if newline:
        print "{}: [{}] {}".format(t, topic, message)
    else:
        print "{}: [{}] {}".format(t, topic, message),

def exist(api, url):

    result = False
    
    response = api.get(url)

    if response[0]['code'] == 0:
        result = True
        
    return result

def getWorkspaceMode(api):
    url = '/cli/global/system/global'
    response = api.get(url)
    result = response[1]['workspace-mode']
    check_response(response)
    return result

def adomWorkspace(api, adom, action='lock'):
    result = True
    url = '/dvmdb/adom/{}/workspace/{}'.format(adom, action)
    response = api.execute(url)
    code = response[0]['code']
    check_response(response)

    if code != 0:
        result = False

    return result


    
if __name__ == '__main__':
    time_start = time.time()
    parser = argparse.ArgumentParser(description='Search and replace tool for FortiManager')
    parser.add_argument('-i', '-ip', '--ip', dest='ip', help='FortiManager IP Address', required=True)
    parser.add_argument('-l', '-login', '--login', dest='login', help='Admin login on FortiManager', required=True)
    parser.add_argument('-p', '-password', '--password', dest='password', help='Admin password on FortiManager')
    parser.add_argument('-s', '-source', '--source', '-src', '--src', dest='source', help='Object to replace', required=True)
    parser.add_argument('-d', '-destination', '--destination', '-dst', '--dst', dest='destination', help='Replacing Objects', required=True, nargs='+')    
    parser.add_argument('-a', '-adom', '--adom', dest='adom', help='FortiManager ADOM name', required=True)
    parser.add_argument('-v', '-version', '--version', action='version', version='%(prog)s {}'.format(__version__))
    args = parser.parse_args()

    ip = args.ip
    login = args.login
    password = args.password
    adom = args.adom
    what_to_replace = args.source
    replace_with = args.destination
    
    if password == None:
        password = getpass.getpass()
        
    api = FortiManagerJSON()
    api.verbose('on')

    response = api.login(ip, login, password)
    if response[0]['code'] != 0:
        my_print("Login", "Wrong credentials", newline = False)
        check_response(response)
        my_print("Login", "Exiting...")
        quit()

    category_urls = {
        140: {
            'name': 'firewall address',
            'url': '/pm/config/adom/{}/obj/firewall/address/{}',            
        },
        142: {
            'name': 'firewall addrgrp',
            'url': '/pm/config/adom/{}/obj/firewall/addrgrp/{}',
        },
        
        181: {
            'name': 'firewall policy',
            'url': '/pm/config/adom/{}/pkg/{}/firewall/policy/{}',
        }
    }

    obj_urls = {
        'addr': 'adom/{}/obj/firewall/address',
        'addrgrp': 'adom/{}/obj/firewall/addrgrp',
    }

    wu_urls = {
        'start': 'cache/search/where/used/start',
        'summary': 'cache/search/where/used/get/summary',
        'detail': 'cache/search/where/used/get/detail',
        'end': 'cache/search/where/used/end',
    }

    # Acknowledging command line arguments
    my_print("Checking", "{:20s}: {:20s}".format("FortiManager IP", ip))
    my_print("Checking", "{:20s}: {:20s}".format("FortiManager Login", login))
    my_print("Checking", "{:20s}: {:20s}".format("FortiManager ADOM", adom))
    my_print("Checking", "{:20s}: {:20s}".format("Object to replace", what_to_replace))
    my_print("Checking", "{:20s}: {:20s}".format("Replacing Object(s)", replace_with))    

    # Figuring out what's the what_to_replace object type (addr or addrgrp)
    obj_type = None

    my_print("Checking", "Figuring out what's the object type for '{}'".format(what_to_replace))
    if exist(api, category_urls[140]['url'].format(adom, what_to_replace)):
        my_print("Checking", "Object {} is a firewall address".format(what_to_replace))
        obj_type = 'addr'
    if exist(api, category_urls[142]['url'].format(adom, what_to_replace)):
        my_print("Checking", "Object {} is a firewall address group".format(what_to_replace))        
        obj_type = 'addrgrp'

    if obj_type == None:
        my_print("Checking", "ADOM {} doesn't exist or Object {} doesn't exist or is neither a firewall address nor a firewall addrgrp".format(adom, what_to_replace))
        my_print("Checking", "Exiting...")
        quit()
    
    # Start the Where Used Process; acquire the tocken
    my_print("Where Used", "Starting Where Used on object {}".format(what_to_replace), newline=False)
    data = {
        'mkey': what_to_replace,
        'obj': obj_urls[obj_type].format(adom),
    }
    response = api.execute(wu_urls['start'], data)
    check_response(response)
    
    token = response[1]['token']

    # Get the Where Used Summary
    my_print("Where Used", "Getting the Where Used Summary", newline=False)
    params = [
        {
            'token': token,
            'url' : wu_urls['summary'].format(adom),
        },
    ]

    response = api.do("exec", params)
    check_response(response)

    while True:
        if response[1]['percent'] == 100:
            break

    # Get the Where Used Detail
    my_print("Where Used", "Getting the Where Used Detail", newline=False)
    params = [
        {
            'token': token,
            'url' : wu_urls['detail'].format(adom),
        },
    ]

    response = api.do("exec", params)
    check_response(response)

    if 'where_used' not in response[1].keys():
        my_print("Where Used", "Object {} isn't used!".format(what_to_replace))
        my_print("Where Used", "Exiting...")
        quit()
    else:
        items  = response[1]['where_used'][0]['data']

        # Display the Where Used result
        my_print("Where Used", "Object {} is used in the following place(s):".format(what_to_replace))
        my_print("Where Used", "{:20s} {:20s} {:20} {:20}".format("NAME", "ATTRIBUTE", "CATEGORY", "POLICY PACKAGE"))
        for item in items:
            category = item['category']
            category_name = category_urls[category]['name']
            attr = item['attr']
            mkey = item['mkey']
            pkg = 'N/A'
            if category == 181:
                pkg = item['pkg']['name']
            my_print("Where Used", "{:20s} {:20s} {:<20} {:20s}".format(mkey, attr, category_name, pkg))

        # Stop the Where Used
        my_print("Where Used", "Ending the Where Used", newline=False)
        params = [
            {
                'token': token,
                'url' : wu_urls['end'].format(adom),
            },
        ]
        response = api.do("exec", params)
        check_response(response)

        # Check whether FortiManager is in workspace mode
        workspace = False

        my_print("Workspace", "Checking FortiManager Workspace mode...", newline=False)
        workspace_mode = getWorkspaceMode(api)

        if workspace_mode == 'normal':
            workspace = True
            my_print("Workspace", "This FortiManager is operating in Workspace [Normal] Mode")
            my_print("Workspace", "Locking ADOM {}".format(adom), newline=False)
            if adomWorkspace(api,adom):
                my_print("Workspace", "ADOM {} successfully locked".format(adom))
            else:
                my_print("Workspace", "Can't lock ADOM {}".format(adom))
                my_print("Workspace", "Exiting...")
                quit()

        elif workspace_mode == 'workflow':
            my_print("Workspace", "This FortiManager is operating in Workspace [Workflow] Mode")
            my_print("Workspace", "Workspace Workflow Mode isn't supported")
            my_print("Workspace", "Exiting...")
            quit()
        elif workspace_mode == 'disable':
            my_print("Workspace", "Workspace mode isn't enabled on this FortiManager")
        
        # Main loop - where we're doing the replace operations.
        for item in items:
            category = item['category']
            mkey = item['mkey']
            attr = item['attr']
            pkg = ''
            url = ''
            
            if category == 181:
                pkg = item['pkg']['name']
                url = category_urls[category]['url'].format(adom, pkg, mkey)
            elif category == 142:
                url = category_urls[category]['url'].format(adom, mkey)

            response = api.get(url)
            objects = response[1][attr]

            # FMG 5.2.x doesn't return a list when there's a unique object in the cell/group
            if type(objects) is not list:
                objects = [objects]

            new_objects = []

            not_in_objects = True
            for object in objects:
                    if object != what_to_replace:
                        new_objects.append(object)
                    else:
                        not_in_objects = False

            if not_in_objects:
                if category == 142:
                    my_print("Replace", "Skiping group {}/{}; no direct reference to {}".format(adom, mkey, what_to_replace))
                elif category == 181:
                    my_print("Replace", "Skiping policy {}/{}/{}; no direct reference to {}".format(adom, pkg, mkey, what_to_replace))                    
                continue
            
            new_objects += replace_with

            data = {
                attr: new_objects,
            }

            if category == 181:
                my_print("Replace", "Replacing {} in {} of policy {}/{}/{}".format(what_to_replace, attr, adom, pkg, mkey), newline=False)
            elif category == 142:
                my_print("Replace", "Replacing {} in {} of firewall address group  {}/{}".format(what_to_replace, attr, adom, mkey), newline=False)                

            check_response(api.update(url, data))

        # Check whether FortiManager is in workspace mode; if this is the case, we have to commit (save) then unlock the ADOM
        if workspace:
            my_print("Workspace", "Saving changes for ADOM {}".format(adom), newline=False)
            if adomWorkspace(api, adom, action='commit'):
                my_print("Workspace", "Save operation succeeded for ADOM {}".format(adom))
            else:
                my_print("Workspace", "Can't save changes for ADOM {}...".format(adom))

            my_print("Workspace", "Unlocking ADOM {}".format(adom), newline = False)
            if adomWorkspace(api, adom, action='unlock'):
                my_print("Workspace", "ADOM {} unlocked successfully".format(adom))
            else:
                my_print("Workspace", "Can't unlock ADOM {}...")

    api.logout()
    time_end = time.time()

    my_print("Timing", "COMPLETED in {} sec".format(time_end - time_start))
