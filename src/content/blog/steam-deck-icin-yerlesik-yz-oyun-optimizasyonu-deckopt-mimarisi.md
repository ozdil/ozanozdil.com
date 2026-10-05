---
title: "Steam Deck İçin Yerleşik YZ ile Otonom Oyun Optimizasyonu: deckopt Mimarisi, Donanım Koruması ve Performans Dinamikleri"
description: "Valve Steam Deck (LCD/OLED) ve SteamOS 3.x çalışma zamanında oyun bazlı TDP, GPU frekansı, FSR ve başlatma parametrelerini otonom optimize eden yerleşik yapay zekâ motoru deckopt'un sistem mimarisi, deterministik güvenlik katmanı ve Godot 4 arayüz mühendisliği."
pubDate: "2026-10-05T13:30:00.000+03:00"
updatedDate: "2026-10-05T13:30:00.000+03:00"
heroImage: "/images/blog/steam-deck-ai-optimizer-architecture.png"
tags: ["steam deck", "yapay zeka", "steamos", "godot 4", "linux", "optimizasyon", "donanim guvenligi", "gemini api", "oyun performansi"]
draft: false
legacyUrl: ""
---

> **Özet:** Elde taşınabilir oyun konsollarında (handheld PC) performans, saf işlem gücünden ziyade termal bütçe (TDP), pil kapasitesi ve kare süresi tutarlılığı (frame pacing) arasındaki hassas dengenin yönetilmesine bağlıdır. Valve Steam Deck kullanıcıları çoğu zaman her oyun için internet forumlarında saatlerce voltaj, GPU saat frekansı ve başlatma parametresi araştırmaktadır. Bu çalışmada; Steam Deck (LCD Jupiter ve OLED Galileo) donanımları üzerinde doğrudan çalışan, kütüphanedeki oyunları tarayarak Google Gemini 2.5 Flash ile oyuna özel optimizasyon profili üreten ve bunu katı deterministik sınırlarla donanım koruma filtrelerinden geçiren **deckopt** motorunun mimarisini, sistem seviyesindeki tasarım kararlarını ve açık kaynaklı alfa dağıtımını inceliyoruz.

---

## Bölüm I: Elde Taşınabilir Konsollarda Termal ve Güç Çıkmazı

Geleneksel masaüstü oyun sistemlerinde donanım bileşenleri (CPU, ayrık GPU) yüzlerce watt güç tüketebilir ve yüksek termal tavanlara (TDP) sahiptir. Ancak Valve Steam Deck gibi mobil form faktörlerinde tüm sistem; 15 Watt'lık tavan termal tasarım gücüne (APU TDP) ve 40 Wh (LCD) / 50 Wh (OLED) kapasiteli bir bataryaya sığdırılmak zorundadır.

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 not-prose font-mono shadow-xl">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
    <span class="font-mono text-xs uppercase tracking-wider font-semibold text-[#ffffff]">
      // STEAM DECK DONANIM DINAMIKLERI VE GUC TAVANI
    </span>
    <span class="text-xs text-[#71717a]">AMD Custom APU (Zen 2 + RDNA 2)</span>
  </div>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-[#a1a1aa]">
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b]">
      <div class="text-[#ffffff] font-semibold mb-2">Steam Deck LCD (Jupiter)</div>
      <div>- SoC: AMD Aerith (7nm, 4C/8T Zen 2)</div>
      <div>- GPU: 8 RDNA 2 CU (1.0 - 1.6 GHz)</div>
      <div>- Ekran: 7 inç 1280x800, 60 Hz sabit</div>
      <div>- Batarya: 40 Wh (~1.5 - 4 saat)</div>
    </div>
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b]">
      <div class="text-[#ffffff] font-semibold mb-2">Steam Deck OLED (Galileo)</div>
      <div>- SoC: AMD Sephiroth (6nm, 4C/8T Zen 2)</div>
      <div>- GPU: 8 RDNA 2 CU (1.0 - 1.6 GHz)</div>
      <div>- Ekran: 7.4 inç HDR OLED, 90 Hz VRR/Adım</div>
      <div>- Batarya: 50 Wh (~2.5 - 7 saat)</div>
    </div>
  </div>
