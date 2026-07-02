import urllib.request
import ssl
import sys
import time

def main():
    ssl._create_default_https_context = ssl._create_unverified_context
    
    url = "https://dw.uptodown.com/dwn/vwa3ZNO0lJReLQHDfdiVtE3ntqo9wN3FXvUO9RWuwKZmOEOYu7jBYw3eFYyw4Lel63Adm7t5TVG3_c6ItwjiIMrJur1QVZBXu_eOYOGAbWZMTrb1HWR13Rfxmaf8FHrn/QZ7Aq79F9R3876nQ6nlgfCr1XJprYUr_K8PU8vhcBNeVza1AHvovE-cETWXddhpxzccwRrbc31hulJpODwNFmOHm_nlQmWDCVZdx7Fpjg3kS2fANx708LW32tyq9vdbJ/z8vZVPOPKiJoLliPY39PuiRiYOqiJp0j50D1jhbIFBTsziZzZHLQ0SrHwqAMq3U7LCs6sAO7YGWEkxJyOMmWxw==/"
    output_path = "/Users/apple/.gemini/antigravity-ide/scratch/tiktok.apk"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"🚀 Starting download of TikTok APK...")
    print(f"🔗 Target: {url[:60]}...")
    print(f"📂 Saving to: {output_path}")
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        start_time = time.time()
        with urllib.request.urlopen(req) as response, open(output_path, 'wb') as out_file:
            total_size = int(response.getheader('Content-Length', 0))
            downloaded = 0
            block_size = 1024 * 1024 # 1MB chunks
            
            print(f"📊 Total File Size: {total_size / (1024*1024):.2f} MB")
            
            last_report = 0
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                
                out_file.write(buffer)
                downloaded += len(buffer)
                
                # Report status every 10MB or when done
                if downloaded - last_report >= 10 * 1024 * 1024 or downloaded == total_size:
                    percentage = (downloaded / total_size) * 100 if total_size else 0
                    print(f"📥 Downloaded: {downloaded / (1024*1024):.2f} MB / {total_size / (1024*1024):.2f} MB ({percentage:.1f}%)")
                    last_report = downloaded
                    
        elapsed = time.time() - start_time
        print(f"✅ Download completed successfully in {elapsed:.1f} seconds!")
        
    except Exception as e:
        print(f"❌ Error during download: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
