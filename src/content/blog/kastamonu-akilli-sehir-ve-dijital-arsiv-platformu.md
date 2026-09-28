---
title: "Kastamonu Akıllı Şehir ve Dijital Kurum Arşivi: Askeri Düzey Güvenlik (DEFCON-1) ve Modern Kamu Mimarisi"
description: "NATO, DoD ve NIST standartlarıyla donatılmış, sıfır-güven (zero-trust) mimarisi üzerine inşa edilen Kastamonu Belediyesi Dijital Kurum Arşivi ve Akıllı Şehir Açık Veri Platformu'nun teknik anatomisi."
pubDate: 2026-09-28
heroImage: "/images/archive_military.png"
tags: ["siber-guvenlik", "kamu-mimarisi", "akilli-sehir", "kriptografi", "linux", "zero-trust", "kastamonu"]
---

Kamu kurumlarının veri yönetimi ve güvenliği, geleneksel yöntemlerle sürdürülemeyecek kadar kritik bir aşamaya gelmiştir. Sadece Kastamonu özelinde değil, küresel çapta yerel yönetimler her gün yeni siber saldırıların, fidye yazılımlarının (ransomware) ve yetki istismarlarının hedefi olmaktadır. Geleneksel güvenlik duvarları ve basit şifrelemeler artık bu organize tehditlere karşı yeterli değildir.

Bu motivasyonla yola çıkarak, T.C. Kastamonu Belediyesi Bilgi İşlem Müdürlüğü için yalnızca bugünün değil, önümüzdeki on yılların tehdit senaryolarına da (kuantum bilgisayarlar dahil) direnecek, **NATO ve DoD (ABD Savunma Bakanlığı) Askeri Siber Savunma (DEFCON-1)** standartlarında yepyeni bir "Dijital Kurum Arşivi ve Akıllı Şehir" platformunu sıfırdan mimarlandırdım ve geliştirdim.

Açık kaynaklı olarak Github üzerinden erişilebilen bu platform, bir belediye altyapısından ziyade bir savunma sanayi kalesini andırmaktadır. Peki bunu neden yaptık ve bu sistem neleri barındırıyor?

## Neden Askeri Düzey Bir Mimari?

Yerel yönetimlerin arşivleri; imar planlarından vatandaşın şahsi KVKK verilerine, ihale evraklarından tarihi encümen kararlarına kadar bir şehrin **kurumsal hafızasını** ve **mahremiyetini** barındırır. Bu hafızanın manipüle edilmesi, silinmesi veya şifrelenip fidye istenmesi, şehrin operasyonel olarak felç olması anlamına gelir.

Bunu engellemek için, sistemi sıradan bir web uygulaması olarak değil, **Sıfır Güven (Zero-Trust)** felsefesine sahip kapalı bir zırhlı kutu olarak tasarladım:

1. **İçerideki Tehditlere Karşı "Two-Man Rule" (DoD 5210.42):** 
Nükleer füzelerin fırlatılmasında kullanılan ve tek bir personelin inisiyatifini ortadan kaldıran "İki Kişi Kuralı", bu sistemde kritik evrakların silinmesi veya şifresinin çözülmesi aşamalarına entegre edildi. Maker (İşlemi Yapan) ve Checker (Onaylayan) ayrılığı ile tekil personel hataları veya ihanetleri imkansız hale getirildi.

2. **Kuantum Sonrası Siber Savaşlara Hazırlık (NIST FIPS 204):** 
Şu anki şifreleme algoritmaları kuantum bilgisayarlar geldiğinde saniyeler içinde kırılacak. Kastamonu arşivi, klasik Ed25519 asimetrik imzalarını, **ML-DSA (Crystals-Dilithium) kafes tabanlı entropi** ile hibritleyerek geleceğe dönük kırılmaz bir kriptografik mühürleme yeteneği kazandı.

3. **Bell-LaPadula MLS ve Yukarı Okuma Yasağı (No Read Up):** 
DoD 5200.28-STD standartlarına göre tasarlanan 5 kademeli gizlilik sınıflandırmasıyla, düşük yetkili bir personelin (örneğin "Hizmete Özel" erişimi olan bir memurun), "Çok Gizli" bir evrakı veritabanı seviyesinde dahi görmesi imkansızlaştırıldı.

## Değişmezlik ve Akıllı Şehir Entegrasyonu

Dijital Arşiv, kendi içerisinde **WORM (Write Once Read Many)** kara kutusuna sahiptir. Atılan hiçbir kayıt silinemez, SHA-512 zinciriyle birbirine mühürlenir. Eğer veritabanı dosyasına doğrudan fiziki bir müdahale edilirse, Merkle Tree kök doğrulaması bunu anında tespit eder ve sistemi savunma moduna alır. Ağ izolasyonu gereken durumlarda tüm veriler **NATO STANAG 4774** formatında şifrelenerek Air-Gap (Hava Boşluğu) ihracına olanak tanır.

![Akıllı Şehir Açık Veri Portalı](/images/smart_city.png)

Projenin sadece kapalı devre savunma tarafı yok; aynı zamanda **Port 3001** üzerinden çalışan şeffaf bir Açık Veri Portalı ve Akıllı Şehir katmanı bulunuyor. Bu katmanda:
* Fen İşleri, Su ve Kanalizasyon (KASKİ), Ulaşım gibi saha ekiplerinin anlık kapalı yol, kazı ve arıza verileri GeoJSON formatında tüm vatandaşlara ve geliştiricilere açılıyor.
* Tahminsel Yapay Zeka, geçmiş verileri analiz ederek hangi mahallede ne tür bir arıza çıkabileceğini hesaplıyor.
* T.C. Cumhurbaşkanlığı Ulusal Akıllı Şehirler Eylem Planı'na ve Avrupa'daki modern kentsel şeffaflık yasalarına tam uyum sağlanıyor.

## Askeri Düzeyde Güvenlik ve Disiplinli Geliştirme Kültürü

Kod tabanının tamamında katı kurallarım devreye girdi:
* **Sıfır Unicode Emoji Politikası:** Hem arka planda hem kullanıcı arayüzünde ciddiyeti zedeleyen tüm emojiler yasaklandı. Uyarılar ve hata mesajları askeri protokol formatında tasarlandı.
* **JetBrainsMono Tipografisi:** Kamu sistemlerinde okunabilirliği ve teknik kesinliği artırmak adına arayüzlerde monospaced bir disiplin kuruldu.
* **Donanım Önerisi:** Kriptografik imzalama esnasında bit-tersinme (bit-flip) hatalarından kaçınmak için ECC (Hata Düzeltme Kodlu) RAM ve minimum 32 çekirdekli AES-NI destekli sunucu mimarileri şart koşuldu.

Bu devasa mimariyi şeffaflık ilkesi gereği tüm kodlarıyla birlikte Kastamonu Belediyesi Github organizasyonunda açık kaynak olarak yayınladım:

[Kastamonu Belediyesi GitHub Deposu - kastamonu-akilli-sehir-platformu](https://github.com/Kastamonu-Belediye-Baskanligi/kastamonu-akilli-sehir-platformu)

Yerel yönetimlerin, veriyi bir "evrak yığını" olarak değil, şehrin siber egemenliğinin temeli olarak göreceği yepyeni bir çağa giriyoruz. Kastamonu bu adımda artık dijital bir kale konumunda.
