---
title: "PolyCodex: 1:1 Mizanpaj ve Görsel Dokunulmazlığı Sunan, 5000 Sayfa Kapasiteli Açık Kaynak PDF Çevirici"
description: "PDF içerik akışındaki metin bloklarını cerrahi hassasiyetle ayıklayan, görselleri ve tabloları piksellerine kadar koruyan, Tz mikrotipografik yatay sıkıştırmayla taşmaları önleyen ve Ollama yerel yapay zekâsıyla tamamen çevrimdışı çalışan Rust ve Quickshell tabanlı yeni nesil kodeks çeviri motoru."
pubDate: "2026-09-22T17:00:00.000+03:00"
heroImage: "/images/quickshell/polycodex-preview.png"
tags: ["polycodex", "rust", "quickshell", "pdf", "yapay-zeka", "ollama", "acik-kaynak", "linux-desktop", "guvenlik"]
---

Akademik araştırmalarda, kapsamlı tıp literatüründe, askeri teknik el kitaplarında ve binlerce sayfalık mühendislik dokümantasyonlarında çalışan herkesin karşılaştığı ortak ve kronik bir açmaz vardır: **PDF çevirisinin imkânsızlığı.**

Geleneksel araçlar (Google Translate PDF modülü, Adobe Acrobat, Calibre veya yaygın OCR yazılımları) bir belgeyi diğer bir dile aktarmaya çalıştığında felaket senaryoları kaçınılmaz hale gelir: Çok sütunlu sayfalar birbirine karışır, teknik çizimler ve vektör şemaları sayfa dışına fırlar, tablolar parçalanır, dipnotlar ana metnin ortasına saplanır ve nihayetinde 10 MB veya 300 sayfa gibi keyfi sunucu sınırlarına takılarak süreç kesintiye uğrar.

Daha da vahimi; kurumsal belgelerin, patent taslaklarının ve gizli araştırmaların üçüncü parti bulut sunucularına kontrolsüzce aktarılması, veri egemenliği ve siber güvenlik açısından kabul edilemez bir zafiyettir.

Bu yapısal problemleri kökünden çözmek, mizanpaj ve görselleri dokunulmaz kılmak ve tamamen yerel donanım üzerinde 5000+ sayfalık kodeksleri dahi akıcı şekilde dönüştürebilmek amacıyla geliştirdiğim **PolyCodex**, bugün bağımsız bir açık kaynak proje olarak yayında.

---

## Temel Felsefe: "Mizanpaj Kutsaldır, Görsel Dokunulmazdır"

PDF (ISO 32000), bir Word dokümanı gibi akışkan metin paragraflarından oluşmaz. PDF, her bir harfin, çizginin ve görselin iki boyutlu bir koordinat düzleminde (`x, y`) mutlak konumlarla tanımlandığı dijital bir baskı tuvalidir.

Mevcut çeviri araçlarının başarısız olmasının temel nedeni, PDF'i metin tabanlı bir belgeye dönüştürüp ardından tekrar derlemeye (re-render) çalışmalarıdır. Bu yaklaşım, orijinal belgenin tüm tipografik geometrisini yok eder.

PolyCodex farklı bir paradigma benimser: **Cerrahi İçerik Akışı Manipülasyonu.**

<div class="my-8 rounded-2xl border border-zinc-200 dark:border-[#27272a] bg-zinc-50 dark:bg-[#121215] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-zinc-200 dark:border-[#27272a] pb-3 mb-6">
    <div class="text-xs font-mono font-semibold uppercase tracking-wider text-zinc-900 dark:text-[#ffffff]">
      PolyCodex İçerik Akışı (Content Stream) Ayrıştırma Hattı
    </div>
    <span class="text-xs font-mono text-sky-600 dark:text-[#38bdf8]">lopdf &amp; Rust Engine</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-xs">
    <div class="p-4 rounded-xl bg-white dark:bg-[#18181b] border border-zinc-200 dark:border-[#27272a]">
      <div class="text-sky-600 dark:text-[#38bdf8] font-bold mb-2">// 1. METİN BLOKLARI (BT / ET)</div>
      <p class="text-zinc-600 dark:text-[#a1a1aa] leading-relaxed">
        Yalnızca BT (Begin Text) ve ET (End Text) arasındaki Tj, TJ operatörleri okunur. Matris konumları (Tm) saklanır, metinler çeviri havuzuna aktarılır.
      </p>
    </div>
    <div class="p-4 rounded-xl bg-white dark:bg-[#18181b] border border-emerald-500/30">
      <div class="text-emerald-600 dark:text-[#34d399] font-bold mb-2">// 2. GÖRSEL DOKUNULMAZLIĞI (Do)</div>
      <p class="text-zinc-600 dark:text-[#a1a1aa] leading-relaxed">
        Do (XObject çağırma) komutları, vektör yolları (re, m, l, c, f, S) ve renk durumları piksellerine kadar korunur. Tek bir bayt dahi silinmez.
      </p>
    </div>
    <div class="p-4 rounded-xl bg-white dark:bg-[#18181b] border border-rose-500/30">
      <div class="text-rose-600 dark:text-[#f43f5e] font-bold mb-2">// 3. Tz MİKROTİPOGRAFİ</div>
      <p class="text-zinc-600 dark:text-[#a1a1aa] leading-relaxed">
        Genişleyen hedef dil metni için dinamik yatay ölçekleme (Tz) hesaplanır. Orijinal sınır kutusu (bounding box) milimetrik olarak korunur.
      </p>
    </div>
  </div>
