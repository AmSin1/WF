import requests

def create_m3u():
    # Use raw.githubusercontent.com for a cleaner data fetch
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        count = 0
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Since your JSON is a Dictionary: {"Channel Name": {"url": "...", "clearkey": {...}}}
            for channel_name, content in data.items():
                if not isinstance(content, dict):
                    continue
                
                url = content.get("url")
                keys = content.get("clearkey", {})

                if url:
                    # Write metadata
                    f.write(f'#EXTINF:-1 tvg-name="{channel_name}",{channel_name}\n')
                    
                    # Handle ClearKey DRM
                    if isinstance(keys, dict) and keys:
                        kid_list = list(keys.keys())
                        if kid_list:
                            kid = kid_list[0]
                            key = keys[kid]
                            f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
                            f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
                    
                    # Write stream URL
                    f.write(f"{url}\n")
                    count += 1
                    
        print(f"Success: Added {count} channels to playlist.m3u")
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    create_m3u()
