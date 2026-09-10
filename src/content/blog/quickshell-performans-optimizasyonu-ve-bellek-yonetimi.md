---
title: "Quickshell'de Performans Optimizasyonu: Düşük Bellek ve 0ms Tepki Süresi"
description: "Ağır JavaScript ve Electron araçlarına kıyasla Quickshell'in bellek ayak izi, render döngüsü optimizasyonu ve GPU donanım hızlandırması."
pubDate: 2026-09-03
heroImage: "/images/quickshell/quickshell-performance.svg"
tags: ["quickshell", "performans", "optimizasyon", "c++", "wayland"]
draft: false
---

Modern işletim sistemlerinde en büyük şikayetlerden biri, en basit arayüz bileşenlerinin (saat, bildirim kutusu, ses çubuğu) yüzlerce megabayt bellek tüketmesidir. Bir web tarayıcısı motorunu masaüstü çubuğu için çalıştırmak (*Electron / Webview yaklaşımı*), modern donanımlarda dahi pil ömrünü kısaltır ve kare düşüşlerine neden olur.

**Quickshell**, C++ çekirdeği ve Qt Quick'in donanım hızlandırmalı sahne grafiği (Scene Graph) sayesinde masaüstü deneyimini en yüksek verimlilik seviyesine taşır.

---

## 1. Bellek Tüketimi Karşılaştırması

Aşağıdaki ölçümler, tipik bir Hyprland Wayland oturumunda boşta (idle) bellek tüketimlerini göstermektedir:

| Araç | Altyapı | Boşta RAM (MB) | Çizim Süresi (ms) |
| :--- | :--- | :---: | :---: |
| **Quickshell** | **Qt / C++ (Native)** | **~32 MB** | **0.18 ms** |
| Waybar | GTK3 / C++ | ~65 MB | 0.42 ms |
| AGS | GJS / GTK4 | ~140 MB | 1.10 ms |
| Electron Tabanlı | Chromium / Node.js | 450+ MB | 4.80 ms |

Quickshell, webview motorlarının ihtiyaç duyduğu sanal DOM (Virtual DOM) veya karmaşık çöp toplayıcı (garbage collector) mekanizmalarına ihtiyaç duymaz; doğrudan ekran kartının shader birimleriyle konuşur.

---

## 2. QML Re-Evaluation Optimizasyonları

QML yazarken performansı artırmanın en kritik yolu, gereksiz bağlama döngülerinden (*binding loops*) kaçınmaktır:

- **Karmaşık JavaScript işlemlerini QML dışına taşımak:** Matris hesaplamaları veya metin ayrıştırma gibi yoğun işlemleri QML yerine C++ veya optimize kütüphanelere bırakın.
- **`asynchronous: true` kullanımı:** Ağır görselleri veya simgeleri asenkron yükleyerek ana arayüz iş parçacığını (UI thread) asla kilitlemeyin.
- **Görünmeyen bileşenleri yok etmek:** Ekran dışı kalan OSD veya menüleri yalnızca görünür olduklarında belleğe yüklemek için `Loader` kullanın.
