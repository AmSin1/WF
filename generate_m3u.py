import requests

def create_m3u():
    json_url = "https://github.com"
    
    try:
        response = requests.get(json_url)
        data = response.json()
        
        # FIX: Your JSON is a DICT with keys like "Sky Sport 1", not a LIST.
        # We must iterate over the items (key and value pairs).
        
        with open("playlist.m3u", "w") as f:
            f.write("#EXTM3U\n")
            
            for stream_name, details in data.items():
                # details is the dictionary containing 'url' and 'clearkey'
                url = details.get("url", "")
                clearkey_dict = details.get("clearkey", {})
                
                f.write(f'#EXTINF:-1 tvg-name="{stream_name}",{stream_name}\n')
                
                if clearkey_dict:
                    # Extracts first KID and KEY pair
                    kid = list(clearkey_dict.keys())[0]
                    key = clearkey_dict[kid]
                    f.write("#KODIPROP:inputstream.adaptive.license_type=clearkey\n")
                    f.write(f"#KODIPROP:inputstream.adaptive.license_key={kid}:{key}\n")
                
                f.write(f"{url}\n")
                
        print("M3U Created Successfully")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    create_m3u()
