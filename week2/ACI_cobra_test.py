from cobra.mit.access import MoDirectory
from cobra.mit.session import LoginSession
import inspect
import pprint

# Import the config request
from cobra.mit.request import ConfigRequest
# Import the tenant class from the model
from cobra.model.fv import Tenant

pp = pprint.PrettyPrinter(indent=4)
apicUrl = 'https://198.18.133.200'
loginSession = LoginSession(apicUrl, 'admin', 'C1sco12345')
moDir = MoDirectory(loginSession)
moDir.login()

configReq = ConfigRequest()

print loginSession.cookie
uniMo = moDir.lookupByDn('uni')
# create the tenant object
fvTenantMo = Tenant(uniMo, 'ExampleCorp')

#print inspect.getmembers(uniMo)
mystatus = uniMo.status
mychildren = uniMo.children
numchildren = uniMo.numChildren
#print inspect.getmembers(mystatus)
#print type(mychildren)
#print mychildren
#print inspect.getmembers(mychildren)
pp.pprint(inspect.getmembers(mychildren))
print numchildren

for child in mychildren:
    print pp.pprint(inspect.getmembers(child))
    print child.__doc__
    print '***********************************'

for prop in uniMo.dirtyProps:
    print prop

# import msvcrt
# c = msvcrt.getch()
# print 'you entered',
configReq.addMo(uniMo)
moDir.commit(configReq)
moDir.logout()
