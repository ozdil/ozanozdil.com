---
title: "Dijital Direniş Serisi - Bölüm 2: Big Tech Kuşatması - Veri Sömürgeciliği ve Algoritmik Panoptikon"
description: "'Eğer bir hizmet için ücret ödemiyorsanız, ürün sizsiniz. Ancak Big Tech söz konusu olduğunda durum daha vahimdir: Siz artık ürün değil, hammadde haline geti..."
pubDate: "2026-04-22T11:07:00.005+03:00"
updatedDate: "2026-04-22T11:12:49.546+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/04/dijital-direnis-serisi-2-bolum-big-tech.html"
---

"Eğer bir hizmet için ücret ödemiyorsanız, ürün sizsiniz. Ancak Big Tech söz konusu olduğunda durum daha vahimdir: Siz artık ürün değil, hammadde haline getirilmiş bir veri kaynağısınız."

## Giriş: Silikon Vadisi’nin Yeni Feodalizmi

Modern ekonomi, "verinin yeni petrol olduğu" tezi üzerinden yükseliyor. Ancak petrolün aksine veri, tükendikçe biten bir kaynak değil; işlendikçe bireyin iradesini zayıflatan bir manipülasyon aracıdır. Google, Meta (Facebook), Apple, Microsoft ve Amazon'dan oluşan bu "Beşli Yapı", dijital dünyada mülkiyeti ortadan kaldırarak bizi birer "veri serfine" dönüştürmüştür. Bu bölümde, bu devlerin kapalı kapılar ardında yürüttüğü telemetri operasyonlarını ve algoritmik panoptikonu teknik detaylarıyla deşifre ediyoruz.

## 1. Google: Dünyanın En Büyük Telemetri İstasyonu

Google, sadece bir arama motoru değil; dünyanın en geniş kapsamlı gözetim ağıdır. Google'ın iş modeli, bireyin niyetini (Search), konumunu (Maps), sosyal çevresini (Gmail) ve ilgi alanlarını (YouTube) tek bir **Google ID** altında birleştirmek üzerine kuruludur.

### 1.1. Android ve Gizli Veri Akışı: Douglas Schmidt Deneyi

Vanderbilt Üniversitesi'nden Profesör Douglas Schmidt'in 2018 yılında yaptığı çığır açan araştırma, Android ekosisteminin karanlık yüzünü ortaya koymuştur. Araştırmaya göre, bir Android telefon "boşta" dururken dahi saatte ortalama 40 kez Google sunucularına veri paketi gönderir. Bu paketler sadece koordinat içermez;

- **BSSID Tarama:** Cihazınız, etrafınızdaki tüm Wi-Fi ağlarının benzersiz kimliklerini (BSSID) Google'a iletir. Bu sayede GPS kapalı olsa bile Google, hangi apartmanın hangi dairesinde olduğunuzu santimetrik hassasiyetle bilir.

- **Sensor Fusion:** İvmeölçer, barometre ve jiroskop verileri birleştirilerek merdiven çıkıp çıkmadığınız, araç içinde mi yoksa yaya mı olduğunuz analiz edilir.

### 1.2. Google My Activity ve "Kalıcı Hafıza"

Kullanıcılar "Geçmişi Sil" butonuna bastığında, veri sadece kullanıcının ekranından kalkar. Google’ın **BigTable** veritabanlarında bu veriler, anonimleştirilmiş etiketler altında reklam algoritmalarını eğitmek için sonsuza dek kalır. Bu, dijital dünyada "unutulma hakkının" teknik olarak imkansızlaştırılmasıdır.

## 2. Meta ve Gölge Profiller (Shadow Profiling)

Meta'nın (Facebook, Instagram, WhatsApp) gözetim stratejisi, platformun sınırlarını çoktan aşmıştır. Facebook hesabınızın olmaması, Meta'nın sizin hakkınızda bir dosyası olmadığı anlamına gelmez.

### 2.1. Facebook Pixel ve SDK Kuşatması

İnternet sitelerinin %70'inden fazlasında "Facebook Pixel" adı verilen görünmez takip kodları bulunur. Bir sağlık sitesinde semptomlarınızı arattığınızda veya bir e-ticaret sitesinde sepete ürün eklediğinizde, bu bilgi anında Meta sunucularına **"Event Data"**olarak akar. Eğer hesabınız yoksa, IP adresiniz ve tarayıcı parmak iziniz üzerinden sizin için bir**"Gölge Profil"** oluşturulur. Bu profil, ileride bir hesap açtığınızda veya arkadaşlarınızın rehber verileri üzerinden kimliğiniz netleştiğinde asıl kimliğinizle birleştirilir.

### 2.2. WhatsApp ve Meta-Veri (Metadata) Analizi

WhatsApp "uçtan uca şifreli" (E2EE) olduğunu iddia etse de, mesajın içeriği dışındaki her şey (metadata) Meta için açıktır. Kiminle, ne kadar süre, hangi sıklıkta ve hangi lokasyonda konuştuğunuz bilgisi; içeriğe ihtiyaç duymadan sizin sosyal grafiğinizi ve yakınlık derecelerinizi çıkarmak için yeterlidir. *"Metadata, mesajın kendisinden daha dürüsttür."*

