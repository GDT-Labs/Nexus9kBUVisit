import cmdmgr
import device
import facts

def main():
    cmd_mgr = cmdmgr.CommandManager()
    commands = cmd_mgr.get_commands()
    devices = cmd_mgr.get_devices()
    for currentDevice in devices:
    	dev = device.Device(currentDevice['IP'],currentDevice['User'],currentDevice['Password'],currentDevice['DeviceName'])
    	print dev

    	devFactsRetriever = facts.Facts(dev, commands)
        devFactsRetriever.process_facts()
    	
if __name__ == "__main__":
    main()