import os
import json
from io import BytesIO
from PIL import Image, ImageEnhance

SSD_DIR_15 = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm/GFX 50r/2020/15.10.2020"
SSD_DIR_21 = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm/GFX 50r/2020/21.10.2020"

DATA_FILE = "src/data/gallery.json"
TARGET_DIR = "public/gallery/cide-gideros-koyu"
THUMBS_DIR = os.path.join(TARGET_DIR, "thumbs")

os.makedirs(TARGET_DIR, exist_ok=True)
os.makedirs(THUMBS_DIR, exist_ok=True)

# Curated aesthetic frames from Cide & Gideros Coast
selected_frames = [
    (SSD_DIR_15, "_DSF0025.RAF", "Cide Sahil Şeridi • Sabah Işığı", "Karadeniz'in sarp kıyı hattında sabah ışığı ve dalga vuruşları."),
    (SSD_DIR_15, "_DSF0030.RAF", "Gideros Koyu Yolu • Falezler", "Sarp kireçtaşı kayalıklar ve derin mavi Karadeniz ufku."),
    (SSD_DIR_15, "_DSF0033.RAF", "Gideros Koyu • 131s İpeksi Dalgalar", "131 saniyelik uzun pozlama ile sisleşen kıyı dalgaları ve kaya dokuları."),
    (SSD_DIR_15, "_DSF0035.RAF", "Karadeniz Ufku • 190s Uzun Pozlama", "190 saniye süren uzun pozlama; suyun ve gökyüzünün mistik bir tül gibi birleştiği an."),
    (SSD_DIR_15, "_DSF0041.RAF", "Gideros Koyu • Korunaklı Havza", "Antik çağlardan beri doğal bir liman olan Gideros Koyu'nun sakin suları."),
    (SSD_DIR_15, "_DSF0046.RAF", "Kıyı Jeolojisi & Taş Dokuları", "Orta format detaycılığıyla kayaların katmanlı jeolojik yapısı."),
    (SSD_DIR_15, "_DSF0050.RAF", "Altın Saat • 180s İkindi Pozlaması", "180 saniyelik uzun pozlamayla gün batımına doğru yumuşayan deniz yüzeyi."),
    (SSD_DIR_21, "_DSF0123.RAF", "Şenpazar Geçidi & Kanyon Silsilesi", "Kıyıdan içeriye uzanan dik kanyon yamaçları ve yoğun Karadeniz orman dokusu."),
    (SSD_DIR_21, "_DSF0128.RAF", "Fırtına Sonrası • 55s Kıyı Hareketi", "55 saniyelik pozlama ile kayalıklara çarpan köpüklerin izleri."),
    (SSD_DIR_21, "_DSF0129.RAF", "Cide Kayalıkları • 133s Kapanış", "133 saniyelik uzun pozlama ile seriyi taçlandıran dingin deniz panoraması.")
]

photos_list = []

for idx, (fdir, fname, title, caption) in enumerate(selected_frames):
    fpath = os.path.join(fdir, fname)
    print(f"Processing [{idx+1}/{len(selected_frames)}]: {fname}")
    
    with open(fpath, 'rb') as fp:
        header = fp.read(128)
        offset = int.from_bytes(header[84:88], 'big')
        length = int.from_bytes(header[88:92], 'big')
        fp.seek(offset)
        jpeg_bytes = fp.read(length)
    
    with Image.open(BytesIO(jpeg_bytes)) as img:
        if img.mode != "RGB":
            img = img.convert("RGB")
        
        orig_w, orig_h = img.size
        
        # Read EXIF
        raw_exif = img._getexif() or {}
        fnum = raw_exif.get(33437)
        exp = raw_exif.get(33434)
        iso = raw_exif.get(34855)
        dt = raw_exif.get(36867) or raw_exif.get(306) or "2020-10-15"
        
        f_str = f"f/{float(fnum):.1f}" if fnum else "f/4.0"
        exp_str = f"{float(exp):.0f}s" if exp and float(exp) >= 1 else f"{exp}s"
        
        # 1. Resize & Grade Full
        max_dim = 2048
        scale = max_dim / max(orig_w, orig_h)
        full_w, full_h = int(orig_w * scale), int(orig_h * scale)
        graded = img.resize((full_w, full_h), Image.Resampling.LANCZOS)
        
        # Tonal & Color Grading
        graded = ImageEnhance.Contrast(graded).enhance(1.08)
        graded = ImageEnhance.Color(graded).enhance(0.96)
        graded = ImageEnhance.Sharpness(graded).enhance(1.15)
        
        out_name = f"{idx+1:02d}_{fname.replace('.RAF', '')}.webp"
        target_full = os.path.join(TARGET_DIR, out_name)
        target_thumb = os.path.join(THUMBS_DIR, out_name)
        
        graded.save(target_full, "WEBP", quality=85)
        
        # 2. Thumbnail
        thumb_dim = 800
        scale_t = thumb_dim / max(orig_w, orig_h)
        tw, th = int(orig_w * scale_t), int(orig_h * scale_t)
        thumb = img.resize((tw, th), Image.Resampling.LANCZOS)
        thumb = ImageEnhance.Contrast(thumb).enhance(1.06)
        thumb.save(target_thumb, "WEBP", quality=80)
        
        photos_list.append({
            "id": f"cide_{idx+1:02d}",
            "index": idx + 1,
            "title": f"Cide & Gideros Koyu • Kare {idx+1:02d}",
            "caption": caption,
            "src": f"/gallery/cide-gideros-koyu/{out_name}",
            "thumb": f"/gallery/cide-gideros-koyu/thumbs/{out_name}",
            "width": full_w,
            "height": full_h,
            "aspectRatio": round(full_w / full_h, 3),
            "orientation": "horizontal" if full_w >= full_h else "vertical",
            "dateTaken": dt.replace(":", "-", 2),
            "exif": {
                "camera": "Fujifilm GFX 50R",
                "make": "FUJIFILM",
                "lens": "GF50mmF3.5 R LM WR",
                "fNumber": f_str,
                "exposureTime": exp_str,
                "iso": str(iso),
                "focalLength": "50 mm",
                "focalLength35mm": "40 mm (35mm eşdeğeri)",
                "exposureProgram": "Manual",
                "meteringMode": "Multi-segment",
                "whiteBalance": "Auto",
                "flash": "No Flash",
                "software": "Adobe Lightroom / Film Simulation",
                "artist": "Ozan Özdil",
                "copyright": "© 2026 Ozan Özdil. Tüm hakları saklıdır. İzinsiz kopyalanamaz.",
                "dateTimeOriginal": dt.replace(":", "-", 2)
            }
        })

