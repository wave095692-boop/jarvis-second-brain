import subprocess
try:
    res = subprocess.run(["npx", "-y", "localtunnel", "--version"], capture_output=True, text=True, timeout=5)
    print("STDOUT:", res.stdout)
    print("STDERR:", res.stderr)
    print("RETURN CODE:", res.returncode)
except Exception as e:
    print("ERROR:", e)
