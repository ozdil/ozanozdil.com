import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("public/images/blog/flagships-2026", exist_ok=True)

font_bold_path = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"
font_reg_path = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf"

font_title = ImageFont.truetype(font_bold_path, 40)
font_subtitle = ImageFont.truetype(font_reg_path, 20)
font_h2 = ImageFont.truetype(font_bold_path, 24)
font_text = ImageFont.truetype(font_reg_path, 16)
font_sm = ImageFont.truetype(font_reg_path, 13)
font_badge = ImageFont.truetype(font_bold_path, 14)

# 1. Hero Image
def create_hero_image():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), color="#090a0f")
    draw = ImageDraw.Draw(img)

    # Grid background
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill="#141724", width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill="#141724", width=1)

    # Border
    draw.rectangle([(25, 25), (W-25, H-25)], outline="#262d47", width=2)
    draw.rectangle([(32, 32), (W-32, H-32)], outline="#191d2d", width=1)

    # Header Tag
    draw.rectangle([(60, 60), (330, 95)], fill="#1a2035", outline="#3b82f6", width=1)
    draw.text((75, 68), "LABORATUVAR & FİZİK ANALİZİ", fill="#60a5fa", font=font_badge)

    # Title
    draw.text((60, 120), "AMİRAL GEMİSİ MOBİL CİHAZLAR", fill="#ffffff", font=font_title)
    draw.text((60, 175), "BİLİMSEL VE MÜHENDİSLİK KIYASLAMASI (2026)", fill="#93c5fd", font=font_title)

    draw.text((60, 245), "iPhone 18 Pro Max • Xiaomi 18 Pro Max • vivo X500 Pro Max • OPPO Find X10 Pro Max", fill="#94a3b8", font=font_subtitle)

    # 4 Device Cards
    devices = [
        {"name": "Xiaomi 18 Pro Max", "score": "97.1", "focus": "12-Bit DDIC • ACES Log • 8500mAh", "color": "#f97316"},
        {"name": "vivo X500 Pro Max", "score": "96.5", "focus": "Sony UHCG • Zeiss APO • vivo V4", "color": "#38bdf8"},
        {"name": "Apple iPhone 18 PM", "score": "94.8", "focus": "2nm GAAFET • ProRes RAW • UMA", "color": "#a855f7"},
        {"name": "OPPO Find X10 PM", "score": "92.6", "focus": "3x 200MP • SUPERVOOC S • MTF", "color": "#10b981"}
    ]

    card_w = 250
    card_h = 240
    start_x = 60
    y_card = 310

    for i, dev in enumerate(devices):
        x = start_x + i * (card_w + 33)
        # Background card
        draw.rectangle([(x, y_card), (x + card_w, y_card + card_h)], fill="#111422", outline="#22283e", width=2)
        # Accent top bar
        draw.rectangle([(x, y_card), (x + card_w, y_card + 4)], fill=dev["color"])
        
        # Rank badge
        draw.rectangle([(x + 15, y_card + 18), (x + 60, y_card + 44)], fill="#1a2035", outline=dev["color"], width=1)
        draw.text((x + 23, y_card + 22), f"#{i+1}", fill=dev["color"], font=font_badge)

        # Score
        draw.text((x + card_w - 70, y_card + 18), dev["score"], fill="#ffffff", font=font_h2)
        draw.text((x + card_w - 22, y_card + 24), "/100", fill="#64748b", font=font_sm)

        # Name
        draw.text((x + 15, y_card + 65), dev["name"], fill="#f8fafc", font=font_badge)

        # Separator line
        draw.line([(x + 15, y_card + 95), (x + card_w - 15, y_card + 95)], fill="#1e293b", width=1)

        # Bullets
        details = dev["focus"].split(" • ")
        for j, det in enumerate(details):
            draw.text((x + 20, y_card + 115 + j * 32), f"> {det}", fill="#94a3b8", font=font_sm)

    # Footer notice
    draw.text((60, 580), "METRİKLER: FOTONİK • LOFIC FİZİĞİ • ACES KOLORİMETRİ • 2nm GAAFET • Si/C ANOT KİNETİĞİ", fill="#64748b", font=font_sm)
    draw.text((1000, 580), "OMARCHY RESEARCH", fill="#475569", font=font_sm)

    img.save("public/images/blog/flagships-2026/hero-flagships-comparison.png")
    print("Hero image saved.")

