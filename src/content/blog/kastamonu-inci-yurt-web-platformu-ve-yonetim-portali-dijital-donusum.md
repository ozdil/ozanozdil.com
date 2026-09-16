---
title: "Kastamonu İnci Yurt: Bir Öğrenci Rezidansının Modern Web Platformu ve Yönetim Portalı Mimarisi"
description: "20 yıllık köklü bir kurumun dijital dönüşümü: Cloudflare Edge mimarisi, LLM/AI discovery (llms.txt), çok dilli uluslararası öğrenci masası ve operasyonel yönetim portalının perde arkası."
pubDate: 2026-09-15
heroImage: "/images/kastamonuinciyurt-preview.webp"
tags: ["kastamonu", "web-gelistirme", "cloudflare", "typescript", "yonetim-portali", "dijital-donusum", "llms-txt", "edge-computing"]
---

Kastamonu Üniversitesi her yıl Türkiye'nin dört bir yanından ve dünyanın 60'tan fazla ülkesinden binlerce yeni öğrenciyi ağırlıyor. Özellikle üniversiteye yeni adım atan öğrencilerin ve onların ailelerinin en büyük önceliği ise şüphesiz **güvenli, huzurlu, kurumsal ve kampüse yürüme mesafesinde bir konaklama** bulmaktır.

Kastamonu merkezde, Eğitim Fakültesi ve Kuzeykent Merkez Kampüsü'ne sadece **150 metre mesafede** 20 yıldır kesintisiz hizmet veren **Özel İnci Yükseköğrenim Kız Öğrenci Yurdu ve Rezidansı** için baştan sona hayata geçirdiğim yeni nesil web platformu ve kurumsal yönetim portalı projesini; mimari kararları, teknik zorlukları ve sağladığı somut dönüşümü bu yazıda özetliyorum.

---

## Projenin Amacı ve Temel Problemler

Geleneksel yurt web siteleri genellikle iki temel çıkmazla maluldür:
1. **Ziyaretçi Tarafında Güvensizlik & Bilgi Kirliliği:** Statik, yıllar öncesinden kalma fotoğraflar, güncellenmeyen fiyatlar ve muğlak konum bilgileri velilerde güvensizlik yaratır. Şehir dışından gelen bir aile; yurdun kampüse olan gerçek yürüme mesafesini, yemeklerin niteliğini ve odaların güncel durumunu şeffafça görmek ister.
2. **Yönetim Tarafında Operasyonel Yük:** Kayıt dönemlerinde (Ağustos - Ekim) yüzlerce telefon, WhatsApp mesajı, kontenjan takibi ve evrak yönetimi klasik yöntemlerle (defterler veya dağınık Excel tabloları) yürütüldüğünde hata payı katlanır.

Bu projede hedefimiz; yalnızca estetik bir vitrin sitesi kurmak değil, **ziyaretçinin aklındaki tüm soruları saniyeler içinde yanıtlayan, veliye güven veren ve yurt yönetiminin tüm operasyonel iş akışını tek merkezden yöneten modern bir ekosistem** inşa etmekti.

---

## Teknik Mimari ve Altyapı Kararları

### 1. Cloudflare Edge-First Dağıtım & Sıfır Sunucu Maliyeti
Sitenin altyapısını geleneksel cPanel/paylaşımlı sunucular yerine doğrudan **Cloudflare Edge** ağı üzerine kurguladık.
- **Mikro-Saniye TTFB:** Statik sayfalar ve optimize edilmiş varlıklar (WebP/AVIF görseller, sıkıştırılmış CSS/JS) dünya genelinde 300'den fazla Cloudflare veri merkezinden doğrudan ziyaretçiye ulaşıyor.
- **Yüksek Trafik & DDoS Kalkanı:** Kayıt döneminde anlık binlerce ziyaretçi aynı anda sayfaya yüklense dahi ne bant genişliği darboğazı ne de sunucu çökmesi yaşanıyor.
- **SSL ve HTTP/3:** Tüm trafik en güncel güvenlik protokolleri (HSTS, TLS 1.3, QUIC/HTTP/3) üzerinden şifreli iletiliyor.

