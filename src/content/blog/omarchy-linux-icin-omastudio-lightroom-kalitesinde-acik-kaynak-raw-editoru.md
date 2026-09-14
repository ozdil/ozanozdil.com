---
title: "Omarchy Linux İçin OmaStudio: Lightroom Kalitesinde, Açık Kaynak ve DaVinci Renk Tekerlekli RAW Fotoğraf Editörü"
description: "Quickshell 4.0 GPU ivmeli arayüzü, çok çekirdekli Rust/Rayon motoru, Hollywood standardı DaVinci 3-Way renk tekerlekleri ve YZ destekli sosyal medya optimizasyonuyla Linux'un eksik kalan yaratıcı halkası tamamlanıyor."
pubDate: 2026-09-14
heroImage: "/images/quickshell/omastudio-preview.png"
tags: ["omarchy", "quickshell", "rust", "fotografcilik", "raw", "acik-kaynak", "davinci-resolve", "linux-desktop"]
---

Linux masaüstünde yaratıcı profesyoneller ve fotoğraf meraklıları için uzun yıllardır süregelen en büyük açmazlardan biri, Adobe Lightroom ekosistemine bağımlılıktır. Darktable ve RawTherapee gibi kıymetli açık kaynak projeler var olsa da; modern Wayland entegrasyonu, akıcı touchpad jestleri, minimalist ergonomi ve video sektörünün altın standardı haline gelen **DaVinci Resolve 3-Way renk derecelendirme (color grading)** tekerleklerini bir arada sunan, hafif ve odaklanmış bir yerel araç eksikliği her zaman hissedildi.

Aylık abonelik zincirlerinden, kapalı kutu telemetrilerden ve hantal arayüzlerden arınmış bir yaratıcı iş akışı inşa etmek amacıyla geliştirdiğim **OmaStudio** (veya terminal dostu adıyla **OmaRaw**), bugün Omarchy Linux ekosistemi için yayında.

---

## 🏛️ Mimari: GPU İvmeli Quickshell ve Çok Çekirdekli Rust

OmaStudio sıradan bir Electron sarmalayıcısı veya hantal bir GTK arayüzü değildir. Sistem mimarisi iki güçlü temel üzerine kuruludur:

1. **Arayüz Katmanı (Quickshell / Qt 6 QML):**
   Masaüstüyle doğrudan konuşan, GPU ivmeli, 60+ FPS yenileme hızına sahip pürüzsüz bir Wayland sahnesi. Dokunmatik ekranlarda ve Mac hassasiyetindeki touchpad'lerde kusursuz çalışan logaritmik **Pinch-to-Zoom**, parmak ucunda serbest kadraj döndürme ve kinetik kaydırma (pan) yeteneği.

2. **İşleme Motoru (Rust + Rayon + LibRaw):**
   Bellek güvenliğinden ve sıfır maliyetli soyutlamalardan taviz vermeyen bağımsız Rust arka plan motoru (`omastudio-engine`). LibRaw FFI üzerinden doğrudan piksellere erişir; çok çekirdekli paralel matris hesaplamalarıyla (Rayon) 50+ megapiksellik RAW fotoğrafları dahi donma ve bellek darboğazı yaşamadan anlık işler.

```
[ RAW Dosyası ] ➔ [ LibRaw Demosaic ] ➔ [ 16-Bit Lineer Pipeline ] ➔ [ Rayon Çok Çekirdek ] ➔ [ Quickshell GPU Viewport ]
                                                    │
                                         [ DaVinci 3-Way Wheels ]
                                         [ 8-Band HSL Renk Mikseri ]
                                         [ Optik Düzeltme & ICC ]
```

---

## 🌟 Öne Çıkan Özellikler