</div>

Bu sınırlı güç bütçesi altında ortaya çıkan üç temel optimizasyon değişkeni şunlardır:

1. **İşlemci ve Grafik Güç Bölüşümü (CPU/GPU Power Starvation):** Eğer bir oyun CPU yoğunsa ve TDP serbest bırakılırsa, CPU çekirdekleri aşırı güç çekerek GPU'yu frekans düşürmeye (downclock) zorlar; bu da ani kare düşüşlerine (stuttering) neden olur.
2. **Kare Süresi Kararlılığı ve Yenileme Senkronizasyonu (Frame Pacing):** 60 Hz bir panelde 45 FPS almak, düzensiz kare aralıkları (33.3ms ve 16.6ms dalgalanması) nedeniyle 30 FPS sabit bir deneyimden çok daha akıcı hissettirmez. Kare hızının ekran yenileme hızının tam böleni olması (`refresh_hz % fps_limit == 0`) gerekir.
3. **Piksel Yeniden Yapılandırma ve Çözünürlük Ölçeği (FSR / Integer):** 800p doğal çözünürlük yerine %70-80 render ölçeğiyle FSR (FidelityFX Super Resolution) devreye sokulduğunda, grafik yükü belirgin derecede hafifler ve 3-4 Watt TDP tasarrufu sağlanır.

---

## Bölüm II: deckopt Sistem Mimarisi

deckopt, kullanıcıyı karmaşık sysfs parametreleri, Proton ortam değişkenleri ve forum girdileri arasında kaybolmaktan kurtarmak için **hibrit bir yapay zekâ orkestrasyon modeli** benimser.

Sistem iki ana katmandan meydana gelir:
1. **İstemci ve Yerleşik Arayüz Katmanı (Godot 4.7 & GDScript):** SteamOS Game Mode içerisinde doğrudan gamepad (D-Pad ve tuşlar) ile kontrol edilen, 1280x800 doğal çözünürlükte çalışan kullanıcı arayüzü.
2. **Otonom Optimizasyon Çekirdeği (Gemini 2.5 Flash & Profile Sanitizer):** Kurulu oyunları tarayan, hedef donanım profilini oluşturan, bulut LLM çıkarımı üzerinden en uygun konfigürasyonu belirleyen ve bunu katı filtrelerden geçiren analiz motoru.

```
+-------------------------------------------------------------------------------+
|                      Valve Steam Deck (SteamOS 3.x / Linux)                   |
+-------------------------------------------------------------------------------+
        |                                                       |
        v                                                       v
  [DMI / BIOS Kontrolü]                                   [Kütüphane Taraması]
  /sys/devices/virtual/dmi/id/product_name                appmanifest_*.acf
  -> jupiter (LCD, 60Hz) / galileo (OLED, 90Hz)           NVMe & MicroSD Mounts
        |                                                       |
        +---------------------------+---------------------------+
                                    |
                                    v
                     +-----------------------------+
                     |  Godot 4.7 Gamepad Arayüzü  |
                     |  (1280x800, D-Pad, Curses)  |
                     +-----------------------------+
                                    |
                                    v
                     +-----------------------------+
                     |  Yerel Veri Deposu (0600)   |
                     |  user://gemini.key          |
                     |  user://profiles.json       |
                     +-----------------------------+
                                    |
             HTTPS POST / Yalnızca: Oyun Adı + AppID + Donanım Modeli
                                    |
                                    v
                     +-----------------------------+
                     |  Google Gemini 2.5 Flash    |
                     +-----------------------------+
                                    |
                                    v (Yapılandırılmış JSON Yanıtı)
                     +-----------------------------+
                     |  DETERMİNİSTİK GÜVENLİK     |
                     |  profile.gd Kırpma Motoru   |
                     +-----------------------------+
                                    |
        +---------------------------+---------------------------+
        |                                                       |
        v                                                       v
[Quick Access Menü Rehberi]                             [Steam Başlatma Satırı]
- TDP Sınırı: 3 - 15 W                                  DXVK_FRAME_RATE=40
- GPU Frekansı: 200 - 1600 MHz                          WINE_FULLSCREEN_FSR=1
- Ekran: 40 - 90 Hz                                     gamemoderun %command%
```

