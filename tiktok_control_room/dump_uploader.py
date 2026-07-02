import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(current_dir, "profiles", "profile_1")

with sync_playwright() as p:
    print("Launching Chromium browser...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,
        channel="chrome",
        viewport={"width": 1280, "height": 800}
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.goto("https://www.tiktok.com/upload?lang=en")
    print("Navigated to upload page, sleeping 10s for full load...")
    time.sleep(10)
    
    print(f"Main page URL: {page.url}")
    print(f"Total frames: {len(page.frames)}")
    
    for idx, frame in enumerate(page.frames):
        print(f"Frame #{idx}: Name: '{frame.name}', URL: '{frame.url}'")
        try:
            inputs = frame.locator('input').count()
            file_inputs = frame.locator('input[type="file"]').count()
            print(f"  -> Inputs count: {inputs}, File inputs count: {file_inputs}")
            if file_inputs > 0:
                print("  -> FOUND FILE INPUT IN THIS FRAME!")
        except Exception as e:
            print(f"  -> Error: {e}")
            
    context.close()
