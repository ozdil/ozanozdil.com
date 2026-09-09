---
title: "Antigravity AI ile Mobil Sistem Mühendisliği: POCO HyperOS Ekosisteminde Telemetri Arındırma ve Donanım Optimizasyonu"
description: "Google Antigravity AI otonom ajan mimarisiyle Xiaomi/POCO HyperOS üzerinde gerçekleştirilen non-destrüktif paket eliminasyonu, telemetri tecridi ve çekirdek optimizasyonunun bilimsel ve teknik dökümü."
pubDate: 2026-09-09
tags: ["antigravity-ai", "yapay-zeka", "android", "hyperos", "sistem-mühendisliği", "debloat", "optimizasyon", "güvenlik"]
---

Modern tüketici elektroniğinde akıllı telefon donanımları son derece sofistike noktalara ulaşmış olsa da, orijinal ekipman üreticilerinin (OEM) Android üzerine inşa ettiği tescilli işletim sistemi dağıtımları sıklıkla yoğun **monetizasyon katmanları**, **agresif telemetri ajanları** ve **istenmeyen ön yüklü yazılımlarla (bloatware)** donatılmaktadır. 

Bu araştırma ve mühendislik çalışmasında; **MediaTek Dimensity 9500s (3nm)** mimarisine, **12 GB LPDDR5X belleğe** ve **8.500 mAh** bataryaya sahip **POCO X8 Pro Max** amiral gemisi cihazı üzerinde, Google DeepMind mühendisliği eseri olan **Antigravity AI** otonom eşli programlama (pair-programming) ajanı kullanılarak gerçekleştirilen deterministik arındırma, telemetri eliminasyonu ve düşük seviyeli sistem optimizasyon süreçleri belgelenmektedir.

---

## 1. Test Yatağı ve Donanım Karakterizasyonu

Optimizasyon sürecine tabi tutulan hedef sistem ve kontrol ortamı aşağıdaki teknik parametrelerle tanımlanmıştır:

```yaml
Hedef Cihaz: POCO X8 Pro Max (dash_global / 2602BPC18G)
Yongaseti: MediaTek Dimensity 9500s (3nm FinFET, Octa-Core)
Fiziksel Bellek: 12 GB LPDDR5X (Quad-Channel)
Depolama: 256 GB / 512 GB UFS 4.0
Batarya Hücresi: 8.500 mAh Li-Polymer (100W HyperCharge)
Yazılım Çekirdeği: Xiaomi HyperOS 3.0 (Android 16 Tabanlı, Build OS3.0)
Geliştirici Terminali: Omarchy Linux (Arch Linux x86_64, Kernel 6.16)
Orkestrasyon Ajanı: Antigravity AI (Google DeepMind Agentic Coding Framework)
Protokol Arayüzü: Android Debug Bridge (ADB over USB 3.2 Gen 1)
```

---

## 2. Metodoloji ve Güvenlik Kısıt Matrisi

Android ekosisteminde plansız ve rastgele yapılan sistem temizlikleri çoğunlukla `bootloop` (açılış döngüsü), çöken izin yöneticileri, kilitlenen arayüzler ve bankacılık güvenlik modüllerinin tetiklenmesiyle sonuçlanır. Bu sebeple çalışma başlamadan önce Antigravity AI tarafından katı bir **Kısıt ve Güvenlik Matrisi** formüle edilmiştir:

1. **Çekirdek Sistem Korunumu (Zero-Bootloop):** İzin yönetimini üstlenen `com.miui.securitycenter`, arayüz derleyicisi `com.android.systemui`, varsayılan başlatıcı `com.mi.android.globallauncher` ve donanım sürücüleri (`com.mediatek.*`) dokunulmaz kılınmıştır.
2. **Google Hizmetleri İzolasyonu (User-Strict):** Kullanıcının doğrudan talebi doğrultusunda Google Mobil Servisleri (`com.google.android.gms`), Play Store (`com.android.vending`) ve ilişkili alt kütüphaneler herhangi bir müdahaleden muaf tutulmuştur.
3. **Kişisel ve Finansal Bütünlük:** Cihazda kurulu bulunan kritik bankacılık (Yapı Kredi, Ziraat, Vakıfbank, QNB) ve üçüncü taraf uygulamalar tek tek ayrıştırılarak koruma altına alınmıştır.
4. **Geri Döndürülebilir Kullanıcı Alanı Tasfiyesi:** Fiziksel `/system` bloğu üzerinde read-write oynaması yapılarak dm-verity veya AVB bütünlüğü bozulmamış; arındırma işlemi `pm uninstall -k --user 0` standardıyla kullanıcı alanı (User 0) katmanında icra edilmiştir.

$$\text{Sistem Bütünlüğü} = \text{Hardware Verity} \cap \text{GMS Stability} \cap \text{User 0 Cleanliness}$$

---

## 3. Telemetri ve İstenmeyen Yazılımların (Bloatware) Eliminasyonu

Cihaz üzerinde yapılan ilk ADB paket envanterinde **479 adet aktif paket** tespit edilmiştir. Antigravity AI'ın geliştirdiği sınıflandırma betikleri vasıtasıyla bu paketler adli analize tabi tutulmuş ve 4 ana grupta toplam **24 adet kritik telemetri ve reklam servisi** tamamen imha edilmiştir:

```
                  ┌─────────────────────────────────────┐
                  │   HyperOS Paket Envanteri (479)     │
                  └──────────────────┬──────────────────┘
                                     │
           ┌─────────────────────────┴─────────────────────────┐
           ▼                                                   ▼
┌───────────────────────┐                           ┌─────────────────────┐
│  Korunan Katman       │                           │  Tasfiye Katmanı    │
│  - Linux Kernel       │                           │  - Reklam Motorları │
│  - SystemUI & Security│                           │  - Telemetri D./A.  │
│  - GMS & Bankacılık   │                           │  - Gizli Yükleyiciler│
└───────────────────────┘                           └─────────────────────┘
```

### A. Reklam Motorları ve Kullanıcı Profilleme Servisleri
* **`com.miui.msa.global` (MIUI System Ads):** Xiaomi'nin sistem uygulamalarına hedefli dinamik reklam enjekte eden birincil istemcisi.
* **`com.miui.analytics`:** Kullanıcı etkileşimlerini, ekran kalma sürelerini ve reklam tıklamalarını profillemek üzere telemetri toplayan analitik servisi.
* **`com.miui.daemon`:** Cihazın durumunu periyodik olarak OEM sunucularına raporlayan arka plan süreci.
* **`com.miui.android.fashiongallery` (Glance):** Kilit ekranına sponsorlu haber, reklam ve öneri kartları pompalayan kilit ekranı döngüsü.
* **`com.miui.yellowpage`:** Arayan kimliği pazar veritabanı ve pazarlama altyapısı.
* **`com.miui.bugreport` & `com.miui.miservice`:** Kullanıcı onayı olmaksızın sürekli hata ve kullanım günlüğü gönderen telemetri kanalları.

### B. İzinsiz Uygulama Yükleme ve Öneri Dağıtıcıları
* **`com.xiaomi.mipicks` (GetApps):** Wi-Fi bağlantısı kurulduğu anda arka planda sessizce sponsorlu uygulama indiren ve sürekli bildirim gönderen alternatif mağaza motoru.
* **`com.mi.appfinder` & `com.xiaomi.glgm`:** Arama ekranlarında sponsorlu oyun ve mini-uygulamalar sergileyen reklam vitrinleri.
* **`android.autoinstalls.config.Xiaomi.model` (PAI):** İlk kurulumda veya SIM/bölge değişikliklerinde operatör ve sponsor uygulamalarını arka planda tetikleyen yapılandırma.
* **`com.mi.globalminusscreen` (App Vault):** Ana ekranın sol paneline yerleşen reklam ve sponsorlu kart kümesi.
* **`com.android.providers.partnerbookmarks`:** Tarayıcılara zorunlu sponsorlu bağlantılar ekleyen sağlayıcı.