new_album = {
    "id": "cide-gideros-koyu",
    "slug": "cide-gideros-koyu",
    "title": "Cide & Gideros Koyu",
    "location": "Cide, Kastamonu",
    "locationFull": "Cide & Gideros Koyu, Kastamonu",
    "year": "2020",
    "dateFormatted": "Ekim 2020",
    "equipment": "Fujifilm GFX 50R • GF50mmF3.5 R LM WR",
    "description": "Cide & Gideros Koyu – Karadeniz'in Vahşi Kıyılarında Uzun Pozlama\n\nKastamonu'nun batı kıyısında yer alan Cide ve antik çağlardan beri denizcilerin doğal sığınağı olan Gideros Koyu, Karadeniz'in en dramatik jeolojik oluşumlarına ev sahipliği yapar. Sarp kireçtaşı falezler, yoğun kestane ve çam ormanlarının denize dikey kavuştuğu koylar, fotoğrafçılar için zamansız bir görsel şölen sunar.\n\nBu seride, yoğun ND filtreler kullanılarak 55 saniyeden 190 saniyeye varan ultra uzun gündüz pozlamaları gerçekleştirilmiştir. Karadeniz'in hırçın dalgaları ipeksi bir sis tabakasına dönüşürken, asırlık kayalıkların heykelsi dokusu orta format sensörün tüm dinamik aralığıyla belgelenmiştir.",
    "coverPhoto": photos_list[2]["thumb"], # Long exposure cover
    "photoCount": len(photos_list),
    "dateCreated": 1602758400,
    "dateUpdated": 1602758400,
    "shootDate": "2020-10-15 10:05:00",
    "photos": photos_list
}

with open(DATA_FILE, "r", encoding="utf-8") as f:
    catalog = json.load(f)

# Replace if exists, or append
existing_slugs = [a["slug"] for a in catalog["albums"]]
if "cide-gideros-koyu" in existing_slugs:
    catalog["albums"] = [a for a in catalog["albums"] if a["slug"] != "cide-gideros-koyu"]

catalog["albums"].append(new_album)

# Sort albums descending: latest first
catalog["albums"].sort(key=lambda a: (int(a.get("year", 0)), a.get("dateCreated", 0)), reverse=True)

catalog["totalAlbums"] = len(catalog["albums"])
catalog["totalPhotos"] = sum(a["photoCount"] for a in catalog["albums"])

years_set = sorted(list(set(a["year"] for a in catalog["albums"])), reverse=True)
catalog["years"] = years_set

# Collect unique cameras and lenses for tag system
cameras_set = sorted(list(set(p["exif"]["camera"] for a in catalog["albums"] for p in a["photos"])))
lenses_set = sorted(list(set(p["exif"]["lens"].strip() for a in catalog["albums"] for p in a["photos"] if p["exif"]["lens"] != "-")))

catalog["cameras"] = cameras_set
catalog["lenses"] = lenses_set

with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(catalog, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully added Cide & Gideros Koyu! Total albums: {catalog['totalAlbums']}, Total photos: {catalog['totalPhotos']}")
print(f"Cameras: {cameras_set}")
print(f"Lenses: {lenses_set}")
