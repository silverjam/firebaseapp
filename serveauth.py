#!/usr/bin/env python3

import sys

import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

import time
import threading
import requests

import urllib.parse

import handlecb

AUTH_HTML_PAGE = open("auth.html", 'rb').read()

class RequestHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.send_header("Content-length", len(AUTH_HTML_PAGE))
		self.end_headers()
		
		self.wfile.write(AUTH_HTML_PAGE)
		
		if self.path == '/done':
			httpd.shutdown()
			
			
		
server_address = ('localhost', 8008)
httpd = HTTPServer(server_address, RequestHandler)

port = httpd.socket.getsockname()[1]
print("Listening on port " + str(port))

def serve_web():
	httpd.serve_forever()

def open_page():
	
	time.sleep(0.5)
	
	cb_url = handlecb.get_cb_url()
	
	url = 'safari-http://localhost:{}/?cb={}'.format(port, cb_url)
	
	webbrowser.open(url)

t = threading.Thread(target=serve_web)
t.start()

open_page()

t.join()
