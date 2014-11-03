import requests
import json

"""
Modify these please
"""

class Exterminate

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
    "input": "show cdp nei",
    "output_format": "json"
  }
}
response = requests.post(url,data=json.dumps(payload), headers=myheaders,auth=(switchuser,switchpassword)).json()
print response