import http.server
import socketserver
import socket
import urllib.request
import json
import os
import threading

PORT = int(os.environ.get("PORT", 8000))
DEFAULT_DIR = "/Users/apple/.gemini/antigravity-ide/scratch/youtube_premium_clone"
DIRECTORY = DEFAULT_DIR if os.path.exists(DEFAULT_DIR) else os.path.dirname(os.path.abspath(__file__))

def get_lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

_cached_public_ip = "Loading..."
def update_public_ip():
    global _cached_public_ip
    try:
        url = 'https://api.ipify.org'
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=4) as response:
            _cached_public_ip = response.read().decode('utf-8').strip()
    except Exception as e:
        print(f"Error fetching public IP: {e}")
        _cached_public_ip = "Unknown"

# Fetch public IP in background
threading.Thread(target=update_public_ip, daemon=True).start()

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path == '/api/network':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            lan = get_lan_ip()
            response_data = {
                'lan_ip': lan,
                'public_ip': _cached_public_ip
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            super().do_GET()

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"BOS WAVE Server running on port {PORT}")
        httpd.serve_forever()
