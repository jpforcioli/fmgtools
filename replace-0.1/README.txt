1. IMPORTANT INFORMATION

a) replace.py only supports replacing Firewall Addresses and Firewall Address Groups

b) replace.py doesn't consider in Dynamic Mapping entries in Firewall Address Groups

For instance:

GRP_001 has default members HOST_001, HOST_002 and HOST_003
GRP_001 has a dynamic mapping entry for device DEV1; members are HOST_004, HOST_005, HOST_006
HOST_004 is used by Policy Package PP1 in different places

If replace HOST_004 with HOST_008 and HOST_009, then PP1 policies referencing HOST_004 will be modified.
But GRP_001, referencing HOST_004 in a dynamic mapping entry won't be modified...

d) replace.py has been tested against FortiManager 5.4.4-INTERIM build 1224

2. INSTALL REPLACE.PY

a) replace.py has been tested with Python 2.7

b) Install FTNTLIB Python Module

For instance on Ubuntu Dekstop where system-wide Python version is 2.7:

$ tar xzvf ftntlib-VERSION.tgz
ftntlib-VERSION/
ftntlib-VERSION/ftntlib/
ftntlib-VERSION/ftntlib/__init__.py
ftntlib-VERSION/ftntlib/fmg_jsonapi.py
ftntlib-VERSION/ftntlib/fmg_xmlapi.py
ftntlib-VERSION/ftntlib/fos_restapi.py
ftntlib-VERSION/README
ftntlib-VERSION/setup.py
$ cd ftntlib-VERSION
$ sudo apt install python-setuptools
$ sudo apt install gcc
$ sudo apt install python-dev
$ sudo apt install libxslt1-dev
$ sudo apt install zlib1g-dev
$ sudo python setup.py install


c) You also need to make sure following Python modules to be:

   time
   argparse
   getpass
   termcolor

d) Make sure your FortiManager user has the proper permissions

It is not enough to assign the Super_User permission profile to your
user.
You also have to make sure it has the "rpc-permit" permisssion set to
read-write.
It can only be changed via FMG CLI:

config system admin user
edit <your user>
set rpc-permit read-write
next
end

3. REPLACE.PY USAGE

a) To get usage information

$ ./replace.py -h
usage: replace.py [-h] -i IP -l LOGIN [-p PASSWORD] -s SOURCE -d DESTINATION [DESTINATION ...] -a ADOM [-v]

Search and replace tool for FortiManager

optional arguments:
  -h, --help            show this help message and exit
  -i IP, -ip IP, --ip IP
                        FortiManager IP Address
  -l LOGIN, -login LOGIN, --login LOGIN
                        Admin login on FortiManager
  -p PASSWORD, -password PASSWORD, --password PASSWORD
                        Admin password on FortiManager
  -s SOURCE, -source SOURCE, --source SOURCE, -src SOURCE, --src SOURCE
                        Object to replace
  -d DESTINATION [DESTINATION ...], -destination DESTINATION [DESTINATION ...], --destination DESTINATION [DESTINATION ...], -dst DESTINATION [DESTINATION ...], --dst DESTINATION [DESTINATION ...]
                        Replacing Objects
  -a ADOM, -adom ADOM, --adom ADOM
                        FortiManager ADOM name
  -v, -version, --version
                        show program's version number and exit

b) To replace HOST_029 by HOST_002, on FortiManager 192.168.123.200 and ADOM ADOM_54_001; if '-p' is omited, you are prompted for a password.

