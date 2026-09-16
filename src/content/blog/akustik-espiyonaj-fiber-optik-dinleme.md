---
title: "Akustik Espiyonaj: Fiber Optik Dinleme"
description: "Telekom Fiber Optik Kablolar ile Akustik Dinleme (COAES) Saldırısının Bilimsel AnaliziModern fiber optik iletişim ağlarının, veri iletimi için kullandığımız ..."
pubDate: "2026-06-01T21:17:36.667+03:00"
updatedDate: "2026-06-01T21:21:36.128+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/06/akustik-espiyonaj-fiber-optik-dinleme.html"
---

**Telekom Fiber Optik Kablolar ile Akustik Dinleme (COAES) Saldırısının Bilimsel Analizi**Modern fiber optik iletişim ağlarının, veri iletimi için kullandığımız bu kabloların aynı zamanda istenmeyen birer "mikrofon dizisi" olarak işlev görebileceğini gösteren yeni bir siber güvenlik tehdidi ortaya çıktı. Bu tehdit, 2026 yılında düzenlenen**NDSS (Network and Distributed System Security) Sempozyumu'** nda kamuoyuna duyuruldu. İşte bu yeni ve gizli tehdidin bilimsel bir incelemesi:

## Çalışma Prensibi: Akustik-Yan Kanal

Saldırının temelinde, optik fiberlerin dış ortamdaki ses dalgalarına karşı olan doğal hassasiyeti yatar. Ses dalgaları, fiber optik kabloya çarptığında, oluşturdukları **mikroskobik basınç dalgalanmaları**, fiberin geometrisinde "**micro-bending**" adı verilen fiziksel deformasyonlara neden olur. Bu micro-bendingler, fiberin içinde yol alan ışığın **refraktif indeksini** (kırılma indisi) ve optik yol uzunluğunu anlık olarak değiştirir.

Saldırganlar, fiberin bir ucuna bağladıkları ticari bir **Distributed Acoustic Sensing (DAS)** sistemi ile lazer darbeleri göndererek geri yansıyan **Rayleigh saçılımı** sinyallerini analiz eder ve bu faz kaymalarından orijinal ses dalgasını yeniden oluşturur.

## Hassasiyeti Artırma Yöntemi: Bobinleme

Standart bir FTTH (Evlere Kadar Fiber) kablosu, havadaki sesi algılayacak kadar hassas değildir. Hassasiyeti artırmak için araştırmacılar, bir **"Duyusal Reseptör" (Sensory Receptor)** adı verilen bir düzenek geliştirmiştir.

Bu düzenek, kablonun fazla kısmının **65 mm çapında PET (polietilen tereftalat) bir silindir etrafına sıkıca sarılması** (bobin yapılması) prensibine dayanır. Bu sarım, gelen akustik basıncı fiber üzerinde yoğunlaştırarak **mekanik-optik dönüşüm verimliliğini** büyük ölçüde artırır.

## Saldırının Performansı ve Sonuçları

Bu sistem, kontrollü laboratuvar ve gerçek ofis ortamlarında test edilmiş, şaşırtıcı sonuçlar elde edilmiştir:

- **Yüksek Başarı Oranı:** 2 metre mesafeden yapılan testlerde, **Kelime Hata Oranı (Word Error Rate - WER)** %20'nin altında kalmıştır. Bu, yapay zeka konuşma tanıma modellerinin, konuşulan içeriğin %80'inden fazlasını başarıyla metne dökebildiği anlamına gelir.

- **Hassas Konum Belirleme:** Sistem, bir odadaki konuşmacının konumunu ortalama **77 cm** hata payı ile tespit edebilmiştir.

- **Gerçek Dünya Senaryosu:** Ofis ortamında 50 metrelik bir kablo hattı üzerinde yapılan testte ise WER, **sadece %9** gibi neredeyse kusursuz bir seviyeye inmiştir.

## Konvansiyonel Tespit Yöntemlerinden Kaçış

Bu saldırıyı özellikle tehlikeli kılan şey, "gizli" doğasıdır. Sistem pasif bir şekilde çalıştığı için, geleneksel güvenlik ve gözetleme karşı önlemlerinden (TSCM) büyük ölçüde etkilenmez:

