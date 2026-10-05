import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("public/images/blog", exist_ok=True)

font_bold_path = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"
font_reg_path = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf"

font_title = ImageFont.truetype(font_bold_path, 38)
font_subtitle = ImageFont.truetype(font_reg_path, 18)
font_h2 = ImageFont.truetype(font_bold_path, 20)
font_text = ImageFont.truetype(font_reg_path, 15)
font_sm = ImageFont.truetype(font_reg_path, 13)
font_badge = ImageFont.truetype(font_bold_path, 13)

def create_deckopt_hero():
    W, H = 1200, 630
    img = Image.new("RGB", (W, H), color="#090a0f")
    draw = ImageDraw.Draw(img)

    # Grid background
    for x in range(0, W, 40):
        draw.line([(x, 0), (x, H)], fill="#141724", width=1)
    for y in range(0, H, 40):
        draw.line([(0, y), (W, y)], fill="#141724", width=1)

    # Frame border
    draw.rectangle([(25, 25), (W-25, H-25)], outline="#262d47", width=2)
    draw.rectangle([(32, 32), (W-32, H-32)], outline="#191d2d", width=1)

    # Header badge
    draw.rectangle([(60, 55), (380, 88)], fill="#1a2035", outline="#3b82f6", width=1)
    draw.text((75, 63), "// STEAMOS 3.x & GODOT 4 ENGINE", fill="#60a5fa", font=font_badge)

    # Title & Subtitle
    draw.text((60, 108), "deckopt: STEAM DECK OTONOM YZ MOTORU", fill="#ffffff", font=font_title)
    draw.text((60, 160), "Yerlesik Oyun Optimizasyonu • Deterministik Donanim Guvenligi • D-Pad Arayuzu", fill="#94a3b8", font=font_subtitle)

    # Core Hub / Architecture Bar
    bar_y = 210
    draw.rounded_rectangle([(60, bar_y), (W - 60, bar_y + 80)], radius=12, fill="#111422", outline="#3b82f6", width=2)
    draw.rectangle([(75, bar_y + 12), (320, bar_y + 36)], fill="#1a2035", outline="#3b82f6", width=1)
    draw.text((85, bar_y + 16), "MERKEZI IS AKISI & PIPELINE", fill="#60a5fa", font=font_badge)
    draw.text((75, bar_y + 46), "SteamOS Kutupahanesi -> Gemini 2.5 Flash -> profile.gd Kirpma -> Steam Baslatma Satiri", fill="#e2e8f0", font=font_h2)

    # 4 Architecture Columns / Cards
    cards = [
        {
            "title": "Donanim Tespiti",
            "tag": "DMI / BIOS",
            "color": "#38bdf8",
            "lines": [
                "Jupiter (LCD 60Hz)",
                "Galileo (OLED 90Hz)",
                "sysfs / APU frekans",
                "Katot & TDP kilitleri"
            ]
        },
        {
            "title": "Gemini 2.5 Flash",
            "tag": "ANALIZ MOTORU",
            "color": "#a855f7",
            "lines": [
                "Oyun adi & AppID",
                "Termal profil analizi",
                "TDP & GPU saat tahmini",
                "FSR ve render olcegi"
            ]
        },
        {
            "title": "profile.gd Guard",
            "tag": "DETERMINISTIK",
            "color": "#10b981",
            "lines": [
                "TDP: [3 - 15W] tavan",
                "GPU: [200 - 1600MHz]",
                "Kare senkron (hz % fps)",
                "Komut enjeksiyon filtre"
            ]
        },
        {
            "title": "Godot 4.7 Gamepad",
            "tag": "GAME MODE",
            "color": "#f59e0b",
            "lines": [
                "1280x800 dogal oran",
                "D-Pad / tus navigasyon",
                "Asenkron iptal emniyeti",
                "JetBrainsMono Nerd Font"
            ]
        }
    ]

    card_w = 250
    card_h = 240
    start_x = 60
    y_card = 315

    for i, card in enumerate(cards):
        x = start_x + i * (card_w + 26)
        draw.rounded_rectangle([(x, y_card), (x + card_w, y_card + card_h)], radius=12, fill="#111422", outline="#22283e", width=2)
        draw.rectangle([(x + 2, y_card + 2), (x + card_w - 2, y_card + 6)], fill=card["color"])

        # Tag
        draw.rectangle([(x + 16, y_card + 18), (x + 140, y_card + 40)], fill="#1a2035", outline=card["color"], width=1)
        draw.text((x + 22, y_card + 22), card["tag"], fill=card["color"], font=font_badge)

        # Title
        draw.text((x + 16, y_card + 52), card["title"], fill="#ffffff", font=font_h2)

        # Content lines
        for l_idx, line in enumerate(card["lines"]):
            draw.text((x + 16, y_card + 92 + l_idx * 28), f"• {line}", fill="#94a3b8", font=font_sm)

    # Footer banner
    draw.text((60, H - 45), "ozanozdil.com // GUVENLI YZ OYUN OPTIMIZASYONU", fill="#64748b", font=font_sm)
    draw.text((W - 360, H - 45), "GITHUB: github.com/ozdil/deckopt", fill="#10b981", font=font_sm)

    target_path = "public/images/blog/steam-deck-ai-optimizer-architecture.png"
    img.save(target_path, "PNG", optimize=True)
    print(f"Generated {target_path} successfully ({img.size})")

if __name__ == "__main__":
    create_deckopt_hero()
