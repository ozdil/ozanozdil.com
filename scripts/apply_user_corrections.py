import os
import shutil
import json

PUB_DIR = "public/gallery"
DATA_FILE = "src/data/gallery.json"

with open(DATA_FILE, "r") as f:
    data = json.load(f)

# =========================================================================
# 1. CORRECTION: Ilıca Şelalesi -> Azdavay Saray Şelalesi
# =========================================================================
old_selale_dir = os.path.join(PUB_DIR, "ilica-selalesi")
new_selale_dir = os.path.join(PUB_DIR, "azdavay-saray-selalesi")

if os.path.exists(old_selale_dir):
    if os.path.exists(new_selale_dir):
        shutil.rmtree(new_selale_dir)
    shutil.move(old_selale_dir, new_selale_dir)
    print(f"Renamed directory: {old_selale_dir} -> {new_selale_dir}")

selale_album = next((a for a in data["albums"] if a["slug"] in ["ilica-selalesi", "azdavay-saray-selalesi"]), None)
if selale_album:
    selale_album["id"] = "azdavay-saray-selalesi"
    selale_album["slug"] = "azdavay-saray-selalesi"
    selale_album["title"] = "Azdavay Saray Şelalesi & Orman Suları"
    selale_album["shortTitle"] = "Azdavay Saray Şelalesi"
    selale_album["location"] = "Azdavay, Kastamonu"
    selale_album["locationFull"] = "Saray Köyü Şelalesi, Azdavay, Kastamonu"
    selale_album["coverPhoto"] = "/gallery/azdavay-saray-selalesi/thumbs/01_DSF0206.webp"
    selale_album["coverThumb"] = "/gallery/azdavay-saray-selalesi/thumbs/01_DSF0206.webp"
    selale_album["description"] = (
        "Kastamonu'nun Azdavay ilçesine bağlı Saray Köyü yakınlarında, el değmemiş gür ormanların derinliklerinde yer alan Saray Şelalesi; yosun kaplı kireçtaşı kayalıkların arasından zümrüt rengi doğal havuzlara dökülür.\n\n"
        "Ekim 2020'de Fujifilm GFX 50R ve GF50mm f/3.5 ile gerçekleştirilen bu seride; 32 ila 91 saniye süren uzun pozlamalarla suyun kadifemsi akışı, nemli kaya dokuları ve sonbaharın dingin orman atmosferi belgelenmiştir."
    )
    for p in selale_album["photos"]:
        p["id"] = p["id"].replace("ilica-selalesi", "azdavay-saray-selalesi")
        p["src"] = p["src"].replace("/gallery/ilica-selalesi/", "/gallery/azdavay-saray-selalesi/")
        p["thumb"] = p["thumb"].replace("/gallery/ilica-selalesi/", "/gallery/azdavay-saray-selalesi/")
        p["title"] = p["title"].replace("Ilıca Şelalesi", "Azdavay Saray Şelalesi").replace("Ilıca", "Saray Şelalesi")
        p["caption"] = p["caption"].replace("Ilıca", "Azdavay Saray Şelalesi").replace("Küre Dağları", "Azdavay ormanları")

    print(f"Updated Azdavay Saray Şelalesi album metadata ({len(selale_album['photos'])} photos).")

# =========================================================================
# 2. CORRECTION: Nasrullah Camii Külliyesi & Kündekari -> Şeyh Şaban-ı Veli Külliyesi (Merge)
# =========================================================================
nasrullah_ic_album = next((a for a in data["albums"] if a["slug"] == "nasrullah-camii-ic-mekan"), None)
seyh_album = next((a for a in data["albums"] if a["slug"] == "seyh-saban-i-veli"), None)

if nasrullah_ic_album and seyh_album:
    seyh_dir = os.path.join(PUB_DIR, "seyh-saban-i-veli")
    seyh_thumbs = os.path.join(seyh_dir, "thumbs")
    old_nasrullah_ic_dir = os.path.join(PUB_DIR, "nasrullah-camii-ic-mekan")
    
    new_photos = []
    for idx, p in enumerate(nasrullah_ic_album["photos"]):
        new_idx = 16 + idx  # Existing Seyh photos are 1..15
        old_full = "public" + p["src"]
        old_thumb = "public" + p["thumb"]
        
        fname = os.path.basename(old_full)
        clean_base = fname.split("_", 1)[1] if "_" in fname else fname
        new_fname = f"{new_idx:02d}_{clean_base}"
        
        new_full_rel = f"/gallery/seyh-saban-i-veli/{new_fname}"
        new_thumb_rel = f"/gallery/seyh-saban-i-veli/thumbs/{new_fname}"
        
        new_full_path = os.path.join(seyh_dir, new_fname)
        new_thumb_path = os.path.join(seyh_thumbs, new_fname)
        
        if os.path.exists(old_full):
            shutil.copy2(old_full, new_full_path)
        if os.path.exists(old_thumb):
            shutil.copy2(old_thumb, new_thumb_path)
            
        up = dict(p)
        up["id"] = f"seyh_{new_idx:02d}"
        up["index"] = new_idx
        up["src"] = new_full_rel
        up["thumb"] = new_thumb_rel
        up["title"] = up["title"].replace("Nasrullah Camii", "Şeyh Şaban-ı Veli Camii").replace("Nasrullah", "Şeyh Şaban-ı Veli")
        up["caption"] = up["caption"].replace("Nasrullah Camii", "Şeyh Şaban-ı Veli Camii").replace("Nasrullah", "Şeyh Şaban-ı Veli")
        new_photos.append(up)
        
    seyh_album["photos"].extend(new_photos)
    seyh_album["photoCount"] = len(seyh_album["photos"])
    seyh_album["description"] = (
        "Anadolu'nun dört büyük manevi kutbundan biri kabul edilen Hz. Pir Şeyh Şaban-ı Veli adına 1490'lı yıllardan itibaren inşa edilen ve külliye haline gelen anıtsal merkez. Cami, türbe, dergâh evleri, hazire, kütüphane ve şifalı Asa Suyu ile Kastamonu'nun manevi kalbidir.\n\n"
        "Fujifilm GFX 50R ve GF50mm f/3.5 ile belgelenen bu seride; külliyenin huzurlu taş avlusu, ahşap sivil mimarisi ve türbesinin yanı sıra; caminin anıtsal taç kapısı, usta işi sedef kakmalı kündekari minberi, dev kristal avizesi ve kalem işi kubbe süslemeleri eksiksiz bir bütünlükle yer almaktadır."
    )
    
    # Remove old nasrullah-camii-ic-mekan album from albums array
    data["albums"] = [a for a in data["albums"] if a["slug"] != "nasrullah-camii-ic-mekan"]
    
    # Remove old directory
    if os.path.exists(old_nasrullah_ic_dir):
        shutil.rmtree(old_nasrullah_ic_dir)
        print(f"Removed old directory: {old_nasrullah_ic_dir}")
        
    print(f"Successfully merged Şeyh Şaban-ı Veli interior photos! Total photos: {seyh_album['photoCount']}")

# Recalculate totals
data["totalAlbums"] = len(data["albums"])
data["totalPhotos"] = sum(len(a["photos"]) for a in data["albums"])

with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"\nCorrection applied successfully!")
print(f"Total Albums: {data['totalAlbums']}")
print(f"Total Photos: {data['totalPhotos']}")
for a in data["albums"]:
    print(f" - {a['slug']}: {a['title']} ({a['photoCount']} photos)")
