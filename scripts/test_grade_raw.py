import os
from io import BytesIO
from PIL import Image, ImageEnhance, ImageFilter

raw_path = "/run/media/ozdil/970 EVO/USB Copy_2023-07-25_230317/Fujifilm/GFX 50r/2020/15.10.2020/_DSF0033.RAF"

with open(raw_path, 'rb') as f:
    header = f.read(128)
    offset = int.from_bytes(header[84:88], byteorder='big')
    length = int.from_bytes(header[88:92], byteorder='big')
    f.seek(offset)
    jpeg_data = f.read(length)

with Image.open(BytesIO(jpeg_data)) as img:
    if img.mode != "RGB":
        img = img.convert("RGB")
    
    print(f"Original preview size: {img.size}")
    
    # 1. Resize to Web standard (max 2048px width/height)
    max_dim = 2048
    w, h = img.size
    scale = max_dim / max(w, h)
    new_w, new_h = int(w * scale), int(h * scale)
    graded = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    
    # 2. Tone & Color Grading (Noble, Film-Like Microcontrast)
    # Contrast slightly lifted for deep velvety blacks
    enh_contrast = ImageEnhance.Contrast(graded)
    graded = enh_contrast.enhance(1.08)
    
    # Color saturation: subtle refinement (0.95 for timeless editorial feel)
    enh_color = ImageEnhance.Color(graded)
    graded = enh_color.enhance(0.96)
    
    # Sharpness: micro-detail enhancement for medium format textures
    enh_sharpness = ImageEnhance.Sharpness(graded)
    graded = enh_sharpness.enhance(1.15)
    
    out_test = "/home/ozdil/.gemini/antigravity/brain/6813f414-850d-4b36-a322-257511dbf362/scratch/test_graded.webp"
    os.makedirs(os.path.dirname(out_test), exist_ok=True)
    graded.save(out_test, "WEBP", quality=85)
    print(f"Saved graded test to {out_test}, size: {os.path.getsize(out_test) / 1024:.1f} KB")

