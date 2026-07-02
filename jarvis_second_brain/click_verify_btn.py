import uiautomator2 as u2
import time
import subprocess

d = u2.connect('emulator-5554')

print("Looking for Verify in the app button...")
btn = d(text="Verify in the app")
if btn.exists:
    print("Found button, clicking...")
    btn.click()
else:
    # Try finding any button or tapping coordinates (approx center of button)
    # The button is in the lower-middle of the screen
    w, h = d.window_size()
    print("Button not found by text. Tapping center-lower (x=500, y=730 in dp/px)...")
    # Coordinates of red button: x is around 540, y is around 730 on screen. Wait, y in pixels:
    # From screenshot, the red button is at y=1400 (which is around 73% of height)
    d.click(w / 2, h * 0.73)

time.sleep(5)

# Take screenshot of whatever app opened
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/verify_app_res.png'])
subprocess.run(['adb', 'pull', '/sdcard/verify_app_res.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])
print("Done")
