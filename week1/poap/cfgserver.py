from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web.server import Site
import templatemgr


class webServer(Resource):
    """
    Server to hos POAP config requests
    """

    def __init__(self):
        Resource.__init__(self)

    def getChild(self, name, request):
        return self

    def render_GET(self, request):
        # print 'Got request'
        print request.args
        if request.args:
            if 'cfg' in request.args:
                param = request.args['cfg']
                print "You requested information for {0}".format(param[0])
                template = templatemgr.TemplateMgr()
                return '{0}'.format(template.process_id(param[0]))
            else:
                print "Unknown parameter found."
        else:
            print "No parameters found in request."
        return None


def main():
    print 'Starting Web Server'
    resource = webServer()
    factory = Site(resource)
    reactor.listenTCP(8880, factory)
    reactor.run()

if __name__ == '__main__':
    main()
