from finder import interactionFinderJsonStr
from config import read_from_config

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import urllib.parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        o = urlparse(self.path)
        path = o.path
        query = urllib.parse.parse_qs(o.query)

        if path == '/find-interactions':
            resp = find_interactions(query['source'])
            return self.wrap_response(to_bytes(resp))

    def wrap_response(self, resp):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp)

def to_bytes(r):
    return bytes(r.encode("utf-8"))

def find_interactions(sources):
    return interactionFinderJsonStr(sources)

# port = 8000
# if 'PORT' in os.environ:
#     port = os.environ['PORT']

port = read_from_config('PORT')

httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
httpd.serve_forever()
