import yaml


class CommandManager:
    """
    Load commands and devices from YAML command file
    and passes the information back to the requestor.
    """
    def __init__(self):
        self.command_file = 'cmds.yaml'

    def get_commands(self, filename=None):
        """
        Opens the given file, or tries the default cmds.yaml
        if no file is supplied.
        """
        command_list = {}
        if isinstance(filename, str) and len(filename) > 0:
            self.command_file = filename
        try:
            yaml_file = open(self.command_file, 'r')
            command_list = yaml.load(yaml_file)
            #print command_list
        except IOError as e:
            print "I/O error({0}): {1} {2}".format(e.errno, e.strerror, self.command_file)
        return dict(command_list)


def main():
    print "Loading Commands and Devices"
    cmd_mgr = CommandManager()
    cmds = cmd_mgr.get_commands()

    print "Sending commands to CommandFactory"
    print cmds

if __name__ == '__main__':
    main()
