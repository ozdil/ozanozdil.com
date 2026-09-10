---
title: "Omarchy Linux İçin OmaSend: AirDrop Benzeri P2P Dosya Köprüsü ve Resmi Android Uygulaması Yayında"
description: "Linux masaüstü ile Android arasında sıfır bulut bağımlılığıyla yerel ağda ışık hızında dosya transferi, çift yönlü Wayland pano köprüsü ve Google Play kapalı test süreci."
pubDate: 2026-09-10
heroImage: "/images/quickshell/omasend-banner.png"
tags: ["omarchy", "omasend", "android", "p2p", "airdrop", "quickshell", "rust", "kotlin", "jetpack-compose", "açık-kaynak"]
---

Apple ekosisteminin kullanıcıları kendi bahçesinde tutan en güçlü halkalarından biri şüphesiz **AirDrop**'tur. Bir Mac ile iPhone arasında dosya aktarmak veya panodaki bir metni kopyalayıp diğer cihazda yapıştırmak o kadar zahmetsizdir ki, pek çok kullanıcı sırf bu akıcılığı kaybetmemek adına tescilli platformlara bağlı kalır.

Açık kaynak dünyasında ise Linux ile Android arasında dosya paylaşmak çoğu zaman can sıkıcı bir süreçtir: Ya dosyayı bir bulut depolama servisine yükleyip karşı cihazdan indirmek zorunda kalırız (ki bu gizliliği zedeler ve internet kotasını tüketir), ya kablo ararız ya da eski ve hantal Bluetooth protokolleriyle boğuşuruz.

Bu eksikliği kökünden çözmek amacıyla geliştirdiğimiz **OmaSend**, Omarchy Linux masaüstü ekosistemi için tasarlanmış bağımsız bir yerel eşler arası (P2P) dosya ve pano aktarım köprüsüdür. Üstelik projenin en büyük müjdesi: **OmaSend for Android** yerel mobil uygulamamız, Google Play Store üzerinde onaylanarak resmi kapalı test (Closed Beta) aşamasında yayına girdi!

---

## ⚡ Temel Mimari: Sıfır Bulut, Tam Gizlilik ve Saf Yerel Hız

OmaSend, Apple AirDrop ve LocalSend mantığında çalışır; ancak Omarchy'nin güvenlik mimarisi ve minimalist masaüstü felsefesiyle birleşir.

1. **Sıfır Bulut Bağımlılığı (Zero-Cloud):** Dosyalarınız ve pano verileriniz asla üçüncü taraf şirketlerin sunucularına veya uzaktaki veri merkezlerine gitmez. Tüm iletişim, evinizdeki veya ofisinizdeki yerel Wi-Fi / Ethernet ağı üzerinden doğrudan soket bağlantısıyla (`socket-to-socket`) gerçekleşir.
2. **Otomatik Eş Keşfi (Port 53317 UDP):** Cihazları eşleştirmek için IP adresi yazma veya QR kod tarama zorunluluğu yoktur. Ağdaki Omarchy bilgisayarlar ve Android telefonlar, arka planda çalışan hafif UDP sinyalleriyle birbirini saniyeler içinde otomatik olarak bulur.
3. **Maksimum Yerel Hız:** Yerel modem/yönlendiricinizin desteklediği tam bant genişliğinde (Wi-Fi 6/6E ağlarda saniyede yüzlerce megabit hızında) aktarım yapılır. Dosya boyutu veya sıkıştırma sınırı yoktur.

---

## 📱 OmaSend for Android: Modern Jetpack Compose ve Sistem Entegrasyonu

Mobil tarafta WebWrapper veya hantal hibrit çatılar yerine, tamamen modern **Kotlin, Jetpack Compose ve Material 3** ile sıfırdan yerel bir Android uygulaması inşa ettik:

