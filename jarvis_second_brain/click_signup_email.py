import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

print("Clicking Email tab on Sign up page...")
d(clickable=True)[3].click()
time.sleep(2)

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/signup_email.png'])
subprocess.run(['adb', 'pull', '/sdcard/signup_email.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements on Email sign up page:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
