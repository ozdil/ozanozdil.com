#!/usr/bin/env python3
"""
publish_article.py - Otomatik Makale Yayınlama, Doğrulama ve Canlıya Alma Aracı

Bu betik:
1. Türkçe imla, sıfır emoji ve terminoloji denetimini çalıştırır.
2. Açık ve koyu tema uyumluluğunu kontrol eder.
3. Otomatik OG görseli ve görsel site haritasını günceller.
4. Astro derlemesini (npm run build) gerçekleştirir.
5. Yeni yazının hem /blog (Yazılar) hem de / (Ana Sayfa - Son Yazılar) sayfasında 1. sırada olduğunu doğrular.
6. Değişiklikleri git ile işler (commit) ve uzak depoya (origin main) iter (push).
7. Cloudflare Workers üzerine derlenmiş siteyi canlıya alır (wrangler deploy).
"""

import sys
import os
import subprocess
import re
from datetime import datetime

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def run_cmd(cmd, desc, abort_on_fail=True):
    print(f"[*] {desc}...")
    res = subprocess.run(cmd, shell=True, cwd=ROOT_DIR, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[!] HATA: {desc} basarisiz oldu!")
        if res.stdout:
            print(res.stdout)
        if res.stderr:
            print(res.stderr)
        if abort_on_fail:
            sys.exit(1)
        return False, res.stdout + res.stderr
    return True, res.stdout

def verify_first_post():
    print("[*] Makale siralamasi dogrulaniyor...")
    blog_html = os.path.join(ROOT_DIR, "dist", "blog", "index.html")
    index_html = os.path.join(ROOT_DIR, "dist", "index.html")
    
    if not os.path.exists(blog_html) or not os.path.exists(index_html):
        print("[!] dist dosyalari bulunamadi. Derleme eksik!")
        sys.exit(1)
        
    with open(blog_html, "r", encoding="utf-8") as f:
        b_content = f.read()
    with open(index_html, "r", encoding="utf-8") as f:
        i_content = f.read()
        
    # En son blog markdown dosyasını bul
    blog_dir = os.path.join(ROOT_DIR, "src", "content", "blog")
    files = [os.path.join(blog_dir, f) for f in os.listdir(blog_dir) if f.endswith(".md")]
    
    latest_file = None
    latest_date_str = ""
    latest_slug = ""
    
    date_regex = re.compile(r'^pubDate:\s*["\']?([0-9T:\-\.+Z ]+)["\']?', re.MULTILINE)
    
    for fpath in files:
        with open(fpath, "r", encoding="utf-8") as f:
            c = f.read()
            m = date_regex.search(c)
            if m:
                d_str = m.group(1).strip()
                if d_str > latest_date_str:
                    latest_date_str = d_str
                    latest_file = fpath
                    latest_slug = os.path.splitext(os.path.basename(fpath))[0]
                    
    if not latest_slug:
        print("[!] En son makale slug bilgisi alinamadi!")
        sys.exit(1)
        
    print(f"[*] Tespit edilen en son makale: {latest_slug} (Tarih: {latest_date_str})")
    
    # dist/blog/index.html ilk post kontrolü
    if f"/blog/{latest_slug}" not in b_content[:b_content.find("</article>") + 500]:
        print(f"[!] UYARI: {latest_slug} Yazilar (/blog) sayfasinda en basta gorunmuyor olabilir!")
    else:
        print(f"[OK] Yazilar (/blog) sayfasinda en basta dogrulandi.")

    # dist/index.html son-yazilar kontrolü
    son_yazilar_idx = i_content.find("son-yazilar")
    if son_yazilar_idx != -1:
        snippet = i_content[son_yazilar_idx:son_yazilar_idx + 3000]
        if f"/blog/{latest_slug}" in snippet:
            print(f"[OK] Ana sayfa Son Yazilar vitrininde 1. sirada dogrulandi.")
        else:
            print(f"[!] UYARI: {latest_slug} Ana sayfa Son Yazilar blogunda 1. sirada tespit edilemedi!")
            
    return latest_slug

def main():
    commit_msg = sys.argv[1] if len(sys.argv) > 1 else None
    
    print("=== OZANOZDIL.COM OTOMATIK MAKALE YAYINLAMA VE DAGITIM ZINCIRI ===")
    
    # 1. Turkce ve terminoloji kontrolu
    run_cmd("python3 scripts/check-turkish-content.py", "Turkce icerik, sifir emoji ve terminoloji denetimi")
    
    # 2. OG Gorselleri ve Site Haritasi
    run_cmd("python3 scripts/generate-og-images.py || true", "OG kart gorselleri uretimi", abort_on_fail=False)
    run_cmd("python3 scripts/generate_image_sitemap.py", "Gorsel site haritasi guncellemesi")
    
    # 3. Astro Derleme
    run_cmd("npx astro build", "Astro statik site derlemesi")
    
    # 4. Siralama ve Vitrin Dogrulamasi
    latest_slug = verify_first_post()
    
    # 5. Git Commit & Push
    if not commit_msg:
        commit_msg = f"feat(blog): yeni makale yayinlandi - {latest_slug}"
        
    run_cmd("git add .", "Git degisiklikleri evreye alma")
    
    status_ok, status_out = run_cmd("git status --porcelain", "Git durumu kontrolu")
    if status_out.strip():
        run_cmd(f'git commit -m "{commit_msg}"', f"Git kaydi olusturma: {commit_msg}")
        run_cmd("git push origin main", "Git uzak depoya (origin main) gonderme")
    else:
        print("[*] Depoda yeni git degisikligi yok, commit adimi atlandi.")
        
    # 6. Cloudflare Workers Canliya Alma (Wrangler Deploy)
    run_cmd("npx wrangler deploy", "Cloudflare Workers canli dagitimi (wrangler deploy)")
    
    print("\n=======================================================")
    print(f"[BASARILI] Makale yayinlandi, git senkronize edildi ve canliya alindi!")
    print(f"Canli URL: https://ozanozdil.com/blog/{latest_slug}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
