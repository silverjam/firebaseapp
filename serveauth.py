#!/usr/bin/env python3

import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

AUTH_HTML_PAGE = open("auth.html", 'rb').read()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-length", len(AUTH_HTML_PAGE))
        self.end_headers()
        self.wfile.write(AUTH_HTML_PAGE)

server_address = ('localhost', 0)
httpd = HTTPServer(server_address, RequestHandler)

port = httpd.socket.getsockname()[1]
print("Listening on port " + str(port))

import time
import threading

def open_page():
    time.sleep(1)
    webbrowser.open('http://localhost:' + str(port))

threading.Thread(target=open_page).start()
httpd.serve_forever()
