from finder import interactionFinderJsonStr
from config import read_from_config
from entity_sign import EntitySign

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
import urllib.parse


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        o = urlparse(self.path)
        path = o.path
        query = urllib.parse.parse_qs(o.query)

        if path == '/find-interactions':
            sign = EntitySign.UNSIGNED
            if 'sign' in query:
                sign = query['sign'][0]

            entities = query['source']
            if sign is not EntitySign.UNSIGNED:
                entities = entities + query['target']

            print(entities)

            resp = find_interactions(entities, sign)
            return self.wrap_response(to_bytes(resp))

    def wrap_response(self, resp):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(resp)

def to_bytes(r):
    return bytes(r.encode("utf-8"))

def find_interactions(entities, sign):
    return interactionFinderJsonStr(entities, sign)

port = read_from_config('PORT')

httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
httpd.serve_forever()
