import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

# Drag using native uiautomator2 drag which holds down the pointer first
sx, sy = 245, 1177
ex, ey = 575, 1177

print(f"Performing native drag from ({sx}, {sy}) to ({ex}, {ey})...")
d.drag(sx, sy, ex, ey, duration=1.5)
time.sleep(4)

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_captcha_drag.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_captcha_drag.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements after drag:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
