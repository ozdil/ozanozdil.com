import os
import io
import json
from PIL import Image, ImageOps, ImageEnhance

SSD_ROOT = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm"
PUB_GALLERY = "public/gallery"

# Define the 5 new collections to extract and curate
COLLECTIONS = [
    {
        "id": "ismail-bey-kulliyesi",
        "title": "İsmail Bey Külliyesi & Tarihi Sokaklar",
        "location": "Kastamonu Merkez",
        "locationFull": "İsmail Bey Külliyesi, Kastamonu Merkez",
        "dateFormatted": "Ağustos 2020",
        "year": "2020",
        "equipment": "Fujifilm GFX 100 • GF23mmF4 R LM WR",
        "description": "Candaroğulları Beyliği'nin son hükümdarı Kemaleddin İsmail Bey tarafından 1454 yılında inşa ettirilen külliye; cami, türbe, medrese, imaret ve Deve Hanı ile Kastamonu'nun en kıymetli anıtsal miraslarındandır.\n\n102 megapiksellik Fujifilm GFX 100 orta format gövde ve GF23mm f/4 ultra geniş açı lens ile kaydedilen bu seride, taş işçiliği, kubbe hat sanatı, kündekari detaylar ve külliyenin etrafını saran tarihi Kastamonu sokakları belgelenmiştir.",
        "folder": "GFX 100/27.08.2020",
        "selected_files": [
            ("_DSF0079.RAF", "İsmail Bey Külliyesi • Dış Cephe & Minare", "1454 yapımı külliyenin kesme taş duvarları ve tek şerefeli zarif minaresi."),
            ("_DSF0080.RAF", "Deve Hanı & Külliye Giriş Avlusu", "İpek Yolu tüccarlarının konakladığı tarihi Deve Hanı'nın taş revakları."),
            ("_DSF0083.RAF", "Külliye Haziresi & Selvi Ağaçları", "Asırlık selvilerin gölgesinde Candaroğulları hanedan mezarları."),
            ("_DSF0086.RAF", "Deve Hanı • Taş Kapı & Merdivenler", "Orta format detaycılığıyla taş blokların beş asırlık aşınma izleri."),
            ("_DSF0090.RAF", "İsmail Bey Türbesi • Sandukalar & Kubbe", "Kemaleddin İsmail Bey ve ailesinin medfun bulunduğu kubbeli türbe içi."),
            ("_DSF0092.RAF", "Kubbe Kalem İşi & Osmanlı Hat Sanatı", "Külliye camiinin kubbesini çevreleyen özgün geometrik kalem işleri."),
            ("_DSF0097.RAF", "Mihrap & Kündekari Ahşap İşçiliği", "Anadolu Beylikleri döneminin usta ahşap oymacılığını yansıtan mihrap detayı."),
            ("_DSF0104.RAF", "Cami İç Mekanı • Işık & Vitray Pencereler", "Taş kemerlerden süzülen doğal ikindi ışığı ve halı dokusu."),
            ("_DSF0113.RAF", "Külliye Taş Duvarı & Sokak Perspektifi", "Külliyeyi çevreleyen dar sokaklar ve tarihi mahalle dokusu."),
            ("_DSF0148.RAF", "Kastamonu Ahşap Konak Sokağı • Kapanış", "Külliye çevresindeki geleneksel cumbalı Kastamonu sivil mimarisi.")
        ]
    },
    {
        "id": "ilica-selalesi",
        "title": "Ilıca Şelalesi & Horma Kanyonu Suları",
        "location": "Pınarbaşı, Kastamonu",
        "locationFull": "Ilıca Şelalesi, Küre Dağları Milli Parkı, Pınarbaşı",
        "dateFormatted": "Ekim 2020",
        "year": "2020",
        "equipment": "Fujifilm GFX 50R • GF50mmF3.5 R LM WR",
        "description": "Küre Dağları Milli Parkı sınırları içerisinde, Horma Kanyonu'nun çıkış noktasında yer alan Ilıca Şelalesi; yaklaşık 15 metre yükseklikten yosun tutmuş dev kireçtaşı kayaların arasından zümrüt yeşili bir gölete dökülür.\n\nFujifilm GFX 50R ve GF50mm f/3.5 ile 60 ila 90 saniye arasında değişen uzun pozlamalarla kaydedilen bu seride, suyun ipeksi akışı ve nemli kanyon ekosisteminin zengin dokusu ölümsüzleştirilmiştir.",
        "folder": "GFX 50r/2020/12.10.2020",
        "selected_files": [
            ("_DSF0206.RAF", "Ilıca Şelalesi • 61s Kadife Dökülüş", "Yosun kaplı kireçtaşı kayalıklarından dökülen 61 saniyelik uzun pozlama."),
            ("_DSF0207.RAF", "Zümrüt Gölet & Su Hareketi • 87s", "Şelalenin döküldüğü doğal gölette suyun dönerek oluşturduğu köpük izleri."),
            ("_DSF0208.RAF", "Kanyon Akıntısı & Yosunlu Taşlar • 70s", "Orman altı ışığında kadifemsi suyun kayalar arasından akışı."),
            ("_DSF0209.RAF", "Şelale Çağlayanı • 91s Derin Pozlama", "91 saniyelik uzun pozlamayla mistik bir sis tabakasına dönüşen şelale."),
            ("_DSF0210.RAF", "Ilıca Kayalıkları • 90s Dikey Perspektif", "Küre Dağları kireçtaşı jeolojisini ve dik kaya yüzeylerini gösteren açı."),
            ("_DSF0211.RAF", "Kanyon Havzası • Anlık Enstantane", "Suyun berraklığını ve dipteki çakıl taşlarını donduran 1/250s anlık kare."),
            ("_DSF0213.RAF", "Orman İçi Akarsu Yatağı • 32s", "Kanyon tabanında sonbahar yaprakları ve berrak dağ suyu."),
            ("_DSF0214.RAF", "Şelale Tülü & Kayalık Duvar • 90s", "Kayanın dokusuyla suyun pürüzsüzlüğünün oluşturduğu yüksek dinamik aralık."),
            ("_DSF0215.RAF", "Ilıca Göleti Masmavi Durgunluk • 90s", "Kanyonun derinliklerinde zümrüt yeşilinden laciverte dönen gölet yüzeyi."),
            ("_DSF0216.RAF", "Kanyon Çıkışı & Sonbahar Işığı • 60s", "Seriyi tamamlayan 60 saniyelik dingin orman ve su manzarası.")
        ]
    },
    {
        "id": "nasrullah-camii-ic-mekan",
        "title": "Nasrullah Camii Külliyesi & Kündekari Sanatı",
        "location": "Kastamonu Kent Merkezi",
        "locationFull": "Nasrullah Camii, Kent Meydanı, Kastamonu",
        "dateFormatted": "Kasım 2020",
        "year": "2020",
        "equipment": "Fujifilm GFX 50R • GF50mmF3.5 R LM WR",
        "description": "1506 yılında Kadı Nasrullah tarafından inşa ettirilen ve Kurtuluş Savaşı döneminde Mehmet Akif Ersoy'un vaazlar vererek milli mücadele ateşini yaktığı anıt mabet.\n\nCaminin sedef kakmalı kündekari minberi, devasa kristal avizesi, kubbe kalem işleri ve tarihi taş taç kapısı, Fujifilm GFX 50R orta format kameranın geniş dinamik aralığıyla belgelenmiştir.",
        "folder": "GFX 50r/2020/09.11.2020",
        "selected_files": [
            ("_DSF0149.RAF", "Nasrullah Camii • Anıtsal Mermer Taç Kapı", "Osmanlı tuğrası ve hat kitabesiyle taçlandırılmış tarihi giriş kapısı."),
            ("_DSF0150.RAF", "Cami İç Mekanı • Kubbeler & Avize İhtişamı", "Çok kubbeli ulu cami mimarisi ve mekanı aydınlatan devasa kristal avize."),
            ("_DSF0151.RAF", "Mihrap & Hat Kuşağı Perspektifi", "Caminin güney duvarında yer alan klasik Osmanlı mihrap süslemeleri."),
            ("_DSF0152.RAF", "Kündekari Sedef Kakma Minber • Detay", "Ahşapların birbirine çivisiz geçmesiyle yapılan kündekari sanatının zirvesi."),
            ("_DSF0156.RAF", "Minber Merdiveni & Ahşap Korkuluk Oymaları", "Geometrik yıldız motifleri ve fildişi/sedef kakma işlemeler."),
            ("_DSF0158.RAF", "Kubbe Kalem İşi • Rumi & Palmet Motifleri", "Kubbe tonozunda Kastamonulu nakkaşların elinden çıkmış tarihi motifler."),
            ("_DSF0160.RAF", "Merkezi Avize Simetrisi & Tavan Detayı", "Göz hizasından doğrudan tavana yönelen kusursuz dikey geometrik simetri."),
            ("_DSF0163.RAF", "Kürsü & Cami İçi Ahşap Sütun Detayı", "Vaaz kürsüsünün ahşap oymacılık detayları ve ortam ışığı."),
            ("_DSF0167.RAF", "Halı Deseni & Kemer Gölgeleri", "Geniş saflar üzerinde iç mekan ışık-gölge dengesi."),
            ("_DSF0171.RAF", "Giriş Revakları & Avlu Işığı • Kapanış", "Mabedin serin iç mekanından güneşli dış avluya açılan kemerli kapı.")
        ]
    },
    {
        "id": "ilgaz-dagi-zirvesi",
        "title": "Ilgaz Dağı Zirvesi & Kış Bulut Denizi",
        "location": "Ilgaz Dağı Milli Parkı",
        "locationFull": "Küçük Hacet & Büyük Hacet Dorukları, Ilgaz Dağı (2587m)",
        "dateFormatted": "Ocak 2021",
        "year": "2021",
        "equipment": "Fujifilm GFX 100 • GF50mm & GF23mm",
        "description": "Anadolu'nun kadim ve şarkılara konu olan ulu dağı Ilgaz (2587m), kış aylarında zirveleri aşan bir bulut denizine ve saf kar beyazlığına bürünür.\n\nFujifilm GFX 100 102MP ve GFX 50R ile eksi 15 derecede çekilen bu karelerde; f/22 ve f/32 diyaframlarla elde edilen optik güneş patlamaları, rüzgarın şekillendirdiği kar sırtları ve ufukta dağ doruklarını adalar gibi bırakan bulut denizi sergilenmektedir.",
        "folder": "GFX 100/23.01.2021",
        "selected_files": [
            ("_DSF1412.RAF", "Ilgaz Doruğu • f/32 Optik Güneş Patlaması", "Kar beyazlığı üzerinde gökyüzünün derin mavisi ve 14 kollu optik yıldız patlaması."),
            ("_DSF1413.RAF", "Bulut Denizi Üzerinde Zirve Sırtları", "Vadiyi tamamen örten bulut katmanının üzerinde yükselen Ilgaz sırtları."),
            ("_DSF1414.RAF", "Rüzgar Şekilli Kar Katmanları (Sastrugi)", "Sert kış rüzgarlarının donmuş kar üzerinde bıraktığı dalga dokuları."),
            ("_DSF1415.RAF", "Ufuk Hattı & Sonsuz Beyazlık", "Kar çizgisinin gökyüzüyle birleştiği yüksek irtifa panoraması."),
            ("_DSF1418.RAF", "Küçük Hacet Doruğuna Bakış", "2546 metrelik doruğun sarp kuzey yamaçları ve kar siperleri."),
            ("_DSF1420.RAF", "Kış Işığı & Dağ Gölgeleri", "Öğle güneşinin dik açısında kar kristallerinin oluşturduğu parıltı."),
            ("_DSF1422.RAF", "Dorukta Donmuş Rüzgar Bayrağı", "Tipi sonrası kayaların üzerinde oluşan buz ve kırağı tabakası."),
            ("_DSF1423.RAF", "Bulutların Dansı & Ilgaz Masifi", "Zirvenin etrafında sürekli yön değiştiren sis ve bulut akışı."),
            ("_DSF1424.RAF", "Yüksek İrtifa Güneşi & Zirve Aynası", "102 megapiksel çözünürlükle en ince kar tanelerine kadar keskin detay."),
            ("_DSF1426.RAF", "Ilgaz Kış Panoraması • Kapanış", "Kastamonu ile Çankırı'yı ayıran kadim dağ silsilesine veda karesi.")
        ]
    },
    {
        "id": "kure-daglari-gece-gokyuzu",
        "title": "Küre Dağları Yaylası & Samanyolu Gece Çekimleri",
        "location": "Küre Dağları Yaylaları",
        "locationFull": "Küre Dağları Milli Parkı Yaylaları, Kastamonu",
        "dateFormatted": "Eylül 2025",
        "year": "2025",
        "equipment": "Fujifilm GFX 50R • GF55mmF1.7 & GF20-35mmF4",
        "description": "Küre Dağları'nın ışık kirliliğinden tamamen izole, 1500 metre rakımlı bakir yaylalarında kurulan gece kampı ve gökyüzü gözlemi.\n\nFujifilm GFX 50R gövde, f/1.7 ultra diyaframlı GF55mm lens ve GF20-35mm ultra geniş açı ile 30 saniyeden 15 dakikaya (900s) uzanan pozlamalar yapılmıştır. Gece çadır ışıkları, kamp ateşi, göl yansımaları ve Samanyolu galaksisinin ihtişamlı sarmalı kaydedilmiştir.",
        "folder": "GFX 50r/2025/Eylül",
        "selected_files": [
            ("_DSF2276.RAF", "Yayla Kampı & Gökyüzü Işıkları • 120s", "Orman kenarında kurulan kamp çadırı ve 120 saniyelik gece atmosferi."),
            ("_DSF2277.RAF", "Samanyolu Galaksisi & Çam Silüetleri • 240s", "Küre Dağları gök kubbesinde beliren Samanyolu sarmalı ve ulu göknarlar."),
            ("_DSF2278.RAF", "Işıkla Boyama & Kamp Ateşi • 480s", "8 dakikalık uzun pozlamada çadırların etrafında ışıkla çizilen büyüleyici izler."),
            ("_DSF2280.RAF", "Derin Uzay & Yıldız Tarlası • 480s", "Işık kirliliğinden arınmış gökyüzünde milyonlarca yıldızın kristal ışıltısı."),
            ("_DSF2285.RAF", "Gece Kampı Dinginliği • 30s", "Gece yarısı gökyüzü ve çadırın sıcak aydınlatması."),
            ("_DSF2292.RAF", "GF55mm f/1.7 ile Samanyolu Çekirdeği • 30s", "f/1.7 açık diyaframla gökyüzünden toplanan saf fotonlar ve nebulalar."),
            ("_DSF2293.RAF", "Göknar Ağaçları & Gece Işıltısı • 30s", "Ormanın heybetli duruşu ve arkasında parıldayan yıldız kümeleri."),
            ("_DSF2298.RAF", "Yıldız Işığında Yayla Dokusu • 15s", "Karanlıkta dahi orta format sensörün ayırt ettiği zengin yayla çayırları."),
            ("_DSF2305.RAF", "Şafak Vakti Yayla Sisleri • 0.5s", "Güneş doğarken yayla çanağına çöken sabah sisi ve ilk ışıklar."),
            ("_DSF2308.RAF", "Sonbahar Renkleri & Sabah Işığı • Kapanış", "Geceyi uğurlayan altın sarısı sabah ışığında Küre Dağları florası.")
        ]
    }
]

