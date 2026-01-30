import requests

def create_m3u():
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        count = 0
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # 1. Process HLS (.m3u8) URLs
            hls_urls = data.get("hls", {}).get("urls", [])
            for i, url in enumerate(hls_urls):
                # Filter out the <style> tags visible in your debug logs
                if url.startswith("http"):
                    f.write(f'#EXTINF:-1 tvg-name="ICC_HLS_{i+1}",ICC Highlight HLS {i+1}\n')
                    f.write(f"{url}\n")
                    count += 1
            
            # 2. Process DASH (.mpd) URLs
            dash_urls = data.get("dash", {}).get("urls", [])
            for i, url in enumerate(dash_urls):
                if url.startswith("http"):
                    f.write(f'#EXTINF:-1 tvg-name="ICC_DASH_{i+1}",ICC Highlight DASH {i+1}\n')
                    # If these ever require DRM, they would need a key lookup here
                    f.write(f"{url}\n")
                    count += 1
                    
        print(f"Success: Added {count} channels to playlist.m3u")
        
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    create_m3u()
