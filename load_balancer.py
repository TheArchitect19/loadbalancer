import http.client
import socket
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


BACKEND_SERVERS = [("localhost", 8000), ("localhost", 8001), ("localhost", 8002)]
current_server = 0
lock = threading.Lock()

class LoadBalancerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_server

        # round-robin logic
        with lock:
            backend_host, backend_port = BACKEND_SERVERS[current_server]
            current_server = (current_server + 1) % len(BACKEND_SERVERS)

        try:
            # forward request to the backend server
            conn = http.client.HTTPConnection(backend_host, backend_port)
            conn.request("GET", self.path)
            resp = conn.getresponse()

            # relay the response back to the client
            self.send_response(resp.status)
            self.send_header("Content-type", resp.getheader("Content-type"))
            self.end_headers()
            self.wfile.write(resp.read())

        except socket.error:
            self.send_error(502, "Bad Gateway")

if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, LoadBalancerHandler)
    print("Load Balancer running on port 8080...")
    httpd.serve_forever()
