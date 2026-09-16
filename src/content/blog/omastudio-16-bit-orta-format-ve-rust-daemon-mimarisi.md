---
title: "OmaStudio 0.2: 16-Bit Medium Format (Orta Format) RAW Desteği ve Kalıcı Rust Daemon Mimarisi"
description: "OmaStudio, 48-bit RGB renk derinliği, Fujifilm GFX ve Hasselblad gibi 100+ MP orta format sensörler için 16-bit kayıpsız boru hattı ve 60 FPS canlı düzenleme sunan kalıcı Rust daemon mimarisiyle güncellendi."
pubDate: 2026-09-15
heroImage: "/images/quickshell/omastudio-preview.png"
tags: ["omarchy", "rust", "medium-format", "fotografcilik", "raw", "quickshell", "acik-kaynak", "davinci-resolve", "hasselblad", "fujifilm-gfx"]
---

Fotoğrafçılıkta tam kare (35mm) sensörlerin sunduğu dinamik aralık etkileyici olsa da; **Orta Format (Medium Format)** dünyası bambaşka bir ligdir. Fujifilm GFX 100 II, GFX 100S, Hasselblad X2D 100C ve Phase One gibi sistemlerin ürettiği 100+ megapiksellik devasa sensörler, piksel başına tam **16-bit analog-dijital çevrim (ADC)** ve 15+ stop dinamik aralık sunar.

Pek çok fotoğraf düzenleme yazılımı, önizleme hızını artırmak adına bu zengin veriyi hafızaya alırken 8-bit'e (kanal başına 256 seviye) indirger. Ancak derin gölgeleri açtığınızda (+4 EV, +100 Shadows) veya sert gökyüzü geçişlerini kurtarmaya çalıştığınızda, tonlar arasındaki basamaklar kırılır; gölgelerde çirkin renk çizgilenmeleri (**banding**) ve renk yırtılmaları (**posterization**) baş gösterir.

Bugün yayımlanan **OmaStudio 0.2.0** güncellemesiyle, Linux masaüstünde orta format ve stüdyo fotoğrafçılığının önündeki tüm teknik engelleri kaldırdık. OmaStudio artık **tam 16-Bit (kanal başına 16-bit / 48-bit RGB)** kayıpsız matematiksel işleme boru hattına ve **kalıcı (persistent) Rust Daemon** mimarisine sahip.

---

## Neden 16-Bit? 8-Bit ile 16-Bit Arasındaki Uçurum

Bir pikselin parlaklık ve renk derinliği, sahip olduğu bit sayısıyla üssel olarak belirlenir:
* **8-Bit:** Kanal başına $2^8 = 256$ seviye (Toplamda 16.7 milyon renk).
* **16-Bit:** Kanal başına $2^{16} = 65,536$ seviye (Toplamda 281 trilyon renk).

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
  <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
  Gölge Kurtarma ve Ton Kuantizasyonu Kıyaslaması
  </div>
  <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">256x Ton Hassasiyeti</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 font-mono text-xs">
  <!-- 8-Bit Card -->
  <div class="rounded-xl border border-red-200 dark:border-red-950/60 bg-red-50/40 dark:bg-red-950/20 p-5">
  <div class="flex items-center justify-between mb-3">
  <span class="text-xs font-bold uppercase tracking-wider text-red-700 dark:text-red-400">8-Bit İşleme Hattı</span>
  <span class="px-2 py-0.5 rounded bg-red-100 dark:bg-red-900/50 text-red-800 dark:text-red-300 font-semibold text-[10px]">256 Seviye</span>
  </div>
  <div class="text-sm font-semibold text-[#1c1917] dark:text-[#f5f5f4] mb-2">Basamaklanma ve Posterizasyon</div>
  <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mb-4">
  Derin gölgeler açıldığında (+4 EV) ara tonlar tükenir; pürüzsüz geçiş yerine sert renk basamakları oluşur.
  </p>
  <div class="space-y-2 text-[11px]">
  <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-red-200/60 dark:border-red-900/40 flex justify-between">
  <span class="text-[#78716c]">Ton Dağılımı:</span>
  <span class="font-bold text-red-600 dark:text-red-400">[1] ... [2] ... [3] (Kaba Adım)</span>
  </div>
  <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-red-200/60 dark:border-red-900/40 flex justify-between">
  <span class="text-[#78716c]">Renk Yırtılması:</span>
  <span class="text-red-600 dark:text-red-400">Belirgin Banding Çizgileri</span>
  </div>
  </div>
  </div>
  <!-- 16-Bit Card -->
  <div class="rounded-xl border border-emerald-300 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20 p-5">
  <div class="flex items-center justify-between mb-3">
  <span class="text-xs font-bold uppercase tracking-wider text-emerald-700 dark:text-emerald-400">16-Bit Lineer Pipeline</span>
  <span class="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/50 text-emerald-800 dark:text-emerald-300 font-semibold text-[10px]">65.536 Seviye</span>
  </div>
  <div class="text-sm font-semibold text-[#1c1917] dark:text-[#f5f5f4] mb-2">İpeksi Pürüzsüz Geçiş (Zero Banding)</div>
  <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mb-4">
  Her bir renk kanalı 65.536 hassasiyetle hesaplanır; gölgelerdeki en ufak mikro detay dahi organik film dokusuyla korunur.
  </p>
  <div class="space-y-2 text-[11px]">
  <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-emerald-200/60 dark:border-emerald-900/40 flex justify-between">
  <span class="text-[#78716c]">Ton Dağılımı:</span>
  <span class="font-bold text-emerald-600 dark:text-emerald-400">[256] -> [257] -> [258]...</span>
  </div>
  <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-emerald-200/60 dark:border-emerald-900/40 flex justify-between">
  <span class="text-[#78716c]">Geçiş Kalitesi:</span>
  <span class="font-bold text-emerald-600 dark:text-emerald-400">Kusursuz Analog Hassasiyet</span>
  </div>
  </div>
  </div>
  </div>
