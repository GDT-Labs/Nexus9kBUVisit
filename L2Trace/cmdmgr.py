import yaml


class CommandManager(object):
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
        yamlDict = {}
        yamlDict = self.readYamlFile(filename)
        return yamlDict['Commands']
        
    def get_devices(self, filename=None):
        """
        Retrieves the devices listed in the provided Yaml file. 
        If no filename is specified the default will be used.
        """
        yamlDict = {}
        yamlDict = self.readYamlFile(filename)
        return yamlDict['Devices']

    def readYamlFile(self, filename=None):
        """
        Opens the given file, or tries the default cmds.yaml
        if no file is supplied.
        """
        yamlData = {}
        if isinstance(filename, str) and len(filename) > 0:
            self.command_file = filename
        try:
            yaml_file = open(self.command_file, 'r')
            yamlData = yaml.load(yaml_file)
            #print command_list
        except IOError as e:
            print "I/O error({0}): {1} {2}".format(e.errno, e.strerror, self.command_file)
        return dict(yamlData)

def main():
    print "Loading Commands and Devices"
    cmd_mgr = CommandManager()
    cmds = cmd_mgr.get_commands()
    devs = cmd_mgr.get_devices()

    print "Printing commands"
    print cmds
    print "Printing Devices"
    print devs
    print type(devs)

if __name__ == '__main__':
    main()
