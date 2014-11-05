#!/usr/bin/env python
""" jinja2-nxos-config

    Accepts arguments from YAML config file
    and generates a Jinja2 configuration
"""

from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('./'))


class TemplateBuilder(object):

    def __init__(self, configfile):
        """Pulls YAML configuration from file and returns dict object"""
        with open(configfile) as _:
            self.config = yaml.load(_)

    def render_template(self, template, dynamicconfig, hostid):
        """Renders a config template."""

        template = ENV.get_template(template)
        return template.render(
            config=self.config,
            hostname=dynamicconfig[hostid]['hostname'],
            mgmtaddr=dynamicconfig[hostid]['mgmtaddr']
        )

if __name__ == '__main__':

    tmpbld = TemplateBuilder('config.yml')

    #Ideally you'd pull this from the URL being passed to the web server
    hostid = 'SAL123456'

    with open('dynamicconfig.yml') as _:
        dynamicconfig = yaml.load(_)

    print tmpbld.render_template('leaftemplate.j2', dynamicconfig, hostid)
