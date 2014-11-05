import cmdmgr
import device
import facts

def main():
    cmd_mgr = cmdmgr.CommandManager()
    devicesAndCmds = cmd_mgr.get_commands()
    for currentDevice in devicesAndCmds['Devices']:
    	dev = device.Device(currentDevice['IP'],currentDevice['User'],currentDevice['Password'],currentDevice['DeviceName'])
    	print dev
    	devFactsRetriever = facts.Facts(dev, devicesAndCmds)
    	devFactsRetriever.proccessFacts()
    	
if __name__ == "__main__":
    main()