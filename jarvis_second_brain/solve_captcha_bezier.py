import uiautomator2 as u2
import time
import random
import subprocess

def bezier_drag(device, sx, sy, ex, ey, steps=30, duration=0.8):
    """Generates a curved path with slight random noise to simulate human drag."""
    # Control point for quadratic bezier
    control_x = (sx + ex) / 2 + random.randint(-20, 20)
    control_y = sy + random.randint(-15, 15)
    
    points = []
    for i in range(steps + 1):
        t = i / steps
        # Bezier interpolation
        x = (1-t)**2 * sx + 2*(1-t)*t * control_x + t**2 * ex
        y = (1-t)**2 * sy + 2*(1-t)*t * control_y + t**2 * ey
        # Add tiny random noise to coordinates
        if i > 0 and i < steps:
            x += random.uniform(-1.5, 1.5)
            y += random.uniform(-1.5, 1.5)
        points.append((int(x), int(y)))
        
    device.swipe_points(points, duration=duration)

d = u2.connect('emulator-5554')

# Drag from x=245, y=1177 to x=573, y=1177
sx, sy = 245, 1177
ex, ey = 573, 1177

print(f"Performing human-like bezier drag from ({sx}, {sy}) to ({ex}, {ey})...")
bezier_drag(d, sx, sy, ex, ey, duration=1.0)
time.sleep(4)

# Take screenshot
subprocess.run(['adb', 'shell', 'screencap', '-p', '/sdcard/after_captcha_bezier.png'])
subprocess.run(['adb', 'pull', '/sdcard/after_captcha_bezier.png', '/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png'])

print("Listing all clickable elements after captcha:")
for i, el in enumerate(d(clickable=True)):
    try:
        print(f"{i}: Text: '{el.get_text()}' | Bounds: {el.info.get('bounds')} | ID: {el.info.get('resourceName')}")
    except Exception as e:
        print(f"{i}: Error: {e}")
