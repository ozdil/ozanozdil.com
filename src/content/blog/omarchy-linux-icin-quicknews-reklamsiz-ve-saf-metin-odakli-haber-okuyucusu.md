---
title: "Omarchy Linux İçin QuickNews: %100 Reklamsız, Resimsiz ve Saf Metin Odaklı Açık Kaynak Haber Okuyucusu"
description: "Görsel kirlilikten, banner reklamlardan ve clickbait tuzaklarından arındırılmış; Quickshell Wayland arayüzü, bağımsız Rust motoru, güncel RSS/Atom XML doğrulama kalkanı ve yerel yapay zeka özetleme özellikleriyle QuickNews projesinin doğuşu."
pubDate: 2026-09-18
heroImage: "/images/quickshell/quicknews-preview.png"
tags: ["omarchy", "quickshell", "rust", "açık-kaynak", "rss", "haber-okuyucu", "gizlilik", "adblock"]
---

İnternette güncel gelişmeleri takip etmek, modern web ortamında giderek yıpratıcı bir mücadeleye dönüştü. Bir haber sitesine girdiğinizde ekranın dört bir yanından fırlayan video reklamlar, tüm görüş alanını kapatan çerez onay pencereleri, bülten aboneliği dayatmaları, her paragrafın arasına sıkıştırılmış yüzlerce piksellik anlamsız stok fotoğraflar ve okuyucuyu sayfalarca tıklamaya zorlayan yanıltıcı (clickbait) başlıklar...

Geliştiriciler, araştırmacılar, sistem yöneticileri ve vaktini bilgiye doğrudan ulaşarak değerlendirmek isteyen kullanıcılar için bu durum kabul edilemez bir bilişsel yük oluşturuyor. Çoğu zaman aradığımız şey sadece birkaç satırlık saf metin, olayın özü ve teknik doğruluğudur.

Bu sorunu kökünden çözmek amacıyla; Omarchy Linux ve modern Wayland masaüstü ekosistemi için tasarladığımız **QuickNews** projesini duyurmaktan heyecan duyuyorum. QuickNews; **%100 açık kaynak kodlu**, **reklamsız**, **resimsiz**, **saf metin odaklı (text-first)**, **güncel RSS/Atom XML doğrulama kalkanına sahip** ve **yerel yapay zeka özetlemeli** bağımsız bir haber okuyucusudur.

---

## Felsefe: Saf Metin ve Bilişsel Sükunet

QuickNews'in temel tasarım felsefesi son derece nettir:

* **Sıfır Reklam:** Hiçbir reklam ağı, sponsorlu içerik widget'ı veya tanıtım paneli arayüze sızamaz.
* **Sıfır Resim ve Medya Kirliliği:** Haberler görsel süslemelerden, animasyonlu giflerden ve bant genişliğini tüketen afişlerden tamamen arındırılır.
* **Sıfır Takip ve Telemetri:** Kullanıcının hangi haberleri okuduğu, ne kadar süre sayfada kaldığı veya ilgi alanları hiçbir merkeze iletilmez; her şey yerel makinenizde kalır.
* **Ergonomik Tipografi:** Okuma paneli, göz yorgunluğunu önlemek adına 880 pikselle sınırlandırılmış metin sütunu, 1.6 satır yüksekliği ve varsayılan olarak **JetBrainsMono Nerd Font** yazı tipi ailesiyle optimize edilmiştir.

![QuickNews Ana Arayüzü](/images/quickshell/quicknews-preview.png)

---

## 1. Açık Kaynak, Yerel ve İzleyicisiz Mimari

QuickNews, MIT lisansı ile tamamen açık kaynaklı olarak geliştirilmektedir. Ticari haber okuyucularının veya web tabanlı servislerin aksine hiçbir bulut bağımlılığı, merkezi kullanıcı hesabı veya telemetri altyapısı barındırmaz.

Arka planda çalışan içerik temizleme motoru (DOM Temizleyici), gelen ham akış ve makale verilerini katı kurallarla süzer:

* HTML içerisindeki tüm `<img>`, `<picture>`, `<svg>`, `<video>`, `<audio>` ve `<iframe>` elemanları DOM ağacından tamamen kazınır.
* `ad-banner`, `sponsored-post`, `outbrain`, `taboola`, `newsletter-signup`, `cookie-consent` gibi yüzlerce popüler reklam ve takipçi sınıfı/kimliği anında silinir.
* URL adreslerindeki `utm_source`, `utm_medium`, `utm_campaign`, `fbclid`, `gclid` gibi kullanıcıyı profillemeye yarayan takip parametreleri daha istek yapılmadan önce ayıklanır.

---

## 2. Güncel RSS / Atom XML Doğrulama Kalkanı

