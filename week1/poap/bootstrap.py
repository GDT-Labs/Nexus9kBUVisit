#!/usr/bin/env python

""" bootstrap.py

    This is the python script that will initially configure a
    Nexus 9000 switch
"""

import urllib2
from cisco.vrf import *
from cli import *
import cisco

#Retrieve HOST ID
hostid = clid('show license host-id')

hostid = hostid[hostid.index('=') + 1:]

set_global_vrf('management')
page = urllib2.urlopen('http://127.0.0.1:8880/?cfg=' + hostid)

#Read contents of page
configfile = page.read()

#Enter configuration mode
cli('conf t')

header_lines, sep, cli_lines = configfile.partition('\n\n')

#Enter each line into CLI
for line in iter(cli_lines.splitlines()):
    cli(line)
