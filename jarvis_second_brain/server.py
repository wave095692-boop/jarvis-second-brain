import http.server
import socketserver
import socket
import json
import os
import subprocess
import shutil
import urllib.request
import urllib.error

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_DIR = os.path.dirname(DIRECTORY)
PORT = int(os.environ.get("PORT", 8500))

PDF_PATH = "/Users/apple/Desktop/rudedog_content_ideas.pdf"
if not os.path.exists(os.path.dirname(PDF_PATH)):
    PDF_PATH = os.path.join(WORKSPACE_DIR, "rudedog_content_ideas.pdf")

PDF_PATH_OLD = "/Users/apple/Desktop/rudedog_fair_10days_content.pdf"
if not os.path.exists(os.path.dirname(PDF_PATH_OLD)):
    PDF_PATH_OLD = os.path.join(WORKSPACE_DIR, "rudedog_fair_10days_content.pdf")

NOTES_FILE = os.path.join(DIRECTORY, "notes.json")
PROJECT_FILES_FILE = os.path.join(DIRECTORY, "project_files.json")
ROOM_LABELS_FILE = os.path.join(DIRECTORY, "room_labels.json")

def load_room_labels():
    default_labels = {
        "Boss": "บอส (Boss)",
        "Friend1": "เพื่อน 1 (Friend 1)",
        "Friend2": "เพื่อน 2 (Friend 2)",
        "Friend3": "เพื่อน 3 (Friend 3)",
        "Friend4": "เพื่อน 4 (Friend 4)"
    }
    if os.path.exists(ROOM_LABELS_FILE):
        try:
            with open(ROOM_LABELS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k in default_labels:
                    if k not in data:
                        data[k] = default_labels[k]
                return data
        except Exception:
            pass
    return default_labels

def save_room_labels(data):
    try:
        with open(ROOM_LABELS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False


def load_project_files():
    if os.path.exists(PROJECT_FILES_FILE):
        try:
            with open(PROJECT_FILES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_project_files(data):
    try:
        with open(PROJECT_FILES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception:
        return False

def get_ssh_tunnel_url(log_path):
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                content = f.read()
            last_url = None
            for line in content.splitlines():
                if 'tunneled with tls termination' in line and 'https://' in line:
                    parts = line.split('https://')
                    if len(parts) > 1:
                        last_url = 'https://' + parts[1].strip()
            return last_url
        except Exception:
            pass
    return None

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

def check_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(('127.0.0.1', port)) == 0

def check_youtube_status(port, url):
    if check_port_open(port):
        return 'ONLINE'
    if url:
        if not any(local in url for local in ['localhost', '127.0.0.1', '0.0.0.0']):
            try:
                req = urllib.request.Request(
                    url,
                    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
                )
                with urllib.request.urlopen(req, timeout=1.0) as response:
                    if response.status in [200, 302, 401, 403, 404, 301]:
                        return 'ONLINE'
            except Exception:
                pass
    return 'OFFLINE'

def resolve_file_path(path):
    if not path:
        return path
    if os.path.exists(path):
        return path
    filename = os.path.basename(path)
    campaign_path = os.path.join(WORKSPACE_DIR, "campaign_files", filename)
    if os.path.exists(campaign_path):
        return campaign_path
    yt_path = os.path.join(WORKSPACE_DIR, "youtube_premium_clone", filename)
    if os.path.exists(yt_path):
        return yt_path
    root_path = os.path.join(WORKSPACE_DIR, filename)
    if os.path.exists(root_path):
        return root_path
    jsb_path = os.path.join(DIRECTORY, filename)
    if os.path.exists(jsb_path):
        return jsb_path
    return path

def check_tunnel_online():

    try:
        # Check if localtunnel process is running (via pgrep)
        res = subprocess.run(['pgrep', '-f', 'localtunnel'], capture_output=True, text=True)
        if res.stdout.strip():
            return True
            
        # Fallback: check URL response
        req = urllib.request.Request(
            'https://boswave-gamer.loca.lt', 
            headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
        )
        with urllib.request.urlopen(req, timeout=1.0) as response:
            return response.status in [200, 302, 401]
    except Exception:
        return False

def get_system_stats():
    stats = {}
    # Load averages (Mac OS compatible)
    try:
        load = os.getloadavg()
        stats['cpu_load'] = f"{load[0]:.2f}, {load[1]:.2f}, {load[2]:.2f}"
    except Exception:
        stats['cpu_load'] = "Unavailable"
        
    # Disk usage
    try:
        total, used, free = shutil.disk_usage("/")
        stats['disk_free'] = f"{free / (2**30):.1f} GB / {total / (2**30):.1f} GB"
    except Exception:
        stats['disk_free'] = "Unavailable"
        
    return stats

class SecondBrainHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        if path == '/api/status':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            # Diagnose PDF
            pdf_exists = os.path.exists(PDF_PATH)
            pdf_time = ""
            if pdf_exists:
                import datetime
                mtime = os.path.getmtime(PDF_PATH)
                pdf_time = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')

            dashboard_tunnel = os.environ.get("DASHBOARD_PUBLIC_URL")
            if not dashboard_tunnel:
                dashboard_tunnel = get_ssh_tunnel_url(os.path.join(WORKSPACE_DIR, "ssh_tunnel_output.log"))
            
            yt_tunnel = os.environ.get("YOUTUBE_PUBLIC_URL")
            if not yt_tunnel:
                yt_tunnel = get_ssh_tunnel_url(os.path.join(WORKSPACE_DIR, "youtube_tunnel_output.log"))
            
            # Fallback to localtunnel if ssh tunnel not running
            if not dashboard_tunnel:
                dashboard_tunnel = 'https://slow-beers-hope.loca.lt'
            if not yt_tunnel:
                yt_tunnel = 'https://boswave-gamer.loca.lt'

            response_data = {
                'lan_ip': get_lan_ip(),
                'youtube_clone': {
                    'status': check_youtube_status(8000, yt_tunnel),
                    'port': 8000,
                    'url': yt_tunnel
                },
                'tunnel': {
                    'status': 'ONLINE' if (yt_tunnel or check_tunnel_online()) else 'OFFLINE',
                    'url': dashboard_tunnel
                },
                'pdf': {
                    'status': 'FOUND' if pdf_exists else 'NOT FOUND',
                    'last_modified': pdf_time,
                    'path': PDF_PATH
                },
                'system': get_system_stats()
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
            
        elif path == '/api/notes':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            
            if os.path.exists(NOTES_FILE):
                with open(NOTES_FILE, 'r', encoding='utf-8') as f:
                    data = f.read()
                    self.wfile.write(data.encode('utf-8'))
            else:
                self.wfile.write(json.dumps([]).encode('utf-8'))

        elif path == '/api/uploads':
            upload_dir = os.path.join(DIRECTORY, "uploads")
            rooms = ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]
            files_data = {}
            for r in rooms:
                r_dir = os.path.join(upload_dir, r)
                if not os.path.exists(r_dir):
                    os.makedirs(r_dir)
                files = os.listdir(r_dir)
                files = [f for f in files if not f.startswith('.')]
                files.sort()
                files_data[r] = files
            
            response_data = {
                'files': files_data,
                'labels': load_room_labels()
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))


        elif path == '/view/upload':
            file_name = query_params.get("file", [""])[0]
            file_name = os.path.basename(file_name)
            room = query_params.get("room", ["Boss"])[0]
            if room not in ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]:
                room = "Boss"
                
            upload_dir = os.path.join(DIRECTORY, "uploads", room)
            file_path = os.path.join(upload_dir, file_name)
            if os.path.exists(file_path):
                self.send_response(200)
                import mimetypes
                mime_type, _ = mimetypes.guess_type(file_path)
                if not mime_type:
                    mime_type = 'application/octet-stream'
                self.send_header('Content-Type', mime_type)
                
                friendly_types = [
                    'application/pdf', 'image/png', 'image/jpeg', 'image/gif', 'image/webp', 'image/svg+xml',
                    'text/plain', 'text/html', 'text/css', 'text/javascript',
                    'video/mp4', 'video/webm', 'video/ogg', 'video/quicktime', 'video/x-m4v',
                    'audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/aac', 'audio/mp4', 'audio/x-m4a'
                ]
                if mime_type not in friendly_types:
                    self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Uploaded file not found'}).encode('utf-8'))
                
        elif path == '/view/war_room':
            data = load_project_files()
            file_path = None
            for item in data.get('campaign', []):
                if item['key'] == 'war_room':
                    file_path = item['path']
                    break
            if not file_path:
                file_path = '/Users/apple/Downloads/RUDEDOG_FAIR_2026_WAR_ROOM.html'
            file_path = resolve_file_path(file_path)
            if os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'WAR ROOM HTML not found'}).encode('utf-8'))

        elif path == '/view/live_strategy':
            data = load_project_files()
            file_path = None
            for item in data.get('campaign', []):
                if item['key'] == 'live_strategy':
                    file_path = item['path']
                    break
            if not file_path:
                file_path = '/Users/apple/Downloads/กลยุทธ์ไลฟ์คืนนี้_แว่น_Jarvis.html'
            file_path = resolve_file_path(file_path)
            if os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Live Strategy HTML not found'}).encode('utf-8'))

        elif path == '/view/pdf':
            data = load_project_files()
            file_path = None
            for item in data.get('campaign', []):
                if item['key'] == 'pdf_latest':
                    file_path = item['path']
                    break
            if not file_path:
                file_path = PDF_PATH
            file_path = resolve_file_path(file_path)
            if os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'PDF not found'}).encode('utf-8'))

        elif path == '/view/pdf_old':
            data = load_project_files()
            file_path = None
            for item in data.get('campaign', []):
                if item['key'] == 'pdf_old':
                    file_path = item['path']
                    break
            if not file_path:
                file_path = PDF_PATH_OLD
            file_path = resolve_file_path(file_path)
            if os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Old PDF not found'}).encode('utf-8'))

        elif path == '/view/pdf_sheet3':
            data = load_project_files()
            file_path = None
            for item in data.get('campaign', []):
                if item['key'] == 'pdf_sheet3':
                    file_path = item['path']
                    break
            if not file_path:
                file_path = '/Users/apple/Desktop/แผ่น3.pdf'
            file_path = resolve_file_path(file_path)
            if os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'application/pdf')
                self.end_headers()
                with open(file_path, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Sheet 3 PDF not found'}).encode('utf-8'))

        elif path == '/api/project-files':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            data = load_project_files()
            for cat in data:
                for item in data[cat]:
                    resolved = resolve_file_path(item['path'])
                    item['exists'] = os.path.exists(resolved)
                    item['path'] = resolved
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


        elif path == '/api/file':
            key = query_params.get("key", [""])[0]
            data = load_project_files()
            file_path = None
            for cat in data:
                for item in data[cat]:
                    if item['key'] == key:
                        file_path = item['path']
                        break
                if file_path:
                    break
            
            if file_path:
                file_path = resolve_file_path(file_path)
            
            if file_path and os.path.exists(file_path):

                self.send_response(200)
                self.send_header('Content-Type', 'text/plain; charset=utf-8')
                self.end_headers()
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.wfile.write(f.read().encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(json.dumps({'error': f'File not found: {key}'}).encode('utf-8'))
        elif path == '/api/farming_status':
            is_running = False
            try:
                res = subprocess.run(['pgrep', '-f', 'emulator_bot.py'], capture_output=True, text=True)
                if res.stdout.strip():
                    is_running = True
            except Exception:
                pass
                
            log_file = os.path.join(DIRECTORY, "farming_bot.log")
            logs = ""
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        logs = "".join(lines[-100:])
                except Exception as ex:
                    logs = f"Error reading logs: {ex}"
            else:
                logs = "Farming bot idle. No log file created yet."
                
            adb_path = '/opt/homebrew/bin/adb' if os.path.exists('/opt/homebrew/bin/adb') else 'adb'
            connected_devices = []
            try:
                res = subprocess.run([adb_path, 'devices'], capture_output=True, text=True)
                lines = res.stdout.strip().split('\n')[1:]
                for line in lines:
                    if not line.strip():
                        continue
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] == 'device':
                        connected_devices.append(parts[0])
            except Exception:
                pass
                
            response_data = {
                'running': is_running,
                'logs': logs,
                'devices': connected_devices
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        elif path == '/api/web_farming_status':
            is_running = False
            try:
                res = subprocess.run(['pgrep', '-f', 'web_farming_bot.py'], capture_output=True, text=True)
                if res.stdout.strip():
                    is_running = True
            except Exception:
                pass
                
            log_file = os.path.join(DIRECTORY, "web_farming_bot.log")
            logs = ""
            if os.path.exists(log_file):
                try:
                    with open(log_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        logs = "".join(lines[-100:])
                except Exception as ex:
                    logs = f"Error reading logs: {ex}"
            else:
                logs = "Web farming bot idle. No log file created yet."
                
            profiles_dir = os.path.join(DIRECTORY, "profiles")
            profiles = []
            if os.path.exists(profiles_dir):
                try:
                    profiles = [d for d in os.listdir(profiles_dir) if os.path.isdir(os.path.join(profiles_dir, d)) and not d.startswith('.')]
                except Exception:
                    pass
            if not profiles:
                profiles = ["profile_1", "profile_2", "profile_3"]
            profiles.sort()
            
            response_data = {
                'running': is_running,
                'logs': logs,
                'profiles': profiles
            }
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        from urllib.parse import urlparse, parse_qs
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        content_length = int(self.headers['Content-Length'])
        
        if path == '/api/verify-pin':
            try:
                post_data = self.rfile.read(content_length).decode('utf-8')
                data = json.loads(post_data) if post_data else {}
                pin = data.get("pin", "")
                if pin == "1112":
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': True, 'token': 'boss_authorized_token_xyz123'}).encode('utf-8'))
                else:
                    self.send_response(401)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Invalid keycode'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        elif path == '/api/rename-room':
            room = query_params.get("room", [""])[0]
            label = query_params.get("label", [""])[0]
            
            if room not in ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid room key'}).encode('utf-8'))
                return
                
            try:
                labels = load_room_labels()
                labels[room] = label
                save_room_labels(labels)
                
                if os.path.exists(NOTES_FILE):
                    with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                        try:
                            notes = json.load(nf)
                        except Exception:
                            notes = []
                else:
                    notes = []
                import datetime
                next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                notes.append({
                    "id": next_id,
                    "text": f"เปลี่ยนชื่อกลุ่มโฟลเดอร์สำหรับ '{room}' เป็น '{label}' สำเร็จ",
                    "timestamp": now_str
                })
                with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                    json.dump(notes, nf, ensure_ascii=False, indent=4)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'room': room, 'label': label}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return


        elif path == '/api/upload-file':
            filename = query_params.get("filename", ["document.dat"])[0]
            filename = os.path.basename(filename)
            room = query_params.get("room", ["Boss"])[0]
            if room not in ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]:
                room = "Boss"
                
            upload_dir = os.path.join(DIRECTORY, "uploads", room)
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
                
            base, ext = os.path.splitext(filename)
            counter = 1
            final_filename = filename
            while os.path.exists(os.path.join(upload_dir, final_filename)):
                final_filename = f"{base}_{counter}{ext}"
                counter += 1
                
            file_path = os.path.join(upload_dir, final_filename)
            
            try:
                file_data = self.rfile.read(content_length)
                with open(file_path, 'wb') as f:
                    f.write(file_data)
                
                # Append upload note to notes.json
                if os.path.exists(NOTES_FILE):
                    with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                        try:
                            notes = json.load(nf)
                        except Exception:
                            notes = []
                else:
                    notes = []
                import datetime
                next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                room_labels = load_room_labels()
                room_lbl = room_labels.get(room, room)

                notes.append({
                    "id": next_id,
                    "text": f"อัปโหลดไฟล์สำเร็จ: '{final_filename}' ไปยังห้อง '{room_lbl}'",
                    "timestamp": now_str
                })
                with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                    json.dump(notes, nf, ensure_ascii=False, indent=4)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'filename': final_filename}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return
            
        elif path == '/api/delete-file':
            filename = query_params.get("filename", [""])[0]
            filename = os.path.basename(filename)
            room = query_params.get("room", ["Boss"])[0]
            if room not in ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]:
                room = "Boss"
                
            upload_dir = os.path.join(DIRECTORY, "uploads", room)
            file_path = os.path.join(upload_dir, filename)
            
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                    # Append delete note to notes.json
                    if os.path.exists(NOTES_FILE):
                        with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                            try:
                                notes = json.load(nf)
                            except Exception:
                                notes = []
                    else:
                        notes = []
                    import datetime
                    next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    room_labels = load_room_labels()
                    room_lbl = room_labels.get(room, room)

                    notes.append({
                        "id": next_id,
                        "text": f"ลบไฟล์สำเร็จ: '{filename}' จากห้อง '{room_lbl}'",
                        "timestamp": now_str
                    })
                    with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                        json.dump(notes, nf, ensure_ascii=False, indent=4)
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'File not found'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return
            
        elif path == '/api/rename-file':
            old_filename = query_params.get("old_filename", [""])[0]
            old_filename = os.path.basename(old_filename)
            new_filename = query_params.get("new_filename", [""])[0]
            new_filename = os.path.basename(new_filename)
            room = query_params.get("room", ["Boss"])[0]
            if room not in ["Boss", "Friend1", "Friend2", "Friend3", "Friend4"]:
                room = "Boss"
                
            upload_dir = os.path.join(DIRECTORY, "uploads", room)
            old_path = os.path.join(upload_dir, old_filename)
            new_path = os.path.join(upload_dir, new_filename)
            
            try:
                if not old_filename or not new_filename:
                    raise Exception("Missing file name parameter")
                if os.path.exists(old_path):
                    if os.path.exists(new_path) and old_filename.lower() != new_filename.lower():
                        raise Exception("Destination file already exists")
                    os.rename(old_path, new_path)
                    
                    # Append rename note to notes.json
                    if os.path.exists(NOTES_FILE):
                        with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                            try:
                                notes = json.load(nf)
                            except Exception:
                                notes = []
                    else:
                        notes = []
                    import datetime
                    next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    room_labels = load_room_labels()
                    room_lbl = room_labels.get(room, room)

                    notes.append({
                        "id": next_id,
                        "text": f"เปลี่ยนชื่อไฟล์สำเร็จ: '{old_filename}' เป็น '{new_filename}' ในห้อง '{room_lbl}'",
                        "timestamp": now_str
                    })
                    with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                        json.dump(notes, nf, ensure_ascii=False, indent=4)
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'filename': new_filename}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Source file not found'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        elif path == '/api/rename-project-file':
            key = query_params.get("key", [""])[0]
            new_filename = query_params.get("new_filename", [""])[0]
            new_filename = os.path.basename(new_filename)
            
            try:
                if not key or not new_filename:
                    raise Exception("Missing parameters")
                
                data = load_project_files()
                target_item = None
                category_key = None
                for cat in data:
                    for item in data[cat]:
                        if item['key'] == key:
                            target_item = item
                            category_key = cat
                            break
                    if target_item:
                        break
                        
                if not target_item:
                    raise Exception("Project file key not found")
                
                old_path = resolve_file_path(target_item['path'])
                old_filename = target_item['name']
                
                if os.path.exists(old_path):

                    dir_name = os.path.dirname(old_path)
                    new_path = os.path.join(dir_name, new_filename)
                    
                    if os.path.exists(new_path) and old_filename.lower() != new_filename.lower():
                        raise Exception("Destination file already exists")
                    
                    os.rename(old_path, new_path)
                    
                    target_item['path'] = new_path
                    target_item['name'] = new_filename
                    target_item['label'] = new_filename
                    save_project_files(data)
                    
                    if os.path.exists(NOTES_FILE):
                        with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                            try:
                                notes = json.load(nf)
                            except Exception:
                                notes = []
                    else:
                        notes = []
                    import datetime
                    next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    category_labels = {
                        "campaign": "RUDEDOG FAIR CAMPAIGN",
                        "youtube": "YOUTUBE PREMIUM APP",
                        "compiler": "COMPILER SCRIPTS"
                    }
                    cat_lbl = category_labels.get(category_key, category_key)
                    
                    notes.append({
                        "id": next_id,
                        "text": f"เปลี่ยนชื่อไฟล์โปรเจกต์สำเร็จ: '{old_filename}' เป็น '{new_filename}' ในกลุ่ม '{cat_lbl}'",
                        "timestamp": now_str
                    })
                    with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                        json.dump(notes, nf, ensure_ascii=False, indent=4)
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'status': 'success', 'filename': new_filename}).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Source file not found on disk'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        elif path == '/api/delete-project-file':
            key = query_params.get("key", [""])[0]
            
            try:
                if not key:
                    raise Exception("Missing key parameter")
                
                data = load_project_files()
                target_item = None
                category_key = None
                for cat in data:
                    for item in data[cat]:
                        if item['key'] == key:
                            target_item = item
                            category_key = cat
                            break
                    if target_item:
                        break
                        
                if not target_item:
                    raise Exception("Project file key not found")
                
                file_path = resolve_file_path(target_item['path'])
                filename = target_item['name']
                
                if os.path.exists(file_path):

                    os.remove(file_path)
                
                data[category_key] = [item for item in data[category_key] if item['key'] != key]
                save_project_files(data)
                
                if os.path.exists(NOTES_FILE):
                    with open(NOTES_FILE, 'r', encoding='utf-8') as nf:
                        try:
                            notes = json.load(nf)
                        except Exception:
                            notes = []
                else:
                    notes = []
                import datetime
                next_id = max([n.get("id", 0) for n in notes]) + 1 if notes else 1
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                category_labels = {
                    "campaign": "RUDEDOG FAIR CAMPAIGN",
                    "youtube": "YOUTUBE PREMIUM APP",
                    "compiler": "COMPILER SCRIPTS"
                }
                cat_lbl = category_labels.get(category_key, category_key)
                
                notes.append({
                    "id": next_id,
                    "text": f"ลบไฟล์โปรเจกต์สำเร็จ: '{filename}' จากกลุ่ม '{cat_lbl}'",
                    "timestamp": now_str
                })
                with open(NOTES_FILE, 'w', encoding='utf-8') as nf:
                    json.dump(notes, nf, ensure_ascii=False, indent=4)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
            return

        post_data = self.rfile.read(content_length).decode('utf-8')
        
        if path == '/api/notes':
            try:
                # Save notes
                notes = json.loads(post_data)
                with open(NOTES_FILE, 'w', encoding='utf-8') as f:
                    json.dump(notes, f, ensure_ascii=False, indent=4)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success'}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))
                
        elif path == '/api/action':
            try:
                req = json.loads(post_data)
                action = req.get('action')
                log_message = ""
                
                if action == 'regenerate_pdf':
                    script_path = os.path.join(WORKSPACE_DIR, "create_pdf.py")
                    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
                    if result.returncode == 0:
                        log_message = "PDF Successfully compiled via headless Chrome."
                    else:
                        log_message = f"Error during compile: {result.stderr}"
                        
                elif action == 'restart_youtube':
                    try:
                        import platform
                        if platform.system() == 'Darwin':
                            subprocess.run(['open', '-a', '/Applications/Brave Browser.app', 'https://www.youtube.com/'])
                            log_message = "Successfully opened official YouTube in Brave Browser on local Mac."
                        else:
                            self.send_response(200)
                            self.send_header('Content-Type', 'application/json')
                            self.end_headers()
                            self.wfile.write(json.dumps({
                                'status': 'error',
                                'reason': 'not_macos',
                                'error': 'Not on macOS. Brave Browser cannot be launched from cloud container.'
                            }).encode('utf-8'))
                            return
                    except Exception as ex:
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json')
                        self.end_headers()
                        self.wfile.write(json.dumps({
                            'status': 'error',
                            'reason': 'exception',
                            'error': f"Failed to launch Brave: {ex}"
                        }).encode('utf-8'))
                        return
                    
                elif action == 'restart_tunnel':
                    # Stop existing localtunnel if any
                    try:
                        ps_res = subprocess.run(['pgrep', '-f', 'localtunnel'], capture_output=True, text=True)
                        if ps_res.stdout.strip():
                            pids = ps_res.stdout.strip().split('\n')
                            for pid in pids:
                                subprocess.run(['kill', '-9', pid])
                            log_message = "Closed existing localtunnel process. "
                        else:
                            log_message = "Localtunnel was not running. "
                    except Exception as ex:
                        log_message = f"Check/kill failed: {ex}. "

                    # Start localtunnel
                    subprocess.Popen(['npx', 'localtunnel', '--port', '8000', '--subdomain', 'boswave-gamer'], start_new_session=True)
                    log_message += "Launched localtunnel in background on subdomain 'boswave-gamer'."
                
                elif action == 'start_farming':
                    try:
                        subprocess.run(['pkill', '-f', 'emulator_bot.py'])
                    except Exception:
                        pass
                    
                    device = req.get('device', '')
                    loops = req.get('loops', 10)
                    like_prob = req.get('like_prob', 0.15)
                    comment_prob = req.get('comment_prob', 0.05)
                    query = req.get('query', '')
                    
                    log_file = os.path.join(DIRECTORY, "farming_bot.log")
                    with open(log_file, 'w', encoding='utf-8') as lf:
                        lf.write(f"--- STARTING TIKTOK FARMING BOT FOR {device or 'ANY'} ---\n")
                    
                    cmd = ['python3', os.path.join(DIRECTORY, 'emulator_bot.py')]
                    if device:
                        cmd += ['--device', device]
                    cmd += ['--loops', str(loops)]
                    cmd += ['--like-prob', str(like_prob)]
                    cmd += ['--comment-prob', str(comment_prob)]
                    if query:
                        cmd += ['--query', query]
                    
                    lf_handle = open(log_file, 'a', encoding='utf-8')
                    subprocess.Popen(cmd, stdout=lf_handle, stderr=lf_handle, start_new_session=True)
                    log_message = f"Farming bot started successfully for device {device}."
                    
                elif action == 'stop_farming':
                    try:
                        subprocess.run(['pkill', '-f', 'emulator_bot.py'])
                        log_file = os.path.join(DIRECTORY, "farming_bot.log")
                        with open(log_file, 'a', encoding='utf-8') as lf:
                            lf.write("\n🛑 STOPPED BY USER ACTIONS FROM DASHBOARD.\n")
                        log_message = "Farming bot stopped successfully."
                    except Exception as ex:
                        log_message = f"Failed to stop farming bot: {ex}"
                        
                elif action == 'start_web_farming':
                    profile = req.get('profile', 'profile_1')
                    try:
                        subprocess.run(['pkill', '-f', 'web_farming_bot.py'])
                        subprocess.run(['pkill', '-9', '-f', f'profiles/{profile}'])
                    except Exception:
                        pass
                    loops = req.get('loops', 10)
                    like_prob = req.get('like_prob', 0.15)
                    comment_prob = req.get('comment_prob', 0.05)
                    follow_prob = req.get('follow_prob', 0.0)
                    target_user = req.get('target_user', '')
                    upload_video = req.get('upload_video', '')
                    upload_caption = req.get('upload_caption', '')
                    query = req.get('query', '')
                    headed = req.get('headed', True)
                    login_mode = req.get('login_mode', False)
                    
                    log_file = os.path.join(DIRECTORY, "web_farming_bot.log")
                    with open(log_file, 'w', encoding='utf-8') as lf:
                        lf.write(f"--- STARTING TIKTOK WEB FARMING BOT FOR {profile} ---\n")
                    
                    venv_python = os.path.join(os.path.dirname(DIRECTORY), '.venv', 'bin', 'python')
                    if not os.path.exists(venv_python):
                        venv_python = 'python3'
                        
                    cmd = [venv_python, '-u', os.path.join(DIRECTORY, 'web_farming_bot.py')]
                    cmd += ['--profile', profile]
                    cmd += ['--loops', str(loops)]
                    cmd += ['--like-prob', str(like_prob)]
                    cmd += ['--comment-prob', str(comment_prob)]
                    cmd += ['--follow-prob', str(follow_prob)]
                    cmd += ['--headed', 'true' if headed else 'false']
                    if login_mode:
                        cmd += ['--login-mode']
                    if target_user:
                        cmd += ['--target-user', target_user]
                    if upload_video:
                        # Map uploaded file from the 'Boss' uploads directory
                        video_path = os.path.join(DIRECTORY, 'uploads', 'Boss', upload_video)
                        cmd += ['--upload-video', video_path]
                    if upload_caption:
                        cmd += ['--upload-caption', upload_caption]
                    if query:
                        cmd += ['--query', query]
                    
                    lf_handle = open(log_file, 'a', encoding='utf-8')
                    subprocess.Popen(cmd, stdout=lf_handle, stderr=lf_handle, start_new_session=True)
                    log_message = f"Web farming bot started successfully for profile {profile}."
                    
                elif action == 'stop_web_farming':
                    try:
                        subprocess.run(['pkill', '-f', 'web_farming_bot.py'])
                        log_file = os.path.join(DIRECTORY, "web_farming_bot.log")
                        with open(log_file, 'a', encoding='utf-8') as lf:
                            lf.write("\n🛑 STOPPED BY USER ACTIONS FROM DASHBOARD.\n")
                        log_message = "Web farming bot stopped successfully."
                    except Exception as ex:
                        log_message = f"Failed to stop web farming bot: {ex}"
                
                elif action == 'open_login_chrome':
                    profile = req.get('profile', 'profile_1')
                    profile_dir = os.path.join(DIRECTORY, "profiles", profile)
                    if not os.path.exists(profile_dir):
                        os.makedirs(profile_dir)
                    
                    try:
                        subprocess.run(['pkill', '-9', '-f', f'profiles/{profile}'])
                    except Exception:
                        pass
                    
                    cmd = [
                        "open", "-n", "-a", "Google Chrome", "--args",
                        f"--user-data-dir={profile_dir}",
                        "--password-store=basic",
                        "--use-mock-keychain",
                        "--disable-blink-features=AutomationControlled",
                        "https://www.tiktok.com/login"
                    ]
                    try:
                        subprocess.Popen(cmd)
                        log_message = f"Opened Google Chrome manually for profile {profile}."
                    except Exception as e:
                        log_message = f"Failed to open Google Chrome: {e}"
                
                else:
                    self.send_response(400)
                    self.end_headers()
                    self.wfile.write(json.dumps({'error': 'Invalid action'}).encode('utf-8'))
                    return
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'success', 'log': log_message}).encode('utf-8'))
                
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode('utf-8'))

if __name__ == "__main__":
    if not os.path.exists(DIRECTORY):
        os.makedirs(DIRECTORY)
    os.chdir(DIRECTORY)
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("", PORT), SecondBrainHandler) as httpd:
        print(f"Jarvis Second Brain Server running on port {PORT}")
        httpd.serve_forever()
