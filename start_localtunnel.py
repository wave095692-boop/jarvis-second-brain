import subprocess
import time
import os

print("Starting localtunnel...")
# Kill any existing localtunnel on port 8500
os.system("pgrep -f 'localtunnel.*8500' | xargs kill -9 2>/dev/null")

log_path = "/Users/apple/.gemini/antigravity-ide/scratch/localtunnel_output.log"
with open(log_path, "w") as f:
    proc = subprocess.Popen(
        ["npx", "-y", "localtunnel", "--port", "8500"],
        stdout=f,
        stderr=f,
        text=True
    )
    print(f"Localtunnel started with PID: {proc.pid}")
    
    for i in range(10):
        time.sleep(1)
        poll = proc.poll()
        if poll is not None:
            print(f"Process terminated after {i+1} seconds with exit code {poll}")
            break
    else:
        print("Process is still running after 10 seconds.")

if os.path.exists(log_path):
    with open(log_path, "r") as f:
        print("LOG OUTPUT:")
        print(f.read())
else:
    print("LOG FILE NOT CREATED")