- **RF Dedektörlerinden Gizlenme:** Saldırı, hiçbir elektromanyetik radyasyon (RF) yaymadığı için, ortamda gizli böcek dinleme cihazlarını tarayan RF tarayıcıları bu tehdidi göremez.

- **Ultrasonik Jammer'lara Bağışıklık:** Ortamdaki gizli mikrofonları etkisiz hale getirmek için kullanılan ultrasonik karıştırıcılar (jammer), bu sisteme hiçbir etki edemez. Fiberin kendisi, bir mikrofona ihtiyaç duymayan dev bir sensördür. Yapılan testlerde, jammer fiberin hemen yanına konulduğunda dahi sistemin performansında herhangi bir düşüş gözlemlenmemiştir.

## Bilimsel Temel ve Laboratuvar Kanıtları

Bu saldırının arkasındaki fiziksel prensip, fiber optik sensör teknolojisinin temel taşlarından birine dayanır. Yapılan bir laboratuvar deneyinde, hoparlörden çalınan bir gitar müziğinin, yanında bulunan uzun fiber optik makaralar (spool) üzerinde ölçülebilir **Polarizasyon Durumu (State of Polarization - SoP)** değişimlerine neden olduğu gözlemlenmiştir.

Bu tespit edilebilir SoP değişimleri, sesin fiber içinde yol açtığı çift kırılma (birefringence) etkisinin doğrudan bir sonucudur ve saldırının fizibilitesini kanıtlamaktadır.

---

## Saldırı Vektörü ve Etki Raporu

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
    <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
      COAES (Covert Acoustic Eavesdropping Attack) Parametreleri
    </div>
    <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">NDSS 2026 Sempozyumu</span>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs mb-4">
    <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50">
      <span class="text-[10px] font-bold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">Fiziksel Dönüşüm Hattı</span>
      <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-1 mb-2">Akustik Yan-Kanal</div>
      <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">Akustik Dalga -> Micro-bending -> Refraktif İndeks Değişimi -> Rayleigh Saçılımı -> Sinyal Çatımı</p>
    </div>

    <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50">
      <span class="text-[10px] font-bold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">Duyusal Reseptör (Bobinleme)</span>
      <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-1 mb-2">PET Silindir (65mm)</div>
      <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">15 metre fiber kablo silindir üzerine sarılarak akustik basınç yoğunlaştırılır ve mekanik-optik verim zirveye çıkarılır.</p>
    </div>
  </div>

  <div class="grid grid-cols-1 sm:grid-cols-3 gap-3 font-mono text-xs">
    <div class="p-3 rounded-xl border border-emerald-300 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20">
      <div class="text-[#78716c] text-[10px]">TESPİT EDİLEBİLİRLİK</div>
      <div class="font-bold text-emerald-700 dark:text-emerald-400 mt-0.5">Sıfır RF Emisyonu</div>
      <div class="text-[10px] text-[#5c4033] dark:text-[#a8a29e] mt-1">Jammer'lara tam bağışıklık</div>
    </div>
    <div class="p-3 rounded-xl border border-sky-200 dark:border-sky-900/40 bg-sky-50/40 dark:bg-sky-950/20">
      <div class="text-[#78716c] text-[10px]">DİNLEME MENZİLİ</div>
      <div class="font-bold text-sky-700 dark:text-sky-400 mt-0.5">50 Metre Hat</div>
      <div class="text-[10px] text-[#5c4033] dark:text-[#a8a29e] mt-1">77 cm konum hassasiyeti</div>
    </div>
    <div class="p-3 rounded-xl border border-amber-200 dark:border-amber-900/40 bg-amber-50/40 dark:bg-amber-950/20">
      <div class="text-[#78716c] text-[10px]">DOĞRULUK ORANI</div>
      <div class="font-bold text-amber-800 dark:text-amber-400 mt-0.5">%91 Transkripsiyon</div>
      <div class="text-[10px] text-[#5c4033] dark:text-[#a8a29e] mt-1">WER sadece %9</div>
    </div>
  </div>
</div>

Bu bulgular, sadece siber güvenlik duvarlarının değil, fiziksel katman güvenliğinin ve hatta ofis içi akustik mahremiyetin de yeniden tanımlanması gerektiğini göstermektedir.
