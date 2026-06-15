import subprocess

print("LSOF PORT 8500:")
res = subprocess.run(["lsof", "-i", ":8500"], capture_output=True, text=True)
print(res.stdout)

print("PS AUX LOCALTUNNEL:")
res2 = subprocess.run(["ps", "aux"], capture_output=True, text=True)
for line in res2.stdout.splitlines():
    if "localtunnel" in line:
        print(line)

print("CURL LOCALTUNNEL.ME:")
import urllib.request
try:
    with urllib.request.urlopen("https://localtunnel.me", timeout=3) as res:
        print("STATUS:", res.status)
        print("READ FIRST 100 BYTES:", res.read(100))
except Exception as e:
    print("CONNECTION ERROR TO LOCALTUNNEL.ME:", e)