## 3. Apple: Mahremiyet Bir Pazarlama Aracı mı?

Apple, kendisini rakiplerinden "Privacy" (Mahremiyet) sloganıyla ayırsa da, teknik analizler durumun bir "kapalı kutu" stratejisi olduğunu göstermektedir.

### 3.1. IAD ve Kendi Gözetim Ağı

Apple, üçüncü taraf reklamcıların veri toplamasını kısıtlayarak (ATT - App Tracking Transparency) mahremiyet puanı toplarken, kendi ekosistemi içinde (App Store, Apple Music, News) kullanıcı verilerini toplamaya devam eder. Bu durum, mahremiyeti korumaktan ziyade, **"veriyi tekelleştirmek"** olarak yorumlanmaktadır.

### 3.2. iCloud ve "Escrow Key" Sorunsalı

Apple, iCloud yedeklemelerindeki "uçtan uca şifreleme" (Advanced Data Protection) özelliğini varsayılan olarak kapalı tutar. Bu kapalıyken, yedeklerinizin anahtarı Apple'ın sunucularında (escrow) saklanır. Bu da devlet taleplerinde veya bir sızıntıda tüm iMessage geçmişinizin, fotoğraflarınızın ve notlarınızın üçüncü tarafların eline geçebileceği anlamına gelir.

## 4. Microsoft: İşletim Sistemi Olarak Telemetri İstasyonu

Windows 10 ve 11 ile birlikte kişisel bilgisayarımız, bir çalışma aracından ziyade bir veri terminaline dönüşmüştür.

### 4.1. Keylogging ve Diagnostic Data

Windows kurulumunda "kişiselleştirilmiş deneyim" adı altında kabul edilen şartlar, Microsoft'un klavye vuruş ritminizden (ink and typing) açtığınız dosya isimlerine kadar devasa bir **Telemetri** verisi toplamasını sağlar. Bu veriler *"Connected User Experiences and Telemetry"* servisi üzerinden sürekli olarak Redmond sunucularına akar.

### 4.2. Advertising ID (Reklam Kimliği)

Her Windows kullanıcısına atanan benzersiz Reklam Kimliği, masaüstü kullanım alışkanlıklarınızı web üzerindeki kimliğinizle birleştirir. İşletim sisteminin kendisi bir reklam izleyicisine dönüştüğünde, "çevrimdışı" mahremiyet kavramı tamamen yok olur.

## 5. Algoritmik Panoptikon ve Davranışsal Mühendislik

Big Tech'in topladığı bu veriler, **Yapay Zeka**(AI) modelleri tarafından işlenerek bireysel psikolojinin en zayıf noktalarını tespit eder. Bu sürece**"Psychographic Profiling"** denir.

- **Dopamin Döngüleri:** Sosyal medya algoritmaları, dikkatinizi platformda tutmak için dopamin salgısını tetikleyen "Infinite Scroll" (Sonsuz Kaydırma) ve değişken ödül sistemlerini kullanır.

- **Echo Chambers (Yankı Odaları):** Algoritmalar, sadece duymak istediğiniz fikirleri önünüze getirerek toplumsal kutuplaşmayı derinleştirir ve sizi manipülasyona açık hale getirir.

## Sonuç: Dijital Esaretten Fiziksel Özgürlüğe

Büyük Teknoloji şirketleri, hayatımızı kolaylaştırma vaadiyle mahremiyetimizi sessizce müsadere etmiştir. Bu kuşatma sadece bir yazılım meselesi değil, bir mülkiyet ve egemenlik meselesidir. Verimizi başkasının bulutuna teslim ettiğimiz sürece, dijital dünyada hür bir birey olmamız imkansızdır.

**Serinin 3. Bölümünde:** Bu kuşatmayı fiziksel olarak nasıl kıracağımızı, *"Kendi Veri Kaleni İnşa Etmek: Homelab ve Donanım Güvenliği"* başlığı altında, Intel i5-14500 mimarisi üzerinden inceleyeceğiz.

#### 2. Bölüm Teknik Terimler Sözlüğü:

- **Metadata:** Veri hakkında veri (Kim, ne zaman, nerede).

- **BSSID:** Kablosuz erişim noktasının benzersiz MAC adresi.

- **Telemetri:** Sistemin performans ve kullanım verilerinin uzaktan izlenmesi.

- **E2EE:** Uçtan uca şifreleme.

- **SDK:** Yazılım geliştirme kiti (İçinde genellikle takip kodları barındırır).

- **Shadow Profile:** Hesabı olmayan kişiler için oluşturulan gizli veri dosyası.

- **ATT:** Apple'ın Uygulama Takibi Şeffaflığı protokolü.

- **Sensor Fusion:**Birden fazla sensör verisinin tek bir anlamlı sonuç için birleştirilmesi.**Kaynakça:**

- Schmidt, D. C. (2018). Google Data Collection: A Detailed Analysis.

- Zuboff, S. (2019). The Age of Surveillance Capitalism.

- Leith, D. J. (2021). Mobile Handset Privacy: Measuring The Data iOS and Android Send to Apple and Google.

- Christl, W. (2017). Corporate Surveillance in Everyday Life.
