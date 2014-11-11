import pprint
import sys
import Insieme.Logger as Logger

#
# Infra API
#
def deviceValidate( device,version ):
    return {
        'state': 0,'version': '1.0'
        }

def deviceModify( device,interfaces,configuration):
    return {
        'state': 0,'faults': [],'health': []
        }

def deviceAudit( device,interfaces,configuration ):
    return {
        'state': 0,'faults': [],'health': []
        }

def deviceHealth( device,interfaces,configuration ):
    return {
        'state': 0,'faults': [],'health': [([], 100)]
        }

def deviceCounters( device,interfaces,configuration ):
    return {
        'state': 0,'counters': [
            ( [(11,'','eth0')],{
                'rxpackets': 100,
                'rxerrors': 101,
                'rxdrops': 102,
                'txpackets': 200,
                'txerrors': 201,
                'txdrops': 202
            }
          )
        ]
    }

def clusterModify( device,interfaces,configuration ):
    return {
        'state': 0,'faults': [],'health': []
        }

def clusterAudit( device,interfaces,configuration ):
    return {
        'state': 0,'faults': [],'health': []
        }

#
# FunctionGroup API
#

def serviceModify( device,configuration ):
    return {
        'state': 0,'faults': [],'health': []
       }

def serviceAudit( device,configuration ):
    return {
        'state': 0,'faults': [],'health': []
        }

def serviceHealth( device,configuration ):
    return {
        'state': 0,'faults': [],'health': []
        }

def serviceCounters( device,configuration ):
    externalIntferface, = [(0, 'Firewall', 4384), (1, '', 4432), (3, 'Firewall-Func', 'FW-1'),
        (2, 'external', 'external1') ]
    internalInterface = [(0, 'Firewall', 4384) (1, '', 4432) (3, 'Firewall-Func', 'FW-1'),
        (2, 'internal','internal1') ]
    Firewall-1-External-Counters = (externalInterface,
        { 'rxpackets': 100,
            'rxerrors': 0,
            'rxdrops': 0
            'txpackets': 100
            'txerrors': 4
            'txdrops': 2} )
    Firewall-1-Internal-Counters = (internalInterface,
        { 'rxpackets': 100,
            'rxerrors': 0,
            'rxdrops': 0
            'txpackets': 100
            'txerrors': 4
            'txdrops': 2} )
    Counters = [ Firewall-1-External-Counters, Firewall-1-Internal-Counters ]
        return {
            'state': 0,
            'counters': Counters
        }

#
# EndPoint/Network API
#

def attachEndpoint( device,
                    configuration,
                    endpoints ):
    return {
        'state': 0,
        'faults': [],
        'health': [],
        }

def detachEndpoint( device,
                    configuration,
                    endpoints ):
    return {
        'state': 0,
        'faults': [],
        'health': [],
        }

def attachNetwork( device,
                   configuration,
                   networks ):
    return {
        'state': 0,
        'faults': [],
        'health': [],
        }

def detachNetwork( device,
                   configuration,
                   networks ):
    return {
        'state': 0,
        'faults': [],
        'health': [],
        }