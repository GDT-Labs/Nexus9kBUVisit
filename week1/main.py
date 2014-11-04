import cmdmgr
import device

def main():
    cmd_mgr = cmdmgr.CommandManager()
    devicesAndCmds = cmd_mgr.get_commands()
    for currentDevice in devicesAndCmds['Devices']:
    	dev = device.Device(currentDevice['IP'],currentDevice['User'],currentDevice['Password'],currentDevice['DeviceName'])
    	print dev
    

if __name__ == "__main__":
    main()