import os
import sys
from PIL import Image, ExifTags

BASE = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm"

def get_exif_sample(file_path):
    try:
        with Image.open(file_path) as img:
            exif_raw = img._getexif()
            if not exif_raw:
                return {}
            exif = {}
            for tag, val in exif_raw.items():
                name = ExifTags.TAGS.get(tag, str(tag))
                exif[name] = val
            return {
                "date": exif.get("DateTimeOriginal") or exif.get("DateTime") or "-",
                "model": exif.get("Model", "-"),
                "lens": exif.get("LensModel", "-"),
                "fNumber": exif.get("FNumber", "-"),
                "iso": exif.get("ISOSpeedRatings", "-"),
                "gps": "GPSInfo" in exif
            }
    except Exception:
        return {}

print(f"Scanning archive at: {BASE}\n")

summary = []

for root, dirs, files in os.walk(BASE):
    # Only report directories that contain images
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.raf', '.tif', '.tiff', '.png'))]
    if image_files:
        rel_path = os.path.relpath(root, BASE)
        raf_count = sum(1 for f in image_files if f.lower().endswith('.raf'))
        jpg_count = sum(1 for f in image_files if f.lower().endswith(('.jpg', '.jpeg')))
        
        # sample first jpg
        first_jpg = next((os.path.join(root, f) for f in image_files if f.lower().endswith(('.jpg', '.jpeg'))), None)
        sample_meta = get_exif_sample(first_jpg) if first_jpg else {}
        
        summary.append({
            "path": rel_path,
            "total": len(image_files),
            "raf": raf_count,
            "jpg": jpg_count,
            "meta": sample_meta
        })

print(f"Found {len(summary)} image directories:\n")
for item in sorted(summary, key=lambda x: x["path"]):
    m = item["meta"]
    meta_str = f"Date: {m.get('date', '-')} | Camera: {m.get('model', '-')} | Lens: {m.get('lens', '-')}" if m else "No JPG metadata"
    print(f"📁 {item['path']} ({item['total']} files: {item['jpg']} JPG, {item['raf']} RAF RAW)")
    if m:
        print(f"   ↳ {meta_str}")
