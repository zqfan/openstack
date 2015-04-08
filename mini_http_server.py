import logging
import sys
import datetime
import wsgiref.simple_server as server

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))
LOG.setLevel(logging.DEBUG)

def hello_world(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    request_body_size = int(environ.get('CONTENT_LENGTH') or 0)
    request_body = environ['wsgi.input'].read(request_body_size)
    LOG.debug('%s: body = %s', datetime.datetime.utcnow(), request_body)
    return 'little apple\n'

server.make_server('', 6666, hello_world).serve_forever()
