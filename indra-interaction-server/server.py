from finder import interactionFinderJsonStr
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import urllib.parse
import os


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        o = urlparse(self.path)
        path = o.path
        query = urllib.parse.parse_qs(o.query)

        if path == '/find-interactions':
            resp = find_interactions(query['gene'])
            return self.wrap_response(to_bytes(resp))

    def wrap_response(self, resp):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp)

def to_bytes(r):
    return bytes(r.encode("utf-8"))

def find_interactions(genes):
    return interactionFinderJsonStr(genes)

port = 8000
if 'PORT' in os.environ:
    port = os.environ['PORT']

httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
httpd.serve_forever()
