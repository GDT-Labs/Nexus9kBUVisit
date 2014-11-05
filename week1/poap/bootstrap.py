#!/usr/bin/env python

""" bootstrap.py

    This is the python script that will initially configure a
    Nexus 9000 switch
"""

import urllib2
from cisco.vrf import *
from cli import *
import cisco

hostid = cli('show license host-id')

hostid = hostid[hostid.index('=') + 1:]

set_global_vrf('management')
page = urllib2.urlopen('http://208.113.172.68/')

configfile = page.read()

print configfile