---

## Bölüm III: Güvenlik, Donanım Kilidi ve Deterministik Kırpma

Üretken yapay zekâ modelleri (LLM) doğası gereği olasılıksaldır ve halüsinasyon riski taşırlar. Bir dil modelinin termal bir parametre için `25W` veya `2200MHz` gibi cihaz donanım sınırlarını aşan ya da sistemi kilitleyecek değerler önermesi fiziksel olarak mümkündür.

Bu nedenle deckopt mimarisinde **YZ çıktısına asla doğrudan güvenilmez**. Tüm çıkarım sonuçları `profile.gd` içerisinde yer alan deterministik kabul kapısından (Sanitization Layer) geçmek zorundadır.

### 1. Donanım Tavan ve Taban Sınırları
```gdscript
const LIMITS := {
    "tdp_w": [3, 15],
    "gpu_clock_mhz": [200, 1600],
    "fps_limit": [0, 90],
    "refresh_hz": [40, 90],
    "render_scale": [50, 100],
}
```
LLM ne önerirse önersin, TDP değeri `[3, 15]` aralığının dışına çıkamaz. Ekran yenileme hızı LCD modelinde tespit edilmişse donanımsal tavan `60 Hz`, OLED modelinde ise `90 Hz` olarak üst sınırla kilitlenir.

### 2. Matematiksel Kare Tutarlılığı Fonksiyonu
```gdscript
static func _fit_fps(fps: int, hz: int) -> int:
    if fps == 0 or hz % fps == 0:
        return fps
    for d in range(fps, 29, -1):
        if hz % d == 0:
            return d
    return hz
```
Kare hızı hedefi, ekran tazeleme hızının tam böleni olacak şekilde otomatik hizalanır. Örneğin LLM 50 FPS önerdiğinde ve ekran 60 Hz olduğunda, kare yırtılmasını veya pacing bozulmasını önlemek için değer otomatik olarak 30 FPS tabanına indirgenir veya ekran hızı ayarlanır.

### 3. Ortam Değişkenleri Beyaz Listesi (Allowlist)
Kabuk enjeksiyonlarını ve sistemik bozulmaları engellemek amacıyla yalnızca Proton ve Mesa grafik katmanının resmî bayrakları kabul edilir:
- `PROTON_USE_WINED3D`, `PROTON_NO_ESYNC`, `PROTON_NO_FSYNC`
- `DXVK_ASYNC`, `DXVK_FRAME_RATE`, `RADV_PERFTEST`
- `WINE_FULLSCREEN_FSR`, `WINE_FULLSCREEN_FSR_STRENGTH`
- `mesa_glthread`, `ENABLE_GAMESCOPE_WSI`

Girdiler `^[A-Za-z0-9_.,:=+\-/]{0,128}$` düzenli ifadesiyle taranır; noktalı virgül (`;`), ampersand (`&`), boru (`|`) gibi kabuk komut zincirleyicileri tespit edildiği anda elenir.

---

## Bölüm IV: Godot 4 ile Game Mode Uyumlu Arayüz Geliştirme

Steam Deck üzerinde çalışan masaüstü araçlarının en büyük eksikliği, Game Mode (Oyun Modu) arayüzünde klavye ve fareye bağımlı olmalarıdır. deckopt'un kullanıcı arayüzü doğrudan **Godot 4.7 Engine** kullanılarak geliştirilmiştir.

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 not-prose font-mono shadow-xl">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
    <span class="font-mono text-xs uppercase tracking-wider font-semibold text-[#ffffff]">
      // ARAYÜZ VE GİRDİ TASARIM PRENSİPLERİ
    </span>
    <span class="text-xs text-[#71717a]">Steam Input & D-Pad Navigasyonu</span>
  </div>
  
  <div class="space-y-3 text-xs text-[#a1a1aa]">
    <div>- <strong>Doğal Çözünürlük:</strong> 1280x800 piksel, CanvasItems esneme moduyla piksel bozulmasız görünüm.</div>
    <div>- <strong>Tipografi Standardı:</strong> Tüm arayüz elemanlarında <code>JetBrainsMono Nerd Font</code> zinciri zorunludur.</div>
    <div>- <strong>Focus Yönetimi:</strong> Ekran geçişlerinde dinamik <code>grab_focus()</code> ile kumanda odağının kaybolması engellenir.</div>
    <div>- <strong>Asenkron İptal Emniyeti:</strong> Çoklu oyun kuyruğunda kullanıcı istediği an optimizasyonu durdurabilir.</div>
  </div>
