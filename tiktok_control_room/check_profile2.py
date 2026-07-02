import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')
w, h = d.window_size()

# Click Profile (bottom right)
print("Clicking profile...")
d.click(w * 0.9, h * 0.96)
time.sleep(3)

# Capture screen
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/profile2.png'])
subprocess.run(['adb', 'pull', '/sdcard/profile2.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

# Check elements
print("Current elements:")
for el in d(className="android.widget.TextView"):
    print(f"TextView: {el.get_text()}")