</div>

---

## Mikrotipografi ve `Tz` Yatay Ölçekleme Çözümü

Farklı dillerin karakter yoğunlukları ve kelime uzunlukları radikal biçimde farklıdır. Örneğin, İngilizce teknik bir doküman Türkçeye veya Almancaya çevrildiğinde metin hacmi ortalama **%25 ile %35** oranında genişler.

Geleneksel yazılımlar bu genişleme karşısında ya metni kırparak okunmaz hale getirir ya da bir sonraki görselin veya tablonun üzerine taşırarak sayfa düzenini bozar.

PolyCodex bu sorunu PDF standardının yerel operatörü olan **`Tz` (Horizontal Scaling / Yatay Ölçekleme)** ile çözer:

1. Çevrilen cümlenin hedef dildeki genişliği (`W_hedef`), orijinal cümlenin sınır kutusu genişliği (`W_orijinal`) ile kıyaslanır.
2. Eğer `W_hedef > W_orijinal` ise, font boyutu veya satır yüksekliği değiştirilmeden dinamik bir sıkıştırma faktörü hesaplanır:
   `Tz = max(75.0, (W_orijinal / W_hedef) * 100.0)`
3. Hesaplanan operatör doğrudan PDF içerik akışına enjekte edilir (örneğin `88.5 Tz`). Böylece harfler mikrotipografik bir zarafetle birbirine yaklaşır, sayfa sınırları aşılmaz ve yanındaki şema veya diyagram asla yerinden oynamaz.

---

## 5000+ Sayfa Kapasitesi ve Akış Bellek Mimarisi

Piyasadaki pek çok PDF aracı Python veya Node.js/Electron kütüphaneleriyle yazılmıştır. Bu araçlar tüm belge ağacını aynı anda RAM'e yüklemeye çalışır; 300-500 sayfadan sonra bellek tüketimi 8-16 GB seviyelerine fırlar ve sistem işletim sistemi tarafından `OOM Killer` (Out Of Memory) ile zorla sonlandırılır.

PolyCodex'in çekirdek motoru **Rust** ile inşa edilmiştir:

- **Sayfa Bazlı Akış (Streaming Architecture):** Belge sayfaları birer birer işlenir, geçici tamponlar temizlenir ve çıktı dosyasına güvenli şekilde yazılır.
- **Sabit Bellek Ayak İzi:** İster 10 sayfalık bir makale, ister 5.200 sayfalık bir farmakoloji el kitabı olsun; PolyCodex motorunun RAM tüketimi **150 MB ile 250 MB** bandında sabit kalır.
- **DoS ve Kaynak Tüketim Kalkanı:** Bellek tükenmesi ve bozuk/zararlı PDF saldırılarını engellemek adına katı **2 GiB tavan sınır kontrolü** uygulanır. Boyut kontrolleri `checked_add` ve güvenli sınır korumalarıyla denetlenir.
- **Sıkılaştırılmış Dosya İzinleri:** Üretilen geçici ve nihai dosyalar yalnızca dosya sahibinin erişebileceği `0600` izinleriyle (okuma/yazma) oluşturulur; sembolik bağlar (symlinks) kesin olarak reddedilir.

---

## Veri Egemenliği: Yerel Ollama ile %100 Çevrimdışı Çeviri

PolyCodex, kullanıcının çeviri motoru tercihinde tam bağımsızlık sağlar:

```
                  +-----------------------------------+
                  |             POLYCODEX             |
                  |     (Rust Core / Quickshell)      |
                  +-----------------+-----------------+
                                    |
          +-------------------------+-------------------------+
          |                         |                         |
          v                         v                         v
+-------------------+     +-------------------+     +-------------------+
|    YEREL OLLAMA   |     |  LIBRETRANSLATE   |     |    MOCK / TEST    |
| (Llama 3 / Qwen)  |     |   (Self-Hosted)   |     | (Yerel Simülatör) |
|  TAM ÇEVRİMDIŞI   |     |   AÇIK KAYNAK     |     |   SIFIR DIŞ AĞ    |
+-------------------+     +-------------------+     +-------------------+
```

1. **Ollama Entegrasyonu (Llama 3.2, Qwen 2.5, DeepSeek, Mistral):**
   Ağ bağlantısı gerektirmeyen, hava boşluklu (air-gapped) ortamlarda ve internet kesintilerinde bile donanımınızın gücüyle çalışan yerel yapay zekâ çevirisi. Hiçbir metin parçası bilgisayarınızın dışına çıkmaz.
