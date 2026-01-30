import requests

def create_m3u():
    # Using the direct raw domain to avoid HTML redirects
    json_url = "https://github.com/StmpupCricket/extract/raw/main/stream-manifests.json"
    
    try:
        response = requests.get(json_url, headers={"User-Agent": "Mozilla/5.0"})
        data = response.json()
        
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            # Case 1: JSON is a List [{}, {}]
            if isinstance(data, list):
                items = data
            # Case 2: JSON is a Dict {"ch1": {}, "ch2": {}}
            elif isinstance(data, dict):
                # If it's a dict, we want the values (the channel info)
                items = data.values()
            else:
                raise ValueError("Unexpected JSON format")

            for item in items:
                # This check prevents the 'str' object error
                if not isinstance(item, dict):
                    continue
                
                name = item.get("name", "Unknown Stream")
                url = item.get("url", "")
                keys = item.get("clearkey", {})

                if url:
                    f.write(f'#EXTINF:-1 tvg-name="{name}",{name}\n')
                    
                    if isinstance(keys, dict) and keys:
                        # Extract the first KID and KEY
                        kid = list(keys.keys())[0]
                        key = keys[kid]
                        f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
                        f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
                    
                    f.write(f"{url}\n")
                    
        print("Playlist generated successfully.")
        
    except Exception as e:
        print(f"Python Error: {e}")
        exit(1)

if __name__ == "__main__":
    create_m3u()
