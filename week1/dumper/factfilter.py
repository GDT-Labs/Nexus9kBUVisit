#!/usr/bin/env python
""" factfilter.py
"""

class FactFilter(object):
    """ FactFilter Class
    """

    def __init__(self):
        pass

    def initfilter(self, factdict):

        #factkey is name of fact family
        #factvalue is the dictionary that represents the facts in that family

        #Loop through each fact family, filtering each one as you go along
        for factkey, factvalue in factdict.iteritems():
            if factkey == 'cdp':
                factdict['cdp'] = self.filtercdp(factkey, factvalue)

        #Return filtered fact dictionary, with all families
        return factdict

    def filtercdp(self, factkey, factvalue):
        pruneddict = {}

        #Get rid of extra NXAPI crap
        pruneddict = factvalue['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']

        #This is a list of keys to delete
        delkeys = [
            'ttl',
            'mtu'
        ]

        #Loop through all CDP neighbor entries
        for entry in pruneddict:

            #Delete all keys listed in delkeys
            for key in delkeys:
                try:
                    del entry[key]
                except:
                    #Key doesn't exist, nothing to do
                    pass

        return pruneddict
