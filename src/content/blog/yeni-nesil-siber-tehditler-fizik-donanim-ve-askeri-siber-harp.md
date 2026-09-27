---
title: "Yeni Nesil Siber Tehditler: Fiber Kablodan Akustik Dinleme, Donanım Saldırıları ve Askeri Siber Harp (2021–2026)"
description: "Fiber optik kablolardan ses dinleme, Apple Silicon açıkları, RAM'den radyo sinyali yayma, uydu silicileri ve denizaltı hat sabotajı: Son beş yılda laboratuvar ortamında kanıtlanmış veya fiilen kullanılmış en şaşırtıcı yeni nesil siber tehditler, birincil akademik kaynaklardan doğrulanmış analiziyle."
pubDate: "2026-09-27T21:45:00.000+03:00"
updatedDate: "2026-09-27T19:55:00.000+03:00"
heroImage: "/images/yeni-nesil-siber-tehditler-hero.jpg"
tags: ["siber güvenlik", "istihbarat", "donanım güvenliği", "yan kanal saldırıları", "askeri", "tempest", "fiber optik"]
draft: false
---

> Bu makale, 2021–2026 döneminde hakemli konferanslarda (USENIX Security, NDSS, USENIX Security, arXiv) yayımlanmış veya yetkili güvenlik araştırma kuruluşları (SentinelLabs, Dragos, Trail of Bits) tarafından kamuoyuna duyurulmuş çalışmalara dayanmaktadır. Tüm atıflar birincil kaynaklara yapılmıştır.

---

Modern siber güvenlik tehditlerinin paradigması köklü biçimde değişiyor. Artık saldırganlar yalnızca yazılım açıklarını değil; **fiziğin kendisini**, yani ışığı, sesi, elektromanyetik dalgaları ve hatta RAM veri yolunun yarattığı radyasyonu silah olarak kullanıyor. Bu dönüşüm hem sivil hem de askeri alanda eş zamanlı ilerliyor.

Bu kapsamlı analizde, son beş yılda laboratuvar ortamında kanıtlanmış ya da savaş alanında aktif olarak kullanılmış en şaşırtıcı yöntemleri, akademik kaynaklarından doğrulayarak inceliyoruz.

---

## Bölüm I: Fiziksel Yan Kanal Saldırıları

### 1. Fiber Optik Kablolardan Akustik Dinleme (COAES)

**Kaynak:** Youqian Zhang, Zheng Fang, Huan Wu ve diğerleri, *"Hiding an Ear in Plain Sight: On the Practicality and Implications of Acoustic Eavesdropping with Telecom Fiber Optic Cables"*, NDSS Symposium 2026.

İnternet altyapısının omurgasını oluşturan fiber optik kablolar, bir odada konuşulduğunda ses dalgalarının yarattığı mikro-basınç değişimlerine karşı doğası gereği hassastır. Bu, *micro-bending* (mikro bükülme) adı verilen fiziksel bir olgudur: ses dalgaları fiberin cam çekirdeğinde nanometre altı deformasyonlara neden olur, bu deformasyonlar fiberin içindeki ışığın faz durumunu değiştirir.

**Saldırı mekanizması:**

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 not-prose font-mono shadow-xl">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
    <span class="font-mono text-xs uppercase tracking-wider font-semibold text-[#ffffff]">
      // COAES: FİBER OPTİK AKUSTİK DİNLEME ZİNCİRİ
    </span>
    <span class="text-[11px] font-mono text-[#71717a]">NDSS 2026</span>
  </div>
  <div class="space-y-3">
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">01</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">Ses → Micro-Bending</h5>
          <p class="text-xs text-[#a1a1aa]">Konuşma dalgaları fiberin cam çekirdeğini nanometre altı düzeyde büker; refraktif indeks anlık değişir.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#38bdf8] hidden sm:inline">DAS / Rayleigh</span>
    </div>
    <div class="flex justify-center text-[#71717a] text-xs font-mono">↓ Lazer darbeleri gönderilir, geri saçılım analiz edilir</div>
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">02</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">Duyusal Reseptör (Sensory Receptor)</h5>
          <p class="text-xs text-[#a1a1aa]">Kablo 65 mm çaplı PET silindir etrafına sarılarak mekanik-optik dönüşüm verimliliği artırılır.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#f59e0b] hidden sm:inline">Bobin / Spool</span>
    </div>
    <div class="flex justify-center text-[#71717a] text-xs font-mono">↓ Faz kaymaları çözümlenir</div>
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">03</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">YZ Transkripsiyon (Whisper / Parakeet)</h5>
          <p class="text-xs text-[#a1a1aa]">Ham titreşim verisi büyük dil modelleriyle işlenerek konuşmalar metne dönüştürülür. Ofis ortamında WER: %9.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#10b981] hidden sm:inline">WER &lt; %9</span>
    </div>
  </div>
