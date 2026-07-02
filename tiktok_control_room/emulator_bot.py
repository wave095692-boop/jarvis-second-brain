import time
import random
import subprocess
import sys
import shutil
import argparse

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

def get_adb_path():
    """Returns the absolute path to adb if it is not in default PATH."""
    if shutil.which('adb'):
        return 'adb'
    elif os.path.exists('/opt/homebrew/bin/adb'):
        return '/opt/homebrew/bin/adb'
    elif os.path.exists('/usr/local/bin/adb'):
        return '/usr/local/bin/adb'
    return 'adb'

def check_adb_devices():
    """Checks if there are any active emulators or devices connected via ADB."""
    print("🔍 กำลังตรวจสอบอุปกรณ์เชื่อมต่อผ่าน ADB (Checking devices)...")
    adb_cmd = get_adb_path()
    try:
        res = subprocess.run([adb_cmd, 'devices'], capture_output=True, text=True)
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
    print(f"☝️ เลื่อนหน้าจอจำลองนิ้วมือจริง (Human-like swipe from {int(sx)},{int(sy)} to {int(ex)},{int(ey)})...")
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

def simulate_comment(device, width, height):
    """Simulates tapping the comment button, typing a random positive comment, and closing it."""
    comments = [
        "สุดยอดเลยครับบอส",
        "ดีงามมากครับชอบ ๆ",
        "เท่สุด ๆ ไปเลย",
        "คอนเทนต์เจ๋งมากครับ",
        "สุดจัดเลยครับ",
        "Wow! Beautiful",
        "Great content!",
        "Amazing video 👍",
        "ชอบมากครับทำต่อเรื่อยๆ นะครับ"
    ]
    selected_comment = random.choice(comments)
    print(f"💬 กำลังจำลองการพิมพ์ความคิดเห็น: \"{selected_comment}\"")
    
    # 1. Tap comment icon (typically on the right, around x=90%, y=60% of screen height)
    cx, cy = width * 0.9, height * 0.60
    device.click(cx, cy)
    time.sleep(2)
    
    # 2. Tap the input comment field (typically near the bottom)
    # uiautomator2 can find the input field by class name or resource-id,
    # but coordinates click on the bottom input bar is a reliable fallback
    device.click(width * 0.3, height * 0.95)
    time.sleep(1)
    
    # 3. Send text keys
    try:
        device.send_keys(selected_comment)
        time.sleep(1.5)
        
        # 4. Tap the send button (typically on the right of the input bar)
        device.click(width * 0.9, height * 0.95)
        print("✅ พิมพ์และส่งความคิดเห็นเรียบร้อย")
        time.sleep(2)
    except Exception as ex:
        print(f"⚠️ ไม่สามารถป้อนข้อความได้: {ex}")
        
    # 5. Tap outside / close comment drawer (tap near the top-middle)
    device.click(width / 2, height * 0.2)
    time.sleep(1)

