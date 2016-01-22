"""
experimental integration between ahab and Flask SSE
"""

from composeui import app
from threading import Thread
import logging
from json import dumps
from ahab import Ahab
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from gevent import monkey
from flask import Response

logging.basicConfig(level=logging.DEBUG)

# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)

#app = Flask(__name__)
subscriptions = []

@app.route("/subscribe")
def subscribe():
    def gen():
        queue = Queue()
        subscriptions.append(queue)
        try:
            while True:
                result = queue.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(queue)

    return Response(gen(), mimetype="text/event-stream")

def sse_handler(event, data):
    """
    default SSE handler for ahab notifications
    """
    label = data['Config']['Labels'] if ('Config' in data and 'Labels' in data['Config']) else None
    notification = dict(status=event['status'], \
        metadata=label)
    for sub in subscriptions[:]:
        sub.put(dumps(notification))

ahab = Ahab(handlers=[sse_handler])

monkey.patch_all(subprocess=True)

Thread(target=ahab.listen).start()