</div>

Özellikle Fujifilm GFX serisinin `.RAF` dosyalarında ve Hasselblad `.3FR` / `.DNG` formatlarında, gölgelerde saklı olan bilgiler inanılmaz derecede zengindir. 16-bit işleme motoru sayesinde:
1. **Sıfır Basamaklanma (Zero Banding):** Derin gölgelerden çıkarılan detaylar, ara ton basamakları pürüzsüzce enterpole edildiği için doğal ve organik bir film dokusunda görünür.
2. **Highlight Rolloff (Yumuşak Vurgu Sönümlemesi):** Güneş batımı, sahne ışıkları veya beyaz gelinlik gibi sert parlak alanlar ani beyaz patlaması yerine pürüzsüz ve kademeli bir şekilde sönümlenir.
3. **Kayıpsız DaVinci Renk Derecelendirmesi:** 3-Way Lift/Gamma/Gain ve 8-Band HSL kontrolleri matematiksel olarak 65,536 seviyeli float matrisler üzerinde döner.

---

## Yeni Mimari: Kalıcı Rust Engine Daemon

Eski mimaride her kaydırıcı (slider) hareketinde ayrı bir alt süreç (`omastudio-engine render`) tetikleniyor, 112 MB'lık RAW dosyasının diskten tekrar okunması gerekiyordu. 16-bit verinin devasa boyutu düşünüldüğünde bu yöntem sürdürülemezdi.

OmaStudio 0.2 ile sistemin omurgasını baştan aşağı yeniledik:

### 1. Hot RAM Cache (Sıcak Bellek Önbelleği)
Fotoğraf açıldığında LibRaw C shim katmanı `output_bps = 16` modunda çalışır. Ham sensör pikselleri yüksek kaliteli AHD/DHT demosaicing ile belleğe bir kez alınır ve `DaemonCache` içinde sıcak RAM tamponunda tutulur. 

### 2. Çift Tamponlu (Double-Buffered) Ping-Pong `/dev/shm`
Arayüz (Quickshell / QML) ile Rust motoru, Linux çekirdeğinin doğrudan RAM tabanlı paylaşımlı belleği olan `/dev/shm` üzerinde haberleşir:
* Birinci kaydırıcı hareketi `/dev/shm/omastudio_preview_0.ppm` tamponuna yazılır.
* İkinci hareket `/dev/shm/omastudio_preview_1.ppm` tamponuna yazılır.
* GPU dokusu (texture) ekranda tek bir piksel bile kırpışmadan (zero flicker) 60 FPS hızında takas edilir (swap).

