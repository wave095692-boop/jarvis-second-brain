import uiautomator2 as u2
import time

d = u2.connect('emulator-5554')
print(f"Window size: {d.window_size()}")

# Tap profile
print("Tapping Profile tab...")
# Try using text or description or coordinates
profile_btn = d(text="Profile")
if profile_btn.exists:
    profile_btn.click()
else:
    # Coordinates of Profile tab (bottom right)
    w, h = d.window_size()
    d.click(w * 0.9, h * 0.96)

time.sleep(3)
# Take screenshot
import subprocess
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/profile.png'])
subprocess.run(['adb', 'pull', '/sdcard/profile.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])
print("Done")
