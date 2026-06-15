import subprocess
import time
import os

print("Starting YouTube SSH tunnel via localhost.run...")
# Kill any existing ssh tunnel for port 8000
os.system("pgrep -f '80:localhost:8000' | xargs kill -9 2>/dev/null")

log_path = "/Users/apple/.gemini/antigravity-ide/scratch/youtube_tunnel_output.log"
with open(log_path, "w") as f:
    proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8000", "nokey@localhost.run"],
        stdout=f,
        stderr=f,
        text=True
    )
    print(f"YouTube SSH process started with PID: {proc.pid}")
    time.sleep(5)

if os.path.exists(log_path):
    with open(log_path, "r") as f:
        print("LOG OUTPUT:")
        print(f.read())
else:
    print("LOG FILE NOT CREATED")
