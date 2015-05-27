#!/usr/bin/env python

import re
import pprint
import json
from argparse import ArgumentParser
import nxapirest
import cmdmgr
import device
#


def findkey(dct, key, value=None):
    found = []
    if isinstance(dct, list):
        for item in dct:
            f = findkey(item, key, value)
            if f:
                found.extend(f)
    if isinstance(dct, dict):
        for k, v in dct.items():
            if isinstance(v, list) or isinstance(v, dict):
                f = findkey(v, key, value)
                if f:
                    found.extend(f)
            if str(k) == str(key):
                if (value and str(v) == str(value)) or not value:
                    found.append(v)
    return found if len(found) > 0 else None


def getarpentry(device, ip=None, vrf='all'):
    # Check the output of the ARP table for the IP address in question
    dev = device
    deviceConnection = nxapirest.NXRestAPI(dev.ip,dev.user,dev.passw)
    deviceConnection.get_JSON_NX_API('sh ip arp {0} vrf {1}'.format(ip,vrf))
    if ip:
        arpoutput = deviceConnection.get_JSON_NX_API('sh ip arp {0} vrf {1}'.format(ip,vrf))
    else:
        arpoutput = deviceConnection.get_JSON_NX_API('show ip arp vrf {0}'.format(vrf))

    rowadjlist = findkey(arpoutput, 'ROW_adj')
    if not rowadjlist:
        return None

    # flatten out the data received from show ip arp into a list of dicts
    arpentries = []
    for rowadj in rowadjlist:
        if isinstance(rowadj, dict):
            arpentries.append(rowadj)
        elif isinstance(rowadj, list):
            arpentries.extend(rowadj)

    arplist = []
    for arp in arpentries:
        try:
            arplist.append(
                [arp['ip-addr-out'], arp['time-stamp'], arp['mac'], arp['intf-out']])
        except KeyError:
            continue
    #print "Printing ARP List for {0}".format(dev.name)
    #print arplist
    return arplist

def checkArpEntries(deviceList, ip):
        uniqueArpEntries = []
        for currentDevice in deviceList:
            arpEntries = getarpentry(currentDevice, ip)

            if arpEntries:
                for arp in arpEntries:
                    ip, timer, mac, interface = arp
                    if uniqueArpEntries.count(mac) == 0:
                        uniqueArpEntries.append(mac)

        return uniqueArpEntries


def getmacentry(device, mac, vlanfilter=None):
    dev = device
    deviceConnection = nxapirest.NXRestAPI(dev.ip,dev.user,dev.passw)
    macaddroutput = deviceConnection.get_JSON_NX_API('show mac address-table address {0}'.format(mac))

    macaddrlist = findkey(macaddroutput, 'ROW_mac_address')
    if not macaddrlist:
        return None

    macentries = []
    for macaddr in macaddrlist:
        if isinstance(macaddr, dict):
            macentries.append(macaddr)
        elif isinstance(macaddr, list):
            macentries.extend(macaddr)

    entries = []
    for macaddr in macentries:
        vlan = macaddr['disp_vlan']
        mac = macaddr['disp_mac_addr']
        entrytype = macaddr['disp_type']
        age = macaddr['disp_age']
        secure = macaddr['disp_is_secure']
        ntfy = macaddr['disp_is_ntfy']
        port = macaddr['disp_port']

        if vlanfilter and vlan != vlanfilter:
            continue


        entries.append(
                [vlan, mac, entrytype, age, secure, ntfy, port, port])

    return entries


def getportchannelmembers(device, port):
    dev = device
    deviceConnection = nxapirest.NXRestAPI(dev.ip,dev.user,dev.passw)
    po = deviceConnection.get_JSON_NX_API('show port-channel summary int {0}'.format(port))
    members = findkey(po, 'port')
    return members