### 3. Satır Tabanlı JSON-RPC Protokolü
Masaüstü paneli kapandığında arkada zombi süreç bırakmamak için `AGENTS.md` standartlarına uygun, stdin üzerinden satır tabanlı JSON-RPC protokolü kuruldu (`load`, `adjust`, `ai_auto`, `ai_social`, `save_recipe`, `exit`).

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
  <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
  OmaStudio Kalıcı Süreç ve Paylaşımlı Bellek Mimarisi
  </div>
  <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">60 FPS /dev/shm IPC</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
  <!-- UI Node -->
  <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50 flex flex-col justify-between">
  <div>
  <span class="text-[10px] font-bold text-[#8b3a2b] dark:text-[#d48372] uppercase tracking-wider">Arayüz Katmanı</span>
  <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-1 mb-2">Quickshell UI (Qt 6 QML)</div>
  <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">GPU ivmeli Wayland penceresi, dokunmatik tuval kontrolleri ve renk tekerlekleri.</p>
  </div>
  <div class="mt-3 px-2 py-1 rounded bg-[#ead9d2]/40 dark:bg-[#2a2421] text-[#3c2a21] dark:text-[#e7e5e4] text-[10px] font-semibold">
  Zero Flicker Dokusu
  </div>
  </div>
  <!-- Communication Bridge -->
  <div class="p-4 rounded-xl border border-[#8b3a2b]/30 bg-[#8b3a2b]/5 dark:bg-[#8b3a2b]/15 flex flex-col justify-between">
  <div>
  <span class="text-[10px] font-bold text-[#8b3a2b] dark:text-[#d48372] uppercase tracking-wider">İki Yönlü IPC Köprüsü</span>
  <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-1 mb-2">stdin RPC + /dev/shm</div>
  <div class="space-y-1.5 text-[11px] text-[#5c4033] dark:text-[#d6d3d1] mt-2">
  <div class="p-1.5 rounded bg-white/80 dark:bg-black/40 border border-[#8b3a2b]/20">
  <strong>İstek:</strong> stdin JSON-RPC
  </div>
  <div class="p-1.5 rounded bg-white/80 dark:bg-black/40 border border-[#8b3a2b]/20">
  <strong>Piksel:</strong> /dev/shm Ping-Pong PPM
  </div>
  </div>
  </div>
  <div class="mt-3 text-[10px] text-[#8b3a2b] dark:text-[#d48372] font-semibold">
  Sıfır Disk G/Ç Gecikmesi
  </div>
  </div>
  <!-- Engine Daemon -->
  <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50 flex flex-col justify-between">
  <div>
  <span class="text-[10px] font-bold text-[#8b3a2b] dark:text-[#d48372] uppercase tracking-wider">Motor Katmanı</span>
  <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-1 mb-2">omastudio-engine (Rust)</div>
  <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">Kalıcı arka plan daemon'ı. Tek seferlik LibRaw demosaic, 16-bit sıcak RAM önbelleği.</p>
  </div>
  <div class="mt-3 px-2 py-1 rounded bg-emerald-100/70 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300 text-[10px] font-semibold">
  Rayon Çok Çekirdekli
  </div>
  </div>
  </div>
</div>

---

## Stüdyo Standardı: Gerçek 16-Bit Master Export

Bir fotoğrafı ekranda 16-bit düzenlemek kadar, laboratuvar baskısına veya müşteriye 16-bit teslim edebilmek de kritiktir. OmaStudio'nun dışa aktarma motoru baştan aşağı güncellendi:

* **16-Bit TIFF (48-bit RGB):** Büyük boy fine-art baskılar için piksel başına 16-bit kayıpsız TIFF çıktısı.
* **16-Bit PNG:** Web ve arşivleme için 48-bit tam renk derinliğinde PNG.
* **10/12/16-Bit JXL ve AVIF:** Yeni nesil JPEG XL (`cjxl`) ve AVIF (`avifenc`) kodlayıcılarına 16-bit ara veri beslenerek Geniş Renk Gamı (WCG) ve HDR dinamik aralığı tam olarak korunur.
* **Akıllı 8-Bit İndirgeme:** JPEG ve WebP gibi geleneksel formatlarda ise renk uzayı güvenli şekilde en yüksek kalitede 8-bit'e sıkıştırılır.

---

## Film Looks & Styles: Reaktif RESET Butonu

Kullanıcılarımızdan gelen geri bildirimler doğrultusunda, **Film Looks & Styles** panelinin başlığına akıllı ve reaktif bir **RESET** butonu entegre edildi. Bir film simülasyonu (Fuji Classic Chrome, Velvia 50, Kodak Portra vb.) seçildiğinde beliren bu buton, tek bir tıklamayla tüm ton eğrilerini ve renk kaymalarını sıfırlayarak fotoğrafı sensörün orijinal nötr profiline döndürür.

---

## Performans Kıyaslaması (112 MB Fujifilm RAF Dosyası)

| İşlem / Metrik | Eski Sürüm (0.1) | Yeni Sürüm (0.2 - 16-Bit Daemon) | Kazanç / Fark |
| :--- | :---: | :---: | :---: |
| **İşleme Renk Derinliği** | 8-Bit (256 seviye) | **16-Bit (65,536 seviye)** | **256 kat ton hassasiyeti** |
| **Gölge Kurtarma Kalitesi** | Renk basamaklanması | **Sıfır banding / İpeksi geçiş** | Kusursuz dinamik aralık |
| **Kaydırıcı Tepki Süresi** | ~450ms (disk okuma) | **108ms (RAM içi Rayon)** | **4.5 kat daha hızlı** |
| **Süreç Çatallanması (Fork)** | Her kaydırmada 1 PID | **0 PID (Tek kalıcı daemon)** | Sıfır CPU tepe noktası |
| **Master Export Derinliği** | 8-Bit TIFF | **16-Bit TIFF (48-bit RGB)** | Profesyonel stüdyo teslimatı |

---

## Güncelleme ve Kurulum

Mevcut OmaStudio kurulumunuzu güncellemek için depoyu çekip derlemeniz yeterlidir:

```bash
git pull origin master
cargo build --release --locked
install -m 755 target/release/omastudio-engine ~/.local/bin/
omastudio
```

Açık kaynak dünyasında orta format RAW düzenlemeyi hak ettiği performansa ve renk zenginliğine kavuşturmaktan mutluluk duyuyoruz.

* **GitHub:** [github.com/ozdil/omarchy-omastudio](https://github.com/ozdil/omarchy-omastudio)
* **Lisans:** MIT License
