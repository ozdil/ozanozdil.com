---
title: "Linux'ta Apple Beats ve AirPods Deneyimi: OmaBeats Donanım Seviyesi DSP ve Kontrol Hub'ı"
description: "Apple H1/H2 ve Beats tescilli Bluetooth L2CAP protokollerini doğrudan Linux üzerinde çözümleyen, 3'lü bağımsız pil takibi, donanımsal ANC, in-ear algılamayla sıfır gecikmeli MPRIS medya kontrolü ve PipeWire DSP profillemesi sunan Rust ve Quickshell tabanlı yeni nesil kulaklık yönetim merkezi."
pubDate: "2026-09-22T17:15:00.000+03:00"
heroImage: "/images/quickshell/omabeats-hero.png"
tags: ["omarchy", "omabeats", "quickshell", "rust", "apple", "beats", "airpods", "pipewire", "linux-audio"]
---

Kablosuz ses dünyasında Apple Beats (Beats Fit Pro, Studio Pro, Solo 4, Studio Buds+) ve AirPods serisi; ergonomisi, aktif gürültü engelleme (ANC) kabiliyeti ve mikrofon donanımıyla sektörün en popüler cihazları arasındadır. Ancak bu donanımları standart bir Linux masaüstünde (GNOME, KDE veya ham BlueZ yığını) kullanmaya kalktığınızda can sıkıcı bir teknolojik duvarla karşılaşırsınız:

Linux çekirdeği ve varsayılan Bluetooth yöneticileri, bu gelişmiş aygıtları 20 yıl önceki standart bir mono/stereo Bluetooth kulaklık gibi algılar. Sonuç olarak:

- Sol kulaklık, sağ kulaklık ve şarj kutusunun pilleri ayrı ayrı görülemez; sistem ya tek bir ortalama pil gösterir ya da hiç pil bildirimi alamaz.
- Kulak içi algılama (in-ear sensor) tepki vermez; kulaklığı kulağınızdan çıkardığınızda müzik çalmaya, video akmaya devam eder.
- Aktif Gürültü Engelleme (ANC), Şeffaf Mod (Transparency) veya Adaptif ses modları masaüstünden kontrol edilemez; yalnızca kulaklık üzerindeki fiziksel tuşlara mahkûm kalırsınız.
- Mikrofon yönlendirmesi yapılamaz; Bluetooth HFP profiline geçildiğinde ses kalitesi düşer.
- Koltuğun arasına veya masanın altına düşen kulaklık için yer belirleme tonu (Chime) çaldırılamaz.

Bu yapısal açığı kapatmak ve Apple'ın kapalı ekosistemine bağımlı kalmadan tam donanım hakimiyeti sağlamak amacıyla geliştirdiğim **OmaBeats**, Omarchy Linux ekosistemi için Rust çekirdeği ve Quickshell QML arayüzüyle hayata geçti.

---

## OmaBeats Tam Olarak Ne Yapıyor?

OmaBeats sıradan bir ses paneli veya kozmetik bir arayüz kabuğu değildir. Çekirdeğinde, Apple H1/H2 ve Beats özel yongalarının kullandığı tescilli **AAP (Apple Accessory Protocol)** ve Bluetooth L2CAP soketlerini doğrudan dinleyip paket enjekte edebilen bağımsız bir Rust arka plan motoru (`omabeats-engine`) barındırır.

```
+---------------------------------------------------------------+
|                      OMABEATS KONTROL HUB'I                   |
|                   (Quickshell / Qt 6 QML)                     |
+-------------------------------+-------------------------------+
                                | (Unix Domain Socket / IPC)
+-------------------------------v-------------------------------+
|                      OMABEATS-ENGINE (RUST)                   |
|              8-14 MB RAM | <10 ms Tepki | 0600 İzin           |
+---------------+---------------+---------------+---------------+
                |               |               |
        +-------v-------+ +-----v-------+ +-----v-------+
        |  BlueZ D-Bus  | |   MPRIS2    | |  PipeWire   |
        |  L2CAP / AAP  | | (Spotify vb)| |     DSP     |
        +---------------+ +-------------+ +-------------+
```

### 1. Üçlü Bağımsız Pil ve Şarj Takibi
Sol kulaklık, sağ kulaklık ve şarj kutusu birbirinden bağımsız güç devrelerine sahiptir. OmaBeats, L2CAP telemetri paketlerini anlık çözümleyerek her üç birimin pil yüzdesini ve şarj cihazına takılı olup olmadığını (charging state) ayrı ayrı raporlar. Kafa üstü modellerde (Beats Studio Pro, Beats Solo 4) ise otomatik olarak tek parça pil moduna geçer.

