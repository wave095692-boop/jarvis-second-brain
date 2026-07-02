import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

email = "jarvisboss_99h6p4pp@web-library.net"

print(f"Entering email: {email}...")
# Clear and set text of EditText field
edit_text = d(className="android.widget.EditText")
if edit_text.exists:
    edit_text.set_text(email)
else:
    # Fallback to coordinate tap and send_keys
    d.click(540, 632)
    time.sleep(1)
    d.send_keys(email)

time.sleep(2)

print("Clicking Continue button...")
continue_btn = d(text="Continue")
if continue_btn.exists:
    continue_btn.click()
else:
    # Fallback to coordinates
    w, h = d.window_size()
    # Click near bottom
    d.click(w / 2, h * 0.88)

time.sleep(6) # Wait for page load or captcha

# Capture screen
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_email_continue2.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_email_continue2.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements on next screen:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