### 1. Kapsamlı Sensör ve RAW Desteği
Fotoğraf makineniz ne olursa olsun OmaStudio hazır:
* **Fujifilm:** X-Trans II, III, IV ve V 6x6 matris sensörleri ve Bayer modelleri (`.RAF`).
* **Nikon:** Z8, Z9 High-Efficiency HE/HE* algoritmaları dahil `.NEF` ve `.NRW`.
* **Sony:** Alpha serisi sıkıştırılmış/kayıpsız `.ARW` ve `.SR2`.
* **Canon:** Modern ISOBMFF yapılı `.CR3` ve klasik `.CR2`.
* **Leica, Hasselblad & DNG:** Akıllı telefonlar, DJI dronelar ve orta format makineler (`.DNG`, `.RWL`, `.3FR`).

### 2. Mac Kalitesinde Touchpad & Mouse Ergonomisi (1:1 Apple Trackpad Hissi)
Linux masaüstüne geçen yaratıcıların en çok dert yandığı konu, trackpad ve fare etkileşimlerinin macOS kadar ipeksi ve tahmin edilebilir olmamasıdır. OmaStudio bu sorunu kökünden çözdü. Arayüz etkileşimleri **Apple Magic Trackpad ve MacBook tuval ergonomisiyle 1:1 aynı tepkiyi verir**:

* **Pinch-to-Zoom:** İki parmağınızı açıp kapattığınızda, imlecin tam altındaki piksel merkezine sıçramasız, pürüzsüz ve logaritmik olarak yakınlaşır.
* **Akıllı Rotasyon & 3.5° Ölü Bölge (Deadzone):** Yakınlaştırma yaparken parmakların hafifçe kayıp fotoğrafı kazara eğmesini engelleyen özel bir filtreleme mekanizması devrededir; bilinçli çevirmelerde ise tuval 360° parmağınızın açısını takip eder.
* **Kinetik Pan:** İki parmakla kaydırma, fotoğrafta tıpkı bir kağıt üzerinde gezinir gibi sürtünmeli (`0.75` sönümleme) ve akıcı bir süzülüş sağlar.
* **Double-Tap (Çift Dokunma / Tıklama):** Tıpkı macOS Preview veya Lightroom'daki gibi, ekrana tam sığdırma (%100 Fit) ile %200 detay odaklama arasında anında geçiş yapar.
* **Alt + Wheel:** Fareyle çalışanlar için fare tekerleği odaklı zum yaparken, `Alt + Wheel` kombinasyonu 1.5° hassasiyetle mikro kadraj düzeltmesi sunar. Resmin tuval dışına fırlayıp kaybolmasını engelleyen akıllı sınırlandırma çıpaları (`clampPan`) ile kontrol daima sizdedir.

### 3. Kademeli Keşif (Simple Mode & Pro Studio)
Fotoğraf düzenleme deneyimi iki ayrı ihtiyaç profiline göre kurgulandı:

* **✨ Basit & Hızlı Mod:** Günlük çekimler için tek tıkla **YZ Sihirbazı (AI Magic Auto)** ve sadece 4 temel ayar sürgüsü (Işık, Sıcaklık, Canlılık, Kontrast).
* **🎛️ Pro Studio Modu:** Her modül başlığında bağımsız **RESET** butonu bulunan stüdyo seviyesi parametrik denetim:
  * **White Balance:** 2,000K – 12,000K Kelvin spektrumu ve $\pm 100$ Tint ayarı.
  * **Light & Dynamic Range:** $-5.00\,\text{EV} \dots +5.00\,\text{EV}$ logaritmik pozlama, S-Curve kontrast, Highlight kurtarma, derin gölge açma, Whites & Blacks çıpaları.
  * **Presence & Texture:** Doku, Netlik (Clarity), Sis giderme (Dehaze), Akıllı canlılık (Vibrance) ve Doygunluk.
  * **8-Band HSL Renk Mikseri:** 8 ayrı spektrum renginde bağımsız Hue, Saturation ve Luminance kontrolü.
  * **Detay & Optik:** Çift kademeli kumlanma temizleme (Luma NR), keskinleştirme, vinyet, mor/yeşil saçaklanma önleyici **Defringe** ve fıçı/yastık bozulmalarını düzelten **Lens Distortion** telafisi.

