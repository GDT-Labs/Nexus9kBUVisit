from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('./'))


class TemplateMgr(object):
    """
    Takes a requested hostname and returns
    a template populated with generic and
    specific configuration data.
    """

    def __init__(self, configfile=None):
        self.configfile = 'templates/config.yml'

    def process_id(self, hostid):
        # Read YAML static config file
        with open(self.configfile) as _:
            self.config = yaml.load(_)

        # Read the host config file
        with open('templates/dynamicconfig.yml') as _:
            dynamicconfig = yaml.load(_)

        # Extract config info from Host file based on id
        # Populate jinja2 template with host data
        return self.render_template('templates/leaftemplate.j2', dynamicconfig, hostid)

    def render_template(self, template, dynamicconfig, hostid):
        """Renders a config template."""

        template = ENV.get_template(template)
        return template.render(
            config=self.config,
            hostname=dynamicconfig[hostid]['hostname'],
            mgmtaddr=dynamicconfig[hostid]['mgmtaddr']
        )


def main():
    t = TemplateMgr()
    print t.process_id('SAL123456')

if __name__ == '__main__':
    main()