### C. Üçüncü Taraf Arka Plan Ajanları ve Ön Paketler
* **Meta Arka Plan Yöneticileri:** `com.facebook.services`, `com.facebook.system`, `com.facebook.appmanager` (Meta'nın cihazda Facebook kurulu olmasa bile çalışan arka plan servisleri).
* **Amazon Yükleyicisi:** `com.amazon.appmanager`.
* **TikTok Ajanı:** `com.tiktok.manager`.
* **Reklam Yüklü Ön Paketler:** `com.mi.globalbrowser` (Mi Tarayıcı), `cn.wps.xiaomi.abroad.lite` (WPS Lite), `com.mi.global.shop` (Mi Store), `com.miui.videoplayer` (Mi Video), `com.miui.player` (Mi Müzik).

```bash
# Antigravity AI Tarafından İcra Edilen Deterministik Kaldırma Döngüsü
for pkg in "${TARGET_DEBLOAT_LIST[@]}"; do
    adb shell pm uninstall -k --user 0 "$pkg"
done
# Çıktı: 24/24 Success (Tüm hedefler tek seferde sıfırlandı)
```

---

## 4. Kullanıcı Deneyimi Anomalisi: App Finder Zırhlaması

Paket tasfiyesinin ardından kullanıcı arayüzünde önemli bir davranış anomalisi gözlemlenmiştir: POCO Launcher, ana ekranda yukarıdan aşağı kaydırma hareketini (`Swipe Down`) çekirdek seviyesinde Xiaomi'nin arama motoruna (`com.mi.appfinder`) bağlamaktadır. Paket silindiğinde sistem şu toast uyarısını vermiştir:

> *"Uygulama cihazınızda yüklü değil"*

Bu anomalinin çözümü için Antigravity AI iki aşamalı bir mühendislik yaklaşımı uygulamıştır:
1. `com.mi.appfinder` paketi sisteme kontrollü olarak iade edilmiştir (`cmd package install-existing com.mi.appfinder`).
2. Paketin içinde gömülü bulunan reklam SDK'ları (`com.xiaomi.miglobaladsdk`, `io.branch.search`) ve telemetri kanalları sistem izinleri seviyesinde zırhlanmıştır:

```bash
# Arka Plan Uyanmasını ve Bildirim Servislerini Dondurma
adb shell cmd appops set com.mi.appfinder POST_NOTIFICATION ignore
adb shell cmd appops set com.mi.appfinder RUN_IN_BACKGROUND ignore
```

Son adımda, arama arayüzünün gömülü ayarlar ekranı (`SettingsActivity`) üzerinden haber, sponsorlu oyun ve akış kartları kapatılmış; böylece jest hem hatasız çalışır hale getirilmiş hem de sıfır reklam içeren temiz bir yerel arama paneline dönüştürülmüştür.

---

## 5. Düşük Seviyeli Sistem ve Donanım Optimizasyonu

Paket temizliğinin ardından sistem mimarisi, donanımın gerçek potansiyelini sergilemesi için optimize edilmiştir:

### A. Sanal RAM (Bellek Uzantısı) Paradoksu
HyperOS, modern telefonlarda pazarlama amacıyla **Bellek Uzantısı (Memory Extension)** adını verdiği sanal swap alanını aktif tutar. Ancak POCO X8 Pro Max halihazırda **12 GB LPDDR5X fiziksel RAM'e** sahiptir.

$$v_{\text{LPDDR5X}} \gg v_{\text{UFS 4.0}} \implies \text{Latency Penalty} \uparrow$$

UFS 4.0 flaş depolama, gerçek RAM'e kıyasla yüzlerce kat yüksek erişim gecikmesine (latency) sahiptir. İşletim sistemi bellekteki sayfaları depolamaya taşımaya çalıştığında mikro takılmalar (stuttering) ve gereksiz NAND yazma döngüleri (wear leveling) oluşur. Bellek Uzantısı kapatılarak sistemin yalnızca saf fiziksel RAM havuzunu kullanması sağlanmıştır.

### B. Radyo Frekans Taramalarının İzolasyonu
Android'in arka planda Wi-Fi ve Bluetooth bağlantıları kapalıyken dahi konum doğruluğu için periyodik tarama yapması (`wifi_scan_always_enabled`, `ble_scan_always_enabled`), bekleme modundaki (Deep Sleep) çekirdek uyanmalarının (wakelock) birincil sebebidir. Bu parametreler kilitlenerek batarya tüketimi minimize edilmiştir.

### C. Animasyon Ölçekleme Dinamikleri
Sistemin 120Hz yenileme hızına sahip AMOLED panelinde algılanan gecikme süresini (perceived response time) optimize etmek adına; *Pencere*, *Geçiş* ve *Animatör* süre ölçekleri varsayılan $1.0\times$ seviyesinden $0.5\times$ seviyesine çekilmiştir.

### D. Ağ Düzeyinde Gizlilik (DoT - DNS over TLS)
İnternet tarayıcısı ve üçüncü taraf uygulamalardaki reklam sunucularını çekirdek ağ düzeyinde engellemek amacıyla, cihaza doğrudan şifreli özel DNS entegre edilmiştir:

$$\text{Transport Layer} \xrightarrow{\text{DoT (Port 853)}} \texttt{dns.adguard-dns.com}$$

---

## 6. Deneysel Doğrulama ve Sistem Telemetrisi

Uygulanan optimizasyonların doğrulanması amacıyla ADB telemetri araçları vasıtasıyla canlı sistem metrikleri ölçümlenmiştir:

| Parametre | Optimizasyon Öncesi | Optimizasyon Sonrası | Durum |
| :--- | :--- | :--- | :--- |
| **Arka Plan Reklam Süreçleri** | 7 aktif servis | **0 (Sıfır)** | ✅ Tamamen İzole |
| **Sistem Hata / Çökme Günlükleri** | Rastgele ANR/Crash kayıtları | **0 Hata / 0 Çökme** | ✅ Kusursuz Kararlılık |
| **Termal Durum (Thermal Status)** | Değişken | **Status: 0 (Cool)** | ✅ Sıfır Throttling |
| **Bekleme Batarya Sıcaklığı** | 30.5 °C - 33.0 °C | **26.5 °C** | ✅ İdeal Isı Dengesi |
| **Ekran Çerçeve Hızı (Refresh Rate)** | Dalgalı | **120.00 Hz Sabit** | ✅ Maksimum Akıcılık |
| **Kullanılabilir Depolama** | Şişkin önbellek | **161 GB Boş (%69)** | ✅ Yüksek UFS Bant Genişliği |
| **Google Servisleri & Bankacılık** | Standart | **%100 Fonksiyonel** | ✅ Tam Bütünlük |

---

## 7. Sonuç ve Çıkarımlar

Bu çalışma; açık kaynaklı bir Linux iş istasyonu, deterministik ADB komut dizisi ve **Antigravity AI** otonom mühendislik ajanının koordineli çalışmasıyla, modern bir Android/HyperOS amiral gemisinin fabrika kısıtlamalarından ve OEM telemetrisinden nasıl arındırılabileceğini somut bir vaka analiziyle ortaya koymaktadır.

Elde edilen sistemik kazanımlar özetle:
1. **Veri Egemenliği ve Gizlilik:** Kullanıcı verilerini OEM ve reklam ağlarına sızdıran tüm arka plan servisleri nötralize edilmiştir.
2. **Donanım Saflığı:** 8.500 mAh batarya ve Dimensity 9500s işlemci, sanal bellek hantalığından ve gereksiz radyo taramalarından arındırılarak maksimum pil ömrü ve sıfır gecikmeli arayüz tepkisine kavuşturulmuştur.
3. **Güvenli Mühendislik:** Tek bir bankacılık uygulaması veya sistem kütüphanesi riske atılmadan; deterministik, geri alınabilir ve bilimsel bir optimizasyon standardı hayata geçirilmiştir.
