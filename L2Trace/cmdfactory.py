import device
import facts


class CommandFactory(object):
    """
    CommandFactory takes a Device object and a list of NXAPI commands
    and runs them through the Facts processor returning the NXAPI
    result
    """

    def __init__(self):
        self.device = None
        self.command_list = []
        self.cmd_response = {}

    def process_device(self, dev, commands):
        """
        Receives a device object and command list and
        sends it to the Facts processor
        """
        if isinstance(dev, device) and isinstance(commands, list):
            self.device = device
            self.commands = commands
            self.cmd_response = facts(self.device, self.commands)
        else:
            print("Invalid input to CommandFactory")

        return self.cmd_response
