# You can run this .tac file directly with:
#    twistd -ny doorbell-service.tac

"""
The important part of this, the part that makes it a .tac file, is
the final root-level section, which sets up the object called 'application'
which twistd will look for
"""

import os

from twisted.internet import epollreactor
epollreactor.install()

from twisted.application import service, internet
from twisted.web import static, server

# nasty hack
import sys
sys.path.append('/var/lib/doorbell')
import doorbell

def getWebService():
    """
    Return a service suitable for creating an application object.
    """
    s = server.Site(doorbell.Simple())
    return internet.TCPServer(80, s,interface="doorbell.verieda.com")

# this is the core part of any tac file, the creation of the root-level
# application object
application = service.Application("Doorbell application")

# attach the service to its parent application
service = getWebService()
service.setServiceParent(application)

# :wrap=soft:maxLineLen=120:mode=python:
