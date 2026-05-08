import os
import http.server
import socketserver

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
PORT = 3000

Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving {ROOT} at http://localhost:{PORT}")
    httpd.serve_forever()