### 4. Hollywood Standardı: DaVinci Resolve 3-Way Renk Tekerlekleri
Fotoğraf dünyasında nadir görülen, ancak sinema sektörünün vazgeçilmezi olan **Lift, Gamma, Gain ve Offset** renk tekerlekleri doğrudan arayüze entegre edildi:

* **Lift:** Gölgelerin renk yönü ve bağımsız taban luma halkası.
* **Gamma:** Ten tonları ve sahne gövdesini şekillendiren orta ton dengesi.
* **Gain:** Gökyüzü ve ışık parlamalarını renklendiren tepe vurgu diski.
* **Offset:** Sahnenin genel renk dengesini kaydırmadan tüm dinamik aralığa dengeli tonlama.

### 5. Yapay Zeka Destekli Sosyal Medya Optimizatörü
Bir fotoğrafı düzenlemek işin yarısıysa, doğru mecrada doğru formatla sunmak diğer yarısıdır. OmaStudio, tek tıkla platforma özel akıllı kadraj ve sıkıştırma kayıplarını telafi eden mikrokontrast algoritmalarını çalıştırır:

| Platform | En-Boy Oranı | Çözünürlük | Optimizasyon Odağı |
| :--- | :---: | :---: | :--- |
| **Instagram Feed** | `4:5` | 1080 × 1350 | Dikey maksimum alan, kenar netliği |
| **Stories & TikTok** | `9:16` | 1080 × 1920 | Tam ekran dikey OLED canlılığı |
| **X (Twitter)** | `16:9` | 1200 × 675 | Mobil ve masaüstü akış berraklığı |
| **Kare Portre** | `1:1` | 1080 × 1080 | Klasik profil ızgara uyumu |
| **YouTube Thumbnail** | `16:9` | 1280 × 720 | Yüksek tıklama oranı (CTR) için canlı renkler |

---

## 🔒 Güvenlik ve Gizlilik: AGENTS.md Standartları

Omarchy Linux ekosisteminin tüm yerel uygulamalarında olduğu gibi, OmaStudio da sıkı güvenlik yönergelerine (`AGENTS.md`) sadık kalır:

1. **İzole Süreç Grupları (`cmd.process_group(0)`):** Harici yardımcı işlemler (Rclone, Zenity vb.) ana süreçten bağımsız PGID ile çalıştırılır; zaman aşımı durumunda zombi süreç bırakılmadan `SIGTERM` ve ardından kaçınılmaz `SIGKILL` ile temizlenir.
2. **Korumalı Dosya İzinleri (`0600` / `0700`):** Katalog ve tarif dosyaları `0600` izniyle geçici dosya üzerinden atomik olarak yazılır (`.tmp_...` + `fs::rename`); symlink saldırıları sıkıca engellenir.
3. **Quickshell Güvenliği:** Dinamik veriler asla `eval()` veya güvensiz QML nesne yükleyicileriyle çalıştırılmaz; tüm metin bileşenlerinde `textFormat: Text.PlainText` zorunludur.

---

## 🚀 Kurulum ve İlk Adım

Omarchy veya Arch Linux üzerinde kaynak koddan derlemek ve çalıştırmak son derece kolaydır:

```bash
# Gerekli kütüphaneleri yükleyin
sudo pacman -S libraw quickshell rclone libjxl libavif zenity rust

# Projeyi derleyin
cargo build --release --locked
install -m 755 target/release/omastudio-engine ~/.local/bin/

# OmaStudio'yu başlatın
omastudio
```

---

## 🎯 Sonuç: Yaratıcı Özgürlük

OmaStudio; açık kaynak dünyasında fotoğraf düzenlemenin yalnızca "mümkün" değil, aynı zamanda son derece hızlı, estetik ve profesyonel standartlarda yapılabileceğinin somut bir kanıtıdır. 

Aylık abonelikler ödemeden, verilerinizi üçüncü taraf bulutlara kaptırmadan, kendi donanımınızın tüm gücünü kullanarak fotoğraf sanatınızı özgürce icra edebilirsiniz.

* **GitHub:** [github.com/ozdil/omarchy-omastudio](https://github.com/ozdil/omarchy-omastudio)
* **Lisans:** MIT License
