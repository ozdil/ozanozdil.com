#!/usr/bin/env python3
"""
Blog Makaleleri ve İçerikler İçin Türkçe Dil, İmla ve Terim Denetleyicisi.
Türkçe yazım kılavuzu standartları, sıfır emoji politikası ve önerilen Türkçe terimler kontrol edilir.
"""

import os
import sys
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT_DIR / "src" / "content" / "blog"

# Sık kullanılan yabancı kelimeler ve Türkçe karşılıkları
TERM_SUGGESTIONS = {
    r"\bpipeline\b": "dağıtım hattı / süreç hattı",
    r"\bdeploy(?:ment)?\b": "dağıtım / yayına alma",
    r"\brepository\b": "depo / kod deposu",
    r"\bcommit\b": "işleme / kayıt",
    r"\bbranch\b": "dal",
    r"\bmerge\b": "birleştirme",
    r"\bbuild\b": "derleme / inşa",
    r"\bworkflow\b": "iş akışı",
    r"\bcache\b": "ön bellek",
    r"\bissue\b": "sorun / hata kaydı",
    r"\bfeature\b": "özellik",
    r"\bbug\b": "yazılım hatası",
    r"\bfix\b": "düzeltme / onarma",
    r"\bbenchmark\b": "başarım ölçütü / kıyaslama",
    r"\bdependency\b": "bağımlılık",
    r"\bruntime\b": "çalışma zamanı",
    r"\bframework\b": "çatı",
    r"\bfrontend\b": "ön yüz",
    r"\bbackend\b": "arka yüz",
    r"\bhardware\b": "donanım",
    r"\bsoftware\b": "yazılım",
}

# Gerçek Unicode Emoji aralıkları (Box drawing ve geometrik karakterler hariç)
EMOJI_PATTERN = re.compile(
    r"[\U0001F600-\U0001F64F"  # Emoticons
    r"\U0001F300-\U0001F5FF"  # Misc Symbols and Pictographs
    r"\U0001F680-\U0001F6FF"  # Transport and Map
    r"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    r"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    r"\U00002600-\U000026FF"  # Misc symbols (e.g. warning, sun)
    r"\U00002700-\U000027BF]+", # Dingbats
    flags=re.UNICODE
)

def check_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = []
    warnings = []

    # 1. Emoji Kontrolü
    emoji_matches = list(EMOJI_PATTERN.finditer(content))
    if emoji_matches:
        for m in emoji_matches:
            errors.append(f"Sıfır emoji kuralı ihlali: '{m.group()}' bulundu.")

    # Kod bloklarını hariç tutarak metin analizi yap
    text_only = re.sub(r"```[\s\S]*?```", "", content)
    text_only = re.sub(r"`[^`]*`", "", text_only)

    # 2. Yabancı Terim Önerileri
    for pattern, suggestion in TERM_SUGGESTIONS.items():
        matches = re.finditer(pattern, text_only, flags=re.IGNORECASE)
        for m in matches:
            warnings.append(f"Yabancı terim '{m.group()}': Yerine '{suggestion}' kullanılması önerilir.")

    # 3. Temel İmla ve Noktalama
    # Noktalama öncesi boşluk hatası (ör. 'merhaba ,')
    if re.search(r"\w\s+[,.:;!?]", text_only):
        warnings.append("Noktalama işaretlerinden önce gereksiz boşluk bırakılmış.")

    return errors, warnings

def main():
    if not BLOG_DIR.exists():
        print(f"Blog dizini bulunamadı: {BLOG_DIR}")
        sys.exit(0)

    all_errors = 0
    total_files = 0

    print("--- Türkçe Dilbilgisi ve Terim Standartları Denetimi ---")
    for md_file in sorted(BLOG_DIR.glob("*.md")):
        total_files += 1
        errors, warnings = check_file(md_file)
        if errors or warnings:
            print(f"\nDosya: {md_file.name}")
            for err in errors:
                print(f"  [HATA] {err}")
                all_errors += 1
            for w in warnings:
                print(f"  [ÖNERİ] {w}")

    print(f"\nToplam {total_files} makale denetlendi.")
    if all_errors > 0:
        print(f"Toplam {all_errors} kural ihlali tespit edildi.")
        sys.exit(1)
    else:
        print("Tüm makaleler kurallara uygundur.")

if __name__ == "__main__":
    main()