def getcdpentry(device, port):
    # Next use the interface we found the device on from CAM and look it up in
    # CDP
    dev = device
    deviceConnection = nxapirest.NXRestAPI(dev.ip,dev.user,dev.passw)
    cdp = deviceConnection.get_JSON_NX_API('show cdp neighbor interface {0}'.format(port))
    cdp = findkey(cdp, 'ROW_cdp_neighbor_brief_info')
    if not cdp:
        raise Exception('Unable to find {0} in CDP output'.format(port))
    if len(cdp) > 0:
        cdp = cdp[0]
    return cdp

def getportfromchannel(device, portchannel, sourceip, sourceport, destinationip, destinationport):
    dev = device
    deviceConnection = nxapirest.NXRestAPI(dev.ip,dev.user,dev.passw)
    clicommand = deviceConnection.get_ASCII_NX_API('show port-channel load-balance forwarding-path interface port-channel {0} src-ip {1} l4-src-port {2} dst-ip {3} l4-dst-port {4}'.format(portchannel,sourceip,sourceport,destinationip,destinationport))
    activeMember = clicommand.splitlines()[0]
    activeMember = activeMember.split('PC member: ')[1]
    return activeMember

def printTraceForMac(deviceList,mac, sourceip, sourceport, destinationip, destinationport):


    print "  Searching device fibs for {0}".format(mac)

    for dev in deviceList:
        macentries = getmacentry(dev, mac)
        if not macentries:
            print '    Unable to find {0} in MAC table on device {1}'.format(mac, dev.name)
            macentries = []
        for macentry in macentries: 
           #print type(macentry)
            #print macentry

            vlan, mac, entrytype, age, secure, ntfy, port, parentport = macentry
        

            if port.find("SUP_INBAND"): #ignore these

                if not port.find("port-channel"): #Do this if it's a port channel
                    poNumber = port.split('port-channel')[1]
                    activeMember = getportfromchannel(dev, poNumber , sourceip, sourceport, destinationip, destinationport)
                    cdp = getcdpentry(dev,activeMember)
                    remoteDevice = re.sub('\(.*\)','',cdp['device_id'])
                    print "    {0} to {1} | {2}(Po{3}) -> {4}".format(dev.name,remoteDevice,activeMember,poNumber,cdp['port_id'],cdp['device_id'])
                elif not port.find("Ethernet"): # Do this if it's an ethernet port
                    cdp = getcdpentry(dev,port)
                    print "    {0} on {1} -> {2} on {3}".format(port,dev.name, cdp['port_id'], cdp['device_id'])
                else:
                    print "    {0} on {1}".format(port,dev.name)




def main():

    # Perform some basic argument parsing for parameters passed to the script
    parser = ArgumentParser('Supercommand')
    parser.add_argument(
        'sourceip', help='Specify the First IP to be checked')
    parser.add_argument(
        'sourceport', help='Specify the L4 port on the first IP')
    parser.add_argument(
        'destinationip', help='Specify the Second IP to be checked')
    parser.add_argument(
        'destinationport', help='Specify the L4 port on the Second IP')

    args = parser.parse_args()
    sourceip = args.sourceip
    sourceport = args.sourceport
    destinationip = args.destinationip
    destinationport = args.destinationport



    cmd_mgr = cmdmgr.CommandManager()
    devices = cmd_mgr.get_devices()


    # Create a list of the devices using the device class
    deviceList = [] 
    for currentDevice in devices:
        deviceList.append(device.Device(currentDevice['IP'],currentDevice['User'],currentDevice['Password'],currentDevice['DeviceName']))


    sourceIpMacs = checkArpEntries(deviceList, sourceip)

    for mac in sourceIpMacs:
        print ""
        print "Found an arp entry for {0} the MAC is {1}".format(sourceip, mac)

        printTraceForMac(deviceList,mac, sourceip, sourceport, destinationip, destinationport)



    destinationIpMacs = checkArpEntries(deviceList, destinationip)

    for mac in destinationIpMacs:
        print ""
        print "Found an arp entry for {0} the MAC is {1}".format(destinationip, mac)
        printTraceForMac(deviceList,mac, destinationip, destinationport, sourceip, sourceport)

 

if __name__ == '__main__':
    main()