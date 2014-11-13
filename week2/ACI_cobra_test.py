from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
from cobra.mit.request import ConfigRequest
from cobra.mit.request import DnQuery
from cobra.model.fv import Tenant
from cobra.mit.naming import Dn
import inspect
import pprint


def do_login():
    apicUrl = 'https://198.18.133.200'
    loginSession = LoginSession(apicUrl, 'admin', 'C1sco12345')
    active_session = MoDirectory(loginSession)
    active_session.login()
    # print loginSession.cookie
    return active_session


def update_config(active_session, change_location):
    configReq = ConfigRequest()
    configReq.addMo(change_location)
    active_session.commit(configReq)


def target_location_lookup(active_session, location):
    change_location = active_session.lookupByDn(location)
    return change_location


def class_object_lookup(active_session, object_name):
    # pp = pprint.PrettyPrinter(indent=4)
    ret_obj = active_session.lookupByClass(object_name)
    # pp.pprint(inspect.getmembers(ret_obj))
    return ret_obj


def new_tenant(active_location, tenant_name):
    tenant = Tenant(active_location, tenant_name)
    return tenant


def logout(active_session):
    active_session.logout()


def target_lookup(session):
    # pp = pprint.PrettyPrinter(indent=4)
    for index in range(1, 5):
        # chose the location to work on
        target_obj = target_location_lookup(session,
                                            'topology/pod-1/node-10{0}'.format(index))
        # pp.pprint(inspect.getmembers(target_obj))
        # print '**********************************************'


def turtles_down(session, referer):
    dnQuery = DnQuery(referer.dn)
    dnQuery.queryTarget = 'children'
    childMo = session.query(dnQuery)
    for newMo in childMo:
        print str(newMo.dn)
        turtles_down(session, newMo)


def main():
    # Create a new session
    session = do_login()
    # Find a MO by class
    class_obj = class_object_lookup(session, 'fabricTopology')
    # Find a MO by DN
    obj_dn = target_location_lookup(session, 'uni')
    # Recursively iterate over all the child nodes for the given DN
    turtles_down(session, obj_dn)
    # Wrap it up
    logout(session)

if __name__ == '__main__':
    main()
