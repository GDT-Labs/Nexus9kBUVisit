"""
REST API interface for NXAPI
"""
import requests
from requests.auth import HTTPBasicAuth
import json
#from requests.auth import HTTPDigestAuth


class NXRestAPI(object):
    """Main REST interface for NXAPI
    """

    def __init__(self, ip, user='admin', password='Cisco.com' ):
        """init
        """
        self.ip = ip
        self.user = user
        self.password = password

    def get_nexus_info_request(self, url=None, headers=None,
                               payload=None):
        """
        Used for Nexus API REST API HTTP Get requests
        Parameters:
            url     - the ViPR URL we are trying to reach
            headers - contains mostly the authentication token
                      for the HTTP header
            payload - parameters being passed to the URL
            auth    - authentication information
        Returns:
            returns the Requests object if successful, otherwise None
        """

        auth = HTTPBasicAuth(self.user, self.password)
        if headers is not None:
            self.headers = headers
        if url is not None:
            self.url = url

        print self.headers

        try:
            resp = requests.post(self.url, data=payload, headers=self.headers,
                                 verify=False, auth=auth)

            print resp
            if resp.status_code == requests.codes.ok:
                #print resp.content
                return resp
            else:
                return None
        except requests.exceptions.ConnectionError:
            print 'Error connecting to', self.url
            return None

    def get_JSON_NX_API(self, cmd):

        """
        Used for Nexus API REST API HTTP Get requests
        Parameters:
            url     - the ViPR URL we are trying to reach
            headers - contains mostly the authentication token
                      for the HTTP header
            payload - parameters being passed to the URL
            auth    - authentication information
        Returns:
            returns the Requests object if successful, otherwise None
        """

        headers = {
            'Accept': 'application/json, text/javascript',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US'}


        payload = build_payload(cmd)

        auth = HTTPBasicAuth(self.user, self.password)

        url = 'http://{0}/ins'.format(self.ip)

        #print headers
        #print payload
        #print url
        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers,
                                 verify=False, auth=auth)

            #print resp
            if resp.status_code == requests.codes.ok:
                resp = resp.json()
                resp = resp['ins_api']['outputs']['output']['body']
                return resp
            else:
                return None
        except requests.exceptions.ConnectionError:
            print 'Error connecting to', url
            return None

    def get_ASCII_NX_API(self, cmd):

        """
        Used for Nexus API REST API HTTP Get requests
        Parameters:
            url     - the ViPR URL we are trying to reach
            headers - contains mostly the authentication token
                      for the HTTP header
            payload - parameters being passed to the URL
            auth    - authentication information
        Returns:
            returns the Requests object if successful, otherwise None
        """

        headers = {
            'Accept': 'application/json, text/javascript',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US'}


        payload ={
            "ins_api": {
                "version": "1.0",
                "type": "cli_show_ascii",
                "chunk": "0",
                "sid": "1",
                "input": cmd,
                "output_format": "json"
            }
           } 

        auth = HTTPBasicAuth(self.user, self.password)

        url = 'http://{0}/ins'.format(self.ip)

        #print headers
        #print payload
        #print url
        try:
            resp = requests.post(url, data=json.dumps(payload), headers=headers,
                                 verify=False, auth=auth)

            #print resp
            if resp.status_code == requests.codes.ok:
                resp = resp.json()
                resp = resp['ins_api']['outputs']['output']['body']
                return resp
            else:
                return None
        except requests.exceptions.ConnectionError:
            print 'Error connecting to', url
            return None

def build_payload(cmd):
    payload ={
        "ins_api": {
            "version": "1.0",
            "type": "cli_show",
            "chunk": "0",
            "sid": "1",
            "input": cmd,
            "output_format": "json"
        }
       } 

    #print payload
    return payload

def build_payload_ascii(cmd):
    payload ={
        "ins_api": {
            "version": "1.0",
            "type": "cli_show_ascii",
            "chunk": "0",
            "sid": "1",
            "input": cmd,
            "output_format": "json"
        }
       } 

    #print payload
    return payload


def main():
    ip = '192.168.1.123'
    user = 'admin'
    password = 'Cisco.com'

 

    nx_obj = NXRestAPI(ip,user,password)
    resp = nx_obj.get_JSON_NX_API("show cdp neig")

    if resp is not None:
        print resp.json()
    else:
        print "No Response"

if __name__ == '__main__':
    main()
