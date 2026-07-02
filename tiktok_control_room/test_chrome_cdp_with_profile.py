import os
import time
import subprocess
import urllib.request
import json
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
profile_dir = os.path.join(current_dir, "profiles", "chrome_debug_profile")
os.makedirs(profile_dir, exist_ok=True)

def is_chrome_debugging_ready():
    try:
        with urllib.request.urlopen("http://localhost:9222/json/version", timeout=2) as response:
            data = json.loads(response.read().decode())
            print("Connected to running Chrome debugging port!")
            return True
    except Exception:
        return False

def launch_chrome_with_cdp():
    if is_chrome_debugging_ready():
        return
    
    print("Launching user's Google Chrome with remote debugging port 9222 and debug profile...")
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    # Close any running Chrome instances
    print("Closing any running Google Chrome instances...")
    subprocess.run(["killall", "Google Chrome"], capture_output=True)
    time.sleep(2)
    
    # Start Chrome with remote debugging port and user-data-dir
    subprocess.Popen([
        chrome_path,
        "--remote-debugging-port=9222",
        f"--user-data-dir={profile_dir}",
        "--restore-last-session"
    ])
    
    # Wait for Chrome to be ready
    for i in range(10):
        time.sleep(1)
        if is_chrome_debugging_ready():
            return
    print("Warning: Chrome debugging port not ready after 10 seconds.")

# Main test flow
launch_chrome_with_cdp()

with sync_playwright() as p:
    print("Connecting Playwright to Chrome over CDP...")
    try:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        print(f"Current page URL: {page.url}")
        
        # Navigate to TikTok upload page
        print("Navigating to TikTok upload page...")
        page.goto("https://www.tiktok.com/tiktokstudio/upload?lang=en", timeout=60000)
        
        # Keep browser open to allow manual login and uploader check
        print("Waiting 120 seconds to allow manual login/use...")
        for i in range(24):
            time.sleep(5)
            screenshot_path = os.path.join(current_dir, "uploads", "TikTokBot", f"chrome_cdp_status_{i}.jpg")
            page.screenshot(path=screenshot_path, type="jpeg", quality=60)
            print(f"Saved debug screenshot {i}: {page.url}")
            
    except Exception as e:
        print(f"CDP connection failed: {e}")
