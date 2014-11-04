import nxapirest
import dumper
import device
import cmdmgr
import json

class Facts(object):
    """
    Facts class will take a device and a list of NXAPI
    commands and run them against the device, returning
    the result
    """

    def __init__(self, device, command_list):
        self.device = device
        self.command_list = command_list['Commands']

    def process_facts(self):
        headers = {
            'Accept': 'application/json, text/javascript',
            'Content-Type': 'application/json',
            'Accept-Language': 'en-US'}

        print 'Processing facts'
        print self.command_list
        print self.device.ip

        nx_reqestor = nxapirest.NXRestAPI('http://' + self.device.ip + '/ins')
        for cmd in self.command_list:
            payload = self.build_payload(cmd)

            resp = nx_reqestor.get_nexus_info_request(headers=headers, payload=json.dumps(payload))
            if resp is not None:
                resp = resp.json()
                resp = resp['ins_api']['outputs']['output']['body']
                dump_dict = dict(cmd=resp)
                #print dump_dict
                dumper.Dumper(self.device.name(), dump_dict)

    def build_payload(self,cmd):
        for inst in cmd:
            payload = {
                "ins_api": {
                    "version": "1.0",
                    "type": "cli_show",
                    "chunk": "0",
                    "sid": "1",
                    "input": cmd[inst],
                    "output_format": "json"
                }
            }

        print payload
        return payload


def main():
    dev = device.Device('FakeTest', '192.168.1.123', 'admin', 'Cisco.com')
    cmd_mgr = cmdmgr.CommandManager()
    commands = cmd_mgr.get_commands()

    facts = Facts(dev, commands)
    facts.process_facts()


if __name__ == '__main__':
    main()