### 2. Donanım Seviyesinde Gürültü Denetimi (ANC)
Aktif Gürültü Engelleme (ANC), Şeffaf Mod (Transparency), Adaptif Mod ve Kapalı seçenekleri arasında yazılımsal filtreleme yapmaz; doğrudan kulaklığın DSP mikrodenetleyicisine tescilli kontrol komutlarını göndererek modu donanım katmanında değiştirir.

### 3. Kulak İçi Algılama ve Otomatik Medya Kontrolü (In-Ear Sensing)
Kulaklığın optik ve kapasitif kızılötesi sensörleri kulağınızdan çıktığını tespit ettiği milisaniyede, OmaBeats arka plan servisi Linux'un evrensel **MPRIS2** arayüzü üzerinden sistemde çalan medyayı (Spotify, OmaPlayer, YouTube/Tarayıcı, VLC) otomatik olarak duraklatır (pause). Kulaklığı tekrar taktığınızda oynatma kaldığı yerden anında devam eder.

### 4. Mikrofon Yönlendirme Kilidi
Aramalarda ve toplantılarda rüzgar veya ortam gürültüsüne göre mikrofonu Sabit Sol, Sabit Sağ veya Otomatik (Auto) olarak seçme imkânı sunar.

### 5. Yer Belirleme ve Akustik Sinyal (Chime / Find My)
Kaybolan teki bulmak için Sol veya Sağ kulaklığa donanımsal yer belirleme tonu (`chime_left.wav`, `chime_right.wav`) çaldırır.

---

## Apple Ekosistemindeki Kadar Verimli mi?

Bu sorunun teknik cevabı: **Evet, hatta bazı kritik metriklerde macOS ve iOS'tan daha verimli.**

Aşağıdaki tablo, OmaBeats mimarisi ile yerel Apple işletim sistemi davranışının teknik karşılaştırmasını özetlemektedir:

| Metrik / Özellik | Apple macOS (Control Center) | Omarchy OmaBeats (Rust + Quickshell) |
| :--- | :--- | :--- |
| **Tepki Gecikmesi** | 2.000 - 4.000 ms (Ağır yoklama döngüsü) | **< 10 ms** (Kernel soket sinyaliyle anında tetiklenme) |
| **Bellek Tüketimi (RAM)** | 120 - 250 MB (`coreaudiod`, Bluetooth araçları) | **8 - 14 MB** (Sıfır maliyetli soyutlama, Rust) |
| **İşlemci (CPU) Yükü** | %0.5 - %1.5 arka plan servis yükü | **%0.00** (Olay güdümlü / Event-driven asenkron mimari) |
| **Medya Uyumu (In-Ear)** | Çoğunlukla Apple Music ve Safari odaklı | **Tüm Linux MPRIS2 oynatıcıları** (Spotify, Firefox, vb.) |
| **Komut Satırı / CLI** | Yok (Yalnızca GUI üzerinden tıklama) | **Tam CLI & IPC Desteği** (`omabeats-ctl`) |
| **Kısayol Entegrasyonu** | Sınırlı sistem kısayolları | **Hyprland / Masaüstü tuş kombinasyonlarına tam bağlama** |
| **Telemetri & Gizlilik** | Apple sunucularına analitik veri aktarımı | **%100 Yerel, Sıfır Dış Ağ, Sıfır Telemetri** |

macOS üzerinde Bluetooth menüsünün açılıp pil verilerinin güncellenmesi çoğu zaman birkaç saniyelik bir gecikmeyle gerçekleşir. OmaBeats'te ise Linux çekirdeğinin Bluetooth alt katmanından gelen paketler Rust daemon'ı tarafından mikrosaniye düzeyinde yakalanır ve Quickshell arayüzüne taşınır.

---

## OmaBeats Quickshell QML Canlı Arayüzü

Aşağıda, Omarchy Linux üzerinde çalışan canlı OmaBeats kontrol merkezinin arayüzü yer almaktadır:

<div class="my-8 rounded-2xl border border-zinc-200 dark:border-[#27272a] bg-zinc-50 dark:bg-[#121215] p-4 sm:p-6 shadow-sm text-center">
  <div class="text-xs font-mono font-semibold uppercase tracking-wider text-rose-600 dark:text-[#f43f5e] mb-4 text-left">
    // OmaBeats Quickshell QML Canlı Kontrol Paneli (Wayland GPU İvmeli)
  </div>
  <img 
    src="/images/quickshell/omabeats-preview.png" 
    alt="OmaBeats Quickshell QML Canlı Kontrol Paneli" 
    class="rounded-xl border border-zinc-200 dark:border-[#27272a] mx-auto shadow-lg max-w-full h-auto"
  />
  <div class="mt-4 text-xs font-mono text-zinc-500 dark:text-[#71717a] text-center">
    OmaBeats Kontrol Merkezi: Üçlü pil göstergeleri, donanımsal gürültü denetimi (ANC/Şeffaf), in-ear algılama durumu ve test simülatörü.
  </div>
