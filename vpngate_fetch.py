#!/usr/bin/python
import csv
import base64
import sys
import os, os.path, time
from datetime import datetime
import urllib
from random import shuffle
import commands

FILE_TMP = '/root/csv_vpngate'

def downloadFile(file_name, base_url):
    f = urllib.urlretrieve(base_url, file_name)
    return 0

if os.path.exists(FILE_TMP):
    now = datetime.now()
    then = datetime.fromtimestamp( os.path.getmtime(FILE_TMP) )

    tdelta = now-then
    if int(tdelta.total_seconds()) < 900:
        print "tdelta < 900s, not fetching"
    else:
        os.unlink(FILE_TMP)
        ret = downloadFile(FILE_TMP, 'http://www.vpngate.net/api/iphone/')
        if ret != 0:
            print("download failed")
            sys.exit(ret)

#country = raw_input("What country? ")
country = ("CA", "US", "GB", "DE", "FR")

possible = []

with open(FILE_TMP, 'r') as fp:
    creader = csv.reader(fp)
    i = 0
    for row in creader:
        i += 1
        if i <= 2:
            continue
        if row[0] == '*':
            continue

        if row[6] in country:
            data = (row[12], row[14])
            possible.append(data)

shuffle(possible)

for row in possible:
    #thisone = raw_input("Do you want %s? [y]" % row[0])
    thisone = 'y'
    if thisone is None or thisone=='' or thisone=='y':
        fp = open('/etc/openvpn/vpngate.conf', 'w')
        fp.write( base64.b64decode(row[1]) )
        fp.close()
        print "/etc/openvpn/vpngate.conf written"
        break


commands.getstatusoutput("sed -i 's/^dev tun.*/dev tun101/' /etc/openvpn/vpngate.conf")

