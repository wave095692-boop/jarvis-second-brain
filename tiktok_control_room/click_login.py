import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

# Click the "Use phone / email / username" button (element index 3 in clickable list)
print("Clicking Use phone / email / username...")
d(clickable=True)[3].click()
time.sleep(3)

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/login_fields.png'])
subprocess.run(['adb', 'pull', '/sdcard/login_fields.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements on new screen:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
