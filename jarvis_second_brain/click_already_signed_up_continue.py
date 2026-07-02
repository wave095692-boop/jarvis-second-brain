import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

print("Clicking Continue on You've already signed up page...")
continue_btn = d(text="Continue")
if continue_btn.exists:
    continue_btn.click()
else:
    # Coordinate click near bottom
    d.click(540, 1800)

time.sleep(6) # Wait for page load or next screen

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_login_continue.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_login_continue.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements on new screen:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
