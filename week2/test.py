import sys
import re
import yaml
import argparse
import getpass
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant
from cobra.internal.codec.xmlcodec import toXMLStr

# add a list the the same type MOs.
def add_mos(msg, key_function, opt_args_function=None, do_first=False, once=False):
    """
    :param msg: message about the input
    :param key_function: main function
    :param opt_args_function: secondary function
    :param do_first: key_function and opt_args_function will be run without asking "if adding a mo"
    :param once:  key_function and opt_args_function will be run only once.
    :return:  an array of all the inputs
    """
    mos = []
    add_one_mo = True if do_first else input_yes_no(prompt=msg, required=True)
    msg = msg.replace(' a ', ' another ')
    msg = msg.replace(' an ', ' another ')
    while add_one_mo:
        new_mo = {}
        new_mo['key_args'] = key_function()
        if opt_args_function is not None:
            new_mo['opt_args'] = opt_args_function(new_mo['key_args'])
        mos.append(new_mo)
        if once:
            add_one_mo = False
        else:
            add_one_mo = input_yes_no(prompt=msg, required=True)
    return mos[0] if once else mos


def read_add_mos_args(add_mos_result, get_opt_args=False):
    """
    :param add_mos_result: result from add_mos
    :param get_opt_args: if there is opt_args_function, an array of opt_args will be return as well
    :return: array of key_args and opt_args
    """
    key_args = []
    opt_args = []
    for i in add_mos_result:
        key_args.append(i['key_args'])
        if get_opt_args:
            opt_args.append(i['opt_args'])
    if get_opt_args:
        return key_args, opt_args
    else:
        return key_args


class ACIObj(object):
    """
    Create a mo
    """

    def __init__(self):
        self.args = None
        self.delete = False
        self.host = '198.18.133.200'
        self.user = 'admin'
        self.password = 'C1sco12345'
        self.tenant = self.tenant if hasattr(self, 'tenant') else 'None'    # the proper way
        self.set_auth('auth.yaml')
        self.application = None
        self.modir = self.apic_login()
        self.mo = None
        self.config_mode = 'yaml'
        # self.optional_args = {}
        # self.set_argparse()
        # if list({'-h', '--help'} & set(sys.argv)):
        #     sys.exit()
        # self.set_mode()
        # self.__getattribute__('run_'+self.config_mode+'_mode')()
        # self.create_or_delete()
        self.tenant = self.create_tenant('mierdinrulez')
        self.commit_change()

    def look_up_mo(self, path, mo_name, set_mo=True):
        return self.modir.lookupByDn(path + mo_name)

    def set_auth(self, yamlfile):
        """ Imports auth info from YAML file """
        with open(yamlfile, 'r') as _:
            args = yaml.load(_)
            print args

    def apic_login(self):
        """Login to APIC"""
        lsess = LoginSession('https://' + self.host, self.user, self.password)
        modir = MoDirectory(lsess)
        modir.login()
        return modir

    def create_tenant(self, tenant):
        """Create a tenant"""

        # Get the top level policy universe directory
        uniMo = self.modir.lookupByDn('uni')

        # create the tenant object
        return Tenant(uniMo, tenant)

    def set_argparse(self):
        parser = argparse.ArgumentParser(description=self.description)
        parser.add_argument('-d', '--delete', help='Flag to run a delete function.',  action='store_const', const=self.set_delete, default=null_function)
        self.subparsers = parser.add_subparsers(help='sub-command help')
        self.parser_yaml = self.subparsers.add_parser(
            'yaml', help='Config with a yaml file.'
        )
        self.parser_cli = self.subparsers.add_parser(
            'cli', help='Config base on the input arguments from Comment line.'
        )
        self.parser_wizard = self.subparsers.add_parser(
            'wizard', help='Config following a wizard.'
        )

        self.set_cli_mode()
        self.set_yaml_mode()
        self.set_wizard_mode()

        args = parser.parse_args()
        args.delete()
        self.args = vars(args)

    def set_yaml_mode(self):
        self.parser_yaml.add_argument('yaml_file', help='yaml file')

    def run_yaml_mode(self):
        f = open(self.args['yaml_file'], 'r')
        self.args = yaml.load(f)
        f.close()
        self.set_host_user_password()
        self.read_key_args()
        self.read_opt_args()
        self.apic_login()

    def input_tenant_name(self, msg='\nPlease specify Tenant info:'):
        print msg
        self.tenant = input_raw_input("Tenant Name", required=True)

    def check_if_tenant_exist(self, return_boolean=False, set_mo=True):
        """
        :param return_boolean: if set, return value is True or False
        :param set_mo: if set, self.mo is set to be Tenant
        :return: the tenant MO
        """
        fv_tenant = self.look_up_mo('uni/tn-', self.tenant, set_mo=set_mo)
        if not isinstance(fv_tenant, Tenant):
            print 'Tenant', self.tenant, 'does not existed. \nPlease create a tenant.'
            return False if return_boolean else sys.exit()
        return fv_tenant

    def check_if_mo_exist(self, path, mo_name='', module=None, description='', detail_description='', set_mo=True, return_false=False):
        """
        :param path: the path to the MO
        :param mo_name: the name of the MO
        :param module: the module of the MO
        :param description: message shown when MO is not existed
        :param detail_description: message shown when MO is not existed
        :param set_mo: if set, self.mo is set to be Tenant
        :param return_false: when true, the function will return false if MO is not existed
        :return: the MO if existed
        """
        temp_mo = self.look_up_mo(path, mo_name, set_mo=set_mo)
        if module is not None and not isinstance(temp_mo, module):
            if detail_description != '':
                print detail_description
            else:
                print description, mo_name, 'does not existed.'
            if return_false:
                return False
            else:
                print 'The programing is exiting.'
                sys.exit()
        if set_mo:
            self.mo = temp_mo
        return temp_mo

    def set_delete(self):
        self.delete = True

    def delete_mo(self):
        self.mo.delete()

    def input_application_name(self, msg='\nPlease specify Application info:'):
        print msg
        self.application = input_raw_input("Application Name", required=True)
        return self.application

    def commit_change(self, changed_object=None, print_xml=True):
        """Commit the changes to APIC"""
        changed_object = self.mo if changed_object is None else changed_object

        config_req = ConfigRequest()
        config_req.addMo(changed_object)
        self.modir.commit(config_req)

    def create_or_delete(self):
        if self.delete:
            self.delete_mo()
        else:
            self.main_function()

    def read_opt_args(self):
        self.optional_args = self.args['optional_args'] if 'optional_args' in self.args.keys() else self.args


if __name__ == '__main__':
    print "start"
    mo = ACIObj()