</div>

Arayüz ayrıca cihazın Steam Deck olmadığını algıladığında (örneğin sıradan bir Linux x86_64 bilgisayarda başlatıldığında) kilit ekranını devreye sokar ve kullanıcıyı bilgilendirerek sonlanır:

```
+---------------------------------------------------------------+
|  Desteklenmeyen cihaz                                         |
|                                                               |
|  deckopt yalnızca Valve Steam Deck (LCD ve OLED) üzerinde     |
|  çalışır.                                                     |
|  Tespit edilen cihaz: slayer 4 ultra                          |
|                                                               |
|  [                     Çıkış                        ]         |
+---------------------------------------------------------------+
```

---

## Bölüm V: Dağıtım, Kurulum ve Gelecek Yol Haritası

deckopt, hiçbir üçüncü taraf mağaza bağımlılığı olmadan doğrudan SteamOS içerisine entegre olabilmektedir.

### Tek Komutla Kurulum
Kullanıcı Steam Deck masaüstü modunda Konsole terminalini açarak aşağıdaki komutu çalıştırır:

```bash
curl -fsSL https://github.com/ozdil/deckopt/releases/latest/download/install.sh | bash
```

Kurulum betiği:
1. `/sys/devices/virtual/dmi/id/product_name` üzerinden cihazın `jupiter` veya `galileo` olduğunu teyit eder.
2. GitHub Releases üzerinden en güncel derlemeyi ve `SHA256SUMS` özetini indirip doğrular.
3. Uygulamayı `~/Applications/deckopt/` dizinine yerleştirir.
4. SteamOS'in yerel `steamos-add-to-steam` aracını tetikleyerek uygulamayı kütüphaneye **"Steam Dışı Oyun"** olarak ekler.

Game Mode'a dönüldüğünde uygulama kütüphanede bir oyun gibi belirir ve doğrudan kontrolcüyle başlatılabilir.

### Gelecek Faz: Decky Loader Eklentisi ve MangoHud Kapalı Çevrim Geri Beslemesi
Alfa sürümünde üretilen profiller kullanıcıya Quick Access Menüsü yönergeleri ve panoya kopyalanabilir başlatma seçenekleri olarak sunulmaktadır. Gelecek sürümlerde planlanan iki ana kabiliyet şunlardır:

1. **Decky Loader Eklentisi:** React/TypeScript tabanlı QAM paneli üzerinden profillerin root yetkisiyle (`ryzenadj` ve `pp_od_clk_voltage`) tek dokunuşla otomatik uygulanması.
2. **MangoHud CSV İnce Ayarı (`deckopt tune`):** Oyun sırasında arka planda toplanan kare hızı ve güç telemetrisinin ayrıştırılması; ortalama kare hızı hedefin altındaysa dinamik FSR ölçeğinin düşürülmesi, hedefin üzerindeyse TDP'nin kısılarak batarya ömrünün uzatılması.

---

## Sonuç

Yapay zekânın uç cihazlarda (edge computing) donanım yönetimi için kullanılması, özellikle termal ve güç kısıtlarının yüksek olduğu el konsollarında büyük bir potansiyele sahiptir. **deckopt**, üretken yapay zekânın analitik gücünü deterministik donanım sınırlarıyla birleştirerek Steam Deck ekosistemine güvenli, açık kaynaklı ve topluluk odaklı bir optimizasyon katmanı kazandırmaktadır.

Projenin kaynak kodlarına, kurulum betiklerine ve sürüm notlarına [GitHub üzerinden](https://github.com/ozdil/deckopt) erişebilirsiniz.
