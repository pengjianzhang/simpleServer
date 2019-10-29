#!/usr/bin/python

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyHandler(BaseHTTPRequestHandler):

    def simple_respond(self, code, data, headers={}):

        data_len = len(data)
        if data_len > 0:
            b = bytes(data, encoding='utf-8')
            data_len = len(b)

        headers['Content-type'] = 'text/html'
        if code >= 200:
            headers['Content-Length'] = str(data_len)
        else:
            data_len = 0

        self.send_response(code)
	
        for name,value in headers.items():	
            self.send_header(name, value)
		
        self.send_header('Connection', 'keep-alive')
		
        self.end_headers()
        if data_len > 0:
            self.wfile.write(b)

    def do_HEAD(self):
        self.simple_respond(200, '')

    def do_GET(self):
        self.protocol_version = 'HTTP/1.1'
        if self.path == "/websocket_upgrade":
            headers = {
                'Upgrade': 'websocket',
                'Connection': 'Upgrade'
            }
  
            self.simple_respond(101, '', headers)
        else:
            self.simple_respond(200, 'hello\n')

def run(ip, port):
    addr = (ip, port)
    httpd = HTTPServer(addr, MyHandler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

def help():
    print(sys.argv)
    print(sys.argv[0], " ip port")

if __name__ == '__main__':

    if len(sys.argv) == 3:
        run(sys.argv[1], int(sys.argv[2]))
    else:
        help()
