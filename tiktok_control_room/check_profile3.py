import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')
w, h = d.window_size()
print(f"Window size: {w}x{h}")

# Target coordinates for Profile: x = 970, y = 1720 (approx)
# Let's use proportional coordinates: x = w * 0.9, y = h * 0.9
target_x = int(w * 0.9)
target_y = int(h * 0.9)
print(f"Tapping Profile at coordinates: {target_x}, {target_y}")
d.click(target_x, target_y)
time.sleep(4)

# Capture screen
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/profile3.png'])
subprocess.run(['adb', 'pull', '/sdcard/profile3.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])
print("Completed clicking profile")
