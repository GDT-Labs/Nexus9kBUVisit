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

    facts = {}

    import requests

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

    #No need for json.loads if being handed a dict as it is, which is what the requests module does
    facts['cdp'] = cdpinfo['ins_api']['outputs']['output']['body']
    thisDumper = Dumper(facts)