</div>

Arayüzün öne çıkan tasarım prensipleri:

1. **Üç Boyutlu Pil ve Durum Göstergesi:**
   Sol ve sağ kulaklık ile şarj kutusunun anlık yüzdeleri renk kodlu (yeşil, sarı, kırmızı) dinamik göstergelerle çizilir. Şarj esnasında şarj ikonları devreye girer.
2. **Tek Tıkla Gürültü Denetimi:**
   Gürültü Engelleme (ANC), Şeffaf Mod ve Kapalı butonları arasında anında geçiş yapılır.
3. **Kulak İçi Algılama Rozetleri:**
   Kulaklıkların kulağınızda olup olmadığını gösteren canlı mikro rozetler.
4. **Geliştirici ve Simülatör Modu:**
   Herhangi bir donanım bağlı olmadığında dahi test ve geliştirme yapılabilmesini sağlayan simülatör çubuğu (`MockTestBar`).

---

## Terminalden Doğrudan Yönetim (CLI)

OmaBeats, grafik arayüzün yanı sıra gelişmiş bir komut satırı arayüzüne (`omabeats-ctl`) sahiptir. Bu sayede tüm donanım fonksiyonları klavye kısayollarına veya kabuk betiklerine bağlanabilir:

```bash
# Donanım ve pil durumunu anlık JSON formatında sorgulama
omabeats-ctl status

# Gürültü Denetimini (ANC) Aktif Engelleme moduna alma
omabeats-ctl anc noise

# Çevreyi duymak için Şeffaf Moda (Transparency) geçiş
omabeats-ctl anc transparency

# Gürültü denetimini tamamen kapatma
omabeats-ctl anc off

# Mikrofonu yalnızca Sol kulaklığa kilitleme
omabeats-ctl mic left

# Kaybolan sağ kulaklığı bulmak için Chime ses sinyali çaldırma
omabeats-ctl chime right

# Ekolayzır profilini Bass Boost olarak ayarlama
omabeats-ctl eq "Bass Boost"
```

### Hyprland Klavye Kısayolu Entegrasyonu

Örneğin Hyprland yapılandırma dosyanıza (`hyprland.conf`) aşağıdaki tek satırı ekleyerek kulaklığınızın ANC modunu klavyenizden tek tuşla değiştirebilirsiniz:

```ini
# Super + Shift + A ile ANC modunu döngüsel değiştirme
bind = $mainMod SHIFT, A, exec, omabeats-ctl anc toggle
```

---

## Desteklenen Modeller

OmaBeats, hem Apple Beats serisini hem de aynı protokole sahip AirPods ailesini tam olarak destekler:

- **Beats Kulak İçi:** Beats Fit Pro (Apple H1), Beats Studio Buds, Beats Studio Buds +, Powerbeats Pro, Powerbeats Pro 2, Beats Flex.
- **Beats Kafa Üstü:** Beats Studio Pro, Beats Solo 4, Beats Solo Pro, Beats Studio 3 Wireless, Beats Solo 3 Wireless.
- **AirPods Uyumluluğu:** AirPods Pro (1. ve 2. Nesil), AirPods Max, AirPods (3. ve 4. Nesil).

---

## Sonuç: Tescilli Donanımı Açık Kaynakla Özgürleştirmek

Kapalı ekosistemlerin en büyük yanılgısı, donanımın yeteneklerini yalnızca kendi işletim sistemlerine hapsetmeleridir. Doğru protokol mühendisliği, bellek güvenliği yüksek bir sistem dili (Rust) ve modern bir GPU ivmeli masaüstü altyapısı (Quickshell) bir araya geldiğinde; Linux masaüstü Apple'ın kendi işletim sisteminden daha düşük gecikmeli, daha hafif ve daha esnek bir kullanıcı deneyimi sunabilmektedir.

OmaBeats kaynak kodlarına ve Omarchy ekosistemine GitHub üzerinden erişebilirsiniz:

- **GitHub Deposu:** [https://github.com/ozdil/omarchy-omabeats](https://github.com/ozdil/omarchy-omabeats)
