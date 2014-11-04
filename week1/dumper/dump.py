#!/usr/bin/env python
""" dump.py

    File that handles writing facts to the filesystem
"""

#import requests
import json
from factfilter import FactFilter
from gitterdun import MyGit


class Dumper(object):
    """ Dumper class. Used to dump facts to the filesystem
    """

    def __init__(self, facts):
        """ Creates a Dumper object """

        #Run through the filter
        thisFilter = FactFilter()

        filteredDict = thisFilter.initfilter(facts)

        for name, table in filteredDict.iteritems():
            self.dumpfact(name, table)

    def dumpfact(self, name, table):

        filename = '/Users/mierdin/Code/Nexus9kBUVisit/week1/facts/' + name + '.json'

        with open(filename, 'w') as f:

            f.write(json.dumps(table, sort_keys=True,
                    indent=4, separators=(',', ': ')))

        thisGit = MyGit()
        thisGit.addfile(filename)
        thisGit.commitchanges()



if __name__ == '__main__':
    print "STARTING"

    import collections

    facts = {}

    import requests
    import json

    """
    Modify these please
    """
    url='http://192.168.1.123/ins'
    switchuser='admin'
    switchpassword='Cisco.com'

    myheaders={'content-type':'application/json'}
    payload={
      "ins_api": {
        "version": "1.0",
        "type": "cli_show",
        "chunk": "0",
        "sid": "1",
        "input": "show cdp nei detail",
        "output_format": "json"
      }
    }
    cdpinfo = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
    #print cdpinfo
    #cdpinfo = '{"ins_api": {"outputs": {"output": {"msg": "Success", "input": "show cdp nei", "code": "200", "body": {"TABLE_cdp_neighbor_brief_info": {"ROW_cdp_neighbor_brief_info": [{"platform_id": "cisco WS-C6509", "intf_id": "mgmt0", "capability": "IGMP_cnd_filtering", "ttl": 172, "ifindex": 83886080, "port_id": "FastEthernet7/21", "device_id": "GDT-STAGING-6509-1.gdtstaging.local"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/1", "capability": "Supports-STP-Dispute", "ttl": 146, "ifindex": 436207616, "port_id": "Ethernet1/3/1", "device_id": "NX9508-01(FGE174702XX)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/2", "capability": "Supports-STP-Dispute", "ttl": 147, "ifindex": 436208128, "port_id": "Ethernet1/3/2", "device_id": "NX9508-01(FGE174702XX)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/3", "capability": "Supports-STP-Dispute", "ttl": 148, "ifindex": 436208640, "port_id": "Ethernet1/3/3", "device_id": "NX9508-01(FGE174702XX)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/4", "capability": "Supports-STP-Dispute", "ttl": 149, "ifindex": 436209152, "port_id": "Ethernet1/3/4", "device_id": "NX9508-01(FGE174702XX)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/5", "capability": "Supports-STP-Dispute", "ttl": 145, "ifindex": 436209664, "port_id": "Ethernet1/3/2", "device_id": "NX9508-02(FGE174702Y7)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/6", "capability": "Supports-STP-Dispute", "ttl": 148, "ifindex": 436210176, "port_id": "Ethernet1/3/4", "device_id": "NX9508-02(FGE174702Y7)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/7", "capability": "Supports-STP-Dispute", "ttl": 145, "ifindex": 436210688, "port_id": "Ethernet1/3/1", "device_id": "NX9508-02(FGE174702Y7)"}, {"platform_id": "N9K-C9508", "intf_id": "Ethernet1/8", "capability": "Supports-STP-Dispute", "ttl": 145, "ifindex": 436211200, "port_id": "Ethernet1/3/3", "device_id": "NX9508-02(FGE174702Y7)"}]}}}}, "version": "1.0", "type": "cli_show", "sid": "eoc"}}'
    #facts['cdp'] = json.loads(str(cdpinfo))['ins_api']['outputs']['output']['body']
    #print facts['cdp']

    #No need for json.loads if being handed a dict as it is, which is what the requests module does
    facts['cdp'] = cdpinfo['ins_api']['outputs']['output']['body']
    thisDumper = Dumper(facts)