def main():
    import os
    parser = argparse.ArgumentParser(description="TikTok Emulator Farming Bot by Jarvis")
    parser.add_argument("--device", type=str, default="", help="ADB serial key of the target device")
    parser.add_argument("--loops", type=int, default=10, help="Number of scrolls/rounds")
    parser.add_argument("--like-prob", type=float, default=0.15, help="Probability of liking a video (0.0 - 1.0)")
    parser.add_argument("--comment-prob", type=float, default=0.05, help="Probability of commenting on a video (0.0 - 1.0)")
    parser.add_argument("--query", type=str, default="", help="Keyword to search for first")
    
    args = parser.parse_args()
    
    devices = check_adb_devices()
    if not devices:
        print("❌ ไม่พบเครื่องจำลอง Android Emulator เชื่อมต่ออยู่!")
        print("กรุณาเปิด Emulator ใน Android Studio (AVD) หรือเปิด ADB ไร้สายก่อนครับ")
        sys.exit(1)
        
    target_device = args.device
    if not target_device:
        target_device = devices[0]
        print(f"⚠️ ไม่ได้ระบุ --device, สุ่มเลือกเครื่องแรกในระบบ: {target_device}")
    elif target_device not in devices:
        print(f"❌ ไม่พบอุปกรณ์รหัส {target_device} ในระบบ! รายการที่เชื่อมต่อ: {devices}")
        sys.exit(1)
        
    print(f"🤖 BOT STARTING: Target Device: {target_device}")
    print(f"⚙️ Config -> Loops: {args.loops} | Like Prob: {args.like_prob} | Comment Prob: {args.comment_prob}")
    if args.query:
        print(f"🔎 ค้นหาคีย์เวิร์ดเป้าหมาย: \"{args.query}\"")
        
    # Initialize connection to the emulator device
    try:
        d = u2.connect(target_device)
        # Verify connection by getting window size
        width, height = d.window_size()
        print(f"✅ เชื่อมต่อสำเร็จ! ขนาดหน้าจออุปกรณ์: {width}x{height}")
    except Exception as e:
        print(f"❌ ล้มเหลวในการเชื่อมต่อกับ uiautomator2: {e}")
        sys.exit(1)
    
    # Check if device screen is on, if not wake it up
    try:
        info = d.info
        screen_on = info.get('screenOn', True)
    except Exception:
        screen_on = True
        
    if not screen_on:
        print("🔓 หน้าจอดับอยู่ กำลังสั่งเปิดและปลดล็อคหน้าจอ...")
        d.screen_on()
        d.swipe(200, 800, 200, 200, 0.3) # Swipe up to unlock
        time.sleep(1.5)

    # TikTok App Package names (Global: com.ss.android.ugc.trill, Asia/Thai: com.zhiliaoapp.musically)
    tiktok_package = "com.ss.android.ugc.trill"
    apps = d.app_list()
    if "com.zhiliaoapp.musically" in apps:
        tiktok_package = "com.zhiliaoapp.musically"
    
    print(f"🎬 กำลังเริ่มต้นเปิดแอป TikTok ({tiktok_package})...")
    d.app_start(tiktok_package)
    time.sleep(6) # Wait for splash screen and ads
    
    # If search query is specified, attempt search workflow
    if args.query:
        print(f"🔎 เริ่มกระบวนการค้นหาคำว่า \"{args.query}\"")
        try:
            # 1. Tap search icon (usually top right corner, roughly x=90%, y=6%)
            d.click(width * 0.9, height * 0.06)
            time.sleep(2)
            # 2. Input search query
            d.send_keys(args.query)
            time.sleep(1)
            # 3. Tap search button on IME / screen (top right of search bar or bottom right of keyboard)
            d.click(width * 0.9, height * 0.06)
            time.sleep(3)
            # 4. Tap on first video in search results (roughly middle-left)
            d.click(width * 0.25, height * 0.25)
            time.sleep(3)
            print("✅ เข้าสู่หน้ารับชมวิดีโอจากผลลัพธ์การค้นหาแล้ว")
        except Exception as se:
            print(f"⚠️ กระบวนการค้นหาขัดข้อง (ข้ามไปรันหน้าฟีดปกติ): {se}")

    print("🚀 เริ่มระบบบอทเลื่อนหน้าฟีดอัตโนมัติ (Feed Auto-Scrolling)...")
    
    try:
        for loop in range(1, args.loops + 1):
            print(f"\n--- รอบที่ {loop}/{args.loops} ---")
            
            # Watch video for a random duration (between 6 to 20 seconds) to mimic human retention
            watch_time = random.uniform(6.0, 20.0)
            print(f"👀 กำลังรับชมคลิปวิดีโอปัจจุบันเป็นเวลา {watch_time:.2f} วินาที...")
            time.sleep(watch_time)
            
            # Random Action 1: Like the video
            if random.random() < args.like_prob:
                print("💖 สุ่มกดหัวใจถูกใจวิดีโอ (Double Tap Like)...")
                d.double_click(width / 2, height / 2)
                time.sleep(1.5)
                
            # Random Action 2: Comment on the video
            if random.random() < args.comment_prob:
                try:
                    simulate_comment(d, width, height)
                except Exception as ce:
                    print(f"⚠️ การจำลองคอมเมนต์ไม่สำเร็จ: {ce}")
                    # Tap outside to close comment in case it got stuck
                    d.click(width / 2, height * 0.2)
                    time.sleep(1)
                
            # Random swipe coordinates to simulate organic finger scroll
            start_x = width / 2 + random.randint(-40, 40)
            start_y = height * 0.8 + random.randint(-20, 20)
            end_x = width / 2 + random.randint(-40, 40)
            end_y = height * 0.2 + random.randint(-20, 20)
            
            bezier_swipe(d, start_x, start_y, end_x, end_y)
            # Wait random delay after swiping (1.5 to 4 seconds)
            time.sleep(random.uniform(1.5, 4.0))
            
        print("\n🎉 บอทรันครบจำนวนรอบทั้งหมดเรียบร้อยแล้ว!")
        
    except KeyboardInterrupt:
        print("\n🛑 หยุดการทำงานของบอทโดยผู้ใช้งาน (KeyboardInterrupt)")
    except Exception as ex:
        print(f"\n❌ เกิดข้อผิดพลาดระหว่างรันบอท: {ex}")

if __name__ == "__main__":
    main()