Geleneksel RSS okuyucularının en sık karşılaşılan yapısal zaafı, sitelerin RSS besleme URL'lerini değiştirmesi veya besleme adreslerinin bozulup geriye düz HTML hata sayfaları (404, Cloudflare engeli, JavaScript meydan okuması vb.) döndürmesidir. Eski nesil okuyucular bu HTML yanıtlarını ayrıştırmaya çalışarak ya kilitlenir ya da kullanıcıya anlamsız kod yığınları gösterir.

QuickNews, bu sorunu önlemek için çekirdek düzeyinde **XML Doğrulama Kalkanı (XML Technology Guard)** mekanizması barındırır:

```
[ Aday URL / Besleme İsteği ]
              │
              ▼
[ HTTP Yanıt Başlığı Denetimi ]
   ├── Content-Type: application/rss+xml, application/atom+xml, text/xml?
   └── Başarısız ise: Gövde İncelemesine Geç
              │
              ▼
[ 8 KiB Başlangıç Gövde İncelemesi ]
   ├── <rss, <feed veya <channel XML kök etiketleri mevcut mu?
   └── HTML, DOCTYPE veya Cloudflare sayfası tespit edilirse: REDDET
              │
              ▼
[ Geçerli XML ] ──► Akış Kabul Edilir ve Kaydedilir
[ Geçersiz / Bozuk ] ──► Güvenle Yoksayılır / Kullanıcıya Bildirilir
```

Bu kalkan sayesinde QuickNews; yalnızca gerçek, canlı ve standartlara uygun RSS 2.0 veya Atom XML beslemelerini kabul eder. Bozuk kaynakların veya JavaScript ile korunan sahte endpoint'lerin arayüzü kirletmesi imkansız hale getirilmiştir.

Sistem; ulusal haberlerden (NTV, Diken, T24), yerel şehir basınından (Haberler Yerel, Yeni Asır, Bursa Hakimiyet), teknoloji yayınlarından (The Verge, Ars Technica, Phoronix, Webtekno, Donanım Arşivi, BTK News) siber güvenlik bültenlerine (Bleeping Computer, The Hacker News) kadar geniş bir doğrulanmış kaynak havuzunu kutudan çıktığı anda destekler.

---

## 3. Doğal Dille Akıllı Kaynak Keşfi

Kullanıcıların tek tek web sitelerinin kaynak kodlarında RSS bağlantıları araması zahmetli bir süreçtir. QuickNews, dahili **Doğal Dil Kaynak Keşif Motoru** sayesinde bu süreci otomatikleştirir.

![QuickNews Kaynak Ekleme Modalı](/images/quickshell/quicknews-modal.png)

Arama çubuğuna *"Turkiye yerel sehir haberlerini ekle"*, *"Top Linux news and kernel blogs"* veya *"Cybersecurity feeds"* gibi doğal dilde bir ifade yazdığınızda:

1. Motor, dahili bilgi tabanındaki güvenilir alan adı dizinini sorgular.
2. Aday sitelerin güncel RSS/Atom adreslerini yoklar.
3. XML Doğrulama Kalkanı ile her bir adresi anlık olarak test eder.
4. Yalnızca testi başarıyla geçen ve çalışan XML akışlarını sisteminize otomatik olarak kaydeder.

---

## 4. Yerel Yapay Zeka ile Nötr Başlık ve 3 Maddelik Özet

Günün yoğun temposunda yüzlerce haber metnini baştan sona okumak çoğu zaman mümkün değildir. QuickNews, makale detay görünümünde yerel yapay zeka çıkarım motorunu devreye sokar:

* **De-Clickbait (Sakinleştirilmiş Nötr Başlık):** Tıklama tuzağı kurmak amacıyla abartılmış başlıkları analiz eder ve sansasyondan uzak, yalın ve olgusal bir Türkçe başlık üretir.
* **3 Maddelik Öz:** Makalenin temel argümanlarını ve somut verilerini 3 kısa madde halinde özetler. Kullanıcı, tüm haberi okumadan saniyeler içinde gelişmenin özünü kavrayabilir.
* **Gizlilik Odaklı İşleyiş:** Özetleme işlemi tamamen yerel makinede koşan modeller veya kullanıcının tanımladığı güvenli yerel çıkarım sunucuları üzerinden gerçekleştirilebilir.

![QuickNews Okuma Görünümü](/images/quickshell/quicknews-reader.png)

---

## 5. İki Katmanlı Hibrit Mimari: Rust ve Quickshell

QuickNews, Omarchy Linux'un diğer yerel araçlarında (OmaStudio, NetRadar, OmaNotes) olduğu gibi ayrık iki katmanlı bir mimari üzerinde yükselir:

