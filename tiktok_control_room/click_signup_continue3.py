import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

print("Clicking Continue button...")
continue_btn = d(text="Continue")
if continue_btn.exists:
    continue_btn.click()
else:
    # Coordinates of Continue button center
    # Based on bounds: {'bottom': 1762, 'left': 84, 'right': 996, 'top': 1625}
    d.click(540, 1693)

time.sleep(6) # Wait for captcha to load

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_signup_continue3.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_signup_continue3.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing clickable elements:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
