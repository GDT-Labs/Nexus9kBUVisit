import yaml


class CommandManager:

    def __init__(self):
        self.initialized = False

    def get_commands(self, filename):
        yaml_file = open(filename, 'r')
        command_list = yaml.load(yaml_file)
        yaml.dump(command_list)


def main():
    print yaml.load("""name: Vorlin Laruknuzum
sex: Male
class: Priest
title: Acolyte
hp: [32, 71]
sp: [1, 13]
gold: 423
inventory:
- a Holy Book of Prayers (Words of Wisdom)
- an Azure Potion of Cure Light Wounds
- a Silver Wand of Wonder""")

    cmd_mgr = CommandManager()
    cmd_mgr.get_commands('test.yaml')

if __name__ == '__main__':
    main()