$ ./replace.py -i 192.168.123.200 -l admin -a ADOM_54_001 -s HOST_029 -d HOST_002
Password:
Thu Oct 19 23:18:28 2017: [Checking] FortiManager IP     : 192.168.123.200
Thu Oct 19 23:18:28 2017: [Checking] FortiManager Login  : admin
Thu Oct 19 23:18:28 2017: [Checking] Object to replace   : HOST_029
Thu Oct 19 23:18:28 2017: [Checking] Replacing Object(s) : ['HOST_002']
Thu Oct 19 23:18:28 2017: [Checking] Figuring out type of object HOST_029
Thu Oct 19 23:18:28 2017: [Checking] Object HOST_029 is a firewall address
Thu Oct 19 23:18:28 2017: [Where Used] Starting Where Used on object HOST_029 [OK]
Thu Oct 19 23:18:28 2017: [Where Used] Getting the Where Used Summary [OK]
Thu Oct 19 23:18:28 2017: [Where Used] Getting the Where Used Detail [OK]
Thu Oct 19 23:18:28 2017: [Where Used] Object HOST_029 is used in the following place(s):
Thu Oct 19 23:18:28 2017: [Where Used] NAME                 ATTRIBUTE            CATEGORY             POLICY PACKAGE
Thu Oct 19 23:18:28 2017: [Where Used] GRP_003              member               firewall addrgrp     N/A
Thu Oct 19 23:18:28 2017: [Where Used] GRP_011              member               firewall addrgrp     N/A
Thu Oct 19 23:18:28 2017: [Where Used] 1                    srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] GRP_004              member               firewall addrgrp     N/A
Thu Oct 19 23:18:28 2017: [Where Used] GRP_007              member               firewall addrgrp     N/A
Thu Oct 19 23:18:28 2017: [Where Used] GRP_010              member               firewall addrgrp     N/A
Thu Oct 19 23:18:28 2017: [Where Used] 4                    srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 4                    srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 4                    srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 1                    srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 2                    srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 3                    srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 6                    dstaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 8                    dstaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 20                   srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 29                   srcaddr              firewall policy      default
Thu Oct 19 23:18:28 2017: [Where Used] 2                    srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 3                    srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 4                    dstaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 6                    dstaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 10                   dstaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 11                   srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 12                   dstaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 15                   srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 20                   srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 28                   dstaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 29                   srcaddr              firewall policy      clone_of_default
Thu Oct 19 23:18:28 2017: [Where Used] 1                    srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 2                    srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 3                    srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 6                    dstaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 20                   srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] 29                   srcaddr              firewall policy      PP_001
Thu Oct 19 23:18:28 2017: [Where Used] Ending the Where Used [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in member of firewall address group  ADOM_54_001/GRP_003 [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in member of firewall address group  ADOM_54_001/GRP_011 [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/1 [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in member of firewall address group  ADOM_54_001/GRP_004 [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in member of firewall address group  ADOM_54_001/GRP_007 [OK]
Thu Oct 19 23:18:29 2017: [Replace] Replacing HOST_029 in member of firewall address group  ADOM_54_001/GRP_010 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/4 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/4 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/4 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/1 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/2 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/3 [OK]
Thu Oct 19 23:18:30 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/default/6 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/default/8 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/20 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/default/29 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/2 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/3 [OK]
Thu Oct 19 23:18:31 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/clone_of_default/4 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/clone_of_default/6 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/clone_of_default/10 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/11 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/clone_of_default/12 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/15 [OK]
Thu Oct 19 23:18:32 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/20 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/clone_of_default/28 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/clone_of_default/29 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/1 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/2 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/3 [OK]
Thu Oct 19 23:18:33 2017: [Replace] Replacing HOST_029 in dstaddr of policy ADOM_54_001/PP_001/6 [OK]
Thu Oct 19 23:18:34 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/20 [OK]
Thu Oct 19 23:18:34 2017: [Replace] Replacing HOST_029 in srcaddr of policy ADOM_54_001/PP_001/29 [OK]
jpforcioli@vulgus:~/Documents/Fortinet/APIs/GIT/fmgtools/replace$ ./replace.py -i 192.168.123.200 -l admin -a ADOM_54_001 -s HOST_029 -d HOST_002
Password:
Thu Oct 19 23:19:29 2017: [Checking] FortiManager IP     : 192.168.123.200
Thu Oct 19 23:19:29 2017: [Checking] FortiManager Login  : admin
Thu Oct 19 23:19:29 2017: [Checking] Object to replace   : HOST_029
Thu Oct 19 23:19:29 2017: [Checking] Replacing Object(s) : ['HOST_002']
Thu Oct 19 23:19:29 2017: [Checking] Figuring out type of object HOST_029
Thu Oct 19 23:19:29 2017: [Checking] Object HOST_029 is a firewall address
Thu Oct 19 23:19:29 2017: [Where Used] Starting Where Used on object HOST_029 [OK]
Thu Oct 19 23:19:29 2017: [Where Used] Getting the Where Used Summary [OK]
Thu Oct 19 23:19:29 2017: [Where Used] Getting the Where Used Detail [OK]
Thu Oct 19 23:19:29 2017: [Where Used] Object HOST_029 isn't used!
Thu Oct 19 23:19:29 2017: [Where Used] Exiting...

c) You can replace a firewall address/group by multiple firewall addresses/groups

-s HOST_001 -d HOST_002 HOST_003 HOST_004 GRP_001 GRP_002
-s GRP_002 -d HOST_002 HOST_003 HOST_004 GRP_001 GRP_002

d) You can replace an object by itself

-s HOST_001 -d HOST_001
-s GRP_001 -d GRP_001

e) FortiManager will prevent incoherent actions:

  * replacement operations that could create circular reference in a
  group

  * replacing an object with a non matching interface binding for a
  particular policy cell
