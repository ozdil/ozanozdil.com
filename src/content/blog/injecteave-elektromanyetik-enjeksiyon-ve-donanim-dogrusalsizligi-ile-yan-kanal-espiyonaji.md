---
title: "InjectEave: Donanım Doğrusalsızlığı ve Aktif EM Enjeksiyonu ile Yan Kanal Espiyonajı"
description: "USENIX Security 2026'da yayımlanan InjectEave araştırmasının teknik ve istihbari analizi: Donanım bileşenlerindeki kaçınılmaz doğrusalsızlık, aktif RF enjeksiyonuyla spektral uyumsuzluğun aşılması, duvar arkası akustik dinleme, TEMPEST doktrini ve savunma mimarisi."
pubDate: "2026-09-24T00:45:00.000+03:00"
updatedDate: "2026-09-24T00:45:00.000+03:00"
tags: ["siber güvenlik", "istihbarat", "donanım güvenliği", "yan kanal saldırıları", "rf", "tempest"]
draft: false
toc: true
---

> **Akademik Bildiri Künyesi:**
> Haoran Yan, Ziyu Shao, Shuhao Zhang, Qinhong Jiang, Yan Long. *"Injected and Leaked: Actively Inducing Side-Channel Leakage Using Electromagnetic Injection and Hardware Nonlinearity"*, **Proceedings of the 35th USENIX Security Symposium (USENIX Security '26)**, 2026, ss. 2485-2504.
> arXiv Ön Baskısı: [arXiv:2609.04785v1 [cs.CR]](https://arxiv.org/abs/2609.04785v1) | Proje Sayfası: [injecteave.github.io](https://injecteave.github.io/) | Açık Kaynak Artefakt: [DOI: 10.5281/zenodo.18500378](https://doi.org/10.5281/zenodo.18500378)

---

## 1. Giriş: Pasif TEMPEST'ten Aktif RF Hibrit Espiyonajına

Siber güvenlik ve sinyal istihbaratı (SIGINT) literatüründe elektromanyetik yan kanal sızıntıları (TEMPEST) onlarca yıldır bilinmektedir. Bir mikroişlemcinin, ekran kablosunun veya analog ses devresinin PCB üzerindeki iletken hatları, istem dışı birer anten (unintentional radiator) gibi davranarak içeride akan elektriksel sinyalleri mikrovolt seviyesinde çevreye yayar. Savunma kurumları ve istihbarat teşkilatları (NATO SDIP-27 gibi standartlar aracılığıyla) uzun yıllardır kritik tesislerdeki cihazları metal zırhlarla kaplayarak veya pasif elektromanyetik ışıma sınırları koyarak korumaya çalışmaktadır.

Ancak klasik pasif elektromanyetik dinlemenin fizik kanunlarından kaynaklanan çok temel bir açmazı vardır: **Spektral Uyumsuzluk (Spectral Mismatch)**.

İnsan konuşması (20 Hz - 20 kHz), analog sensör sinyalleri veya güç tüketimi gibi düşük frekanslı (LF) analog veriler, dalga boyları onlarca kilometreyi bulduğu için santimetrelik kulaklık kablolarından ya da PCB yollarından neredeyse hiçbir elektromanyetik ışıma üretemez. Bir antenin verimli ışıma yapabilmesi için boyutunun sinyalin dalga boyuyla orantılı olması gerekir ($\lambda/2$ veya $\lambda/4$). Düşük frekanstaki zayıf akımlar kablodan dışarı yayılamadan sönümlenir. Bu nedenle geleneksel TEMPEST saldırılarında kulaklıktan ses sızdırmak ya imkânsız kabul edilmiş ya da cihazın birkaç milimetre yanına yerleştirilen yüksek hassasiyetli manyetik problarla sınırlandırılmıştır.

Hong Kong Bilim ve Teknoloji Üniversitesi (Guangzhou) ve Hong Kong Politeknik Üniversitesi araştırmacıları tarafından **USENIX Security 2026** konferansında sunulan **InjectEave** çalışması, bu fiziksel engeli tamamen ters yüz eden aktif bir saldırı sınıfı tanımlamaktadır: **Enjeksiyonla Tetiklenen Elektromanyetik Yan Kanallar (Injection-Induced EM Side Channels)**.

Araştırmacılar, pasif olarak beklemek yerine hedefe harici bir yüksek frekanslı RF taşıyıcı dalgası (carrier) gönderildiğinde, modern donanımlardaki kaçınılmaz analog doğrusalsızlıkların (hardware nonlinearity) bu taşıyıcı ile içerideki sırrı çarparak havaya geri fırlattığını (re-radiation) kanıtlamıştır.

---

## 2. Fiziksel ve Matematiksel Mekanizma: IME Çevrimi

InjectEave saldırısı, **Enjeksiyon - Modülasyon - Emisyon (IME)** olarak adlandırılan üç aşamalı bir fiziksel model üzerinden işler.

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 not-prose font-mono shadow-xl">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
    <span class="font-mono text-xs uppercase tracking-wider font-semibold text-[#ffffff]">
      // INJECTEAVE: ENJEKSİYON - MODÜLASYON - EMİSYON (IME) ÇEVRİMİ
    </span>
    <span class="text-[11px] font-mono text-[#71717a]">Fiziksel Katman Akışı</span>
  </div>
  <div class="space-y-3">
    <!-- Adım 1 -->
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between shadow-xs">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">01</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">1. ENJEKSİYON (Injection)</h5>
          <p class="text-xs text-[#a1a1aa]">Saldırgan yüksek frekanslı RF taşıyıcı dalga (fc) basar. Kablolar ve hatlar alıcı anten gibi bu enerjiyi çeker.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#38bdf8] hidden sm:inline">RF Taşıyıcı [fc]</span>
    </div>
    <div class="flex justify-center text-[#71717a] text-xs font-mono">↓ PCB Hatlarında Çiftlenim (Coupling)</div>
    <!-- Adım 2 -->
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between shadow-xs">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">02</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">2. DOĞRUSALSIZ MODÜLASYON (Modulation)</h5>
          <p class="text-xs text-[#a1a1aa]">Op-amp, ADC veya MOSFET içindeki non-lineer transfer karakteristiği fc ve fs sinyallerini çarpar.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#f59e0b] hidden sm:inline">İntermodülasyon [fc ± fs]</span>
    </div>
    <div class="flex justify-center text-[#71717a] text-xs font-mono">↓ Yukarı Çevrim (Up-conversion) & Rezonans</div>
    <!-- Adım 3 -->
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between shadow-xs">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">03</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">3. GERİ IŞIMA VE EMİSYON (Emission)</h5>
          <p class="text-xs text-[#a1a1aa]">Modüle olan sinyal, yüksek frekansta verimli antene dönüşen hatlar üzerinden havaya geri saçılır.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#ef4444] hidden sm:inline">Geri Saçılım (Backscatter)</span>
    </div>
    <div class="flex justify-center text-[#71717a] text-xs font-mono">↓ SDR Alıcı & Spektrum Analizörü</div>
    <!-- Adım 4 -->
    <div class="p-4 rounded-xl border border-[#27272a] bg-[#18181b] flex items-center justify-between shadow-xs">
      <div class="flex items-center gap-3">
        <span class="w-7 h-7 rounded-lg bg-[#27272a] text-[#ffffff] flex items-center justify-center font-mono font-bold text-xs">04</span>
        <div>
          <h5 class="font-bold text-sm text-[#ffffff]">4. DEMODÜLASYON VE AI İYİLEŞTİRME (SGMSE)</h5>
          <p class="text-xs text-[#a1a1aa]">AM demodülasyonu sonrasında difüzyon tabanlı üretken ses modeliyle gürültü ayıklanır ve ses çözülür.</p>
        </div>
      </div>
      <span class="font-mono text-xs text-[#10b981] hidden sm:inline">Net Ses & Veri</span>
    </div>
  </div>
</div>

### Aşama 1: Enjeksiyon (Injection)
Saldırgan, hedef cihazın fiziksel kablo veya hat uzunluklarına uygun bir rezonans frekansı seçer (genellikle yüzlerce MHz veya GHz bandı). Yazılım tanımlı radyo (SDR, örneğin USRP B210) ve bir yönlü anten kullanılarak hedefe tek-tonlu (single-tone) sürekli bir RF taşıyıcı sinyali $x_{inj}(t) = A_c \cos(2\pi f_c t)$ gönderilir. Hedef cihazın kulaklık kablosu veya PCB hatları, bu frekansta verimli bir alıcı anten görevi üstlenerek RF enerjisini aygıtın iç devrelerine çeker.

### Aşama 2: Donanım Doğrusalsızlığı ve Modülasyon (Modulation)
Saf matematiksel teoride elektronik bileşenler doğrusal kabul edilse de, fiziksel dünyada hiçbir yarı iletken tam doğrusal değildir. Kulaklık amplifikatörleri (op-amp), analog-dijital dönüştürücüler (ADC), anahtarlamalı güç dönüştürücüler ve MOSFET'ler kaçınılmaz olarak doğrusal olmayan bir transfer karakteristiğine sahiptir:

$$y(t) = a_1 x(t) + a_2 x^2(t) + a_3 x^3(t) + \dots$$

Devre içerisindeki toplam giriş voltajı, enjekte edilen RF taşıyıcısı ile cihazın o anda işlediği düşük frekanslı gizli analog sinyalin (örneğin kulaklığa giden ses voltajı $x_s(t)$) toplamıdır:

$$x(t) = x_{inj}(t) + x_s(t) = A_c \cos(2\pi f_c t) + s(t)$$

İkinci dereceden karesel terim ($a_2 x^2(t)$) açıldığında çapraz çarpım ortaya çıkar:

$$x^2(t) = \dots + 2 A_c s(t) \cos(2\pi f_c t) + \dots$$

Bu matematiksel gerçek, düşük frekanslı $s(t)$ sırrının doğrudan RF taşıyıcısının frekansı $f_c$ etrafındaki yan bantlara genlik modülasyonu (AM) ile bindirilmesi (up-conversion) anlamına gelir. Yani saldırganın dışarıdan bastığı yüksek frekanslı sinyal, kurbanın devre elemanı içinde hedefin gizli sesiyle bizzat modüle edilmektedir.

Araştırmacılar, bu durumu makalede şu ifadelerle açıklar:

> *"The intuition is that the frequency of the secret signal and the device's efficient EM emission frequency often face a mismatch... InjectEave follows an Injection-Modulation-Emission model. Injection: the carrier couples into the device's unintentional antennas. Modulation: a nonlinear component mixes the secret with the carrier, up-converting it into sidebands at the carrier frequency. Emission: the device's unintentional antennas re-radiate the modulated carrier back into the air."*
>
> *(Türkçe Çevirisi: "Temel sezgi şudur: Gizli sinyalin frekansı ile cihazın verimli elektromanyetik ışıma frekansı sıklıkla birbiriyle uyuşmaz... InjectEave bir Enjeksiyon-Modülasyon-Emisyon modeli izler. Enjeksiyon: Taşıyıcı dalga cihazın istem dışı antenlerine çiftlenir. Modülasyon: Doğrusal olmayan bir bileşen sır ile taşıyıcıyı karıştırarak sırrı taşıyıcı frekansının yan bantlarına yukarı-çevirir. Emisyon: Cihazın istem dışı antenleri modüle edilmiş taşıyıcıyı havaya geri ışıtır.")*

### Aşama 3: Emisyon ve Geri Saçılım (Emission)
Modülasyona uğrayan sinyal artık düşük frekanslı değil, $f_c$ gibi yüksek bir RF frekansındadır. Cihazın kabloları ve PCB hatları bu frekansta verimli bir verici antene dönüştüğü için sinyali güçlü bir şekilde çevreye geri saçar (backscatter re-radiation).

### Aşama 4: Alım ve Üretken Yapay Zekâ ile Netleştirme
Saldırgan yönlü alıcı anten ve bir spektrum analizörü (örneğin Siglent SSA3075X Plus) kullanarak $f_c$ frekansındaki yan bantları yakalar ve standart AM demodülasyonu uygular.

Geri dönen seste donanım bozulmaları, intermodülasyon gürültüleri ve ortam parazitleri bulunacaktır. Araştırmacılar bu sinyali difüzyon tabanlı **SGMSE (Score-based Generative Model for Speech Enhancement)** mimarisiyle temizleyerek insan kulağının kusursuz anlayabileceği ve otomatik ses tanıma (ASR) sistemlerinin deşifre edebileceği kristal berraklığında ses kayıtlarına dönüştürmüştür.

---

## 3. Siber Güvenlik ve İstihbarat (SIGINT / TEMPEST / TSCM) Analizi

InjectEave, siber güvenlik ve teknik istihbarat doktrinleri açısından geleneksel tehdit modellemelerini altüst eden özelliklere sahiptir:

### A. Dijital Güvenlik Katmanlarının Mutlak İflası
InjectEave, işletim sistemi çekirdeğinden, şifreleme algoritmalarından ve ağ güvenlik protokollerinden tamamen bağımsız bir fiziksel katman saldırısıdır.
- İletişim ister Signal, ister TLS 1.3, ister askeri kriptolu telsiz protokolleriyle şifrelensin; veri DAC (Digital-to-Analog Converter) çipinden çıkıp operasyonel amplifikatör üzerinden kulaklık hoparlörüne veya ahizeye giderken artık analog elektrik akımıdır.
- Güvenli işlemci adacıkları (Secure Enclave, TPM, ARM TrustZone) veya sanallaştırma bariyerleri (Qubes OS, SE-Linux) analog çıkış hattındaki voltaj salınımlarını engelleyemez. Zafiyet yazılımda değil, atomların ve yarı iletkenlerin fiziksel doğrusalsızlığındadır.

### B. TEMPEST Doktrininin Boşa Çıkması
Klasik TEMPEST ve TSCM (Technical Surveillance Counter-Measures) protokolleri pasif ışıma kontrolü üzerine kuruludur. Kripto odalarında veya elçiliklerde (SCIF) cihazların dışarıya RF sızdırıp sızdırmadığı pasif spektrum tarayıcılarıyla ölçülür. Bir kulaklık veya sabit hat pasif durumdayken tamamen sessizdir (sıfır emisyon). Ancak InjectEave hedefe dışarıdan radyo dalgası enjekte ettiği anda, pasif kalkan standartlarını sağlayan cihaz bir anda aktif bir radyo vericisi haline gelir. Bu durum, pasif dinleme testlerinden tam not almış donanımların bile aktif radar/enjeksiyon taktikleriyle dinlenebileceğini ortaya koyar.

### C. Frekans ve Uzamsal Hedef Seçiciliği (Selectivity)
Bir salonda yan yana oturan birden fazla kişi varken saldırganın istediği hedefi izole edebilmesi istihbari operasyonlar için kritiktir. Makaledeki Demo 10, bu seçiciliği net biçimde sergiler:
- **Frekans Seçiciliği:** Yan yana duran Philips TAH2020 ve UGreen MAX2 kulaklıklarının iç empedans ve filtre yapıları farklı olduğundan, saldırgan sadece enjeksiyon frekansını birkaç megahertz kaydırarak bir hedeften diğerine anında geçiş yapabilmektedir.
- **Uzamsal Seçicilik:** Tamamen aynı model iki kulaklık kullanıldığında bile, yönlü antenin dar huzmesi (beamforming) sayesinde hedefler mekânsal olarak birbirinden ayrılabilmektedir.

### D. Ortam RF Parazitlerine Karşı Dayanıklılık (Robustness)
Makaledeki Demo 9'da, Wi-Fi erişim noktaları, Bluetooth (BLE) cihazları ve çok sayıda çalışan bilgisayarın bulunduğu yoğun elektromanyetik gürültüye sahip bir toplantı odasında test yapılmıştır. Enjekte edilen dar bantlı taşıyıcı sinyali, geniş bantlı dijital gürültü tabanının üzerinden ayrıştırılarak kararlı bir şekilde demodüle edilebilmiştir.

---

## 4. Başlıca Kullanım Alanları ve Saldırı Senaryoları

Araştırma makalesinde, ticari olarak raftan satın alınabilen (COTS) 11 farklı cihaz üzerinde ve hiçbir fiziksel müdahalede bulunulmaksızın gerçekleştirilen saha testleri paylaşılmıştır:

### 1. Otel ve Toplantı Odalarında Duvar Arkası Dinleme (Through-Wall)
Saldırgan hedef odanın bitişiğindeki odaya yerleşir. Araya giren **30 cm kalınlığındaki betonarme duvara** rağmen, 1 metre mesafeden kurbanın kulaklığında çalan sesler veya yaptığı görüşmeler dinlenmiştir. Araştırma ekibi, hedef kişinin banka kartı PIN kodunu ("9-5-2-7") ve transfer miktarını ("3,500 US dollars") fısıltıyla dinlerken bile sıfır hata ile deşifre etmiştir.

### 2. Uzun Menzilli Açık Alan Espiyonajı (30 Metreye Kadar)
Açık alanda, bir parkta veya kampüste çalılıkların arasına gizlenen bir saldırgan düzeneği, düşük maliyetli ticari bir RF güç yükseltici desteğiyle **6 metreden çalılık arkasından** ve açık görüş hattında **30 metre mesafeden** kablolu ve kablosuz kulaklıklardan ses verisini başarıyla çekmiştir.

### 3. Akıllı Ev Cihazlarından Bağlam ve Davranış Profili Çıkarma (Behavioral Profiling)
Ses sızıntısı tek tehdit değildir. Ev içi nesnelerin interneti (IoT) cihazlarının düşük frekanslı kontrol ve güç sinyalleri de aynı mekanizmayla sızdırılabilmektedir:
- **Akıllı Vantilatörler:** PWM (Darbe Genişlik Modülasyonu) kontrol sinyallerinin frekansı enjeksiyonla okunarak vantilatörün hız kademesi ve "Uyku Modu"na geçip geçmediği tespit edilmiş; böylece hedef şahsın uyuduğu kesinleştirilmiştir.
- **Akıllı Aydınlatmalar:** Lambanın parlaklık seviyesine bağlı güç tüketimi uzaktan izlenerek kullanıcının odada olup olmadığı, kitap okuma veya dinlenme moduna geçip geçmediği davranışsal bir profil olarak haritalanmıştır.

### 4. Kapalı Çevrim Konuşma Manipülasyonu (Closed-loop Eavesdrop-Synthesize-Inject)
Makaledeki en sarsıcı senaryolardan biri (Demo 7), sabit telefon hatları (landline) üzerinde kurgulanan kapalı çevrim saldırıdır:
1. **Dinleme (Eavesdrop):** Saldırgan telefon hattındaki analog görüşmeyi InjectEave ile gerçek zamanlı dinler.
2. **Sentezleme (Synthesize):** Görüşmede kritik bir onay veya teklif anı yakalandığında (örneğin "fiyat teklifini onaylıyor musunuz?"), IndexTTS-2 gibi gelişmiş ses klonlama modelleri kurbanın kendi ses tonu ve tınısıyla anında sahte bir onay cümlesi ("Evet, onaylıyorum") üretir.
3. **Enjeksiyon (Inject):** Üretilen sahte ses sinyali manyetik/RF enjeksiyon yoluyla ahize hattına basılarak karşı tarafa kurbanın ağzından çıkmış gibi iletilir. Bu senaryo, üst düzey diplomatik veya kurumsal telefon diplomasisini sabote edebilecek boyuttadır.

---

## 5. Nasıl Korunabiliriz? Savunma ve Karşı Tedbir Stratejileri

InjectEave karşısında geleneksel yazılımsal güvenlik yamaları çaresizdir. Savunma, donanım mimarisi ve radyo frekansı fiziği düzeyinde kurgulanmalıdır:

```
+-------------------------------------------------------------------------+
|                  İNJECTEAVE SAVUNMA VE SERTLEŞTİRME KATMANLARI          |
+-------------------------------------------------------------------------+
| 1. FİZİKSEL EKRANLAMA: Metal şasi, tam kapalı örgülü Faraday koruması   |
| 2. BÜKÜMLÜ ÇİFT (TWISTED-PAIR): Ortak modlu (common-mode) RF iptali     |
| 3. ANALOG RF FİLTRELEME: Op-amp ve ADC girişlerine ferrit boncuk & LC   |
| 4. TSCM & SPEKTRUM İZLEME: Ortamdaki şüpheli tek-tonlu RF sinyal tespiti|
+-------------------------------------------------------------------------+
```

### A. Donanımsal Ekranlama (Shielding)
Kulaklık kablolarının ve cihaz içi analog sinyal hatlarının yüksek yoğunluklu metal örgü (braided shield) ve folyo ile kaplanması gerekir. Ekranlama, dışarıdan gelen RF taşıyıcı dalganın iç iletken hatlara çiftlenmesini (coupling) önemli ölçüde zayıflatır.

### B. Bükümlü Çift (Twisted-Pair) ve Diferansiyel Sinyalleşme
Tek uçlu (single-ended) ses hatları yerine diferansiyel bükümlü çift hatların kullanılması hayati önem taşır. Enjekte edilen harici RF dalgası birbirine bükülmüş iki iletkene de eşit fazda (ortak mod - common mode) binecektir. Girişteki diferansiyel alıcı iki hat arasındaki farkı aldığında ($V_+ - V_-$), enjekte edilen RF bileşeni matematiksel olarak birbirini sıfırlar.

### C. Giriş/Çıkış Hatlarına RF Sönümleme Filtreleri Eklenmesi
Operasyonel amplifikatörlerin, ADC çiplerinin ve kulaklık jaklarının hemen dibine:
- **Ferrit Boncuklar (Ferrite Beads):** Yüksek frekanslı RF akımlarına karşı yüksek empedans göstererek RF enerjisini ısıya dönüştürüp sönümler.
- **Alçak Geçiren Filtreler (Low-Pass LC/RC Filters):** 20 kHz üzerindeki tüm RF frekanslarını doğrudan toprağa (GND) boşaltan kapasitör ve indüktör dizilimleri, sinyalin yarı iletkenin non-lineer bölgesine ulaşmasını engeller.

### D. Elektronik Karşı Tedbirler ve TSCM Spektrum İzleme
Kurumsal kriz merkezleri ve gizli toplantı odalarında (SCIF), oda spektrumunu sürekli dinleyen otomatik RF analiz sensörleri bulunmalıdır. InjectEave saldırısı tipik olarak dar bantlı, yüksek güçlü tek bir RF taşıyıcısı yayar. Bu tür olağan dışı taşıyıcı sinyalleri algılayan bir spektrum izleme sistemi anında alarm üreterek saldırıyı deşifre edebilir.

### E. Savunmanın Asimetrik Sınırları
Araştırma ekibinin FAQ bölümünde belirttiği gibi:

> *"InjectEave is immune to digital defenses such as encryption, masking, and randomization, because the leakage comes from the analog path. Hardware-aware mitigations such as twisted-pair wiring, shielding, and filtering can lower the energy that the injected carrier couples into the device, reducing the exposure. These mitigations raise the bar, but they do not guarantee immunity. Since injection-induced leakage grows with the injected power, a well-resourced adversary can often overcome them by transmitting at higher power."*
>
> *(Türkçe Çevirisi: "InjectEave şifreleme, maskeleme ve rastgeleleştirme gibi dijital savunmalara karşı bağışıktır, çünkü sızıntı analog yoldan kaynaklanır. Bükümlü çift kablolama, ekranlama ve filtreleme gibi donanım farkındalıklı önlemler enjekte edilen taşıyıcının cihaza çiftlediği enerjiyi düşürerek maruziyeti azaltabilir. Bu önlemler çıtayı yükseltir ancak mutlak bağışıklık garantisi vermez. Enjeksiyon kaynaklı sızıntı enjekte edilen güçle birlikte arttığından, yeterli kaynağa sahip bir saldırgan daha yüksek güçte iletim yaparak bu engelleri aşabilir.")*

---

## 6. Sonuç ve Değerlendirme

InjectEave, siber güvenlik dünyasına çok net bir uyarıda bulunmaktadır: Dijital dünyada kurduğumuz kusursuz şifreleme kuleleri, verinin fiziksel dünyayla temas ettiği analog sınırlarda ansızın yıkılabilir.

Donanım bileşenlerindeki non-lineerite (doğrusalsızlık), fizik kanunlarının bir sonucudur ve modern yarı iletkenlerden tamamen temizlenemez. Aktif elektromanyetik enjeksiyon ile bu zayıflığın birleştirilmesi, TEMPEST ve sinyal istihbaratı alanında yeni bir çağın kapısını aralamıştır. Kurumsal veri gizliliğini ve devlet düzeyindeki iletişimi korumak isteyen güvenlik mimarları; savunma stratejilerini yalnızca yazılım yamaları ve VPN tünelleriyle sınırlı tutamaz. Gerçek güvenlik, devre kartlarının tasarımından kabloların sarım geometrisine ve RF spektrum nöbetçilerine kadar uzanan bütüncül bir fiziksel donanım farkındalığı gerektirmektedir.

---

### Kaynakça

1. **Yan, H., Shao, Z., Zhang, S., Jiang, Q., & Long, Y.** (2026). *Injected and Leaked: Actively Inducing Side-Channel Leakage Using Electromagnetic Injection and Hardware Nonlinearity.* Proceedings of the 35th USENIX Security Symposium (USENIX Security '26), ss. 2485–2504.
2. **arXiv Ön Baskı Arşivi:** [arXiv:2609.04785v1 [cs.CR]](https://arxiv.org/abs/2609.04785v1)
3. **InjectEave Resmi Araştırma Portali:** [https://injecteave.github.io/](https://injecteave.github.io/)
4. **Araştırma Artefaktı ve SGMSE Kod Tabanı:** [Zenodo Kaydı (DOI: 10.5281/zenodo.18500378)](https://doi.org/10.5281/zenodo.18500378)
