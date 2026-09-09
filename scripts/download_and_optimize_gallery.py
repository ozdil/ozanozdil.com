import os
import re
import json
import urllib.request
from io import BytesIO
from PIL import Image

API_KEY = "3954ec9c533459f470080bf24178df16"
USER_ID = "204447030@N04"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_GALLERY_DIR = os.path.join(BASE_DIR, "public", "gallery")
DATA_FILE = os.path.join(BASE_DIR, "src", "data", "gallery.json")

def slugify(text):
    text = text.lower()
    replacements = {
        'ç': 'c', 'ğ': 'g', 'ı': 'i', 'ö': 'o', 'ş': 's', 'ü': 'u',
        'İ': 'i', 'I': 'i'
    }
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode('utf-8'))

def get_full_exif(photo_id):
    url = f"https://www.flickr.com/services/rest/?method=flickr.photos.getExif&api_key={API_KEY}&photo_id={photo_id}&format=json&nojsoncallback=1"
    
    tags = {
        "camera": "Fujifilm GFX 50R",
        "make": "FUJIFILM",
        "lens": "-",
        "fNumber": "-",
        "exposureTime": "-",
        "iso": "-",
        "focalLength": "-",
        "focalLength35mm": "-",
        "exposureProgram": "Manual",
        "meteringMode": "-",
        "whiteBalance": "Auto",
        "flash": "No Flash",
        "software": "Adobe Lightroom",
        "artist": "Ozan Özdil",
        "copyright": "Ozan Özdil",
        "dateTimeOriginal": "-"
    }
    
    try:
        data = fetch_json(url)
        if "photo" in data and "exif" in data["photo"]:
            photo_data = data["photo"]
            if photo_data.get("camera"):
                tags["camera"] = photo_data["camera"]
            
            for item in photo_data["exif"]:
                t = item.get("tag")
                val = item.get("clean", {}).get("_content") or item.get("raw", {}).get("_content", "-")
                
                if t == "Model":
                    tags["camera"] = f"Fujifilm {val}" if not val.lower().startswith("fuji") else val
                elif t == "Make":
                    tags["make"] = val
                elif t == "LensModel" or t == "Lens":
                    tags["lens"] = val
                elif t == "FNumber":
                    tags["fNumber"] = val if val.startswith("f/") else f"f/{val}"
                elif t == "ExposureTime":
                    tags["exposureTime"] = val if ("s" in val or "/" in val) else f"{val}s"
                elif t == "ISO" or t == "StandardOutputSensitivity":
                    tags["iso"] = val
                elif t == "FocalLength":
                    tags["focalLength"] = val
                elif t == "FocalLengthIn35mmFormat":
                    tags["focalLength35mm"] = f"{val} (35mm eşdeğeri)"
                elif t == "ExposureProgram":
                    tags["exposureProgram"] = val
                elif t == "MeteringMode":
                    tags["meteringMode"] = val
                elif t == "WhiteBalance":
                    tags["whiteBalance"] = val
                elif t == "Flash":
                    tags["flash"] = val
                elif t == "Software":
                    tags["software"] = val
                elif t == "Artist" or t == "By-line":
                    tags["artist"] = val
                elif t == "DateTimeOriginal":
                    tags["dateTimeOriginal"] = val
    except Exception as e:
        print(f"  [WARN] EXIF fetch for {photo_id}: {e}")
    
    return tags

