import time
import random
import sys
import os
import argparse
from playwright.sync_api import sync_playwright

# List of text-only comments
TEXT_COMMENTS = [
    "สุดยอดเลยครับบอส",
    "ดีงามมากครับชอบ ๆ",
    "เท่สุด ๆ ไปเลย",
    "คอนเทนต์เจ๋งมากครับ",
    "สุดจัดเลยครับ",
    "Wow! Beautiful",
    "Great content!",
    "Amazing video",
    "ชอบมากครับทำต่อเรื่อยๆ นะครับ"
]

# List of emoji-only comments
EMOJI_COMMENTS = [
    "👍", "❤️", "🔥", "🥰", "👏", "💯", "🙌", "🤩", "✨", "🎉",
    "👍👍", "🔥🔥🔥", "🥰❤️", "💯💯", "👏👏👏", "🤩✨", "💖💖", "😂🤣", "😎👍",
    "🙌🔥", "👍🥰", "💯🔥👍", "✨🤩✨", "🎉🥳", "❤️🔥🙌", "🥺😍", "😎🍿"
]

# List of mixed comments (text + emojis)
MIXED_COMMENTS = [
    "สุดยอดเลยครับบอส 👍🔥",
    "ดีงามมากครับชอบ ๆ 🥰",
    "เท่สุด ๆ ไปเลย 😎👍",
    "คอนเทนต์เจ๋งมากครับ 💯✨",
    "สุดจัดเลยครับ 🔥👏",
    "Wow! Beautiful 💖",
    "Great content! 🙌",
    "Amazing video 👍🤩",
    "ชอบมากครับทำต่อเรื่อยๆ นะครับ 🎉",
    "ชอบคอนเทนต์นี้จัง 🥰❤️",
    "ติดตามเลยครับบอส 💯🙌"
]

def human_mouse_move(page, end_x, end_y, steps=15):
    try:
        # Generate a random starting position for the cursor
        start_x = random.randint(100, 1000)
        start_y = random.randint(100, 700)
        
        # Calculate Bezier control points for a curved path
        control_x1 = start_x + (end_x - start_x) * random.uniform(0.1, 0.4)
        control_y1 = start_y + (end_y - start_y) * random.uniform(0.1, 0.8)
        control_x2 = start_x + (end_x - start_x) * random.uniform(0.6, 0.9)
        control_y2 = start_y + (end_y - start_y) * random.uniform(0.2, 0.9)
        
        for i in range(steps + 1):
            t = i / steps
            x = int((1-t)**3 * start_x + 3*(1-t)**2 * t * control_x1 + 3*(1-t) * t**2 * control_x2 + t**3 * end_x)
            y = int((1-t)**3 * start_y + 3*(1-t)**2 * t * control_y1 + 3*(1-t) * t**2 * control_y2 + t**3 * end_y)
            page.mouse.move(x, y)
            time.sleep(random.uniform(0.005, 0.015))
    except Exception as e:
        print(f"⚠️ Human mouse move warning: {e}")
        page.mouse.move(end_x, end_y)

def scroll_to_next_video(page):
    print("👇 Attempting to scroll to the next video...")
    try:
        # Blur any active elements to release keyboard focus (e.g. comment input boxes)
        page.evaluate("document.activeElement && document.activeElement.blur()")
        time.sleep(0.5)
        
        # Check if theater mode or video page (URL contains '/video/')
        if "/video/" in page.url:
            print("🎬 Theater/Player mode detected.")
            # Try to click the next video button
            next_button_selectors = [
                'button[data-e2e="arrow-right"]',
                '[data-e2e="arrow-right"]',
                'button[aria-label="Next video"]',
                'button[aria-label="วิดีโอถัดไป"]',
                '.arrow-right',
                'button:has(svg[class*="ArrowRight"])'
            ]
            clicked = False
            for selector in next_button_selectors:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible() and btn.is_enabled():
                        btn.click()
                        print(f"✅ Clicked next video button: {selector}")
                        clicked = True
                        break
                except Exception:
                    pass
            
            if not clicked:
                # Fallback to pressing ArrowDown keyboard key
                page.keyboard.press("ArrowDown")
                print("✅ Pressed ArrowDown key in theater mode.")
        else:
            print("🏠 Feed mode detected.")
            # Scroll down using mouse wheel with curved movement
            feed_x = random.randint(580, 700)
            feed_y = random.randint(350, 480)
            human_mouse_move(page, feed_x, feed_y)
            time.sleep(0.2)
            page.mouse.wheel(0, random.randint(700, 800)) # Scroll down by random pixels
            print("✅ Scrolled page down via mouse wheel.")
            
            # Also press ArrowDown as a backup
            time.sleep(0.5)
            page.keyboard.press("ArrowDown")
    except Exception as e:
        print(f"⚠️ Error during scrolling: {e}")