# 2. Display Technology Diagram
def create_display_image():
    W, H = 1000, 500
    img = Image.new("RGB", (W, H), color="#0c0e17")
    draw = ImageDraw.Draw(img)

    draw.rectangle([(15, 15), (W-15, H-15)], outline="#1e2438", width=1)
    draw.text((35, 30), "EKRAN FOTONİKLERİ VE ALT-PİKSEL SÜRÜCÜ MİMARİSİ", fill="#60a5fa", font=font_h2)
    draw.text((35, 65), "10-Bit Simülasyon (FRC) vs. Xiaomi TCL CSOT Natif 12-Bit DDIC Donanımı", fill="#94a3b8", font=font_text)

    # Left Box: 10-Bit
    draw.rectangle([(40, 110), (470, 440)], fill="#111422", outline="#262d47", width=1)
    draw.rectangle([(40, 110), (470, 114)], fill="#64748b")
    draw.text((60, 130), "10-Bit Klasik Panel (Apple / Standart)", fill="#f8fafc", font=font_badge)
    draw.text((60, 165), "• Kanal Basamağı: 2^10 = 1024 Seviye", fill="#cbd5e1", font=font_sm)
    draw.text((60, 195), "• Toplam Renk Hacmi: 1.07 Milyar Renk", fill="#cbd5e1", font=font_sm)
    draw.text((60, 225), "• Gradyan: Rec.2020 alanında bantlaşma riski", fill="#cbd5e1", font=font_sm)
    draw.text((60, 255), "• Piksel Dizilimi: Diamond PenTile (Paylaşımlı Alt-Piksel)", fill="#cbd5e1", font=font_sm)
    draw.text((60, 285), "• Efektif Çözünürlük: Matematikselin %75-80'i", fill="#ef4444", font=font_sm)
    draw.text((60, 315), "• PWM Frekansı: 480Hz - 960Hz (Göz Yorgunluğu Riski)", fill="#ef4444", font=font_sm)

    # Right Box: 12-Bit Xiaomi
    draw.rectangle([(510, 110), (940, 440)], fill="#111422", outline="#f97316", width=2)
    draw.rectangle([(510, 110), (940, 114)], fill="#f97316")
    draw.text((530, 130), "Xiaomi 18 Pro Max: Natif 12-Bit TCL CSOT", fill="#f97316", font=font_badge)
    draw.text((530, 165), "• Kanal Basamağı: 2^12 = 4096 Seviye (Donanımsal DAC)", fill="#cbd5e1", font=font_sm)
    draw.text((530, 195), "• Toplam Renk Hacmi: 68.7 Milyar Renk (Rekor)", fill="#22c55e", font=font_sm)
    draw.text((530, 225), "• Gradyan: Sıfır Posterizasyon / Kusursuz Akıcılık", fill="#22c55e", font=font_sm)
    draw.text((530, 255), "• Piksel Dizilimi: TCL Pearl Geometrisi (Yüksek Dolgu Oranı)", fill="#cbd5e1", font=font_sm)
    draw.text((530, 285), "• Çözünürlük Verimi: Metin kenarlarında sıfır saçaklanma", fill="#22c55e", font=font_sm)
    draw.text((530, 315), "• PWM Frekansı: 4320Hz IEEE 1789 Sıfır Risk Güvenliği", fill="#22c55e", font=font_sm)

    img.save("public/images/blog/flagships-2026/display-12bit-comparison.png")
    print("Display image saved.")

