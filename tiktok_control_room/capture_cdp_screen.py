import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))

with sync_playwright() as p:
    try:
        browser = p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = context.pages[0] if context.pages else context.new_page()
        
        print(f"Current page URL: {page.url}")
        screenshot_path = os.path.join(current_dir, "uploads", "TikTokBot", "cdp_post_success.jpg")
        page.screenshot(path=screenshot_path, type="jpeg", quality=80)
        print(f"Saved CDP success screenshot to {screenshot_path}")
    except Exception as e:
        print(f"Error capturing screenshot: {e}")