# Photo contextual description generator based on album and index
def get_photo_context(album_slug, idx, total, exif):
    contexts = {
        "agli-fortress": [
            "Ağlı Kalesi zirvesinden vadiye ve sıradağlara doğru geniş açı gece çekimi. 60 saniyelik uzun pozlama ile gökyüzü ve kayalık dokusu.",
            "Ortaçağ savunma surlarının kalıntıları ve gece gökyüzünün birleştiği anıt kompozisyon.",
            "Tarihi taş duvarların dokusu ve ufuk çizgisi.",
            "Kalenin doğal savunma hattı oluşturan sarp kayalık yamaçları.",
            "Doğanın ve tarihin iç içe geçtiği Ağlı coğrafyasında zamansız bir kare.",
            "Yüksek rakımdan Kastamonu dağ silsilelerine bakış.",
            "Gece ışığında kalenin silüeti ve derinlik hissi.",
            "Kalenin gözetleme noktalarından birine odaklanan perspektif.",
            "Ağlı Kalesi'nin rüzgarlı tepesinden panoramik gece kapanış karesi."
        ],
        "seyh-saban-i-veli-mosque": [
            "Şeyh Şaban-ı Veli Külliyesi genel giriş cephesi ve avlu perspektifi.",
            "Tarihi cami taç kapısı ve Osmanlı taş işçiliği detayları.",
            "Külliyenin manevi dinginliğini yansıtan avlu revakları ve kemer yapıları.",
            "Türbe ve dergah yapılarının mimari uyumu.",
            "Cami iç mekanında ahşap sütunlar ve huzur veren aydınlatma.",
            "Tarihi şadırvan ve çevre dokusu.",
            "Külliyenin ahşap bindirme saçakları ve kiremit çatı dokuları.",
            "İç mekan kalem işleri ve hat sanatı levhaları.",
            "Ziyaretgahın taş döşemeli patikası ve asırlık çınar ağaçları gölgesi.",
            "Mihrap ve minber ahşap oymacılığı detayı.",
            "Akşam ışığında külliyenin sıcak ve samimi atmosferi.",
            "Tarihi konak mimarisiyle bütünleşen dergah binaları.",
            "Sufi geleneğinin sadelik felsefesini yansıtan pencere detayları.",
            "Külliyenin Kastamonu şehir silüetiyle buluştuğu nokta.",
            "Şeyh Şaban-ı Veli Külliyesi'nin asırlara meydan okuyan vakur duruşu."
        ],
        "nasrullah-meydani": [
            "Nasrullah Meydanı ve tarihi Nasrullah Camii genel görünümü.",
            "1506 tarihli cami kubbe ve kemer mimarisinin meydanla ilişkisi.",
            "Tarihi şadırvanın sekizgen mermer havuzu ve su kemerleri.",
            "Meydandaki tarihi Nasrullah Köprüsü ve dere yatağı akışı.",
            "Kastamonu geleneksel kent dokusu ve meydanın günlük ritmi.",
            "Tarihi taş revakların altında oluşan gölge ve ışık oyunları.",
            "Milli Mücadele'de Mehmet Akif Ersoy'un vaaz verdiği tarihi mekanın atmosferi.",
            "Nasrullah Meydanı'nın tarihi saat kulesine uzanan panoramik bakışı."
        ],
        "mahmutbey-camii": [
            "Mahmutbey Camii (Kasaba Köyü) - 1366 Candaroğulları dönemine ait ahşap bindirme mimari.",
            "Tek bir çivi dahi kullanılmadan (kündekari tekniği) inşa edilen ahşap taşıyıcı sütunlar.",
            "Kök boyası ile bezenmiş Selçuklu ve Beylikler dönemi geometrik tavan nakışları.",
            "Ahşap konsollar ve kirişlerin geometrik birbirine geçme detayları.",
            "Tarihi ahşap minber ve oyma işçiliğinin üstün ustalığı.",
            "Cami mahfili ve kadınlar mahfiline çıkan ahşap merdiven detayları.",
            "Yüzyıllardır canlılığını koruyan bitkisel ve geometrik motifler.",
            "İç mekanın loş ışıkta ahşabın sıcaklığıyla oluşan mistik ortamı.",
            "UNESCO Dünya Mirası Listesi'nde yer alan benzersiz çivisiz cami mimarisinin kubbe geçişleri.",
            "Tavan kirişlerindeki kırmızı, siyah ve aşı boyası renk ahengi.",
            "Ahşap sütun başlıklarındaki stalaktit (mukarnas) oyma sanatı.",
            "Caminin dış taş duvarları ve köy dokusundaki mütevazı dış görünümü.",
            "Anadolu Türk ahşap sanatının zirvesi: Mahmutbey Camii tavan kompozisyonu."
        ]
    }
    album_list = contexts.get(album_slug, [])
    if idx < len(album_list):
        return album_list[idx]
    return f"{album_slug.replace('-', ' ').title()} serisinden {idx + 1}. fotoğraf karesi."

