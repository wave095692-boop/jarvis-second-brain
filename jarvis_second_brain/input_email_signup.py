import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

email = "jarvisboss_99h6p4pp@web-library.net"

print(f"Entering email: {email}...")
# Click the Email address input field
d.click(540, 632)
time.sleep(1)

# Set the text
d.send_keys(email)
time.sleep(2)

print("Clicking Continue button...")
# Click Continue
d.click(540, 846)
time.sleep(6) # Wait for page load or captcha

# Capture screen
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_email_continue.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_email_continue.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements on next screen:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
