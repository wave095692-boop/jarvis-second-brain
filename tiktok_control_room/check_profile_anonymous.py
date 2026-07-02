import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    print("Launching Chromium (anonymous)...")
    # Launch browser without user_data_dir to avoid lock issues
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 1000})
    
    profile_url = "https://www.tiktok.com/@wavekosin"
    print(f"Navigating to profile anonymously: {profile_url}...")
    try:
        page.goto(profile_url, timeout=60000)
        time.sleep(8)
        
        # Save screenshot
        preview_path = os.path.join(current_dir, "uploads", "TikTokBot", "profile_check_anonymous.jpg")
        os.makedirs(os.path.dirname(preview_path), exist_ok=True)
        page.screenshot(path=preview_path, type="jpeg", quality=60)
        print(f"Saved anonymous profile check screenshot to {preview_path}")
        
        # Find all video links
        videos = page.locator("a[href*='/video/']")
        count = videos.count()
        print(f"Total video elements found anonymously: {count}")
        for i in range(min(5, count)):
            href = videos.nth(i).get_attribute("href")
            print(f"Video #{i}: {href}")
    except Exception as e:
        print(f"Error checking profile: {e}")
    finally:
        browser.close()
