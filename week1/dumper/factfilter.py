#!/usr/bin/env python
""" factfilter.py
"""

import json


class FactFilter(object):
    """ FactFilter Class
    """

    def __init__(self):
        pass

    def initfilter(self, factdict):
        for factkey, factvalue in factdict.iteritems():
            if factkey == 'cdp':
                factdict['cdp'] = self.filtercdp(factkey, factvalue)
        return factdict

    def filtercdp(self, factkey, factvalue):
        pruneddict = {}

        pruneddict = factvalue['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']

        #print pruneddict

        delkeys = [
            'ttl'
        ]

#        print pruneddict[0]

        #Loop through all CDP neighbor entries
        for entry in pruneddict:
            print entry
            #Delete all keys listed in delkeys
            for key in delkeys:
                del entry['ttl']

        return pruneddict