### A. Çekirdek Motor (`quicknews-engine` - Rust)
* **Yüksek Başarımlı Eşzamanlılık:** `tokio` asenkron çalışma zamanı ile onlarca haber akışı saniyeler içinde paralel olarak indirilir ve ayrıştırılır.
* **Hızlı XML ve HTML İşleme:** `quick-xml` ve `scraper` kütüphaneleriyle sıfır bellek sızıntılı, doğrudan bayt akışı üzerinden çalışan ayrıştırma.
* **CLI Bağımsızlığı:** Motor yalnızca grafik arayüze hizmet etmekle kalmaz; terminal üzerinden `--fetch`, `--summary`, `--sources`, `--discover` argümanlarıyla bağımsız bir komut satırı aracı olarak da kullanılabilir.

### B. Grafik Kullanıcı Arayüzü (Quickshell / Qt 6 QML)
* **GPU İvmeli Wayland Arayüzü:** Akıcı 60+ FPS kaydırma, minimalist pencere düzeni ve klavye kısayolları.
* **Canlı Sistem Teması:** Omarchy'nin `colors.toml` yapılandırmasını gerçek zamanlı izler; masaüstü renk paleti değiştiğinde haber okuyucunun renkleri anında güncellenir.
* **Ergonomik Tipografi:** `JetBrainsMono Nerd Font` ile tek tip ve okunaklı karakter dizilimi.

---

## 6. HANCORE Linux Güvenlik Standartları

QuickNews, sistem güvenliğini en üst düzeyde tutmak adına katı HANCORE yönergelerine tam uyumla geliştirilmiştir:

1. **SSRF Savunması (Server-Side Request Forgery Koruması):** İstemci, bir haber kaynağına bağlanmadan önce hedef IP adresini doğrular. Özel ağ (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), yerel bağlantı (RFC 3927: `169.254.0.0/16`) ve geri döngü (`127.0.0.0/8`) bloklarına yönlendirilen istekler soket seviyesinde reddedilir.
2. **Bellek ve Yanıt Tavan Sınırları:** Ağ üzerinden çekilen XML veya HTML verileri için 8 MiB tavan sınır uygulanır (`take(MAX_BYTES)`). Devasa boyutlu yanıtlarla belleği tüketmeye yönelik hizmet engelleme (DoS) girişimleri bertaraf edilir.
3. **Atomik ve İzin Korumalı Depolama:** Yapılandırma ve haber önbellek dosyaları doğrudan dosya üzerine yazılmaz; önce `.tmp_*` geçici dosyasına yazılıp atomik olarak taşınır (`fs::rename`). Dosya izinleri katı bir şekilde `0600` (yalnızca sahip okur/yazar), dizin izinleri ise `0700` olarak atanır. Sembolik bağlar (symlink) kesinlikle kabul edilmez.
4. **Harici Süreç İzolasyonu:** CLI çağrıları ve alt süreçler bağımsız süreç gruplarında (`process_group(0)`) çalıştırılarak sistem kararlılığı güvence altına alınır.

---

## 7. Derleme ve Kullanım

QuickNews, Rust derleyicisi ve Cargo paket yöneticisinin bulunduğu herhangi bir modern Linux sisteminde kolaylıkla derlenebilir.

### Depoyu Klonlama ve Derleme
```bash
git clone https://github.com/ozdil/quicknews.git
cd quicknews

# Rust motorunu optimize olarak derleyin
cargo build --release

# Çalıştırılabilir dosyayı kullanıcı yoluna kurun
install -m 755 target/release/quicknews-engine ~/.local/bin/
```

### Komut Satırı Kullanımı
```bash
# Tüm kaynaklardan güncel haberleri çekin
quicknews-engine --fetch

# Belirli bir haberin 3 maddelik nötr özetini çıkarın
quicknews-engine --summary "https://haber-sitesi.com/ornek-haber"

# Doğal dille yeni kaynaklar keşfedip ekleyin
quicknews-engine --discover "Linux kernel and open source news"
```

### Grafik Arayüzü Başlatma
```bash
# Quickshell Wayland arayüzü ile başlatın
quickshell -p /path/to/quicknews/ui/shell.qml
```

---

## Sonuç

QuickNews; modern internetin dikkat dağıtıcı reklam, takip ve görsel gürültü duvarını aşarak haberi en saf, en dürüst ve en hızlı haliyle kullanıcıya ulaştırma çabasıdır. Bilgiyi tüketirken kontrolü yeniden kullanıcıya veren bu açık kaynak yaklaşım, Omarchy Linux'un sade, güvenli ve bağımsız masaüstü vizyonunun önemli bir parçasıdır.

Projeyi incelemek, katkı sağlamak veya kendi iş akışınıza dahil etmek için GitHub depomuzu ziyaret edebilirsiniz:

* **GitHub Deposu:** [github.com/ozdil/quicknews](https://github.com/ozdil/quicknews)
