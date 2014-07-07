#!/usr/bin/env python3
from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from subprocess import Popen
import cgi

def channel_file(source, destination):
    destination.write(source.read().encode("utf8"))

class ShoutRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        with open('index.html') as index:
            self.send_response(200, "Shout!")
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            
            channel_file(index, self.wfile)
    
    def do_POST(self):
        length = int(self.headers.get('Content-Length'))
        body = self.rfile.read(length).decode("utf8")
        arguments = cgi.parse_qs(body)
        
        command = ["say"]
        command.extend(arguments['text'])
        Popen(command)
        
        self.do_GET()

httpd = HTTPServer(('0.0.0.0', 8000), ShoutRequestHandler)
httpd.serve_forever()