def process_and_add_collections():
    with open("src/data/gallery.json", "r") as f:
        gallery_data = json.load(f)

    existing_album_ids = [a["id"] for a in gallery_data["albums"]]

    for col in COLLECTIONS:
        album_id = col["id"]
        target_dir = os.path.join(PUB_GALLERY, album_id)
        thumbs_dir = os.path.join(target_dir, "thumbs")
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(thumbs_dir, exist_ok=True)
        
        folder_path = os.path.join(SSD_ROOT, col["folder"])
        photos_list = []
        
        print(f"\n==========================================")
        print(f"Processing Collection: {col['title']} ({len(col['selected_files'])} frames)")
        print(f"Folder: {col['folder']}")
        print(f"==========================================")
        
        for idx, (fname, p_title, p_caption) in enumerate(col["selected_files"]):
            fpath = os.path.join(folder_path, fname)
            if not os.path.exists(fpath):
                print(f"WARNING: File {fpath} does not exist! Skipping...")
                continue
                
            with open(fpath, "rb") as fp:
                header = fp.read(128)
                offset = int.from_bytes(header[84:88], "big")
                length = int.from_bytes(header[88:92], "big")
                fp.seek(offset)
                jpeg_bytes = fp.read(length)
                
            with Image.open(io.BytesIO(jpeg_bytes)) as raw_img:
                # 1. READ EXIF FROM RAW JPEG BEFORE TRANSPOSE
                raw_exif = raw_img._getexif() or {}
                fnum = raw_exif.get(33437)
                exp = raw_exif.get(33434)
                iso = raw_exif.get(34855)
                foc = raw_exif.get(37386)
                foc35 = raw_exif.get(41989)
                dt = raw_exif.get(36867) or raw_exif.get(306) or "2020-10-15 12:00:00"
                lens_name = str(raw_exif.get(42036, "")).replace("\x00", "").strip()
                camera_name = str(raw_exif.get(272, "")).strip() or "Fujifilm GFX"
                
                f_str = f"f/{float(fnum):.1f}" if fnum else "f/4.0"
                if exp:
                    exp_val = float(exp)
                    if exp_val >= 1:
                        exp_str = f"{exp_val:.0f}s" if exp_val.is_integer() else f"{exp_val:.1f}s"
                    else:
                        exp_str = f"1/{int(round(1.0 / exp_val))}s"
                else:
                    exp_str = "1/125s"

                # 2. CRITICAL STEP: EXIF ORIENTATION TRANSPOSE (DIKEY / YATAY DÜZELTME)
                img = ImageOps.exif_transpose(raw_img)
                if img.mode != "RGB":
                    img = img.convert("RGB")
                
                orig_w, orig_h = img.size
                
                # 3. RESIZE & GRADE FULL RESOLUTION (max 2048px)
                max_dim = 2048
                scale = max_dim / max(orig_w, orig_h)
                full_w, full_h = int(orig_w * scale), int(orig_h * scale)
                graded = img.resize((full_w, full_h), Image.Resampling.LANCZOS)
                
                # Film-grade toning
                graded = ImageEnhance.Contrast(graded).enhance(1.08)
                graded = ImageEnhance.Color(graded).enhance(0.96)
                graded = ImageEnhance.Sharpness(graded).enhance(1.15)
                
                clean_fname = fname.replace(".RAF", "").lstrip("_")
                out_name = f"{idx+1:02d}_{clean_fname}.webp"
                target_full = os.path.join(target_dir, out_name)
                target_thumb = os.path.join(thumbs_dir, out_name)
                
                graded.save(target_full, "WEBP", quality=85)
                
                # 4. THUMBNAIL (max 800px)
                thumb_dim = 800
                scale_t = thumb_dim / max(orig_w, orig_h)
                tw, th = int(orig_w * scale_t), int(orig_h * scale_t)
                thumb = img.resize((tw, th), Image.Resampling.LANCZOS)
                thumb = ImageEnhance.Contrast(thumb).enhance(1.06)
                thumb.save(target_thumb, "WEBP", quality=80)
                
                is_vert = full_h > full_w
                print(f"  [{idx+1:02d}] {out_name}: {full_w}x{full_h} ({'vertical' if is_vert else 'horizontal'}) | {camera_name} | {f_str} | {exp_str} | ISO {iso}")
                
                photos_list.append({
                    "id": f"{album_id}_{idx+1:02d}",
                    "index": idx + 1,
                    "title": p_title,
                    "caption": p_caption,
                    "src": f"/gallery/{album_id}/{out_name}",
                    "thumb": f"/gallery/{album_id}/thumbs/{out_name}",
                    "width": full_w,
                    "height": full_h,
                    "aspectRatio": round(full_w / full_h, 3),
                    "orientation": "vertical" if is_vert else "horizontal",
                    "dateTaken": dt.replace(":", "-", 2) if dt else col["dateFormatted"],
                    "exif": {
                        "camera": camera_name,
                        "make": "FUJIFILM",
                        "lens": lens_name if lens_name else col["equipment"].split("•")[1].strip(),
                        "fNumber": f_str,
                        "exposureTime": exp_str,
                        "iso": str(iso) if iso else "100",
                        "focalLength": f"{float(foc):.0f}mm" if foc else "50mm",
                        "focalLength35mm": f"{float(foc35):.0f}mm eq." if foc35 else "",
                        "dateTimeOriginal": dt,
                        "exposureProgram": "Manual" if "s" in exp_str else "Aperture Priority",
                        "meteringMode": "Multi-segment",
                        "artist": "Ozan Özdil",
                        "copyright": "© Ozan Özdil. Tüm hakları saklıdır."
                    }
                })
        
        album_obj = {
            "id": col["id"],
            "title": col["title"],
            "location": col["location"],
            "locationFull": col["locationFull"],
            "dateFormatted": col["dateFormatted"],
            "year": col["year"],
            "equipment": col["equipment"],
            "description": col["description"],
            "cover": photos_list[0]["src"],
            "coverThumb": photos_list[0]["thumb"],
            "coverAspect": photos_list[0]["aspectRatio"],
            "photoCount": len(photos_list),
            "photos": photos_list
        }
        
        # Replace if exists, else append
        if col["id"] in existing_album_ids:
            idx_exist = next(i for i, a in enumerate(gallery_data["albums"]) if a["id"] == col["id"])
            gallery_data["albums"][idx_exist] = album_obj
        else:
            gallery_data["albums"].append(album_obj)

    # Sort albums: Descending by Year / Chronology (2025 -> 2021 -> 2020)
    def album_sort_key(a):
        yr = int(a.get("year", "2020"))
        # Prioritize 2025 -> 2021 -> 2020
        # For ties, sort by id
        return (yr, a["id"])
    
    gallery_data["albums"].sort(key=album_sort_key, reverse=True)
    
    # Recalculate summary stats
    all_years = sorted(list(set(a["year"] for a in gallery_data["albums"])), reverse=True)
    all_cameras = sorted(list(set(p["exif"]["camera"] for a in gallery_data["albums"] for p in a["photos"])))
    all_lenses = sorted(list(set(p["exif"]["lens"].replace("\x00", "").strip() for a in gallery_data["albums"] for p in a["photos"] if p["exif"]["lens"] != "-")))
    
    gallery_data["years"] = all_years
    gallery_data["cameras"] = all_cameras
    gallery_data["lenses"] = all_lenses
    gallery_data["totalAlbums"] = len(gallery_data["albums"])
    gallery_data["totalPhotos"] = sum(len(a["photos"]) for a in gallery_data["albums"])

    with open("src/data/gallery.json", "w") as f:
        json.dump(gallery_data, f, indent=2, ensure_ascii=False)
        
    print(f"\nSUCCESS: Catalog updated!")
    print(f"Total Albums: {gallery_data['totalAlbums']}")
    print(f"Total Photos: {gallery_data['totalPhotos']}")
    print(f"Years: {gallery_data['years']}")
    print(f"Cameras: {gallery_data['cameras']}")
    print(f"Lenses: {gallery_data['lenses']}")

if __name__ == "__main__":
    process_and_add_collections()
