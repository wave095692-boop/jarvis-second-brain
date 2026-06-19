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
            # Scroll down using mouse wheel
            page.mouse.move(640, 400) # Move mouse to the center of the viewport
            page.mouse.wheel(0, 750) # Scroll down by 750 pixels
            print("✅ Scrolled page down via mouse wheel.")
            
            # Also press ArrowDown as a backup
            time.sleep(0.5)
            page.keyboard.press("ArrowDown")
    except Exception as e:
        print(f"⚠️ Error during scrolling: {e}")

def main():
    parser = argparse.ArgumentParser(description="TikTok Web Farming Bot by Jarvis")
    parser.add_argument("--profile", type=str, default="profile_1", help="Name of the browser profile")
    parser.add_argument("--loops", type=int, default=10, help="Number of scrolls/videos to watch")
    parser.add_argument("--like-prob", type=float, default=0.15, help="Probability of liking (0.0 - 1.0)")
    parser.add_argument("--comment-prob", type=float, default=0.05, help="Probability of commenting (0.0 - 1.0)")
    parser.add_argument("--comment-style", type=str, default="mixed", choices=["text", "emoji", "mixed"], help="Style of comments to post")
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
    
    # Path setup
    current_dir = os.path.dirname(os.path.abspath(__file__))
    profiles_dir = os.path.join(current_dir, "profiles")
    user_data_dir = os.path.join(profiles_dir, profile_name)
    
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
        try:
            # Try to launch with real Google Chrome channel first to bypass TikTok QR scan blocking
            context = p.chromium.launch_persistent_context(
                user_data_dir=user_data_dir,
                headless=not headed_mode,
                channel="chrome",
                viewport={"width": 1280, "height": 800},
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--use-fake-ui-for-media-stream"
                ]
            )
            print("Successfully launched with Google Chrome channel.")
        except Exception as e:
            print(f"⚠️ Warning: Failed to launch with Google Chrome channel: {e}")
            print("Retrying launch with default Playwright Chromium...")
            try:
                context = p.chromium.launch_persistent_context(
                    user_data_dir=user_data_dir,
                    headless=not headed_mode,
                    viewport={"width": 1280, "height": 800},
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--use-fake-ui-for-media-stream"
                    ]
                )
            except Exception as e2:
                print(f"❌ Failed to launch browser persistent context: {e2}")
                sys.exit(1)
            
        page = context.pages[0] if context.pages else context.new_page()
        
        # Grant microphone permissions for TikTok to allow real voice typing
        try:
            context.grant_permissions(["microphone"], origin="https://www.tiktok.com")
            context.grant_permissions(["microphone"], origin="https://tiktok.com")
            print("✅ Granted microphone permissions for TikTok.")
        except Exception as pe:
            print(f"⚠️ Warning: Failed to grant microphone permissions: {pe}")
        
        # Override navigator.webdriver to bypass basic bot checks
        page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("Navigating to TikTok...")
        try:
            page.goto("https://www.tiktok.com", timeout=60000)
            page.wait_for_load_state("networkidle")
            print("Successfully loaded TikTok homepage.")
            time.sleep(5)
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
                
                # Print a reminder every 10 seconds
                now = time.time()
                if now - last_ping_time >= 10:
                    elapsed = int(now - start_time)
                    print(f"⏳ Waiting for manual login... ({elapsed}s elapsed)")
                    last_ping_time = now
                
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
                    page.wait_for_load_state("networkidle")
                    time.sleep(5)
                    
                    file_input_found = False
                    try:
                        page.wait_for_selector('input[type="file"]', timeout=15000)
                        file_input_found = True
                    except Exception:
                        pass
                        
                    if not file_input_found:
                        print("⚠️ Upload file input not found. You might need to login first on this profile.")
                    else:
                        print("👉 Selecting video file...")
                        file_input = page.locator('input[type="file"]')
                        file_input.set_input_files(upload_path)
                        time.sleep(5) # Let upload start
                        
                        # Write caption if provided
                        if args.upload_caption:
                            print(f"✍️ Writing caption: \"{args.upload_caption}\"")
                            caption_selectors = [
                                'div[data-e2e="desc-input"]',
                                'div[class*="editor"]',
                                'div[contenteditable="true"]',
                                '.public-DraftEditor-content'
                            ]
                            caption_field = None
                            for sel in caption_selectors:
                                if page.locator(sel).first.is_visible():
                                    caption_field = page.locator(sel).first
                                    break
                            
                            if caption_field:
                                caption_field.click()
                                time.sleep(1)
                                page.keyboard.press("Meta+A")
                                page.keyboard.press("Control+A")
                                page.keyboard.press("Backspace")
                                time.sleep(1)
                                caption_field.fill(args.upload_caption)
                                time.sleep(1)
                            else:
                                print("⚠️ Caption input field not found.")
                        
                        # Wait for upload/processing
                        print("⏳ Waiting for video uploading and processing to complete (30s)...")
                        time.sleep(30)
                        
                        # Click post button
                        post_selectors = [
                            'button[data-e2e="post_video_button"]',
                            'button:has-text("Post")',
                            'button:has-text("โพสต์")'
                        ]
                        post_btn = None
                        for sel in post_selectors:
                            if page.locator(sel).first.is_visible() and page.locator(sel).first.is_enabled():
                                post_btn = page.locator(sel).first
                                break
                                
                        if post_btn:
                            print("🚀 Clicking Post button...")
                            post_btn.click()
                            time.sleep(10)
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
                            # Fallback: Double click the middle of the page (in the video container)
                            page.mouse.dblclick(640, 400)
                            print("✅ Double clicked video container to like (fallback).")
                        time.sleep(1.5)
                    except Exception as le:
                        print(f"⚠️ Like failed: {le}")
                
                # Comment probability
                if random.random() < args.comment_prob:
                    if args.comment_style == "text":
                        comment_text = random.choice(TEXT_COMMENTS)
                    elif args.comment_style == "emoji":
                        comment_text = random.choice(EMOJI_COMMENTS)
                    else:
                        comment_text = random.choice(MIXED_COMMENTS)
                    print(f"💬 Randomly commenting ({args.comment_style}): \"{comment_text}\"")
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
                
                # Random load delay
                time.sleep(random.uniform(1.5, 4.0))
                
            print("\n🎉 Web Farming Bot has completed all rounds successfully!")
        except KeyboardInterrupt:
            print("\n🛑 Bot execution interrupted by user.")
        except Exception as ex:
            print(f"\n❌ Error during feed loop: {ex}")
            
        print("Closing browser context...")
        context.close()
        print("Bot finished.")

if __name__ == "__main__":
    main()
