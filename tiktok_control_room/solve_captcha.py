import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

# Drag coordinates: from x=245, y=1177 to x=475, y=1177
print("Dragging puzzle piece...")
d.drag(245, 1177, 475, 1177, duration=0.8)
time.sleep(4)

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_captcha.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_captcha.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements after captcha:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
