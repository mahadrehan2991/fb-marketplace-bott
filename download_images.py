import os
import urllib.request
import time

# Create output folder
output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images")
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Map filenames to keywords for LoremFlickr
images_to_download = {
    "s23ultra1.jpg": "samsung,s23,phone&lock=1",
    "s23ultra2.jpg": "samsung,s23,phone&lock=2",
    "city1.jpg": "honda,city,car&lock=1",
    "city2.jpg": "honda,city,car&lock=2",
    "city3.jpg": "honda,city,car&lock=3",
    "dellxps1.jpg": "dell,xps,laptop&lock=1",
    "dellxps2.jpg": "dell,xps,laptop&lock=2",
    "apt1.jpg": "apartment,livingroom&lock=1",
    "apt2.jpg": "apartment,bedroom&lock=2",
    "apt3.jpg": "apartment,building&lock=3",
    "ac1.jpg": "airconditioner,ac&lock=1",
    "ac2.jpg": "airconditioner&lock=2",
    "suit1.jpg": "mensuit,suit&lock=1",
    "suit2.jpg": "mensuit,suit&lock=2",
    "ps4_1.jpg": "playstation,console&lock=1",
    "ps4_2.jpg": "playstation,game&lock=2",
    "meteor1.jpg": "motorcycle,bike&lock=1",
    "meteor2.jpg": "motorcycle&lock=2",
    "fridge1.jpg": "refrigerator,fridge&lock=1",
    "fridge2.jpg": "refrigerator,kitchen&lock=2",
    "bicycle1.jpg": "bicycle,cycle&lock=1",
    "chair1.jpg": "officechair,chair&lock=1",
    "chair2.jpg": "officechair,chair&lock=2",
    "canon1.jpg": "canon,camera&lock=1",
    "canon2.jpg": "canon,camera&lock=2",
    "tutor_profile.jpg": "teacher,portrait&lock=1"
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

print("Starting to download listings images...")
print(f"Destination folder: {output_folder}\n")

for filename, query in images_to_download.items():
    filepath = os.path.join(output_folder, filename)
    if os.path.exists(filepath):
        print(f"[Skipped] {filename} already exists.")
        continue
        
    url = f"https://loremflickr.com/800/600/{query}"
    print(f"Downloading {filename} from LoremFlickr ({query.split('&')[0]})...")
    
    success = False
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as response:
                with open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"[Success] Saved {filename}")
            success = True
            break
        except Exception as e:
            print(f"[Attempt {attempt+1} Failed] Error downloading {filename}: {e}")
            time.sleep(2)
            
    if not success:
        # Create a simple fallback color placeholder if download fails entirely
        print(f"[Fallback] Creating placeholder image for {filename}")
        try:
            from PIL import Image, ImageDraw
            img = Image.new('RGB', (800, 600), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.text((350, 280), filename, fill=(255, 255, 0))
            img.save(filepath)
        except Exception:
            # Create an empty file as a last resort
            with open(filepath, 'w') as f:
                f.write('')

    time.sleep(1) # Polite delay to avoid rate limiting

print("\nAll image downloads completed!")
input("Press Enter to close...")
