import os
from io import BytesIO
from PIL import Image, ExifTags

BASE = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm"

def parse_raf_exif(raf_path):
    try:
        with open(raf_path, 'rb') as f:
            header = f.read(128)
            offset = int.from_bytes(header[84:88], byteorder='big')
            length = int.from_bytes(header[88:92], byteorder='big')
            if offset > 0 and length > 0:
                f.seek(offset)
                jpeg_data = f.read(length)
                with Image.open(BytesIO(jpeg_data)) as img:
                    raw_exif = img._getexif()
                    if not raw_exif:
                        return None
                    
                    date = raw_exif.get(36867) or raw_exif.get(306) or "-"
                    model = raw_exif.get(272) or "-"
                    lens = raw_exif.get(42036) or "-"
                    f_num = raw_exif.get(33437)
                    exp = raw_exif.get(33434)
                    iso = raw_exif.get(34855)
                    gps_raw = raw_exif.get(34853)
                    
                    gps_coords = None
                    if gps_raw:
                        # Extract lat/lon if present
                        lat_ref = gps_raw.get(1)
                        lat = gps_raw.get(2)
                        lon_ref = gps_raw.get(3)
                        lon = gps_raw.get(4)
                        if lat and lon:
                            def to_deg(d):
                                return float(d[0]) + float(d[1])/60.0 + float(d[2])/3600.0
                            lat_val = to_deg(lat) * (-1 if lat_ref == 'S' else 1)
                            lon_val = to_deg(lon) * (-1 if lon_ref == 'W' else 1)
                            gps_coords = (round(lat_val, 5), round(lon_val, 5))
                            
                    return {
                        "date": str(date),
                        "model": str(model),
                        "lens": str(lens),
                        "f": f"f/{float(f_num):.1f}" if f_num else "-",
                        "exp": f"{exp}s" if exp else "-",
                        "iso": str(iso) if iso else "-",
                        "gps": gps_coords
                    }
    except Exception as e:
        return None

results = []

for root, dirs, files in os.walk(BASE):
    raf_files = sorted([f for f in files if f.lower().endswith('.raf')])
    jpg_files = sorted([f for f in files if f.lower().endswith(('.jpg', '.jpeg'))])
    
    total = len(raf_files) + len(jpg_files)
    if total == 0:
        continue
        
    rel_folder = os.path.relpath(root, BASE)
    
    # Sample first and last RAF for date span
    first_meta = None
    last_meta = None
    lenses_in_folder = set()
    gps_found = None
    
    target_files = raf_files if raf_files else jpg_files
    
    # Check sample files
    sample_indices = [0, len(target_files)//2, len(target_files)-1]
    for idx in set(sample_indices):
        fpath = os.path.join(root, target_files[idx])
        m = parse_raf_exif(fpath) if fpath.lower().endswith('.raf') else None
        if m:
            if not first_meta:
                first_meta = m
            last_meta = m
            if m["lens"] and m["lens"] != "-":
                lenses_in_folder.add(m["lens"])
            if m["gps"]:
                gps_found = m["gps"]

    results.append({
        "folder": rel_folder,
        "total": total,
        "raf": len(raf_files),
        "jpg": len(jpg_files),
        "startDate": first_meta["date"] if first_meta else "-",
        "endDate": last_meta["date"] if last_meta else "-",
        "camera": first_meta["model"] if first_meta else "-",
        "lenses": list(lenses_in_folder),
        "gps": gps_found
    })

# Sort by folder
results.sort(key=lambda x: x["folder"])

print(f"{'KLASÖR':<40} | {'DOSYA':<8} | {'TARİH':<20} | {'KAMERA':<12} | {'LENS':<24} | {'GPS'}")
print("-" * 120)

for r in results:
    l_str = ", ".join(r["lenses"]) if r["lenses"] else "-"
    gps_str = f"{r['gps'][0]},{r['gps'][1]}" if r["gps"] else "-"
    date_str = r['startDate'].split(' ')[0] if r['startDate'] != '-' else '-'
    print(f"{r['folder']:<40} | {r['total']:<8} | {date_str:<20} | {r['camera']:<12} | {l_str[:24]:<24} | {gps_str}")