</div>

Araştırmanın en kritik bulgusu: FTTH evlere kadar fiber altyapısındaki **"dark fiber"** (kullanılmayan hatlar) bu saldırı için kullanılabilir ve **ultrasonik jammer'lar bu tehdide karşı tamamen etkisizdir** çünkü sistemin bir mikrofona ihtiyacı yoktur; fiberin kendisi sensördür.

> *"We show that COAES can be successfully conducted on telecom fiber-optic cables by leveraging off-the-shelf DAS systems with a specialized sensory receptor... The attack remains effective even when an ultrasonic jammer is deployed right next to the cable."*
>
> — Youqian Zhang ve diğerleri, NDSS 2026

---

### 2. Glowworm: Güç LED'inden Konuşma Kurtarma (2021)

**Kaynak:** Ben Nassi, Yaron Pirutin ve diğerleri, *"Glowworm Attack: Optical TEMPEST Sound Recovery via a Device's Power Indicator LED"*, CCS 2021, Ben-Gurion Üniversitesi.

Akıllı hoparlörler, USB hub'lar ve masaüstü hoparlörlerin üzerindeki küçük güç göstergesi LED'leri doğrudan amplifikatörün güç hattına bağlıdır. Ses çalındığında güç tüketimi dalgalanır, LED'in parlaklığı değişir. Bu değişim **insan gözüyle görülmez** ancak 35 metre uzaktan fotodiyot bağlı bir teleskopla yakalanabilir.

**Etkilenen cihazlar:** Google Home Mini, Google Nest Audio, Logitech Z120/S120, JBL Go 2, Raspberry Pi 3/4. Test edilen cihazların yaklaşık **%50'si savunmasız** çıkmıştır. Çözüm ise son derece basittir: LED üzerine yapıştırılan siyah bir bant.

---

### 3. LidarPhone: Robot Süpürge LiDAR'ını Lazer Mikrofona Dönüştürme (2020/2021)

**Kaynak:** Sriram Sami, Sean Rui Xiang Tan ve diğerleri, *"LidarPhone: Using Telerobotic LiDAR as a Microphone"*, SenSys 2020, Ulusal Singapur Üniversitesi & Maryland Üniversitesi.

Robot süpürgelerin navigasyon için kullandığı döner LiDAR sensörleri yazılım istismarıyla sabitlenebilir. Bir çöp kovası, cips paketi veya poşet gibi hafif nesnelere sabitlendiğinde, insan sesi nesneyi titreştirir ve yansıyan lazerin uçuş süresi (ToF) değişir. Derin öğrenme filtresiyle işlenen bu verilerden **%90 üzeri doğrulukla** konuşulan rakamlar ve müzik türleri tespit edilmiştir.

---

## Bölüm II: Mikroişlemci ve Donanım Açıkları

### 4. GoFetch: Apple Silicon'da Yamalanması Mümkün Olmayan Kriptografik Sızıntı (2024)

**Kaynak:** Boru Chen, Yingchen Wang, Pradyumna Shome ve diğerleri, *"GoFetch: Breaking Constant-Time Cryptographic Implementations Using Data Memory-Dependent Prefetchers"*, USENIX Security 2024. Pwnie Award 2024 — En İyi Kriptografik Saldırı.

Apple Silicon çiplerindeki (M1, M2, M3, A14) **Veri Belleğe Bağlı Ön Bellekleyici (DMP — Data Memory-Dependent Prefetcher)** performansı artırmak için tasarlanmıştır. Ancak DMP, bellekteki verinin içeriğini okuyarak işaretçi (pointer) gibi görünen değerleri spekülatif olarak önbelleğe çeker. Bu davranış, **sabit zamanlı (constant-time)** çalışan ve yan kanal saldırılarına karşı güvenli kabul edilen şifreleme algoritmalarını (RSA, Diffie-Hellman, CRYSTALS-Kyber, Dilithium) tamamen devre dışı bırakır.