2. **Açık Kaynak LibreTranslate Desteği:**
   Kendi sunucunuzda veya yerel ağınızda barındırdığınız açık kaynak çeviri API'ları ile tam uyum.
3. **Mock Modu:**
   Ağ ve LLM kaynağı bulunmayan test ortamlarında anında çeviri simülasyonu ve mizanpaj doğrulaması.

---

## Quickshell ve Modern Wayland Kullanıcı Deneyimi

PolyCodex, hantal ve bağımlılık yükü ağır geleneksel arayüzler yerine Omarchy masaüstünün amiral gemisi olan **Quickshell (Qt 6 / QML)** teknolojisini kullanır:

- **GPU İvmeli Akıcı Arayüz:** 60+ FPS pürüzsüz animasyonlar, OLED uyumlu saf siyah ve grafit koyu tema paleti.
- **Sistem Font Standardı:** Arayüzün tüm tipografik hiyerarşisi netlik ve okunabilirlik için `JetBrainsMono Nerd Font` standardıyla şekillendirilmiştir.
- **Canlı İlerleme ve Sayfa Takibi:** Çok büyük dokümanlarda hangi sayfada olunduğu, kalan süre ve anlık çeviri adımları milisaniye hassasiyetinde kullanıcıya raporlanır.
- **Tekil Süreç Kilit Kalkanı (Single-Instance Lock):** Uygulamanın aynı anda birden fazla başlatılarak sistem kaynaklarını tüketmesini önlemek amacıyla `$XDG_RUNTIME_DIR/polycodex.lock` dosya kilidi mekanizması devreye alınmıştır.

### Terminal Üzerinden Doğrudan Otomasyon (CLI Modu)

```bash
# Tek komutla PDF çevirisi (Kaynak: Otomatik, Hedef: Türkçe, Sağlayıcı: Ollama)
polycodex --input "/path/to/quantum_physics.pdf" \
          --output "/path/to/kuantum_fizigi.pdf" \
          --target "tr" \
          --provider "ollama"

# 5000 sayfalık teknik el kitabını yerel LibreTranslate ile dönüştürme
polycodex -i handbook.pdf -o el_kitabi.pdf -t tr -p libretranslate
```

---

## Kurulum ve Dağıtım Kanalları

PolyCodex; Arch Linux, Fedora, Ubuntu, Debian ve diğer tüm modern Linux dağıtımlarında zahmetsizce çalışacak şekilde paketlenmiştir.

### 1. Evrensel Tek Komutla Kurulum Betiği

Sisteminize en uygun ikiliyi indirip yapılandıran resmi kurulum betiği:

```bash
curl -sSL https://raw.githubusercontent.com/ozdil/polycodex/main/install.sh | bash
```

### 2. Arch Linux / AUR (Arch User Repository)

Arch Linux ve Omarchy kullanıcıları için resmi AUR paketi:

```bash
yay -S polycodex-bin
# veya kaynak koddan derlemek için:
yay -S polycodex
```

### 3. Evrensel Flatpak / Flathub Dağıtımı

Flathub resmi inceleme sürecinde yer alan (`org.ozdil.PolyCodex`) paketi ile tüm Linux platformlarında tek tıkla sandbox korumalı kurulum:

```bash
flatpak install flathub org.ozdil.PolyCodex
```

### 4. GitHub Bağımsız İkili Varlıklar (Releases)

Herhangi bir bağımlılık kurmadan doğrudan çalıştırmak isteyenler için GitHub Releases sayfasında derlenmiş x86_64 ikilileri mevcuttur:

- **Kaynak Kodu ve Sürümler:** [github.com/ozdil/polycodex](https://github.com/ozdil/polycodex)
- **Lisans:** Çift Lisans - MIT / Apache 2.0 (Özgür yazılım güvencesi)

---

## Sonuç: Bilginin Serbest Dolaşımı ve Açık Kaynak Gücü

İnsanlığın ürettiği bilimsel ve teknik bilginin çok büyük bir kısmı yabancı dillerde ve kapalı PDF formatlarının ardında hapsolmuş durumdadır. Bu bilgiye erişmek isteyen araştırmacıların, öğrencilerin ve mühendislerin mizanpajı bozulmuş, şemaları silinmiş veya sayfaları kırpılmış çevirilere mahkûm kalması kabul edilemez.

**PolyCodex**, hem yerel donanımın gücünü sonuna kadar kullanarak gizliliği korur hem de belgenin orijinal estetiğine ve tipografisine mutlak saygı gösterir.

Tüm kaynak kodları, katkı rehberi ve dokümantasyonu GitHub üzerinde topluluğun erişimine açıktır.

- **GitHub Deposu:** [https://github.com/ozdil/polycodex](https://github.com/ozdil/polycodex)
