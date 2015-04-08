# do the following command before you run this script:
# openssl req -new -x509 -keyout server.pem -out server.pem -days 365 -nodes
import BaseHTTPServer
import SimpleHTTPServer
import cgi
import datetime
import logging
import os
import ssl
import sys

LOG = logging.getLogger(__name__)
LOG.addHandler(logging.StreamHandler(sys.stdout))
LOG.setLevel(logging.DEBUG)

PORT = 6666

class ServerHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    def do_GET(self):
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)

handler = ServerHandler
httpd = BaseHTTPServer.HTTPServer(('localhost', PORT), handler)
httpd.socket = ssl.wrap_socket (httpd.socket, certfile='server.pem', server_side=True)
httpd.serve_forever()
