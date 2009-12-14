from twisted.internet import defer
from twisted.web import server, resource
from twisted.internet import reactor

import re

re_uid = re.compile("^/([0-9]+)$")
re_post = re_uid
re_get = re_uid


class Simple(resource.Resource):
	isLeaf = True
	def __init__(self):
		self.firedEvents = set()
		self.waitingEvents = {}
	def render_GET(self, request):
		m = re_get.match(request.path)
		if m:
			uid = int(m.group(1))
			if uid in self.firedEvents:
				setHeaders(request)
				return getResponse(request)
			else:
				try:
					l = self.waitingEvents[uid]
					l.append(request)
				except KeyError,e:
					self.waitingEvents[uid] = [request]
				return server.NOT_DONE_YET
		else:
			return "Invalid Request"
	def render_POST(self,request):
		m = re_post.match(request.path)
		if m:
			uid = int(m.group(1))
			self.firedEvents.add(uid)
			try:
				for req in self.waitingEvents[uid]:
					writeRes(req)
				del(self.waitingEvents[uid])
			except KeyError,e:
					pass
			return "ok"
		else:
			return "Invalid Request"
			

def setHeaders(request):
	request.setHeader("content-type","text/javascript")
def getResponse(request):
	uid = int(re_uid.match(request.path).group(1))
	return "doorbell(%d);" % uid
	


def writeRes(request):
	try:
		setHeaders(request)
		request.write(getResponse(request))
		request.finish()
	except Exception, e:
		print e

def main(port=8080, interface=None):
	from twisted.internet import reactor
	from twisted.web import server
	r = Simple()
	reactor.listenTCP(8080, server.Site(r), interface=interface) 
	reactor.run()


if __name__ == '__main__':
	main()
