import subprocess
import time
import os

print("Starting SSH tunnel via localhost.run...")
# Kill any existing ssh tunnel to localhost.run
os.system("pgrep -f 'nokey@localhost.run' | xargs kill -9 2>/dev/null")

log_path = "/Users/apple/.gemini/antigravity-ide/scratch/ssh_tunnel_output.log"
with open(log_path, "w") as f:
    proc = subprocess.Popen(
        ["ssh", "-o", "StrictHostKeyChecking=no", "-R", "80:localhost:8500", "nokey@localhost.run"],
        stdout=f,
        stderr=f,
        text=True
    )
    print(f"SSH process started with PID: {proc.pid}")
    time.sleep(5)

if os.path.exists(log_path):
    with open(log_path, "r") as f:
        print("LOG OUTPUT:")
        print(f.read())
else:
    print("LOG FILE NOT CREATED")
