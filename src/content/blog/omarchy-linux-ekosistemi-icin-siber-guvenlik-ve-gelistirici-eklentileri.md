---
title: "Omarchy Linux Masaüstü Ekosistemi İçin 9 Özgün Siber Güvenlik ve Geliştirici Eklentisi"
description: "Arch Linux tabanlı Omarchy ortamı için geliştirilen açık kaynak siber savunma, donanım güvenliği ve geliştirici verimlilik araçlarının mimari dökümü."
pubDate: 2026-09-01
tags: ["omarchy", "siber-güvenlik", "linux", "arch-linux", "açık-kaynak", "opsec"]
---

Linux ve açık kaynak dünyasında masaüstü deneyimini kurumsal güvenlik standartlarıyla buluşturmak amacıyla; modern Arch Linux masaüstü ortamı olan **Omarchy** ekosistemine özel **9 adet özgün siber güvenlik ve geliştirici eklentisi (plugin)** ile **4 adet resmi masaüstü temasını** geliştirip açık kaynak olarak yayınladık.

Geliştirilen tüm eklentiler resmi **Omarchy Plugin Marketplace** ([plugins.omarchy.org](https://plugins.omarchy.org)) dizinine sunulmuş olup, **MIT lisansı** ile tamamen ücretsiz ve bağımsızdır.

---

## 1. Siber Güvenlik, OPSEC ve Donanım Kalkanı Eklentileri

### 🛡️ BadUSB Shield (Donanım Nöbetçisi & USB Güvenliği)
Sisteme takılan tüm USB veri yollarını anlık izler. Masum bir depolama birimi gibi görünen fakat arka planda klavye/HID olarak tanıtılarak otomatik zararlı komut enjekte eden aygıtları (BadUSB / Rubber Ducky saldırıları) anında tespit ederek erişimi sınırlar.

* **GitHub Deposu:** [`ozdil/omarchy-badusb-shield`](https://github.com/ozdil/omarchy-badusb-shield)

### 🚨 Auth Watch (SSH ve Sudo Yetkisiz Giriş Takibi)
Sistem üzerindeki hatalı `sudo` parola denemelerini ve dış ağlardan gelen SSH sızma / brute-force girişimlerini gerçek zamanlı filtreleyerek bildirim alanında anlık alarm üretir.

* **GitHub Deposu:** [`ozdil/omarchy-auth-watch`](https://github.com/ozdil/omarchy-auth-watch)

### 🪤 Tripwire Vault (Kanarya Dosya ve Fidye Yazılımı Tuzağı)
Kritik sistem ve kullanıcı dizinlerine kriptografik kanarya (honey-token) dosyalar yerleştirir. Herhangi bir yetkisiz süreç veya fidye yazılımı (ransomware) bu dosyalara temas ettiği anda işlemi dondurur ve acil durum protokolünü tetikler.

* **GitHub Deposu:** [`ozdil/omarchy-tripwire-vault`](https://github.com/ozdil/omarchy-tripwire-vault)

### 🌐 DNS Leak Guard (DNS Sızıntısı & DoT Doğrulayıcı)
Sistem DNS sorgularının yerel internet servis sağlayıcısına şifresiz (plain-text) sızıp sızmadığını denetler. DNS-over-TLS (DoT) veya DNS-over-HTTPS (DoH) şifreleme tünelini sürekli test ederek ağ gizliliğini güvence altına alır.

* **GitHub Deposu:** [`ozdil/omarchy-dns-leak-guard`](https://github.com/ozdil/omarchy-dns-leak-guard)

### 🎭 Ghost MAC (Wi-Fi Donanım Kimliği Maskeleme)
Halka açık veya paylaşımlı Wi-Fi ağlarında fiziksel donanım adresinizi (MAC) ve ağ ana makine adınızı (hostname) dinamik olarak sahte kimliklerle maskeler; fiziksel konum ve cihaz takibini zorlaştırır.

* **GitHub Deposu:** [`ozdil/omarchy-ghost-mac`](https://github.com/ozdil/omarchy-ghost-mac)

### 🔒 OpSec Cleaner (Dijital Meta Veri Temizleyici)
Belge veya görselleri ağa aktarmadan önce üzerlerinde yer alan GPS koordinatları, kamera seri numaraları, çekim zaman damgaları ve cihaz izlerini sıfırlayan dijital hijyen aracıdır.

* **GitHub Deposu:** [`ozdil/omarchy-opsec-cleaner`](https://github.com/ozdil/omarchy-opsec-cleaner)

### 🛡️ CVE Radar (Paket ve Binary Zafiyet Denetimi)
Arch Linux resmi Security Tracker API entegrasyonu ile sistemdeki 1.100+ kurulu paketi ve SUID yetkili sistem binary'lerini tarayarak bilinen güvenlik açıklarını anlık raporlar.

* **GitHub Deposu:** [`ozdil/omarchy-cve-radar`](https://github.com/ozdil/omarchy-cve-radar)

### 🌐 Cyber Sentinel (Canlı Ağ Radarı & Port İzleyici)
Dış ağlara açılan tüm aktif ağ soketlerini izler. Standart dışı portlara veya şüpheli IP bloklarına giden oturumlarda tek komutla süreci sonlandırma imkanı sunar.

* **GitHub Deposu:** [`ozdil/omarchy-cyber-sentinel`](https://github.com/ozdil/omarchy-cyber-sentinel)

---

## 2. Geliştirici ve Verimlilik Araçları

### ⚡ Git Radar (Depo Nabzı ve Commit Isı Haritası)
Yerel depolardaki çalışma durumunu denetler; güncellenmemiş dosyaları, kaydedilmemiş değişiklikleri ve son 7 günün commit dağılımını doğrudan üst panelde görselleştirir.

* **GitHub Deposu:** [`ozdil/omarchy-git-radar`](https://github.com/ozdil/omarchy-git-radar)

---

## 3. Açık Kaynak Lisans ve Kurulum

Geliştirilen tüm modüller MIT lisansı altında topluluk kullanımına açıktır. Omarchy ortamında doğrudan paket yöneticisi ve Git üzerinden kurulabilir.
