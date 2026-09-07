---
title: "Esaretten Kurtul"
description: "Ekosistem Yalanı: Konforlu Bir Esaretin Anatomisi Teknoloji devleri bizlere 'her şeyin birbiriyle konuştuğu' kusursuz bir dünya vadediyor."
pubDate: "2026-05-05T08:39:00.001+03:00"
updatedDate: "2026-05-05T08:39:26.116+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/05/esaretten-kurtul.html"
---

## 1. Ekosistem Yalanı: Konforlu Bir Esaretin Anatomisi

Teknoloji devleri bizlere "her şeyin birbiriyle konuştuğu" kusursuz bir dünya vadediyor. Ancak bu vaat, bir noktadan sonra bir dayatmaya dönüşüyor. Apple’ın cihazları sadece kendi ekosisteminde "tam" çalışıyor; farklı bir markayı araya soktuğunuzda sistem sizi dışlıyor. Google, "bedava" servisleri karşılığında en mahrem verilerinizi, konumunuzu, alışkanlıklarınızı reklam verenlere satıyor.

**Neden Kaçtım?**-**Veri Madenciliği:** Biz kullanıcı değil, ürün haline geldik. Attığımız her adım, çektiğimiz her fotoğraf bir veri noktası olarak işleniyor.

-

**Planlı Eskitme ve Kısıtlama:** Donanım üzerinde tam yetkimiz yok. Mac kullanırken bir dosya sistemine veya çekirdek (kernel) seviyesine müdahale etmek neredeyse imkansız.

-

**Bağımlılık Döngüsü:** "Cloud" dedikleri şey aslında bir başkasının bilgisayarıdır. Fotoğraflarınızı iCloud’a yüklediğinizde, artık onlara sahip değil, sadece kira karşılığı erişiyor olursunuz.

Bu yüzden Mac'i bıraktım. Bu yüzden iPhone'dan **GrapheneOS**'e geçme planları yapıyorum. Ve bu yüzden evime bir kale inşa ettim.

---

## 2. Özgürlüğün Yeni Adresi: CachyOS ve Arch Linux Dünyası

Mac’in kısıtlı dünyasından sonra **CachyOS**'e geçmek, bir mühendis için karanlık bir odadan çıkıp ışığı görmek gibiydi. CachyOS, sadece bir işletim sistemi değil; performansın ve kontrolün en üst seviyeye taşındığı bir Arch Linux türevi.

-

**Neden CachyOS?**x86-64-v3 ve v4 optimizasyonları sayesinde**i5-14500** işlemcimin her çekirdeğinden, her döngüsünden tam verim alıyorum. Apple'ın size sunduğu "yeteri kadar performans" yerine, donanımın sınırlarını ben belirliyorum.

-

**Kontrol:** Paket yönetiminden masaüstü ortamına kadar her şey benim kontrolümde. Arka planda hangi servisin ne kadar veri gönderdiğini görebiliyorum. Gizlilik artık bir ayar değil, bir varsayılan.

---

## 3. Donanım Mimarisi: Verilerim Artık Evimde

Dijital bağımsızlığın fiziksel ayağı, verilerinizi başkasının sunucusundan alıp kendi diskinize koymaktır. i5-14500 tabanlı sunucum, bu bağımsızlığın kumanda merkezi.

-

**İşlemci Gücü:** i5-14500, 14 çekirdeği ile arka planda verileri şifrelerken ve ZFS dosya sistemini yönetirken asla daralıyor.

-

**Depolama (ZFS ve WD Red Plus):** Veri bütünlüğü için ZFS dosya sistemini ve WD Red Plus diskleri seçtim. Teknoloji devleri verilerinizi sildiğinde veya hesabınızı kapattığında her şey gider; ZFS ile verilerimin "bit çürümesine" (bit rot) karşı bile koruması bende.

-

**RAM ve Önbellek:**32GB DDR4 RAM ve**Samsung 990 Pro** SSD'ler, sistemin teknoloji devlerinin bulut servislerinden çok daha hızlı çalışmasını sağlıyor. ZFS'nin ARC yapısı, RAM'i bir sünger gibi kullanarak mekanik disklerin hantallığını tamamen ortadan kaldırıyor.

---

## 4. Mühendislik Çözümleri: Port Sınırlarını Aşmak

Anakartımın 4 SATA portuyla sınırlı olması, 5. diskimi dışarıda bıraktı. Kasanın 9 disk kapasitesi olsa da teknolojik kısıtlamalar her yerde karşımıza çıkıyor. Ancak burada "satın al ve kabullen" mantığı yok. Gelecekte ekleyeceğim **ASMedia** tabanlı bir PCIe-SATA genişletme kartı ile bu sınırı aşacağız. Bu, bir mühendisin problem çözme iradesidir; sistemin bize dayattığı sınırlara boyun eğmemektir.

---

## 5. Cloudflare Zero Trust: Dış Dünyaya Karşı Zırhlı Tünel

Sunucuyu eve kurmak yetmez, ona dışarıdan güvenle erişmek gerekir. Modemden port açmak, teknoloji devlerinin gözetleme sistemlerine veya bot saldırılarına kapıyı açmaktır. Ben ise **Cloudflare Tunnel**kullanarak evimi dijital bir hayalete dönüştürdüm.**Zero Trust ve OTP Katmanı:**
Cloudflare panelindeki anlık arayüz hatalarına rağmen (ki bu bile merkezi sistemlerin ne kadar kırılgan olduğunu gösteriyor), sunucumu zırhlandırdım:

-

**OTP (Tek Kullanımlık Kod):** Şifrelerim çalınsa bile kimse içeri giremez. Giriş için e-postama gelen o tek kullanımlık koda sahip olmaları gerekiyor.

-

**Wildcard (*) Stratejisi:** `*.ozdil.cloud` üzerinden tüm subdomainlerimi (servislerimi) tek bir kural setiyle korumaya aldım. Teknoloji devlerinin "biz sizin güvenliğinizi sağlarız" vaadini, kendi kurduğum profesyonel altyapı ile gerçeğe dönüştürdüm.

---

## 6. Sonuç: Neden Bu Zahmete Katlanıyoruz?

Birçok kişi soracaktır: "Apple veya Google varken neden bu kadar zahmet?" Cevap basit: **Haysiyet ve Bağımsızlık.**

Teknoloji devlerinin sunduğu "konfor", aslında bizim üzerimizdeki hakimiyetlerini pekiştirmek için kullandıkları bir uyuşturucudur. Verilerimizi kendi mülkiyetimize almak, kapalı kaynaklı yazılımların boyunduruğundan kurtulup CachyOS gibi şeffaf sistemlere geçmek, sadece teknik bir tercih değil, bir duruş sergilemektir.

Şu an sistemim tıkır tıkır işliyor. i5-14500 arka planda devasa GFX 100S dosyalarımı işlerken, ben Cloudflare tüneli üzerinden dünyanın her yerinden kendi kaleme güvenle erişiyorum. Ne Apple’ın kısıtlamaları, ne Google’ın takibi... Sadece ben ve kendi yönettiğim donanımım.

Dijital özgürlük bedava değildir; emek ve bilgi ister. Ama o kaleye ilk adımınızı attığınızda, harcadığınız her kuruşun ve her saniyenin karşılığını aldığınızı hissedeceksiniz.