def save_preview(page, profile_name):
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        uploads_dir = os.path.join(current_dir, "uploads", "TikTokBot")
        if not os.path.exists(uploads_dir):
            os.makedirs(uploads_dir)
        preview_path = os.path.join(uploads_dir, f"web_farming_bot_{profile_name}_preview.jpg")
        page.screenshot(path=preview_path, type="jpeg", quality=40)
    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser(description="TikTok Web Farming Bot by Jarvis")
    parser.add_argument("--profile", type=str, default="profile_1", help="Name of the browser profile")
    parser.add_argument("--loops", type=int, default=10, help="Number of scrolls/videos to watch")
    parser.add_argument("--like-prob", type=float, default=0.15, help="Probability of liking (0.0 - 1.0)")
    parser.add_argument("--comment-prob", type=float, default=0.05, help="Probability of commenting (0.0 - 1.0)")
    parser.add_argument("--comment-style", type=str, default="mixed", choices=["text", "emoji", "mixed"], help="Style of comments to post")
    parser.add_argument("--custom-comments-file", type=str, default="", help="Path to file containing custom comments (one per line)")
    parser.add_argument("--follow-prob", type=float, default=0.0, help="Probability of following creators in feed (0.0 - 1.0)")
    parser.add_argument("--target-user", type=str, default="", help="TikTok username to search/follow at startup")
    parser.add_argument("--upload-video", type=str, default="", help="Path to local video file to upload")
    parser.add_argument("--upload-caption", type=str, default="", help="Caption for uploaded video")
    parser.add_argument("--query", type=str, default="", help="Search query keyword")
    parser.add_argument("--headed", type=str, default="true", help="Run browser in headed mode ('true' or 'false')")
    parser.add_argument("--login-mode", action="store_true", help="Wait for user to login manually first before farming")

    args = parser.parse_args()
    
    headed_mode = (args.headed.lower() == "true") or args.login_mode
    profile_name = args.profile
    
    # Load custom comments pool if file is provided
    custom_comments_pool = []
    if args.custom_comments_file and os.path.exists(args.custom_comments_file):
        try:
            with open(args.custom_comments_file, 'r', encoding='utf-8') as f:
                custom_comments_pool = [line.strip() for line in f if line.strip()]
            print(f"✅ Loaded {len(custom_comments_pool)} custom comments from {args.custom_comments_file}")
        except Exception as ce_err:
            print(f"⚠️ Failed to load custom comments: {ce_err}")
    
    # Path setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_dir = os.path.join(current_dir, "profiles")
    user_data_dir = os.path.join(profiles_dir, profile_name)
    
    # Sync from the most recently active regular Chrome Profile (Profile 11 or Profile 24) to have all login cookies/sessions
    chrome_dir = "/Users/apple/Library/Application Support/Google/Chrome"
    src_profile = None
    if os.path.exists(chrome_dir):
        try:
            # We explicitly have sandbox permission to read Profile 11 and Profile 24
            permitted_profiles = ["Profile 11", "Profile 24"]
            candidates = []
            for name in permitted_profiles:
                p_path = os.path.join(chrome_dir, name)
                if os.path.isdir(p_path):
                    candidates.append(p_path)
            if candidates:
                # Sort by folder modification time to find the most active one
                candidates.sort(key=lambda x: os.path.getmtime(x), reverse=True)
                src_profile = candidates[0]
                print(f"🔎 Auto-detected most active Chrome profile: {os.path.basename(src_profile)}")
        except Exception as pe:
            print(f"⚠️ Warning during active profile auto-detection: {pe}")
            
    # Fallback to Profile 24 if auto-detection failed
    if not src_profile:
        src_profile = os.path.join(chrome_dir, "Profile 24")
        
    dest_profile = os.path.join(user_data_dir, "Default")
    # Only sync if the destination profile does not exist to avoid recurring 'This profile will be managed' alerts
    if os.path.exists(src_profile) and not os.path.exists(dest_profile):
        print(f"🔄 Syncing regular Chrome {os.path.basename(src_profile)} to bot profile: {profile_name}...")
        try:
            import shutil
            if not os.path.exists(user_data_dir):
                os.makedirs(user_data_dir)
            
            # Copy Local State file to assist with cookie/session decryption
            src_local_state = os.path.join(chrome_dir, "Local State")
            dest_local_state = os.path.join(user_data_dir, "Local State")
            if os.path.exists(src_local_state):
                shutil.copy2(src_local_state, dest_local_state)
                print("🔄 Copied Chrome Local State for cookie decryption.")
                
            def ignore_locks(db_dir, contents):
                ignored = []
                for item in contents:
                    if item in ['SingletonLock', 'SingletonSocket', 'SingletonCookie', 'lockfile']:
                        ignored.append(item)
                return ignored
                
            shutil.copytree(src_profile, dest_profile, ignore=ignore_locks, symlinks=True)
            # Remove Sessions folder to prevent restoring old tabs
            sessions_dir = os.path.join(dest_profile, "Sessions")
            if os.path.exists(sessions_dir):
                shutil.rmtree(sessions_dir, ignore_errors=True)
            print(f"✅ Chrome {os.path.basename(src_profile)} synced successfully!")
        except Exception as se:
            print(f"⚠️ Warning: Profile sync failed: {se}")
            
    print(f"--- STARTING TIKTOK WEB FARMING BOT ---")
    print(f"Profile Directory: {user_data_dir}")
    print(f"Config -> Loops: {args.loops} | Like Prob: {args.like_prob} | Comment Prob: {args.comment_prob} | Follow Prob: {args.follow_prob}")
    print(f"Headed Browser: {headed_mode}")
    if args.target_user:
        print(f"Target User: \"{args.target_user}\"")
    if args.upload_video:
        print(f"Upload Video: \"{args.upload_video}\"")
    if args.query:
        print(f"Search Query: \"{args.query}\"")
    
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir)
        print(f"Created new profile directory: {user_data_dir}")

    with sync_playwright() as p:
        print("Launching Chromium browser context...")
        context = None
        browser = None
        
        if headed_mode:
            print("Checking if MAIN Google Chrome is running with debugging active...")
            try:
                import urllib.request
                # Step 1: Try to connect to existing Chrome with debugging already enabled
                cdp_connected = False
                try:
                    urllib.request.urlopen("http://localhost:9222/json/version", timeout=1)
                    browser = p.chromium.connect_over_cdp("http://localhost:9222")
                    context = browser.contexts[0]
                    print("✅ Connected to existing main Chrome (debugging was already active)!")
                    cdp_connected = True
                except Exception:
                    print("Chrome debugging port 9222 not active. Skipping main Chrome connection...")
            except Exception as cdp_err:
                print(f"⚠️ CDP check failed: {cdp_err}. Proceeding with persistent context launch...")

        if not context:
            try:
                args_list = [
                    "--disable-blink-features=AutomationControlled",
                    "--use-fake-ui-for-media-stream",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]

                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=not headed_mode,
                    channel="chrome",
                    viewport=None,
                    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                    ignore_default_args=["--disable-extensions", "--enable-automation"],
                    args=args_list
                )
                print("Successfully launched with Google Chrome channel.")
            except Exception as e:
                print(f"⚠️ Warning: Failed to launch with Google Chrome channel: {e}")
                print("Retrying launch with default Playwright Chromium...")
                try:
                    context = p.chromium.launch_persistent_context(
                        user_data_dir=user_data_dir,
                        headless=not headed_mode,
                        viewport=None,
                        ignore_default_args=["--disable-extensions", "--enable-automation"],
                        args=args_list
                    )
                except Exception as e2:
                    print(f"❌ Failed to launch browser persistent context: {e2}")
            
            # Bring Chrome to the front on macOS to ensure visibility
            try:
                import subprocess
                subprocess.run(['osascript', '-e', 'tell application "Google Chrome" to activate'], timeout=2)
                print("🚀 Activated Google Chrome to bring it to front focus.")
            except Exception:
                pass

        page = context.pages[0] if context.pages else context.new_page()
        
        # Grant microphone permissions for TikTok to allow real voice typing
        try:
            context.grant_permissions(["microphone"], origin="https://www.tiktok.com")
            context.grant_permissions(["microphone"], origin="https://tiktok.com")
            print("✅ Granted microphone permissions for TikTok.")
        except Exception as pe:
            print(f"⚠️ Warning: Failed to grant microphone permissions: {pe}")
        
        # Override navigator properties to bypass advanced bot checks
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
            Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});
            window.chrome = { runtime: {} };
        """)
        
        print("Navigating to TikTok...")
        try:
            page.goto("https://www.tiktok.com", timeout=60000)
            page.wait_for_load_state("networkidle")
            print("Successfully loaded TikTok homepage.")
            time.sleep(5)
            save_preview(page, profile_name)
        except Exception as e:
            print(f"⚠️ Warning: Navigation timeout or networkidle issue: {e}")
            # Continue anyway

        # Wait for login if login-mode is enabled
        if args.login_mode:
            print("\n⏳ [LOGIN MODE] Please log in manually in the opened browser window (QR code, phone, or email)...")
            start_time = time.time()
            login_timeout = 600  # 10 minutes
            logged_in = False
            last_ping_time = start_time
            
            while time.time() - start_time < login_timeout:
                try:
                    # Look for profile selectors and login buttons specifically
                    profile_visible = page.locator('[data-e2e="profile-icon"]').first.is_visible()
                    avatar_visible = page.locator('[data-e2e="avatar-icon"]').first.is_visible()
                    inbox_visible = page.locator('[data-e2e="notification-icon"]').first.is_visible()
                    login_button_visible = page.locator('[data-e2e="nav-login-button"]').first.is_visible()
                    
                    # Logged in if profile/avatar/inbox is visible and login button is gone
                    if (profile_visible or avatar_visible or inbox_visible) and not login_button_visible:
                        print("🎉 [LOGIN SUCCESS] Login detected successfully!")
                        logged_in = True
                        break
                except Exception:
                    pass
                
                # Print a reminder and update preview every 10 seconds
                now = time.time()
                if now - last_ping_time >= 10:
                    elapsed = int(now - start_time)
                    print(f"⏳ Waiting for manual login... ({elapsed}s elapsed)")
                    last_ping_time = now
                    save_preview(page, profile_name)
                
                time.sleep(2)
                
            if not logged_in:
                print("❌ [LOGIN TIMEOUT] Login timeout of 10 minutes reached.")
            else:
                # Save session storage state
                try:
                    state_path = os.path.join(user_data_dir, "storage_state.json")
                    context.storage_state(path=state_path)
                    print(f"✅ Saved session storage state to {state_path}")
                except Exception as sse:
                    print(f"⚠️ Warning: Failed to save storage state: {sse}")
                time.sleep(3)

        # Follow target user if specified
        if args.target_user:
            username = args.target_user.lstrip('@')
            target_url = f"https://www.tiktok.com/@{username}"
            print(f"\n👤 Navigating to target user profile: {target_url}")
            try:
                page.goto(target_url, timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(5)
                
                # Look for buttons on profile page
                buttons = page.locator("button")
                count = buttons.count()
                followed = False
                follow_btn = None
                
                for i in range(count):
                    btn = buttons.nth(i)
                    txt = btn.inner_text().strip()
                    if txt in ["Follow", "ติดตาม"]:
                        follow_btn = btn
                        break
                    elif txt in ["Following", "กำลังติดตาม", "Message", "ส่งข้อความ", "Messages"]:
                        followed = True
                        break
                
                if followed:
                    print(f"✅ Already following @{username} (or account has Messages/Following button).")
                elif follow_btn:
                    print(f"👉 Clicking Follow button for @{username}...")
                    follow_btn.click()
                    time.sleep(3)
                    print(f"✅ Follow button clicked.")
                else:
                    print(f"⚠️ Could not find a Follow or Following button on @{username}'s page.")
            except Exception as e:
                print(f"⚠️ Failed to follow target user @{username}: {e}")

        # Video Upload flow if specified
        if args.upload_video:
            upload_path = os.path.abspath(args.upload_video)
            if not os.path.exists(upload_path):
                print(f"\n❌ Video upload file does not exist: {upload_path}")
            else:
                print(f"\n📤 Preparing to upload video: {upload_path}")
                try:
                    upload_url = "https://www.tiktok.com/upload?lang=en"
                    page.goto(upload_url, timeout=60000)
                    time.sleep(5)
                    print(f"Current page URL: {page.url}")
                    try:
                        page.screenshot(path=os.path.join(current_dir, "uploads", "TikTokBot", "uploader_debug.jpg"), type="jpeg", quality=50)
                        print("Saved uploader debug screenshot.")
                    except Exception as se_err:
                        print(f"Failed to save screenshot: {se_err}")
                    
                    # Check and handle any "Continue editing / Discard" popups (can be multiple levels)
                    print("🧹 Checking for any active draft or uploader overlays/popups...")
                    for discard_attempt in range(5):
                        clicked_any = False
                        # Try page first, then all frames
                        for target in [page] + list(page.frames):
                            try:
                                locs = target.locator('button:has-text("Discard"), button:has-text("ละทิ้ง")')
                                count = locs.count()
                                for i in range(count):
                                    btn = locs.nth(i)
                                    if btn.is_visible() and btn.is_enabled():
                                        print(f"👉 Found Discard button (attempt {discard_attempt+1}, index {i}), clicking with force=True...")
                                        btn.click(force=True)
                                        clicked_any = True
                                        time.sleep(1.5)
                            except Exception:
                                pass
                        if clicked_any:
                            time.sleep(3)
                        else:
                            break

                    file_input = None
                    target_page = page
                    # Try main page first
                    try:
                        page.wait_for_selector('input[type="file"]', state="attached", timeout=5000)
                        file_input = page.locator('input[type="file"]').first
                        print("Found file input on main page.")
                    except Exception:
                        pass

                    # If not found, search in all frames (iframes)
                    if not file_input:
                        print("File input not found on main page, searching in frames...")
                        for frame in page.frames:
                            if "content/publish" in frame.url or "publish" in frame.url:
                                print(f"Targeting publish frame: {frame.url}")
                                try:
                                    frame.wait_for_selector('input[type="file"]', state="attached", timeout=15000)
                                    file_input = frame.locator('input[type="file"]').first
                                    target_page = frame
                                    print("Successfully located file input inside publish frame!")
                                    break
                                except Exception as e:
                                    print(f"Failed to find input inside publish frame: {e}")
                        
                        # Fallback to search all frames if target url match wasn't found/loaded yet
                        if not file_input:
                            for frame in page.frames:
                                try:
                                    frame.wait_for_selector('input[type="file"]', state="attached", timeout=2000)
                                    file_input = frame.locator('input[type="file"]').first
                                    target_page = frame
                                    print(f"Found file input inside frame (fallback): {frame.name or frame.url}")
                                    break
                                except Exception:
                                    pass

                    if not file_input:
                        print("⚠️ Upload file input not found in main page or any frames. You might need to login first on this profile.")
                    else:
                        print("👉 Selecting video file...")
                        file_input.set_input_files(upload_path)
                        time.sleep(5) # Let upload start
                        
                        # Clean up onboarding tutorial overlays
                        try:
                            # Clean up in both main page and all frames
                            for target in [page] + list(page.frames):
                                try:
                                    target.evaluate("document.querySelectorAll('#react-joyride-portal, .react-joyride__overlay, .react-joyride__spotlight, [class*=\"joyride\"]').forEach(el => el.remove())")
                                except Exception:
                                    pass
                            print("Cleaned up any onboarding tutorial overlays in all frames.")
                        except Exception as e:
                            print(f"Failed to clean overlays: {e}")
                        
                        # Write caption if provided
                        if args.upload_caption:
                            print(f"✍️ Writing caption: \"{args.upload_caption}\"")
                            caption_selectors = [
                                'div[contenteditable="true"]',
                                '[contenteditable="true"]',
                                '.public-DraftEditor-content',
                                'div[data-e2e="desc-input"]',
                                'div[class*="editor"]'
                            ]
                            caption_field = None
                            # Search in main page and all frames
                            for target in [page] + list(page.frames):
                                for sel in caption_selectors:
                                    try:
                                        loc = target.locator(sel).first
                                        if loc.is_visible():
                                            caption_field = loc
                                            print(f"Found caption selector: {sel} in frame {target.name or target.url}")
                                            break
                                    except Exception:
                                        pass
                                if caption_field:
                                    break
                            
                            if caption_field:
                                try:
                                    # Wait for element to be stable
                                    time.sleep(1)
                                    caption_field.click()
                                    time.sleep(1)
                                    # Clear existing text
                                    page.keyboard.press("Meta+A")
                                    page.keyboard.press("Control+A")
                                    page.keyboard.press("Backspace")
                                    time.sleep(1)
                                    page.keyboard.type(args.upload_caption)
                                    print("✅ Filled caption using page.keyboard.type")
                                    time.sleep(1)
                                except Exception as fe:
                                    print(f"⚠️ Keyboard type failed: {fe}. Trying locator.fill...")
                                    try:
                                        caption_field.fill(args.upload_caption)
                                        print("✅ Filled caption using locator.fill")
                                    except Exception as fe2:
                                        print(f"❌ Failed to write caption: {fe2}")
                            else:
                                print("⚠️ Caption input field not found.")
                        
                        # Wait for upload/processing
                        print("⏳ Sleeping 45 seconds to let the video upload and process...")
                        time.sleep(45)
                        
                        # Find post button
                        post_selectors = [
                            'button[data-e2e="post_video_button"]',
                            'button:has-text("Post")',
                            'button:has-text("โพสต์")',
                            'button:has-text("Share")',
                            'button:has-text("แชร์")'
                        ]
                        post_btn = None
                        for target in [page] + list(page.frames):
                            for sel in post_selectors:
                                try:
                                    btn = target.locator(sel).first
                                    if btn.is_visible() and btn.is_enabled():
                                        if btn.get_attribute("data-tt") == "Sidebar_Sidebar_Clickable":
                                            continue
                                        if "Sidebar" in (btn.get_attribute("class") or ""):
                                            continue
                                        post_btn = btn
                                        break
                                except Exception:
                                    pass
                            if post_btn:
                                break
                                
                        if post_btn:
                            print("🚀 Clicking Post button...")
                            post_btn.click()
                            time.sleep(5)
                            
                            # Check for captcha or verification popup
                            print("🔎 Checking for any post verification captcha...")
                            captcha_detected = False
                            for check_sec in range(120):  # Wait up to 2 minutes for captcha solving
                                captcha_visible = False
                                for target in [page] + list(page.frames):
                                    try:
                                        # Match typical TikTok captcha texts
                                        captcha_elements = target.locator('div:has-text("Drag the slider"), div:has-text("verification"), [class*="captcha"], [id*="captcha"]')
                                        if captcha_elements.first.is_visible():
                                            captcha_visible = True
                                            break
                                    except Exception:
                                        pass
                                
                                if captcha_visible:
                                    if not captcha_detected:
                                        print("\n⚠️ [CAPTCHA DETECTED] Please solve the puzzle/slider captcha in the opened browser window! ⏳")
                                        captcha_detected = True
                                    time.sleep(3)
                                else:
                                    if captcha_detected:
                                        print("🎉 Captcha solved! Continuing post flow...")
                                    break
                            
                            # Wait for post confirmation redirect or success message
                            print("⏳ Waiting for post to finish publishing...")
                            time.sleep(15)
                            print("✅ Video posted successfully!")
                        else:
                            print("⚠️ Post button not found or not enabled yet.")
                except Exception as ue:
                    print(f"❌ Video upload failed: {ue}")

        # Navigate back to homepage feed if we did target user follow or upload and loops > 0
        if (args.target_user or args.upload_video) and args.loops > 0:
            print("\n🏠 Navigating back to TikTok homepage feed...")
            try:
                page.goto("https://www.tiktok.com", timeout=60000)
                page.wait_for_load_state("networkidle")
                time.sleep(5)
            except Exception as e:
                print(f"⚠️ Warning: Navigation to homepage failed: {e}")

        # If keyword search is specified
        if args.query:
            print(f"🔎 Initiating search for keyword: \"{args.query}\"")
            try:
                # Find search input
                search_selectors = [
                    "input[type='search']",
                    "input[placeholder*='Search']",
                    "input[placeholder*='ค้นหา']",
                    "input[name='q']"
                ]
                search_input = None
                for selector in search_selectors:
                    if page.locator(selector).is_visible():
                        search_input = page.locator(selector)
                        break
                
                if search_input:
                    search_input.click()
                    search_input.fill(args.query)
                    time.sleep(1)
                    search_input.press("Enter")
                    print("Submitted search query. Waiting for search results...")
                    time.sleep(5)
                    
                    # Click on first video item in search results
                    # Look for video items
                    video_selector = "a[href*='/video/']"
                    first_video = page.locator(video_selector).first
                    if first_video.is_visible():
                        print("Clicking first video in search results...")
                        first_video.click()
                        time.sleep(5)
                    else:
                        print("⚠️ No search result video links found, continuing on homepage feed.")
                else:
                    print("⚠️ Search input field not found. Continuing on homepage feed.")
            except Exception as se:
                print(f"⚠️ Search failed: {se}. Continuing on homepage feed.")

        # Start scrolling feed
        print("🚀 Starting Web feed auto-scrolling loop...")
        try:
            for loop in range(1, args.loops + 1):
                print(f"\n--- Round {loop}/{args.loops} ---")
                save_preview(page, profile_name)
                
                # Random watch time
                watch_time = random.uniform(6.0, 20.0)
                print(f"👀 Watching current video for {watch_time:.2f} seconds...")
                time.sleep(watch_time)
                
                # Like probability
                if random.random() < args.like_prob:
                    print("💖 Randomly liking video...")
                    try:
                        # Try to find and click the like button/icon first
                        like_selectors = [
                            'button[data-e2e="like-icon"]',
                            '[data-e2e="like-icon"]',
                            'button[data-e2e="like-button"]',
                            'span[class*="LikeIcon"]',
                            'svg[class*="Like"]'
                        ]
                        like_clicked = False
                        for sel in like_selectors:
                            elements = page.locator(sel)
                            count = elements.count()
                            for i in range(count):
                                el = elements.nth(i)
                                if el.is_visible() and el.is_enabled():
                                    el.click()
                                    print(f"✅ Clicked like button using selector: {sel}")
                                    like_clicked = True
                                    break
                            if like_clicked:
                                break
                        
                        if not like_clicked:
                            # Fallback: Double click the middle of the page (in the video container) using human-like movement
                            like_x = random.randint(600, 680)
                            like_y = random.randint(380, 450)
                            human_mouse_move(page, like_x, like_y)
                            time.sleep(0.1)
                            page.mouse.dblclick(like_x, like_y)
                            print("✅ Double clicked video container to like (fallback).")
                        time.sleep(1.5)
                    except Exception as le:
                        print(f"⚠️ Like failed: {le}")
                
                # Comment probability
                if random.random() < args.comment_prob:
                    if custom_comments_pool:
                        comment_text = random.choice(custom_comments_pool)
                        style_info = "custom"
                    elif args.comment_style == "text":
                        comment_text = random.choice(TEXT_COMMENTS)
                        style_info = args.comment_style
                    elif args.comment_style == "emoji":
                        comment_text = random.choice(EMOJI_COMMENTS)
                        style_info = args.comment_style
                    else:
                        comment_text = random.choice(MIXED_COMMENTS)
                        style_info = args.comment_style
                    print(f"💬 Randomly commenting ({style_info}): \"{comment_text}\"")
                    try:
                        comment_input_selectors = [
                            "div[data-e2e='comment-input']",
                            "[placeholder*='Add comment']",
                            "[placeholder*='เพิ่มความคิดเห็น']",
                            "input[placeholder*='comment']"
                        ]
                        comment_field = None
                        for selector in comment_input_selectors:
                            if page.locator(selector).is_visible():
                                comment_field = page.locator(selector)
                                break
                        
                        if comment_field:
                            comment_field.click()
                            comment_field.fill(comment_text)
                            time.sleep(1)
                            
                            # Post button
                            post_selectors = [
                                "div[data-e2e='comment-post']",
                                "button:has-text('Post')",
                                "button:has-text('โพสต์')"
                            ]
                            post_btn = None
                            for selector in post_selectors:
                                if page.locator(selector).is_visible():
                                    post_btn = page.locator(selector)
                                    break
                            
                            if post_btn:
                                post_btn.click()
                                print("✅ Comment posted successfully.")
                            else:
                                # Press enter to submit comment if post button not found
                                comment_field.press("Enter")
                                print("✅ Comment submitted via Enter key.")
                            time.sleep(2)
                        else:
                            print("⚠️ Comment input field not visible.")
                    except Exception as ce:
                        print(f"⚠️ Comment failed: {ce}")
                
                # Follow creator probability
                if args.follow_prob > 0 and random.random() < args.follow_prob:
                    print("👤 Randomly following video creator...")
                    try:
                        follow_selectors = [
                            "button[data-e2e='feed-follow']",
                            "div[data-e2e='feed-follow']",
                            "button:has-text('Follow')",
                            "button:has-text('ติดตาม')"
                        ]
                        follow_btn = None
                        for selector in follow_selectors:
                            elements = page.locator(selector)
                            count = elements.count()
                            for i in range(count):
                                el = elements.nth(i)
                                if el.is_visible() and el.is_enabled():
                                    txt = el.inner_text().strip()
                                    if txt in ["Follow", "ติดตาม", ""]:
                                        follow_btn = el
                                        break
                            if follow_btn:
                                break
                        
                        if follow_btn:
                            follow_btn.click()
                            print("✅ Followed video creator successfully.")
                            time.sleep(2)
                        else:
                            print("⚠️ Active Follow button not found in feed.")
                    except Exception as fe:
                        print(f"⚠️ Follow failed: {fe}")
                
                # Scroll to next video
                scroll_to_next_video(page)
                save_preview(page, profile_name)
                
                # Random load delay
                time.sleep(random.uniform(1.5, 4.0))
                
            print("\n🎉 Web Farming Bot has completed all rounds successfully!")
        except KeyboardInterrupt:
            print("\n🛑 Bot execution interrupted by user.")
        except Exception as ex:
            print(f"\n❌ Error during feed loop: {ex}")
            
        # Save updated storage state before closing
        try:
            state_path = os.path.join(user_data_dir, "storage_state.json")
            context.storage_state(path=state_path)
            print(f"✅ Saved updated session storage state to {state_path}")
        except Exception as sse:
            print(f"⚠️ Warning: Failed to save updated storage state: {sse}")

        if args.loops == 0:
            print("\n⏳ [BROWSER ACTIVE] Keeping browser open for 300 seconds so you can inspect the state, log in, or complete any manual steps...")
            try:
                time.sleep(300)
            except KeyboardInterrupt:
                pass

        print("Closing browser context...")
        context.close()
        print("Bot finished.")

if __name__ == "__main__":
    main()
