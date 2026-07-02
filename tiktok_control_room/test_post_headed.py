import os
import time
from playwright.sync_api import sync_playwright

current_dir = os.path.dirname(os.path.abspath(__file__))
user_data_dir = os.path.join(current_dir, "profiles", "profile_1")
upload_path = os.path.abspath(os.path.join(current_dir, "uploads", "TikTokUpload", "DownTown6.mp4"))

with sync_playwright() as p:
    print("Launching Chromium Chrome channel (Headed)...")
    context = p.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        headless=False,  # Headed mode!
        channel="chrome",
        viewport={"width": 1280, "height": 1000},
        args=[
            "--disable-blink-features=AutomationControlled"
        ]
    )
    page = context.pages[0] if context.pages else context.new_page()
    page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("Navigating to TikTok upload page...")
    page.goto("https://www.tiktok.com/upload?lang=en", timeout=60000)
    time.sleep(8)
    
    # Save init screenshot
    page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "live_step1_init.jpg"))
    print("Saved step 1 screenshot.")
    
    # Clean popups
    for attempt in range(5):
        discard_btn = None
        for target in [page] + list(page.frames):
            try:
                btn = target.locator('button:has-text("Discard"), button:has-text("ละทิ้ง")').first
                if btn.is_visible() and btn.is_enabled():
                    discard_btn = btn
                    break
            except Exception:
                pass
        if discard_btn:
            print("Clicking discard on popup...")
            discard_btn.click(force=True)
            time.sleep(3)
        else:
            break
            
    page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "live_step2_clean.jpg"))
    print("Saved step 2 screenshot.")
    
    # Locate file input (attached, not necessarily visible)
    file_input = None
    try:
        page.wait_for_selector('input[type="file"]', state="attached", timeout=10000)
        file_input = page.locator('input[type="file"]').first
        print("Found file input attached to page.")
    except Exception as e:
        print(f"Failed to find file input: {e}")
        
    if file_input:
        print("Selecting video file...")
        file_input.set_input_files(upload_path)
        time.sleep(5)
        
        # Clean overlays
        page.evaluate("document.querySelectorAll('#react-joyride-portal, .react-joyride__overlay, .react-joyride__spotlight, [class*=\"joyride\"]').forEach(el => el.remove())")
        
        # Write caption
        print("Writing caption...")
        try:
            caption_field = page.locator('div[contenteditable="true"]').first
            caption_field.click()
            time.sleep(1)
            page.keyboard.press("Meta+A")
            page.keyboard.press("Control+A")
            page.keyboard.press("Backspace")
            time.sleep(1)
            page.keyboard.type("Test Live Upload #rudedog #downtown")
            time.sleep(2)
        except Exception as e:
            print(f"Failed to write caption: {e}")
            
        page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "live_step3_before_sleep.jpg"))
        
        # Wait 45 seconds for upload
        print("Waiting 45 seconds for upload...")
        time.sleep(45)
        
        page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "live_step4_after_sleep.jpg"))
        
        # Locate post button
        post_selectors = [
            'button[data-e2e="post_video_button"]',
            'button:has-text("Post")',
            'button:has-text("Share")'
        ]
        post_btn = None
        for sel in post_selectors:
            btn = page.locator(sel).first
            if btn.is_visible() and btn.is_enabled():
                if btn.get_attribute("data-tt") != "Sidebar_Sidebar_Clickable":
                    post_btn = btn
                    break
                    
        if post_btn:
            print("Clicking Post button...")
            post_btn.click()
            time.sleep(2)
            
            # Take screenshots every 5 seconds for 60 seconds to monitor post status
            print("Monitoring post transition...")
            for i in range(12):
                time.sleep(5)
                screenshot_path = os.path.join(current_dir, "uploads", "TikTokBot", f"live_post_monitor_{i}.jpg")
                page.screenshot(path=screenshot_path)
                print(f"Saved monitor screenshot {i}: URL is {page.url}")
        else:
            print("Post button not found or not enabled.")
    else:
        print("File input not found.")
        
    print("Keeping browser open for 60 seconds to inspect...")
    time.sleep(60)
    context.close()
