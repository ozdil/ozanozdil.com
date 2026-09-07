---
title: "PC Oyun Optimizasyonu ve FPS Artırma Rehberi: Antigravity ile Kare Süresi ve Takılma (Stutter) Çözümü"
description: "Oyunlarda FPS artırma, kare süresi (frame time) stabilizasyonu ve mikro-takılma sorunlarına yönelik sistem telemetrisi ve motor konfigürasyonu rehberi."
pubDate: "2026-09-07T14:12:51.608+03:00"
updatedDate: "2026-09-07T14:14:28.583+03:00"
tags: ["oyun optimizasyonu", "fps artırma", "kare süresi", "frame time", "1% low fps", "stutter çözümü"]
draft: false
legacyUrl: "/2026/09/pc-oyun-optimizasyonu-kare-suresi-antigravity.html"
---

**Özet:** Oyun performansında en kritik metrik ortalama FPS değil, kare süresi tutarlılığıdır (Frame Pacing). Yüksek ortalama FPS alırken yaşanan mikro-takılmalar (stuttering); önbellek yetersizliği, VRAM taşması ve çekirdekler arası gecikmeden kaynaklanır. Google Antigravity, PresentMon ve CapFrameX telemetri kayıtlarını analiz ederek darboğazları saptar; oyun motoru yapılandırmalarını (Engine.ini, Cvars) ve işlemci çekirdek yakınlığını (Affinity) donanıma tam uyumlu hale getirir.

## 1. Ortalama FPS Yanılgısı ve Kare Süresi (Frame Time) Mantığı

Geleneksel kıyaslama testlerinde en sık yapılan hata, yalnızca saniye başına üretilen kare sayısına (FPS) odaklanmaktır. Ancak FPS bir toplam değerdir ve zaman içindeki dağılımı göstermez.

Örneğin, 60 Hz yenileme hızına sahip bir ekranda her kare tam 16.67 milisaniyede bir ekrana çizilmelidir. Eğer bir saniye içinde 59 kare 10'ar milisaniyede üretilip, kalan tek bir kare 410 milisaniye gecikmeyle ekrana gelirse, yazılımsal sayaç yine "60 FPS" gösterecektir; ancak kullanıcı ekranın yarım saniyeye yakın donduğunu hissedecektir.

Bu nedenle arama motorlarında sıkça araştırılan 1% Low FPS ve 0.1% Low FPS metrikleri, oyun deneyiminin gerçek kalitesini gösteren temel parametrelerdir. Akıcı bir oyun deneyimi, bu iki değerin ortalama FPS'ye mümkün olan en yakın seviyeye sabitlenmesiyle elde edilir.

## 2. Neden "Game Booster" ve RAM Temizleyicileri Kullanılmamalıdır?

İnternette "tek tıkla hızlandırma" vaadiyle sunulan yazılımların büyük kısmı işletim sisteminin doğal bellek hiyerarşisini olumsuz etkiler:

- **Standby Belleğin Boşaltılması Hatası:** Windows, sık kullanılan dosya bloklarını boş RAM alanında "Standby List" olarak önbelleğe alır. Üçüncü parti yazılımlar bu alanı sildiğinde, oyun kaplamaları doğrudan SSD veya HDD üzerinden okunmak zorunda kalır ve bu durum anlık takılmaları tetikler.

- **Kayıt Defteri (Registry) Temizleyicileri:** Modern Windows NT çekirdeğinde kayıt defterindeki boş girdiler arama hızını etkilemez. Bilinçsizce yapılan müdahaleler donanım sürücüsü stabilitesini bozar.

- **Arka Plan İşlem Müdahaleleri:** Kritik sistem servislerini agresif şekilde kapatmak, DPC (Deferred Procedure Call) gecikmelerini tetikleyerek ses ve görüntü desenkronizasyonuna sebep olur.

## 3. Google Antigravity ile Adım Adım Bilimsel Optimizasyon

Google Antigravity, sistem dosyalarını ezbere değiştiren bir araç değildir. Kullanıcının sağladığı donanım profillerini, log kayıtlarını ve oyun dosyalarını analiz ederek sisteme özel çözümler geliştiren bir yapay zeka mühendislik ortamıdır.

### Adım 1: Donanım Telemetrisini Çıkarma

Kullanıcı, CapFrameX veya Intel tarafından geliştirilen PresentMon yazılımı ile oyun esnasında 60 saniyelik bir kare süresi kaydı alır. Bu işlem sonucunda elde edilen CSV dosyası işlemci, ekran kartı, VRAM kullanımı ve milisaniye bazlı gecikmeleri içerir.

### Adım 2: Antigravity ile Darboğaz Teşhisi

Telemetri verisi Antigravity ortamına aktarıldığında, ajan şu parametreleri karşılaştırır:

- GPU kullanımının %95 altına düştüğü anlardaki CPU tek çekirdek yükü (CPU Bound tespiti).

- VRAM sınırına ulaşıldığında PCIe veri yolunda oluşan gecikmeler (VRAM Spilling).

