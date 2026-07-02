import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(current_dir, "profiles", "profile_1")

with sync_playwright() as p:
    print("Launching Chromium Chrome channel...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,
        channel="chrome",
        viewport={"width": 1280, "height": 1000}
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    profile_url = "https://www.tiktok.com/@wavekosin"
    print(f"Navigating to profile: {profile_url}...")
    page.goto(profile_url, timeout=60000)
    time.sleep(8)
    
    # Save screenshot of profile page to verify if the video is visible
    preview_path = os.path.join(current_dir, "uploads", "TikTokBot", "profile_check.jpg")
    page.screenshot(path=preview_path, type="jpeg", quality=60)
    print(f"Saved profile check screenshot to {preview_path}")
    
    # Find all video links
    videos = page.locator("a[href*='/video/']")
    count = videos.count()
    print(f"Total video elements found: {count}")
    for i in range(min(5, count)):
        href = videos.nth(i).get_attribute("href")
        print(f"Video #{i}: {href}")
        
    context.close()
