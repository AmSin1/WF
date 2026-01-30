import requests
import json

def create_m3u():
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        # DEBUG: Print the first bit of data to the GitHub Action logs
        print(f"DEBUG: Data type is {type(data)}")
        print(f"DEBUG: First 500 chars: {str(data)[:500]}")
        
        count = 0
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Scenario A: JSON is a Dictionary {"Name": {"url": "..."}}
            if isinstance(data, dict):
                for channel_name, content in data.items():
                    if isinstance(content, dict) and "url" in content:
                        write_stream(f, channel_name, content)
                        count += 1
            
            # Scenario B: JSON is a List [{"name": "...", "url": "..."}]
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict) and "url" in item:
                        name = item.get("name", item.get("channel_name", "Unknown"))
                        write_stream(f, name, item)
                        count += 1
                    
        print(f"Success: Added {count} channels to playlist.m3u")
        
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

def write_stream(f, name, content):
    url = content.get("url")
    keys = content.get("clearkey") # or content.get("clearKeys")
    
    f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
    
    # Handle both "clearkey" and "clearKeys" naming
    if not keys:
        keys = content.get("clearKeys", {})

    if isinstance(keys, dict) and keys:
        kid_list = list(keys.keys())
        if kid_list:
            kid = kid_list[0]
            key = keys[kid]
            f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
            f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
    
    f.write(f"{url}\n")

if __name__ == "__main__":
    create_m3u()
