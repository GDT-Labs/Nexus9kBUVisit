"""
REST API interface for NXAPI
"""
import requests
from requests.auth import HTTPBasicAuth
#from requests.auth import HTTPDigestAuth


class NXRestAPI(object):
    """Main REST interface for NXAPI
    """

    def __init__(self, baseURL):
        """init
        """
        self.url = baseURL
        self.headers = {}
        self.user = "admin"
        self.password = "Cisco.com"

    def get_nexus_info_request(self, url, headers=None,
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
        try:
            resp = requests.post(url, data=payload, headers=headers,
                                 verify=False, auth=auth)

            if resp.status_code == requests.codes.ok:
                #print resp.content
                return resp
            else:
                return None
        except requests.exceptions.ConnectionError:
            print 'Error connecting to', url
            return None


def main():
    url = 'http://192.168.1.123/ins'
    #user = 'admin'
    #password = 'Cisco.com'

    headers = {
        'Accept': 'application/json, text/javascript',
        'Content-Type': 'application/json-rpc',
        'Referer': 'http://192.168.1.123/',
        'Accept-Encoding': 'gzip,deflate',
        'Accept-Language': 'en-US'}

    payload = """
         [
          {
            "jsonrpc": "2.0",
            "method": "cli",
            "params": {
              "cmd": "show cdp neighbor",
              "version": 1
            },
            "id": 1
          }
        ]
    """

    nx_obj = NXRestAPI(url)
    resp = nx_obj.get_nexus_info_request(url, headers, payload)

    print resp.json()

if __name__ == '__main__':
    main()
