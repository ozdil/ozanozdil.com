---
title: "Omarchy Linux İçin Geliştirdiğim 9 Özgün Siber Güvenlik Eklentisi ve 4 Resmi Tema"
description: "Generate Clean Semantic HTML (without any CSS / custom styling) for Blogger cat << 'EOF' /home/ozdil/. gemini/antigravity/scratch/blogger_clean_post."
pubDate: "2026-09-01T15:09:24.078+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/09/omarchy-linux-icin-gelistirdigim-9.html"
---

# Generate Clean Semantic HTML (without any CSS / custom styling) for Blogger
cat << 'EOF' > /home/ozdil/.gemini/antigravity/scratch/blogger_clean_post.html

Linux ve açık kaynak dünyasında masaüstü deneyimini bir üst seviyeye taşımak için modern Arch Linux masaüstü ortamı olan **Omarchy**ekosistemine özel**9 adet özgün siber güvenlik & geliştirici eklentisi (plugin)**ile**4 adet resmi masaüstü temasını** geliştirip açık kaynak olarak yayınladım.

Geliştirilen tüm eklentiler resmi **Omarchy Plugin Marketplace**([plugins.omarchy.org](https://plugins.omarchy.org)) dizinine sunulmuş olup,**MIT lisansı** ile tamamen ücretsiz ve açık kaynaklıdır.

---

## 🔒 1. Siber Güvenlik, OPSEC & Sistem Kalkanı Eklentileri

### 🛡️ BadUSB Shield (Anti-BadUSB & Donanım Nöbetçisi)

Sisteme takılan USB donanımları izler. Masum bir USB bellek gibi görünen ancak arka planda klavye gibi davranarak zararlı kod enjekte eden aygıtları (BadUSB / Rubber Ducky saldırıları) anında tespit eder.

🔗 [GitHub Deposu: ozdil/omarchy-badusb-shield](https://github.com/ozdil/omarchy-badusb-shield)

### 🚨 Auth Watch (SSH & Sudo Yetkisiz Giriş Nöbetçisi)

Sistemdeki hatalı `sudo` parola denemelerini ve dışarıdan gelen SSH sızma / brute-force girişimlerini canlı filtreleyerek üst barda anlık uyarı verir.

🔗 [GitHub Deposu: ozdil/omarchy-auth-watch](https://github.com/ozdil/omarchy-auth-watch)

### 🪤 Tripwire Vault (Kanarya Dosya & Fidye Yazılımı Tuzağı)

Kritik sistem dizinlerine kriptografik kanarya (honey-token) dosyalar yerleştirir. Bir zararlı yazılım veya fidye yazılımı (ransomware) dosyalara dokunduğu anda masaüstünde alarm fırlatır.

🔗 [GitHub Deposu: ozdil/omarchy-tripwire-vault](https://github.com/ozdil/omarchy-tripwire-vault)

### 🌐 DNS Leak Guard (Canlı DNS Sızıntısı & DoT Kalkanı)

DNS sorgularınızın İSS'ye açık metin sızıp sızmadığını denetler. DNS-over-TLS (DoT) şifrelemesini doğrulayarak internet gizliliğinizi korur.

🔗 [GitHub Deposu: ozdil/omarchy-dns-leak-guard](https://github.com/ozdil/omarchy-dns-leak-guard)

### 🎭 Ghost MAC (Wi-Fi Anonimlik & Rastgele MAC Maskesi)

Halka açık Wi-Fi ağlarında (belediye, kafe, havalimanı) fiziksel donanım MAC adresinizi ve makine adınızı rastgele sahte bir kimlikle maskeleyerek fiziksel takibi engeller.

🔗 [GitHub Deposu: ozdil/omarchy-ghost-mac](https://github.com/ozdil/omarchy-ghost-mac)

### 🔒 OpSec Cleaner (Dijital Parmak İzi & EXIF Sanitizörü)

Sosyal medyaya fotoğraf yüklemeden önce üzerindeki GPS konum koordinatlarını, kamera seri numarasını, çekim zaman damgasını ve kullanıcı izlerini sıfırlayan dijital hijyen aracıdır.

🔗 [GitHub Deposu: ozdil/omarchy-opsec-cleaner](https://github.com/ozdil/omarchy-opsec-cleaner)

### 🛡️ CVE Radar (Arch Linux Paket & Binary Güvenlik Denetçisi)

Resmi Arch Linux Security Tracker API'si ile sistemdeki 1,100+ paketi ve SUID yetkili sistem binary'lerini tarayarak güvenlik açıklarını anlık raporlar.

🔗 [GitHub Deposu: ozdil/omarchy-cve-radar](https://github.com/ozdil/omarchy-cve-radar)

### 🌐 Cyber Sentinel (Canlı Ağ Radarı & Port Nöbetçisi)

Dış dünyaya açılan tüm aktif ağ soketlerini canlı izler. Şüpheli ve standart dışı portlara giden bağlantılarda anında tek tıkla süreci sonlandırma imkanı sunar.

🔗 [GitHub Deposu: ozdil/omarchy-cyber-sentinel](https://github.com/ozdil/omarchy-cyber-sentinel)

---

## ⚡ 2. Geliştirici & Çalışma Alanı Eklentileri

### ⚡ Git Radar (Geliştirici Nabzı & Commit Isı Haritası)

Tüm yerel depolarınızı tarar. Günlük commit sayınızı, kaydedilmemiş değişiklik olan repoları ve son 7 günün GitHub tarzı commit ısı haritasını doğrudan barda görselleştirir.

🔗 [GitHub Deposu: ozdil/omarchy-git-radar](https://github.com/ozdil/omarchy-git-radar)

---

## 🎨 3. Resmi Omarchy Masaüstü Temaları

- **🇹🇷 Türkiye Teması (21 İkonik Mekan):** Kapadokya, Göbeklitepe, Pamukkale, Nemrut, Sümela ve Türkiye'nin 21 eşsiz tarihi mekanını 8K vektörel duvar kağıtları ve OLED turkuaz renk paletiyle buluşturur. ([GitHub](https://github.com/ozdil/omarchy-turkiye-theme))

- **🎮 Steam Machine Teması:** Valve, Half-Life ve retro arcade ruhunu taşıyan karanlık siberpunk oyun teması. ([GitHub](https://github.com/ozdil/omarchy-steammachine-theme))

- **🏛️ Ankara & 🌙 İstanbul Temaları:** Başkent ve Boğaziçi'nin kadim estetiğini modern Linux masaüstüne taşıyan temalar. ([GitHub Ankara](https://github.com/ozdil/omarchy-ankara-theme) | [GitHub İstanbul](https://github.com/ozdil/omarchy-istanbul-theme))

---

**Yazar:** Ozan Özdil ([github.com/ozdil](https://github.com/ozdil) | [@ozanozdil](https://nsosyal.com/ozanozdil))

*Tüm projeler MIT lisansıyla açık kaynak olarak paylaşılmıştır.*

EOF

# Copy clean HTML to clipboard
wl-copy < /home/ozdil/.gemini/antigravity/scratch/blogger_clean_post.html
echo "✅ Temiz HTML panoya kopyalandı!"
