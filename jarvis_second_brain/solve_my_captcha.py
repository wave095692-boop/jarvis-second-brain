import uiautomator2 as u2
import time
import random
import subprocess

def bezier_drag(device, sx, sy, ex, ey, steps=35, duration=1.2):
    # Control point for quadratic bezier to simulate curved hand movement
    control_x = (sx + ex) / 2 + random.randint(-10, 10)
    control_y = sy + random.randint(-8, 8)
    
    points = []
    for i in range(steps + 1):
        t = i / steps
        x = (1-t)**2 * sx + 2*(1-t)*t * control_x + t**2 * ex
        y = (1-t)**2 * sy + 2*(1-t)*t * control_y + t**2 * ey
        if i > 0 and i < steps:
            x += random.uniform(-1, 1)
            y += random.uniform(-1, 1)
        points.append((int(x), int(y)))
        
    device.swipe_points(points, duration=duration)

d = u2.connect('emulator-5554')

sx, sy = 245, 1177
dx = 325
ex, ey = sx + dx, sy

print(f"Dragging from ({sx}, {sy}) to ({ex}, {ey}) with bezier curve...")
bezier_drag(d, sx, sy, ex, ey, duration=1.3)
time.sleep(5)

# Take screenshot to verify success
subprocess.run(['adb', 'exec-out', 'screencap', '-p'], stdout=open('/Users/apple/.gemini/antigravity-ide/scratch/emulator_screen.png', 'wb'))
print("Screenshot taken after drag.")
