import time
import random
import subprocess
import sys

# Import uiautomator2. If not installed, we provide a warning and explain how to install it.
try:
    import uiautomator2 as u2
except ImportError:
    print("----------------------------------------------------------------")
    print("❌ Error: 'uiautomator2' library is not installed.")
    print("Please install it by running the following command in Terminal:")
    print("👉 pip install uiautomator2 pillow")
    print("----------------------------------------------------------------")
    sys.exit(1)

def check_adb_devices():
    """Checks if there are any active emulators or devices connected via ADB."""
    print("🔍 กำลังตรวจสอบอุปกรณ์เชื่อมต่อผ่าน ADB (Checking devices)...")
    try:
        res = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
        lines = res.stdout.strip().split('\n')[1:]
        devices = []
        for line in lines:
            if not line.strip():
                continue
            parts = line.split()
            if len(parts) >= 2 and parts[1] == 'device':
                devices.append(parts[0])
        return devices
    except FileNotFoundError:
        print("❌ Error: ADB command not found. Please install Android Platform Tools.")
        return []

def bezier_swipe(device, sx, sy, ex, ey, steps=25):
    """
    Simulates a human-like swipe gesture using a curve (Bezier curve)
    instead of a perfectly straight linear line to bypass bot detection.
    """
    print(f"☝️ เลื่อนหน้าจอจำลองนิ้วมือจริง (Human-like swipe from {sx},{sy} to {ex},{ey})...")
    # Generate points along a Bezier curve
    control_x = sx + random.randint(-60, 60)
    control_y = (sy + ey) / 2 + random.randint(-40, 40)
    
    points = []
    for i in range(steps + 1):
        t = i / steps
        # Quadratic Bezier formula
        x = (1-t)**2 * sx + 2*(1-t)*t * control_x + t**2 * ex
        y = (1-t)**2 * sy + 2*(1-t)*t * control_y + t**2 * ey
        points.append((int(x), int(y)))
    
    # Perform swipe using the custom coordinates path
    device.swipe_points(points, duration=0.18)

def main():
    devices = check_adb_devices()
    if not devices:
        print("❌ ไม่พบเครื่องจำลอง Android Emulator เชื่อมต่ออยู่!")
        print("กรุณาเปิด Emulator ใน Android Studio (เช่น AVD) หรือเช็คคำสั่ง 'adb devices' ก่อนครับ")
        return
        
    device_ip = devices[0]
    print(f"✅ เชื่อมต่ออุปกรณ์สำเร็จ: {device_ip}")
    
    # Initialize connection to the emulator device
    d = u2.connect(device_ip)
    
    # Check if device screen is on, if not wake it up
    # info is a dictionary in newer u2 versions
    try:
        info = d.info
        screen_on = info.get('screenOn', True)
    except Exception:
        screen_on = True
        
    if not screen_on:
        print("🔓 หน้าจอดับอยู่ กำลังสั่งเปิดและปลดล็อคหน้าจอ...")
        d.screen_on()
        d.swipe(200, 800, 200, 200, 0.3) # Swipe up to unlock
        time.sleep(1)

    # TikTok App Package names (Global: com.ss.android.ugc.trill, Asia/Thai: com.zhiliaoapp.musically)
    tiktok_package = "com.ss.android.ugc.trill"
    
    apps = d.app_list()
    if "com.zhiliaoapp.musically" in apps:
        tiktok_package = "com.zhiliaoapp.musically"
    
    print(f"🎬 กำลังเปิดแอป TikTok ({tiktok_package})...")
    d.app_start(tiktok_package)
    time.sleep(6) # Wait for splash screen and ads

    print("🚀 เริ่มระบบบอทเลื่อนหน้าฟีดอัตโนมัติ (Feed Auto-Scrolling)...")
    
    # Screen size for calculations
    width, height = d.window_size()
    
    try:
        for loop in range(1, 11): # Loop 10 times for testing
            print(f"\n--- รอบที่ {loop}/10 ---")
            
            # Watch video for a random duration (between 6 to 18 seconds) to mimic human retention
            watch_time = random.uniform(6.0, 18.0)
            print(f"👀 กำลังรับชมคลิปวิดีโอปัจจุบันเป็นเวลา {watch_time:.2f} วินาที...")
            time.sleep(watch_time)
            
            # Random action: 15% chance to like the video
            if random.random() < 0.15:
                print("💖 สุ่มกดหัวใจถูกใจวิดีโอ (Double Tap Like)...")
                d.double_click(width / 2, height / 2)
                time.sleep(1)
                
            # Random swipe coordinates to simulate organic finger scroll
            start_x = width / 2 + random.randint(-40, 40)
            start_y = height * 0.8 + random.randint(-20, 20)
            end_x = width / 2 + random.randint(-40, 40)
            end_y = height * 0.2 + random.randint(-20, 20)
            
            bezier_swipe(d, start_x, start_y, end_x, end_y)
            time.sleep(random.uniform(1.0, 3.0)) # Wait before doing anything else
            
        print("\n🎉 บอทรันครบจำนวนรอบที่ตั้งค่าไว้เรียบร้อยแล้ว!")
        
    except KeyboardInterrupt:
        print("\n🛑 หยุดการทำงานของบอทโดยผู้ใช้งาน")

if __name__ == "__main__":
    main()
