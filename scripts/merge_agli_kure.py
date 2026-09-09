import os
import shutil
import json

AGLI_DIR = "public/gallery/agli-kalesi"
AGLI_THUMBS = os.path.join(AGLI_DIR, "thumbs")
KURE_DIR = "public/gallery/kure-daglari-gece-gokyuzu"

with open("src/data/gallery.json", "r") as f:
    data = json.load(f)

# Find albums
kure_album = next((a for a in data["albums"] if a["slug"] == "kure-daglari-gece-gokyuzu"), None)
agli_album = next((a for a in data["albums"] if a["slug"] == "agli-kalesi"), None)

if not kure_album or not agli_album:
    print("Albums not found!")
    exit(1)

# Move kure photos to agli directory with indexes 10..19
new_kure_photos = []
for idx, p in enumerate(kure_album["photos"]):
    new_idx = 10 + idx
    old_full = "public" + p["src"]
    old_thumb = "public" + p["thumb"]
    
    fname = os.path.basename(old_full)
    # create new filename like 10_DSF2276.webp
    clean_base = fname.split("_", 1)[1] if "_" in fname else fname
    new_fname = f"{new_idx:02d}_{clean_base}"
    
    new_full_rel = f"/gallery/agli-kalesi/{new_fname}"
    new_thumb_rel = f"/gallery/agli-kalesi/thumbs/{new_fname}"
    
    new_full_path = os.path.join(AGLI_DIR, new_fname)
    new_thumb_path = os.path.join(AGLI_THUMBS, new_fname)
    
    if os.path.exists(old_full):
        shutil.copy2(old_full, new_full_path)
    if os.path.exists(old_thumb):
        shutil.copy2(old_thumb, new_thumb_path)
        
    updated_p = dict(p)
    updated_p["id"] = f"agli_{new_idx:02d}"
    updated_p["index"] = new_idx
    updated_p["src"] = new_full_rel
    updated_p["thumb"] = new_thumb_rel
    
    # Update title to mention Ağlı
    t = p["title"]
    t = t.replace("Yayla Kampı", "Ağlı Platosu & Gece Kampı")
    t = t.replace("Samanyolu Galaksisi & Çam Silüetleri", "Ağlı Kalesi Semalarında Samanyolu")
    t = t.replace("Yayla Dokusu", "Ağlı Kalesi Çevresi Gece Dokusu")
    t = t.replace("Yayla Sisleri", "Ağlı Vadisi Sabah Sisleri")
    updated_p["title"] = t
    
    c = p["caption"]
    c = c.replace("Küre Dağları", "Ağlı Kalesi platosunda")
    c = c.replace("yayla", "kale çevresi")
    updated_p["caption"] = c
    
    new_kure_photos.append(updated_p)

# Append to agli photos
agli_album["photos"].extend(new_kure_photos)
agli_album["photoCount"] = len(agli_album["photos"])
agli_album["equipment"] = "Fujifilm GFX 50R • GF20-35mmF4 & GF55mmF1.7"
agli_album["description"] = (
    "Kastamonu'nun kuzeyinde, sarp kayalıklar üzerine kurulmuş doğal bir kale ve gözetleme noktası olan Ağlı Kalesi; vadilere hâkim coğrafi konumu ve zengin orman dokusuyla öne çıkar.\n\n"
    "Eylül 2025'te Fujifilm GFX 50R, GF20-35mm ultra geniş açı ve GF55mm f/1.7 açık diyafram lens ile gerçekleştirilen bu seride; gündüz kale kayalıkları ve sonbahar florasından, gece kale platosunda kurulan kamp, ışıkla boyama, Samanyolu yıldız pozlamaları ve şafak vakti vadilere çöken sislere uzanan görsel bir anlatı belgelenmiştir."
)

# Remove kure album from albums
data["albums"] = [a for a in data["albums"] if a["slug"] != "kure-daglari-gece-gokyuzu"]

# Remove kure directory
if os.path.exists(KURE_DIR):
    shutil.rmtree(KURE_DIR)
    print(f"Removed old directory {KURE_DIR}")

# Update stats
data["totalAlbums"] = len(data["albums"])
data["totalPhotos"] = sum(len(a["photos"]) for a in data["albums"])

with open("src/data/gallery.json", "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Successfully merged Küre Dağları into Ağlı Kalesi!")
print(f"Ağlı Kalesi now has {agli_album['photoCount']} photos.")
print(f"Total albums: {data['totalAlbums']}, Total photos: {data['totalPhotos']}")
