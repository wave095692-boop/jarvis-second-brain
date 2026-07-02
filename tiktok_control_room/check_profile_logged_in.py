import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(current_dir, "profiles", "profile_1")

with sync_playwright() as p:
    print("Launching Chromium Chrome channel with profile_1...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,
        channel="chrome",
        viewport={"width": 1280, "height": 1000}
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    # Overriding navigator.webdriver
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    profile_url = "https://www.tiktok.com/@wavekosin"
    print(f"Navigating to profile: {profile_url}...")
    try:
        page.goto(profile_url, timeout=60000)
        time.sleep(10)
        
        # Save screenshot
        preview_path = os.path.join(current_dir, "uploads", "TikTokBot", "profile_check_logged_in.jpg")
        os.makedirs(os.path.dirname(preview_path), exist_ok=True)
        page.screenshot(path=preview_path, type="jpeg", quality=60)
        print(f"Saved logged-in profile check screenshot to {preview_path}")
        
        # Find all video links
        videos = page.locator("a[href*='/video/']")
        count = videos.count()
        print(f"Total video elements found: {count}")
        for i in range(min(10, count)):
            href = videos.nth(i).get_attribute("href")
            print(f"Video #{i}: {href}")
    except Exception as e:
        print(f"Error checking profile: {e}")
    finally:
        context.close()
