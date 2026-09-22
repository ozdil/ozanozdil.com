#!/usr/bin/env python3
import os
import sys
import re
from datetime import datetime

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow (PIL) bulunamadı. OG kartları üretimi atlanıyor.")
    sys.exit(0)

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(ROOT_DIR, "src", "content", "blog")
OG_DIR = os.path.join(ROOT_DIR, "public", "images", "og")
DEFAULT_OG_PATH = os.path.join(ROOT_DIR, "public", "og-image.png")
AVATAR_PATH = os.path.join(ROOT_DIR, "public", "avatar-400.webp")

os.makedirs(OG_DIR, exist_ok=True)

FONT_PATH_BOLD = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"
FONT_PATH_REG = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf"

if not os.path.exists(FONT_PATH_BOLD):
    FONT_PATH_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    FONT_PATH_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

font_title = ImageFont.truetype(FONT_PATH_BOLD, 38)
font_meta = ImageFont.truetype(FONT_PATH_BOLD, 18)
font_desc = ImageFont.truetype(FONT_PATH_REG, 21)
font_author_name = ImageFont.truetype(FONT_PATH_BOLD, 20)
font_author_role = ImageFont.truetype(FONT_PATH_REG, 16)
font_tag = ImageFont.truetype(FONT_PATH_BOLD, 16)

MONTHS_TR = {
    1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran",
    7: "Temmuz", 8: "Ağustos", 9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık"
}

def format_date_tr(iso_str):
    if not iso_str:
        return "2026"
    cleaned = iso_str.strip().strip("'\"")
    # match YYYY-MM-DD
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", cleaned)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        mo_name = MONTHS_TR.get(mo, "")
        return f"{d} {mo_name} {y}"
    return cleaned

def create_og_card(title, description, tag="// SİSTEM ARAŞTIRMALARI", date_text="2026", output_path=""):
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), "#09090b")
    draw = ImageDraw.Draw(img)

    # Main Card Box with clean borders
    draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, fill="#121215", outline="#27272a", width=2)

    # Top Bar Badge
    badge_label = tag if tag.startswith("//") else f"// #{tag.upper()}"
    badge_bbox = draw.textbbox((0, 0), badge_label, font=font_tag)
    badge_w = badge_bbox[2] - badge_bbox[0] + 32
    draw.rounded_rectangle([64, 64, 64 + badge_w, 102], radius=8, fill="#18181b", outline="#27272a", width=1)
    draw.text((80, 75), badge_label, font=font_tag, fill="#a1a1aa")

    domain_text = "ozanozdil.com"
    draw.text((W - 64 - 150, 75), domain_text, font=font_meta, fill="#71717a")

    draw.line([64, 122, W - 64, 122], fill="#27272a", width=1)

    # Title Wrap
    words = title.split()
    lines = []
    curr_line = ""
    for w in words:
        test_line = f"{curr_line} {w}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_title)
        if bbox[2] - bbox[0] > (W - 140):
            if curr_line:
                lines.append(curr_line)
            curr_line = w
        else:
            curr_line = test_line
    if curr_line:
        lines.append(curr_line)

    lines = lines[:3]
    if len(title.split()) > sum(len(l.split()) for l in lines):
        lines[-1] = lines[-1].rstrip(".,;:") + "..."

    y_text = 155
    for line in lines:
        draw.text((64, y_text), line, font=font_title, fill="#ffffff")
        y_text += 50

    # Description Wrap
    desc_words = (description or "").split()
    desc_lines = []
    curr_line = ""
    for w in desc_words:
        test_line = f"{curr_line} {w}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font_desc)
        if bbox[2] - bbox[0] > (W - 140):
            if curr_line:
                desc_lines.append(curr_line)
            curr_line = w
        else:
            curr_line = test_line
    if curr_line:
        desc_lines.append(curr_line)

    y_text += 16
    for line in desc_lines[:2]:
        draw.text((64, y_text), line, font=font_desc, fill="#a1a1aa")
        y_text += 32

    # Bottom Divider
    draw.line([64, H - 120, W - 64, H - 120], fill="#27272a", width=1)

    # Avatar
    if os.path.exists(AVATAR_PATH):
        try:
            avatar = Image.open(AVATAR_PATH).convert("RGBA")
            avatar = avatar.resize((60, 60), Image.Resampling.LANCZOS)
            mask = Image.new("L", (60, 60), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 60, 60), fill=255)
            img.paste(avatar, (64, H - 100), mask)
            draw.ellipse([64, H - 100, 124, H - 40], outline="#3f3f46", width=2)
        except Exception as e:
            pass

    draw.text((140, H - 98), "Ozan Özdil", font=font_author_name, fill="#ffffff")
    draw.text((140, H - 72), "YZ Kodcusu & Açık Kaynak Sistem Mimarı", font=font_author_role, fill="#71717a")

    date_bbox = draw.textbbox((0, 0), date_text, font=font_meta)
    date_w = date_bbox[2] - date_bbox[0]
    draw.text((W - 64 - date_w, H - 85), date_text, font=font_meta, fill="#a1a1aa")

    img.save(output_path, "PNG", optimize=True)

def generate_default_og():
    create_og_card(
        title="Ozan Özdil — Açık Kaynak Sistem Mimarileri & YZ Kodcusu",
        description="Omarchy Linux, CachyOS, otonom ajan iş akışları, çekirdek düzeyinde sistem optimizasyonları ve fotonik belgesel araştırmaları.",
        tag="// SİSTEM MİMARİSİ",
        date_text="ozanozdil.com",
        output_path=DEFAULT_OG_PATH
    )
    print(f"Varsayılan OG görseli oluşturuldu: {DEFAULT_OG_PATH}")

def parse_frontmatter(content):
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    fm_text = parts[1]
    data = {}
    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip("'\"")
            data[k] = v
    # tags check
    tags_match = re.search(r"tags:\s*\[(.*?)\]", fm_text)
    if tags_match:
        raw_tags = tags_match.group(1)
        data["tags"] = [t.strip().strip("'\"") for t in raw_tags.split(",") if t.strip()]
    return data

def generate_blog_og():
    files = [f for f in os.listdir(BLOG_DIR) if f.endswith(".md")]
    print(f"Toplam {len(files)} blog yazısı taranıyor...")
    generated_count = 0
    for filename in files:
        slug = filename[:-3]
        filepath = os.path.join(BLOG_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        fm = parse_frontmatter(content)
        title = fm.get("title", slug)
        desc = fm.get("description", "")
        pub_date = format_date_tr(fm.get("pubDate", ""))
        tags = fm.get("tags", [])
        primary_tag = tags[0] if tags else "ARAŞTIRMA"

        out_path = os.path.join(OG_DIR, f"{slug}.png")
        # Regenerate if not exists or markdown newer than image
        should_generate = False
        if not os.path.exists(out_path):
            should_generate = True
        else:
            if os.path.getmtime(filepath) > os.path.getmtime(out_path):
                should_generate = True

        if should_generate:
            create_og_card(title, desc, primary_tag, pub_date, out_path)
            generated_count += 1

    print(f"{generated_count} adet blog OG kartı güncellendi / oluşturuldu.")

if __name__ == "__main__":
    generate_default_og()
    generate_blog_og()
