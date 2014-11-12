import yaml
from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.model.fv import Tenant


class ACIObj(object):
    """
    Create an ACI Object
    """

    def __init__(self):
        self.host = '198.18.133.200'
        self.user = 'admin'
        self.password = 'C1sco12345'
        self.tenantStr = 'testtenant'
        #self.set_auth('auth.yaml')
        self.modir = self.apic_login()
        self.mo = self.modir.lookupByDn('uni')

        self.tenant = self.create_tenant(self.tenantStr)
        self.commit_change()

    def look_up_mo(self, path, mo_name, set_mo=True):
        return self.modir.lookupByDn(path + mo_name)

    def set_auth(self, yamlfile):
        """ Imports auth info from YAML file """
        with open(yamlfile, 'r') as _:
            auth = yaml.load(_)
            print auth
            self.user = auth['user']
            self.password = auth['password']
            self.host = auth['host']
            self.tenantStr = auth['tenant']

    def apic_login(self):
        """Login to APIC"""
        lsess = LoginSession('https://' + self.host, self.user, self.password)
        modir = MoDirectory(lsess)
        modir.login()
        print lsess.cookie
        return modir

    def create_tenant(self, tenantStr):
        """Create a tenant"""

        # Get the top level policy universe directory
        uniMo = self.modir.lookupByDn('uni')

        # create the tenant object
        return Tenant(uniMo, tenantStr)

    def commit_change(self, changed_object=None, print_xml=True):
        """Commit the changes to APIC"""

        # config_req = ConfigRequest()
        # config_req.addMo(self.mo)
        # self.modir.commit(config_req)
        # modir.logout()
        configReq = ConfigRequest()
        configReq.addMo(self.mo)
        self.modir.commit(configReq)
        self.modir.logout()

if __name__ == '__main__':
    print "start"
    mo = ACIObj()
