import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(current_dir, "profiles", "profile_1")
upload_path = os.path.abspath(os.path.join(current_dir, "uploads", "TikTokUpload", "DownTown6.mp4"))

with sync_playwright() as p:
    print("Launching Chromium Chrome channel...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=True,
        channel="chrome",
        viewport={"width": 1280, "height": 800}
    )
    page = context.pages[0] if context.pages else context.new_page()
    
    print("Navigating to TikTok upload page...")
    page.goto("https://www.tiktok.com/upload?lang=en", timeout=60000)
    time.sleep(5)
    
    page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "test_step1_init.jpg"))
    print("Saved step 1 screenshot.")
    
    # Handle "Continue editing / Discard" popup if present
    discard_btn = page.locator('button:has-text("Discard"), button:has-text("ละทิ้ง")').first
    if discard_btn.is_visible():
        print("Found Discard button, clicking it...")
        discard_btn.click()
        time.sleep(3)
        page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "test_step2_after_discard.jpg"))
        print("Saved step 2 screenshot (after discard).")
    else:
        print("Discard button not visible.")
        
    # Locate file input
    file_input = None
    target_page = page
    try:
        page.wait_for_selector('input[type="file"]', state="attached", timeout=5000)
        file_input = page.locator('input[type="file"]').first
        print("Found file input on main page.")
    except Exception:
        pass

    if not file_input:
        print("Searching in frames...")
        for frame in page.frames:
            if "content/publish" in frame.url or "publish" in frame.url:
                print(f"Targeting publish frame: {frame.url}")
                try:
                    frame.wait_for_selector('input[type="file"]', state="attached", timeout=5000)
                    file_input = frame.locator('input[type="file"]').first
                    target_page = frame
                    print("Found file input inside frame!")
                    break
                except Exception as e:
                    print(f"Frame error: {e}")
                    
    if file_input:
        print("Uploading file...")
        file_input.set_input_files(upload_path)
        time.sleep(5)
        page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "test_step3_after_upload_start.jpg"))
        print("Saved step 3 screenshot.")
        
        # Let's wait and print what buttons are visible every 5 seconds
        for i in range(12):  # Wait up to 60 seconds
            time.sleep(5)
            page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", f"test_step4_wait_{i}.jpg"))
            print(f"--- Wait {i*5}s: Checking buttons ---")
            
            # Print all buttons on main page
            buttons = page.locator("button")
            btn_count = buttons.count()
            print(f"Main page buttons count: {btn_count}")
            for idx in range(btn_count):
                btn = buttons.nth(idx)
                if btn.is_visible():
                    print(f"  [Main Page] Button #{idx}: text='{btn.inner_text().strip()}', e2e='{btn.get_attribute('data-e2e') or ''}', enabled={btn.is_enabled()}")
                    
            # Print all buttons inside frames
            for f_idx, frame in enumerate(page.frames):
                if frame != page:
                    try:
                        f_buttons = frame.locator("button")
                        f_btn_count = f_buttons.count()
                        if f_btn_count > 0:
                            for idx in range(f_btn_count):
                                btn = f_buttons.nth(idx)
                                if btn.is_visible():
                                    print(f"  [Frame #{f_idx} '{frame.name or frame.url}'] Button #{idx}: text='{btn.inner_text().strip()}', e2e='{btn.get_attribute('data-e2e') or ''}', enabled={btn.is_enabled()}")
                    except Exception as fe:
                        pass
    else:
        print("File input not found at all.")
        
    context.close()