### 2. Kurumsal Yönetim Portalı (İnci Portal)
Yurt yöneticilerinin ve kayıt görevlilerinin arka planda kullandığı yönetim modülü şu temel yeteneklerle donatıldı:
- **Akıllı Ön Kayıt & Başvuru İşleme:** Web sitesindeki form üzerinden gelen başvurular anlık olarak yönetim paneline düşer; ad-soyad, fakülte, tercih edilen oda tipi (1, 2, 3 veya 4 kişilik) ve özel talepler otomatik sınıflandırılır.
- **Kontenjan ve Oda Matrisi:** 135 yatak kapasiteli rezidansın oda doluluk oranları, boş yataklar ve sözleşme durumları görsel bir kat planı arayüzüyle izlenir.
- **WhatsApp API ve Bildirim Köprüsü:** Başvuru yapan öğrenci ve velilere tek tıkla resmi bilgilendirme, sözleşme evrak listesi ve onay metinleri WhatsApp Business köprüsü üzerinden iletilir.
- **Ödeme ve İskonto Simülatörü:** Peşin ödeme indirimleri (%10), taksitli ödeme planları ve veli bütçesine göre yapılandırılan mali tablolar sistem üzerinden otomatik hesaplanır.

---

## Yapay Zekâ ve LLM Keşif Altyapısı (`llms.txt` ve Schema.org)

Modern web artık yalnızca insanların gözleriyle gezdiği bir mecra değil; yapay zekâ asistanlarının (Perplexity, ChatGPT Search, Claude, Google Gemini) kullanıcı adına bilgi derlediği bir dönüşüm sürecinde.

Bu doğrultuda, Kastamonu İnci Yurt platformuna bölgedeki tüm konaklama işletmelerine öncülük edecek bir **LLM Context & Discovery altyapısı** entegre ettik:
- **`/llms.txt` ve `/llms-full.txt`:** Yurdun 20 yıllık kurumsal geçmişi, Gençlik ve Spor Bakanlığı ruhsatı, fakültelere olan metre metre yürüme mesafeleri, oda özellikleri ve dahil olan tüm hizmetler yapılandırılmış Markdown formatında yapay zekâ motorlarına açıldı.
- **`/.well-known/api-catalog` & Schema.org:** Arama motoru robotları ve açık web ajanları için `LocalBusiness`, `Hostel`, `AggregateRating` (Google 4.6 puan, 231+ onaylı değerlendirme) verileri eksiksiz JSON-LD formatında sunuldu.

Bu optimizasyon sayesinde, bir veli yapay zekâya *"Kastamonu Eğitim Fakültesi'ne en yakın, güvenli ve yemekli kız yurdu hangisi?"* diye sorduğunda, model hiçbir hayal ürününe sapmadan doğrudan doğruya **Özel İnci Kız Öğrenci Yurdu**'nun güncel verilerini referans gösteriyor.

---

## Kullanıcı Deneyimini Zenginleştiren Özel Modüller

1. **Ev vs. Yurt Tasarruf Analiz Hesaplayıcısı:**
   Kastamonu'da kiralık ev tutmak ile yurt konaklaması arasındaki gizli maliyetleri (kira, doğalgaz/ısınma, elektrik, su, internet, sabah kahvaltısı, akşam yemeği, kampüs dolmuş ücreti, depozito ve eşya masrafları) karşılaştıran interaktif bir hesaplama tablosu hazırladık. Aileler, yurtta kaldıklarında yıllık ne kadar tasarruf ettiklerini somut rakamlarla görebiliyor.

2. **Uluslararası Öğrenci Masası (Çok Dilli Entegrasyon):**
   Kastamonu Üniversitesi'nde okuyan yabancı uyruklu öğrenciler için ikamet izni, Göç İdaresi randevu süreçleri ve çok dilli iletişim kılavuzları hazırlandı.

3. **Kastamonu Şehir ve Gastronomi Rehberi:**
   İlk kez şehre gelecek aileler için Kastamonu Kalesi, Saat Kulesi, Şeyh Şaban-ı Veli Külliyesi, Horma Kanyonu ve yerel gastronomi (Kuyu Kebabı, Pastırma, Çekme Helva) duraklarını içeren samimi bir gezi rotası entegre edildi.

---

## Sonuçlar ve Katkılar

- **Sıfır Çağrı Karmaşası:** Kayıt döneminde rutin soruların (%80'i) web sayfası, sıkça sorulan sorular alanı ve interaktif modüller üzerinden yanıtlanmasıyla telefon trafiğinde ciddi bir optimizasyon sağlandı.
- **Hızlı Dönüşüm:** Şeffaf oda fotoğrafları, 150m yürüyüş avantajının net vurgulanması ve tek tıkla WhatsApp erişimi sayesinde ön kayıt dönüşüm oranları kayda değer ölçüde yükseldi.
- **Kastamonu'nun Dijital Yüzü:** Kastamonu öğrenci konaklama sektöründe modern web teknolojilerini ve yapay zekâ okuryazarlığını en üst düzeyde uygulayan referans bir proje ortaya çıktı.

Projeyi canlı olarak incelemek için:
**[kastamonuinciyurt.com](https://www.kastamonuinciyurt.com)**