def main():
    os.makedirs(PUBLIC_GALLERY_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

    print("Fetching album list from Flickr...")
    albums_url = f"https://www.flickr.com/services/rest/?method=flickr.photosets.getList&api_key={API_KEY}&user_id={USER_ID}&format=json&nojsoncallback=1"
    albums_data = fetch_json(albums_url)
    
    raw_albums = albums_data.get("photosets", {}).get("photoset", [])
    print(f"Found {len(raw_albums)} albums.")

    catalog_albums = []

    for album in raw_albums:
        album_id = album["id"]
        album_title = album["title"]["_content"]
        album_desc = album["description"]["_content"]
        date_created = int(album.get("date_create", 0))
        date_updated = int(album.get("date_update", 0))

        slug = slugify(album_title.split(',')[0])
        print(f"\n==========================================")
        print(f"Processing album: {album_title} (Slug: {slug})")
        
        album_dir = os.path.join(PUBLIC_GALLERY_DIR, slug)
        thumbs_dir = os.path.join(album_dir, "thumbs")
        os.makedirs(album_dir, exist_ok=True)
        os.makedirs(thumbs_dir, exist_ok=True)

        photos_url = (
            f"https://www.flickr.com/services/rest/?method=flickr.photosets.getPhotos"
            f"&api_key={API_KEY}&photoset_id={album_id}&user_id={USER_ID}&format=json&nojsoncallback=1"
            f"&extras=date_taken,url_k,url_h,url_l,url_c,url_z,url_o"
        )
        photos_data = fetch_json(photos_url)
        raw_photos = photos_data.get("photoset", {}).get("photo", [])

        # Sort photos inside album ASCENDING by datetaken (chronological journey)
        sorted_photos = sorted(raw_photos, key=lambda p: p.get("datetaken", "") or "")

        album_photos = []

        for idx, p in enumerate(sorted_photos):
            photo_id = p["id"]
            date_taken = p.get("datetaken", "")

            # Highest available quality url
            img_url = p.get("url_k") or p.get("url_h") or p.get("url_l") or p.get("url_c") or p.get("url_z")
            if not img_url:
                server = p.get("server")
                secret = p.get("secret")
                img_url = f"https://live.staticflickr.com/{server}/{photo_id}_{secret}_b.jpg"

            filename = f"{idx + 1:02d}_{photo_id}.webp"
            target_path = os.path.join(album_dir, filename)
            thumb_path = os.path.join(thumbs_dir, filename)

            rel_src = f"/gallery/{slug}/{filename}"
            rel_thumb = f"/gallery/{slug}/thumbs/{filename}"

            print(f"  [{idx + 1}/{len(sorted_photos)}] Processing: {filename}")

            width, height = 2048, 1536
            if not os.path.exists(target_path) or not os.path.exists(thumb_path):
                try:
                    req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(req, timeout=30) as resp:
                        img_bytes = resp.read()

                    with Image.open(BytesIO(img_bytes)) as pil_img:
                        if pil_img.mode in ("RGBA", "P"):
                            pil_img = pil_img.convert("RGB")
                        
                        orig_w, orig_h = pil_img.size

                        # Full display standard: max 2048px (Web standard for 2K/Retina)
                        max_dim = 2048
                        if max(orig_w, orig_h) > max_dim:
                            scale = max_dim / max(orig_w, orig_h)
                            width, height = int(orig_w * scale), int(orig_h * scale)
                            full_img = pil_img.resize((width, height), Image.Resampling.LANCZOS)
                        else:
                            width, height = orig_w, orig_h
                            full_img = pil_img
                        
                        full_img.save(target_path, "WEBP", quality=85)

                        # Thumbnail standard: max 800px
                        thumb_dim = 800
                        scale_t = thumb_dim / max(orig_w, orig_h)
                        thumb_w, thumb_h = int(orig_w * scale_t), int(orig_h * scale_t)
                        thumb_img = pil_img.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                        thumb_img.save(thumb_path, "WEBP", quality=80)
                except Exception as e:
                    print(f"  [ERROR] Failed to process {img_url}: {e}")
            else:
                try:
                    with Image.open(target_path) as existing_img:
                        width, height = existing_img.size
                except Exception:
                    pass

            # Fetch Comprehensive Full EXIF
            exif = get_full_exif(photo_id)
            if date_taken and exif["dateTimeOriginal"] == "-":
                exif["dateTimeOriginal"] = date_taken

            # Specific descriptive caption
            photo_caption = get_photo_context(slug, idx, len(sorted_photos), exif)
            custom_title = f"{album_title.split(',')[0]} • Kare {idx + 1:02d}"

            album_photos.append({
                "id": photo_id,
                "index": idx + 1,
                "title": custom_title,
                "caption": photo_caption,
                "src": rel_src,
                "thumb": rel_thumb,
                "width": width,
                "height": height,
                "aspectRatio": round(width / max(height, 1), 3),
                "orientation": "horizontal" if width >= height else "vertical",
                "dateTaken": date_taken,
                "exif": exif
            })

        dates = [p["dateTaken"] for p in album_photos if p.get("dateTaken")]
        shoot_date = dates[0] if dates else ""
        cover_photo = album_photos[0]["thumb"] if album_photos else ""

        catalog_albums.append({
            "id": album_id,
            "slug": slug,
            "title": album_title,
            "shortTitle": album_title.split(',')[0],
            "description": album_desc,
            "coverPhoto": cover_photo,
            "photoCount": len(album_photos),
            "dateCreated": date_created,
            "dateUpdated": date_updated,
            "shootDate": shoot_date,
            "photos": album_photos
        })

    # Sort albums DESCENDING (Latest first: "son galeri en başta")
    catalog_albums.sort(key=lambda a: a.get("dateCreated", 0), reverse=True)

    print(f"\nSaving full catalog to {DATA_FILE}...")
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({
            "updatedAt": "2026-09-09",
            "totalAlbums": len(catalog_albums),
            "totalPhotos": sum(a["photoCount"] for a in catalog_albums),
            "albums": catalog_albums
        }, f, ensure_ascii=False, indent=2)

    total_size = 0
    for root, dirs, files in os.walk(PUBLIC_GALLERY_DIR):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))

    print(f"\nSuccess! Total gallery storage: {total_size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    main()