* **Sistem Paylaşım Menüsü (Share Sheet):** Galeriden bir fotoğraf seçtiğinizde, WhatsApp'tan gelen bir belgeyi iletmek istediğinizde veya Dosyalar uygulamasındayken sadece "Paylaş -> OmaSend" diyorsunuz. Ağdaki Omarchy masaüstünüz tek tıkla hedef olarak beliriyor ve dosya ışık hızında bilgisayarınıza akıyor.
* **Canlı Pano (Clipboard) Köprüsü:** Telefondaki bir metni kopyalayıp tek tıkla Linux masaüstünüzün Wayland panosuna gönderebilir veya masaüstünüzdeki bir linki anında telefonunuzun panosuna çekebilirsiniz.
* **Cyber Dark AMOLED Tasarım:** Omarchy'nin ikonik piksel ve karanlık tema estetiğini yansıtan, göz yormayan, batarya dostu arayüz.

---

## 🛡️ Gatekeeper İzni & Siber Güvenlik Standartları (`AGENTS.md`)

OmaSend sadece hızlı değil, aynı zamanda son derece güvenli olacak şekilde katı güvenlik kurallarıyla tasarlandı:

| Güvenlik Katmanı | Gerçekleştirilen Koruma |
| :--- | :--- |
| **Gatekeeper Onayı** | Hiçbir dosya izinsiz veya gizlice diske yazılamaz. Gelen her aktarımda gönderici adı, dosya listesi ve boyutu masaüstü bildiriminde onayınıza sunulur. |
| **İzole Süreçler** | Arka plan motoru (`omasend-engine`) bağımsız süreç gruplarında (`cmd.process_group(0)`) ve kilitlenmeyen I/O ile çalışır. |
| **0600 Güvenli Saklama** | Cihaz anahtarları ve eş listeleri umask'a güvenilmeksizin atomik geçici dosyalar ve `0600` (`-rw-------`) izinleriyle diske mühürlenir. |
| **Düz Metin Arayüz** | Quickshell tarafındaki tüm dinamik metinler `textFormat: Text.PlainText` ile işlenerek HTML/komut enjeksiyonu imkansız hale getirilir. |

---

## 🚀 Google Play Resmi Kapalı Testine Katılın (3 Adım)

OmaSend for Android, Google Play Store'da **Play Protect** güvenlik taramalarından geçmiş ve resmi uygulama imzasıyla doğrulanmış olarak dağıtılmaktadır. 

Google Play kapalı test programına dahil olup uygulamayı telefonunuza hemen kurmak için aşağıdaki 3 adımı takip edebilirsiniz:

1. **Test Topluluğu Grubuna Katılın:**  
   👉 **[OmaSend Testers Google Grubu](https://groups.google.com/g/omasend-testers)** sayfasına gidip telefonunuzda kullandığınız Google hesabınızla *"Gruba katıl"* butonuna tıklayın.
2. **Play Store Test Programını Onaylayın:**  
   👉 **[Google Play Test Kayıt Bağlantısı](https://play.google.com/apps/testing/io.omarchy.omasend)** üzerinden *"Test kullanıcısı ol"* butonuna basın.
3. **Uygulamayı İndirin:**  
   👉 **[OmaSend Google Play İndirme Bağlantısı](https://play.google.com/store/apps/details?id=io.omarchy.omasend)** üzerinden doğrudan Play Store'dan resmi sürümü yükleyin.

> 💡 **İpucu:** Eğer Play Store'da *"Öğe bulunamadı"* uyarısı alırsanız, Google Grubu'na katıldığınız Google hesabıyla telefonunuzdaki Google Play hesabının aynı olduğundan emin olun.

---

## 🌐 Açık Kaynak Depoları

Proje tamamen özgür, bağımsız ve açık kaynak kodludur. Katkı vermek, kaynak kodu incelemek veya yıldızlayarak destek olmak isterseniz:

* 💻 **Omarchy Linux Masaüstü Eklentisi:** [github.com/ozdil/omarchy-omasend](https://github.com/ozdil/omarchy-omasend)
* 📱 **OmaSend Android Mobil Uygulaması:** [github.com/ozdil/omasend-android](https://github.com/ozdil/omasend-android)

Deneyimlerinizi, test geri bildirimlerinizi ve önerilerinizi heyecanla bekliyoruz!
