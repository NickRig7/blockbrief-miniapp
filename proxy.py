#!/usr/bin/env python3
"""
Simple HTTP proxy that bypasses localtunnel auth
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.request

class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve miniapp.html directly
        if self.path.startswith('/miniapp.html') or self.path == '/':
            try:
                with open('/workshop/blockbrief/miniapp.html', 'r') as f:
                    content = f.read()
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode())
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404)
    
    def log_message(self, format, *args):
        pass

if __name__ == '__main__':
    PORT = 8888
    print(f"Proxy running on port {PORT}")
    server = HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    server.serve_forever()