# 3. Camera & Sensor Physics Diagram
def create_sensor_image():
    W, H = 1000, 500
    img = Image.new("RGB", (W, H), color="#0c0e17")
    draw = ImageDraw.Draw(img)

    draw.rectangle([(15, 15), (W-15, H-15)], outline="#1e2438", width=1)
    draw.text((35, 30), "SENSÖR VE VİDEO FİZİĞİ: SİNYAL-GÜRÜLTÜ & ACES RENK BORU HATTI", fill="#38bdf8", font=font_h2)
    draw.text((35, 65), "Sony LYTIA Triple-Gain UHCG vs. Xiaomi ACES IDT vs. Apple ProRes RAW", fill="#94a3b8", font=font_text)

    # 3 Columns
    col_w = 280
    start_x = 40
    y_top = 110

    # vivo
    draw.rectangle([(start_x, y_top), (start_x + col_w, 440)], fill="#111422", outline="#38bdf8", width=1)
    draw.rectangle([(start_x, y_top), (start_x + col_w, y_top + 4)], fill="#38bdf8")
    draw.text((start_x + 15, y_top + 18), "vivo X500 Pro Max", fill="#38bdf8", font=font_badge)
    draw.text((start_x + 15, y_top + 42), "FOTOĞRAF FİZİĞİ", fill="#64748b", font=font_sm)
    draw.text((start_x + 15, y_top + 80), "> Sony LYT-818 Mimarisi", fill="#cbd5e1", font=font_sm)
    draw.text((start_x + 15, y_top + 110), "> 0.95 e- Okuma Gürültüsü", fill="#22c55e", font=font_sm)
    draw.text((start_x + 15, y_top + 140), "> Triple-Gain Tek Pozlama HDR", fill="#cbd5e1", font=font_sm)
    draw.text((start_x + 15, y_top + 170), "> 86dB Dinamik Aralık", fill="#22c55e", font=font_sm)
    draw.text((start_x + 15, y_top + 200), "> Zeiss APO Florit Optik", fill="#cbd5e1", font=font_sm)
    draw.text((start_x + 15, y_top + 230), "> Sıfır Kromatik Sapma", fill="#22c55e", font=font_sm)
    draw.text((start_x + 15, y_top + 260), "> vivo V4: 45MB SRAM NPU", fill="#38bdf8", font=font_sm)

    # Xiaomi
    x2 = start_x + col_w + 30
    draw.rectangle([(x2, y_top), (x2 + col_w, 440)], fill="#111422", outline="#f97316", width=2)
    draw.rectangle([(x2, y_top), (x2 + col_w, y_top + 4)], fill="#f97316")
    draw.text((x2 + 15, y_top + 18), "Xiaomi 18 Pro Max", fill="#f97316", font=font_badge)
    draw.text((x2 + 15, y_top + 42), "SİNEMATİK KOLORİMETRİ", fill="#64748b", font=font_sm)
    draw.text((x2 + 15, y_top + 80), "> Resmi ACES Ürün Ortağı", fill="#22c55e", font=font_sm)
    draw.text((x2 + 15, y_top + 110), "> Natif Sensör IDT Matrisi", fill="#22c55e", font=font_sm)
    draw.text((x2 + 15, y_top + 140), "> Tüm Lenslerde 10-Bit Log", fill="#cbd5e1", font=font_sm)
    draw.text((x2 + 15, y_top + 170), "> 4K 120fps MasterCinema", fill="#cbd5e1", font=font_sm)
    draw.text((x2 + 15, y_top + 200), "> Leica 1G+7P Mekanik İris", fill="#cbd5e1", font=font_sm)
    draw.text((x2 + 15, y_top + 230), "> f/1.4 - f/4.0 Fiziksel İris", fill="#22c55e", font=font_sm)
    draw.text((x2 + 15, y_top + 260), "> Surge P3 + G2 + T1 Yongalar", fill="#f97316", font=font_sm)

    # Apple
    x3 = x2 + col_w + 30
    draw.rectangle([(x3, y_top), (x3 + col_w, 440)], fill="#111422", outline="#a855f7", width=1)
    draw.rectangle([(x3, y_top), (x3 + col_w, y_top + 4)], fill="#a855f7")
    draw.text((x3 + 15, y_top + 18), "Apple iPhone 18 Pro Max", fill="#a855f7", font=font_badge)
    draw.text((x3 + 15, y_top + 42), "KODLAYICI & GECİKME", fill="#64748b", font=font_sm)
    draw.text((x3 + 15, y_top + 80), "> Donanımsal ProRes RAW", fill="#22c55e", font=font_sm)
    draw.text((x3 + 15, y_top + 110), "> 7.2 ms Rolling Shutter", fill="#22c55e", font=font_sm)
    draw.text((x3 + 15, y_top + 140), "> A20 Pro 2nm GAAFET", fill="#a855f7", font=font_sm)
    draw.text((x3 + 15, y_top + 170), "> Birleşik Bellek (UMA)", fill="#cbd5e1", font=font_sm)
    draw.text((x3 + 15, y_top + 200), "> Dolby Vision Frame-by-Frame", fill="#cbd5e1", font=font_sm)
    draw.text((x3 + 15, y_top + 230), "> 10-Bit Renk Kısıtı", fill="#ef4444", font=font_sm)
    draw.text((x3 + 15, y_top + 260), "> ~5000mAh Batarya Sınırı", fill="#ef4444", font=font_sm)

    img.save("public/images/blog/flagships-2026/sensor-optics-comparison.png")
    print("Sensor image saved.")

create_hero_image()
create_display_image()
create_sensor_image()