- Yeni bir alana girildiğinde oluşan shader derleme sıçramaları (Shader Compilation Stutter).

### Adım 3: Oyun Motoru Yapılandırması (.ini Ayarları)

Unreal Engine tabanlı oyunlarda grafik menüsünden erişilemeyen parametreler, Antigravity tarafından donanım sınırlarına göre hesaplanır ve Engine.ini dosyasına işlenir:


```text
[SystemSettings]
; Donanım VRAM kapasitesine göre doku akış havuzunun sınırlandırılması
r.Streaming.PoolSize=4096
r.Streaming.LimitPoolSizeToVRAM=1

; Ekrana ilk kez gelen nesnelerin shader derlemesini senkron döngüden çıkarma
r.CreateShadersOnLoad=1

; Çok çekirdekli sistemlerde asenkron hesaplama kuyruklarını aktifleştirme
r.AsyncCompute=1
r.Shadow.CSM.MaxCascades=3
```


## 4. Donanım Mimarisine Özel İnce Ayarlar: CPU Çekirdek Yakınlığı

Güncel işlemcilerde karşılaşılan temel problem mimari karmaşıklıktır:

- **Intel Hibrit Mimarisi (P-Core / E-Core):** Windows Zamanlayıcısı bazen oyunun ana iş parçacığını E-çekirdeklerine (Verimlilik) gönderir. Bu durumda anlık kare süresi 5 katına çıkabilir.

- **AMD Ryzen X3D (Çift CCD'li Modeller):** Oyunların yalnızca 3D V-Cache bulunan CCD üzerinde çalıştırılması gerekir. İkinci standart CCD'ye geçen iş parçacıkları önbellek gecikmesine neden olur.

Antigravity, bu işlemcileri tespit ettiğinde oyuna özel başlatma betikleri ve PowerShell çekirdek yakınlığı maskeleri (Affinity Mask) oluşturarak oyunun yalnızca en yüksek L3 önbelleğe veya en hızlı çekirdeklere kilitlenmesini sağlar.

## 5. Geleneksel Yöntemler ile Bilimsel Optimizasyon Karşılaştırması

Problem / Alan
Geleneksel Yanlış Uygulama
Antigravity Bilimsel Yaklaşımı
Kare Süresine Etkisi

Mikro-Takılma (Stutter)
Grafik kalitesini doğrudan en düşüğe almak
Doku akış havuzu ve VRAM sınırlaması ayarlama
1% Low değerinde %35-50 artış

Eski DirectX 11 Oyunları
Çözünürlük düşürmek (CPU darboğazını çözmez)
DXVK ile çizim çağrılarını Vulkan'a çevirmek
CPU tek çekirdek darboğazının kalkması

Hibrit CPU Gecikmesi
Tüm çekirdekleri kontrolsüz açık bırakmak
İş parçacıklarını P-çekirdeklere/V-Cache'e kilitlemek
Kare süresi varyansında %70 düşüş

Bellek Yönetimi
Üçüncü parti RAM temizleme programları
Standby List koruması ve sayfa dosyası sabitleme
Disk okuma takılmalarının sıfırlanması

## 6. Sıkça Sorulan Sorular (SSS)

### Oyunlarda ortalama FPS yüksek olmasına rağmen takılma (stutter) neden olur?

Ortalama FPS değeri kareler arasındaki zaman farkını (frame pacing) göstermez. Bir kare 6 ms'de üretilirken diğeri 35 ms'de üretilirse ortalama yüksek görünse bile kullanıcı gecikme dalgalanmasını takılma olarak algılar. Temel nedenler VRAM taşması, shader derleme gecikmesi veya CPU çekirdekleri arası gecikmedir.

### RAM temizleme ve Game Booster programları FPS artırır mı?

Hayır. Geleneksel RAM temizleyiciler işletim sisteminin Standby List önbelleğini zorla boşaltarak oyun dosyalarının RAM yerine daha yavaş olan SSD/HDD disklerden tekrar okunmasına yol açar ve takılmaları artırır.

### 1% Low ve 0.1% Low FPS değeri neden önemlidir?

1% Low ve 0.1% Low değerleri, test boyunca üretilen en yavaş karelerin ortalamasını temsil eder. Akıcılık hissini ortalama FPS değil, doğrudan 1% Low değerinin yüksekliği ve istikrarı belirler.

### Google Antigravity ile oyun optimizasyonu nasıl yapılır?

Antigravity kapalı devre bir hızlandırıcı değildir; sistem telemetri loglarını (PresentMon, CapFrameX) analiz ederek donanım darboğazlarını saptayan ve oyun motoru yapılandırma dosyalarını (.ini/.cfg) donanım mimarisine göre optimize eden otonom bir analiz platformudur.

## Referanslar

1. Intel Corporation. PresentMon Performance Telemetry Standard.

1. Epic Games Developer Community. Unreal Engine Scalability and Texture Memory Management.

1. Microsoft Docs. Understanding Processor Scheduling and Thread Affinity on Hybrid Architectures.