![GoFetch — Apple Silicon DMP saldırısı resmi görseli (gofetch.fail)](/images/gofetch-apple-silicon-dmp.jpg)
*Kaynak: [gofetch.fail](https://gofetch.fail) — Resmi proje logosu ve saldırı özeti. USENIX Security 2024.*

> *"GoFetch is a microarchitectural side-channel attack that can extract secret keys from constant-time cryptographic implementations via data memory-dependent prefetchers (DMPs). We show that DMPs are present in many Apple CPUs and pose a real threat to multiple cryptographic implementations, allowing us to extract keys from OpenSSL Diffie-Hellman, Go RSA, as well as CRYSTALS Kyber and Dilithium."*
>
> — Boru Chen, Yingchen Wang ve diğerleri, USENIX Security 2024

Açık doğrudan silikon tasarımında bulunduğu için mevcut cihazlarda yazılım yamasıyla kapatılamaz. M1 ve M2 için yalnızca kernel müdahalesiyle (HID11_EL1[30] bit) DMP devre dışı bırakılabilir, ancak bu macOS tarafından henüz desteklenmemektedir.

---

### 5. Hertzbleed: CPU Frekansını Uzaktan Kriptografik Zamanlama Saldırısına Dönüştürme (2022)

**Kaynak:** Yingchen Wang, Riccardo Paccagnella ve diğerleri, *"Hertzbleed: Turning Power Side-Channel Attacks Into Remote Timing Attacks on x86"*, USENIX Security 2022. CVE-2022-24436 (Intel) / CVE-2022-23823 (AMD).

Modern x86 işlemciler güç ve ısı dengesini yönetmek için **Dinamik Voltaj ve Frekans Ölçekleme (DVFS)** kullanır. Elektrik tüketimi, işlenen verinin bitlerine göre değişir; tüketim artınca işlemci frekansı düşer. Saldırgan bu frekans değişimini **yalnızca ağ gecikmesini (RTT) mikrosaniye hassasiyetiyle ölçerek** uzaktan gözlemleyebilir ve sunucunun kriptografik anahtarlarını çıkarabilir. Fiziksel güç ölçümü gerektirmez.

---

### 6. Downfall / GDS (2023): Intel Gather Talimatındaki Spekülatif Sızıntı

**Kaynak:** Daniel Moghimi, *"Downfall: Exploiting Speculative Data Gathering"*, USENIX Security 2023. CVE-2022-40982. Intel Core 6. nesil (Skylake) ile 11. nesil (Tiger Lake) arası tüm işlemciler etkilenmiştir.

Intel CPU'lardaki `GATHER` bellek optimizasyon talimatı, spekülatif yürütme sırasında dahili vektör registerlarındaki verileri istemeden dışarı sızdırabilir. Aynı fiziksel işlemci çekirdeğini paylaşan başka bir işlem (VM veya güvenilir uygulama dahil), şifreler ve kriptografik anahtarlar dahil hassas verileri okuyabilir.

---

### 7. ZenHammer: DDR5 Belleklerde Rowhammer (2024)

**Kaynak:** Patrick Jattke, Max Wipfli, Flavien Solt, Michele Marazzi ve diğerleri, *"ZenHammer: Rowhammer Attacks on AMD Zen-based Platforms"*, USENIX Security 2024, ETH Zürih.

DDR5 bellekler, dahili hata düzeltme (On-Die ECC) ve hedef satır yenileme (TRR) mekanizmalarıyla Rowhammer saldırılarına karşı bağışık kabul ediliyordu. ETH Zürih araştırmacıları, AMD Zen mimarisinin bellek kontrolcüsü zamanlama desenlerini tersine mühendislikle çözerek bu savunmaları devre dışı bırakmış ve **DDR5 yongalarında hedeflenen bellek bitlerini ilk kez manipüle etmeyi başarmıştır**.

---

### 8. LeftoverLocals: GPU Belleği Veri Kalıntısı Sızıntısı (2024)

**Kaynak:** Tyler Sorensen ve diğerleri, *"LeftoverLocals: Listening to LLM Responses Through Leaked GPU Local Memory"*, Trail of Bits, Ocak 2024.

AMD, Apple ve Qualcomm GPU'larında bir işlem GPU yerel belleğini kullandıktan sonra bu bellek tam olarak temizlenmez. Aynı sistemi kullanan başka bir işlem bu "kalıntı" verileri okuyabilir. Çok kullanıcılı sunucu ortamlarında çalışan LLM uygulamalarında **çağrı başına megabaytlarca veri** bu yöntemle sızdırılabilmiştir.

---

## Bölüm III: Air-Gap Geçen Veri Sızdırma Teknikleri

### 9. RAMBO: RAM Veri Yolundan Radyo Sinyali Yayarak İzole Sistemleri Ele Geçirme (2024)

**Kaynak:** Mordechai Guri, *"RAMBO: Leaking Secrets from Air-Gap Computers by Spelling Covert Radio Signals from Computer RAM"*, arXiv:2409.02292, Ben-Gurion Üniversitesi, Eylül 2024.

**RAMBO (Radiation of Air-gapped Memory Bus for Offense)** yöntemi, internete bağlı olmayan izole (air-gapped) bilgisayarları hedef alır. Sisteme sızdırılan hafif zararlı yazılım, DDR RAM'in veri yolundaki voltajı ve transfer desenlerini nanosaniye hassasiyetiyle modüle eder. RAM modülleri birer radyo anteni gibi elektromanyetik dalga yaymaya başlar. **7 metre mesafeden ucuz bir SDR (Software-Defined Radio) alıcısıyla** bu sinyaller yakalanabilir, saniyede yaklaşık 1.000 bit hızla şifreler, tuş vuruşları ve belgeler çalınabilir.

---

### 10. Deep-TEMPEST: Yapay Zeka ile HDMI'dan Ekran İçeriği Okuma (2024)

**Kaynak:** Santiago Fernandez, Emilio Martinez ve diğerleri, *"Deep-TEMPEST: Using Deep Learning to Eavesdrop on HDMI from its Unintended Electromagnetic Emanations"*, arXiv:2407.09717, Universidad de la República, Uruguay, Temmuz 2024. Açık kaynak: [github.com/emidan19/deep-tempest](https://github.com/emidan19/deep-tempest).

HDMI kablolarının yaydığı parazitik elektromanyetik emisyonlar (Van Eck Phreaking) eski yöntemlerle yalnızca gürültülü bir gölge olarak yakalanabiliyordu. Uruguaylı araştırmacılar bu problemi bir **ters-problem derin öğrenme modeli** olarak tanımlayarak çözdü: SDR anteniyle toplanan zayıf RF sinyali derin öğrenme modeline verildiğinde Karakter Hata Oranı (CER) **%90'dan %30'un altına düşürüldü** ve ekrandaki metin ile görüntüler binanın duvarının ötesinden okunur hale geldi.

![Deep-TEMPEST: HDMI elektromanyetik emisyonlarından derin öğrenme ile ekran kurtarma örnekleri](/images/deep-tempest-hdmi-eavesdropping.png)
*Kaynak: [github.com/emidan19/deep-tempest](https://github.com/emidan19/deep-tempest) — Resmi proje görseli. arXiv:2407.09717.*

---

## Bölüm IV: Yapay Zeka Sistemlerine Yönelik Saldırılar

### 11. Akustik Klavye Dinleme ile YZ Destekli Parola Kurtarma (2023)

**Kaynak:** Joshua Harrison, Ehsan Toreini, Maryam Mehrnezhad, *"A Practical Deep Learning-Based Acoustic Side Channel Attack on Keyboards"*, arXiv:2308.01074, Ağustos 2023.

Mekanik veya laptop klavyelerindeki her tuşun fiziksel konumu ve kasa yapısı nedeniyle mikro düzeyde farklı bir ses imzası vardır. Araştırmacılar, hedefin katıldığı bir **Zoom görüşmesinden** veya **yanındaki akıllı telefon mikrofonundan** gelen tuş seslerini kaydedip spektrograma dönüştürerek CoAtNet derin öğrenme modeliyle işledi. Sonuç: **%95 doğrulukla** yazılan içerik tespit edildi. LLM destekli bağlam düzeltmesiyle bu oran daha da yükselmektedir.

---

### 12. Morris II: Kendini Kopyalayan YZ Solucanı (2024)

**Kaynak:** Stav Cohen, Ron Bitton, Ben Nassi, *"Here Comes the AI Worm: Unleashing Zero-click Worms that Target GenAI-Powered Applications"*, arXiv:2403.02817, Mart 2024.

Geleneksel zararlı yazılım yerine **LLM'lerin talimat takip mekanizmasını** istismar eden ilk solucan konseptidir. Bir e-postaya yerleştirilen özel hazırlanmış zehirli metin (adversarial prompt), e-postayı özetleyen YZ asistanına ulaştığında modeli ele geçirir. Model kullanıcının verilerini sızdırırken aynı zararlı talimatı yanıtladığı diğer e-postalara da ekler. ChatGPT ve Gemini tabanlı sistemler üzerinde **sıfır tıklama (zero-click)** ile yayılan bu solucan konsepti doğrulanmıştır.

---

## Bölüm V: Askeri ve Devlet Destekli Siber Harp

### 13. Lübnan Çağrı Cihazı ve Telsiz Operasyonu (Eylül 2024)

Siber istihbarat ile kinetik imhanın tedarik zincirinde birleştiği, tarihin en büyük operasyonu olarak kayıtlara geçmiştir. Paravan şirketler aracılığıyla Hizbullah'a satılan çağrı cihazlarının lityum pillerinin içine patlayıcı entegre edilmiş; merkezi sunucudan gönderilen şifreli bir sinyal tüm cihazları eşzamanlı olarak tetiklemiştir. Bu operasyon, **tedarik zinciri güvenliğinin donanım katmanında nasıl çöktürülebileceğini** somut biçimde ortaya koymuştur.

---

### 14. AcidRain: Viasat Uydu Saldırısı (Şubat 2022)

**Kaynak:** Juan Andrés Guerrero-Saade, Max van Amerongen, *"AcidRain: A Modem Wiper Rains Down on Europe"*, SentinelLabs, Mart 2022. Atıf: Rusya GRU / Sandworm.

![AcidRain Viasat KA-SAT uydu saldırısı — SentinelLabs (SentinelOne)](/images/acidrain-viasat-satellite-wiper.jpg)
*Kaynak: [sentinelone.com/labs/acidrain](https://www.sentinelone.com/labs/acidrain-a-modem-wiper-rains-down-on-europe/) — SentinelLabs resmi yayını. Mart 2022.*

Ukrayna'ya kara harekâtının başladığı saatlerde (24 Şubat 2022), Sandworm grubu Viasat'ın KA-SAT uydu ağının yönetim segmentine VPN açığı üzerinden sızmıştır. MIPS mimarisi için yazılmış **AcidRain** adlı ELF ikili dosyası, OTA (Over-The-Air) firmware güncellemesi kılığında on binlerce uydu terminaline aktarılmış ve cihazların flash belleklerini geri dönüşsüz biçimde silmiştir. Ukrayna ordusunun haberleşme altyapısı felç olmuş, Avrupa genelinde binlerce rüzgar türbininin kontrol hattı devre dışı kalmıştır.

> *"AcidRain is a wiper malware designed to attack modems and routers. Following a VPN exploitation, the threat actor deployed AcidRain to wipe Viasat KA-SAT modems across Europe, causing a major internet outage in Ukraine..."*
>
> — SentinelLabs, *AcidRain: A Modem Wiper Rains Down on Europe*, Mart 2022

---

### 15. PIPEDREAM / INCONTROLLER: Endüstriyel Kontrol Sistemleri Silahı (2022)

**Kaynak:** Dragos Inc., *"CHERNOVITE's PIPEDREAM Malware Targeting Industrial Control Systems"*, Nisan 2022. Mandiant (Google Cloud) tarafından INCONTROLLER adıyla da yayımlanmıştır.

![PIPEDREAM — Dragos CHERNOVITE ICS saldırı çerçevesi](/images/pipedream-chernovite-dragos.png)
*Kaynak: [dragos.com](https://www.dragos.com/threat/chernovite/) — Resmi Dragos tehdit raporu görseli. Nisan 2022.*

Tarihte yalnızca yedinci kez tespit edilen ICS odaklı zararlı yazılımdır. Schneider Electric ve Omron PLC'lerini, OPC-UA sunucularını ve CODESYS çalışma zamanını modüler beş bileşenle hedef alır:

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 not-prose font-mono shadow-xl">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
    <span class="font-mono text-xs uppercase tracking-wider font-semibold text-[#ffffff]">
      // PIPEDREAM: BEŞ MODÜLERİN MATRİSİ
    </span>
    <span class="text-[11px] font-mono text-[#71717a]">Dragos / CHERNOVITE</span>
  </div>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
    <div class="p-3 rounded-xl border border-[#27272a] bg-[#18181b]">
      <span class="font-mono font-bold text-xs text-[#38bdf8]">EVILSCHOLAR</span>
      <p class="text-xs text-[#a1a1aa] mt-1">Schneider Electric Modicon PLC keşfi ve manipülasyonu</p>
    </div>
    <div class="p-3 rounded-xl border border-[#27272a] bg-[#18181b]">
      <span class="font-mono font-bold text-xs text-[#f59e0b]">BADOMEN</span>
      <p class="text-xs text-[#a1a1aa] mt-1">CODESYS tabanlı Omron PLC komuta kontrol</p>
    </div>
    <div class="p-3 rounded-xl border border-[#27272a] bg-[#18181b]">
      <span class="font-mono font-bold text-xs text-[#10b981]">MOUSEHOLE</span>
      <p class="text-xs text-[#a1a1aa] mt-1">OPC-UA sunucu taraması ve şema haritalaması</p>
    </div>
    <div class="p-3 rounded-xl border border-[#27272a] bg-[#18181b]">
      <span class="font-mono font-bold text-xs text-[#ef4444]">DUSTTUNNEL</span>
      <p class="text-xs text-[#a1a1aa] mt-1">Şifreli C2 tüneli ve ağ pivoting modülü</p>
    </div>
    <div class="p-3 rounded-xl border border-[#27272a] bg-[#18181b] md:col-span-2">
      <span class="font-mono font-bold text-xs text-[#a78bfa]">LAZYCARGO</span>
      <p class="text-xs text-[#a1a1aa] mt-1">CVE-2020-15368 (ASRock sürücü açığı) üzerinden Windows kernel privilege escalation</p>
    </div>
  </div>
</div>

Dragos'un analizine göre PIPEDREAM, **bilinen ICS saldırı tekniklerinin %38'ini ve taktiklerinin %83'ünü** tek başına uygulayabilme kapasitesine sahiptir.

---

### 16. Denizaltı Fiber Optik Hat Sabotajı ve Pasif İstihbarat

Küresel veri trafiğinin **%95'inden fazlası** okyanus tabanındaki denizaltı kablolarından geçer. Bu hatlar bugün askeri doktrinlerin birincil hedefleri haline gelmiştir.

**Pasif Tapping:** Özel görev denizaltıları (ABD'de USS Jimmy Carter, Rusya'da Yantar araştırma gemisi ve Losharik nükleer denizaltısına bağlı ROV'lar) *macro-bending* tekniğiyle fiberleri hafifçe eğerek sinyal keser; veri akışı bölünmeden kopyalanır.

**Gri Bölge Sabotajları (2023–2025):** Baltık Denizi, Kızıldeniz ve Tayvan Boğazı çevresinde ticari görünümlü gemilerin çıpalarını okyanus tabanında kilometrelerce sürükleyerek stratejik fiber hatları kasıtlı olarak kopardığı belgelenmiştir. Bu tür olaylar 2024 yılında NATO'nun resmi güvenlik gündemine girmiştir.

---

### 17. CosmicStrand / MoonBounce: UEFI Firmware Rootkit'leri

**Kaynak:** Kaspersky Labs, *"CosmicStrand: Discovery of a Sophisticated UEFI Firmware Rootkit"*, Temmuz 2022. Çin APT grubuna atfedilmektedir.

Doğrudan anakart üzerindeki SPI Flash çipine veya UEFI Boot Manager katmanına yerleşen bu araçlar, sabit disk sökülse, format atılsa veya işletim sistemi tamamen yeniden kurulsa dahi **silinemez**. Windows Güvenli Önyükleme (Secure Boot) mimarisini imzasız sürücüler üzerinden devre dışı bırakarak işletim sistemi çekirdeği (kernel) yüklenmeden önce devreye girer.

---

### 18. GNSS Spoofing ve Bilişsel Elektronik Harp

2022'den itibaren Ukrayna, Orta Doğu ve Karadeniz bölgesinde aktif olarak kullanılan **GNSS meaconing ve spoofing** saldırıları, GPS koordinatlarını sahte değerlerle değiştirerek insansız hava araçlarını ve güdümlü mühimmatı yanlış konumlara yönlendirmektedir. Bilişsel elektronik harp (Cognitive EW) algoritmaları, taktik veri ağlarının (Link-16 gibi) frekans atlamalı iletim desenlerine doğrudan RF katmanından paket enjeksiyonu deneme kapasitesine ulaşmıştır.

---

## Sonuç: Yeni Tehdit Katmanı

Bu saldırılar ortak bir eksende buluşuyor: **Fizik kanunları artık bir saldırı yüzeyi.** Işık, ses, elektromanyetik dalga ve kristal bellek dinamikleri; saldırganlar tarafından yazılım güvenlik modellerini hiç devreye sokmadan kullanılabiliyor. Savunma perspektifinden bakıldığında bu durum şu anlama geliyor:

- Yazılım yamaları tek başına yetersiz; silikon tasarım, elektromanyetik yalıtım ve fiziksel güvenlik katmanları birlikte düşünülmeli.
- Fiber altyapı TSCM (Teknik Gözetleme Karşı Önlem) kapsamına alınmalı.
- LLM tabanlı sistemler indirekt prompt enjeksiyonuna karşı mimari düzeyde tasarlanmalı.
- Askeri ve kritik altyapı sistemlerinde tedarik zinciri donanım güvencesi standartları (SBOM + hardware BOM) zorunlu hale gelmeli.

---

## Kaynaklar

1. Zhang, Y. ve diğerleri. *"Hiding an Ear in Plain Sight."* NDSS 2026. [ndss-symposium.org](https://www.ndss-symposium.org/ndss2026/)
2. Nassi, B. ve diğerleri. *"Glowworm Attack."* ACM CCS 2021. [nassiben.com](https://nassiben.com/glowworm-attack)
3. Sami, S. ve diğerleri. *"LidarPhone."* SenSys 2020. [nus.edu.sg](https://www.nus.edu.sg/)
4. Chen, B. ve diğerleri. *"GoFetch."* USENIX Security 2024. [gofetch.fail](https://gofetch.fail)
5. Wang, Y. ve diğerleri. *"Hertzbleed."* USENIX Security 2022. [hertzbleed.com](https://www.hertzbleed.com/)
6. Moghimi, D. *"Downfall."* USENIX Security 2023. [downfall.page](https://downfall.page/)
7. Jattke, P. ve diğerleri. *"ZenHammer."* USENIX Security 2024. [comsec.ethz.ch](https://comsec.ethz.ch/)
8. Sorensen, T. ve diğerleri. *"LeftoverLocals."* Trail of Bits, 2024. [leftoverlocals.com](https://leftoverlocals.com/)
9. Guri, M. *"RAMBO."* arXiv:2409.02292, 2024. [arxiv.org](https://arxiv.org/abs/2409.02292)
10. Fernandez, S. ve diğerleri. *"Deep-TEMPEST."* arXiv:2407.09717, 2024. [github.com/emidan19/deep-tempest](https://github.com/emidan19/deep-tempest)
11. Harrison, J. ve diğerleri. *"Acoustic Side Channel Attack on Keyboards."* arXiv:2308.01074, 2023.
12. Cohen, S. ve diğerleri. *"Morris II."* arXiv:2403.02817, 2024.
13. Guerrero-Saade, J.A. ve diğerleri. *"AcidRain."* SentinelLabs, 2022. [sentinelone.com/labs/acidrain](https://www.sentinelone.com/labs/acidrain-a-modem-wiper-rains-down-on-europe/)
14. Dragos Inc. *"PIPEDREAM: CHERNOVITE's ICS Malware."* 2022. [dragos.com](https://www.dragos.com/threat/chernovite/)
15. Kaspersky GReAT. *"CosmicStrand UEFI Rootkit."* 2022. [kaspersky.com](https://securelist.com/cosmicstrand-uefi-firmware-rootkit/)
