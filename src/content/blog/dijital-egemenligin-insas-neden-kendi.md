---
title: "Dijital Egemenliğin İnşası: Neden Kendi Kalemizi Kurmalıyız?"
description: "Dijital Gözetim Toplumu ve Veri Sömürgeciliği Shoshana Zuboff, Gözetim Kapitalizmi Çağı adlı eserinde, insan deneyiminin bedelsiz bir şekilde 'davranışsal ve..."
pubDate: "2026-04-28T09:10:00.003+03:00"
updatedDate: "2026-04-28T09:10:21.567+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/04/dijital-egemenligin-insas-neden-kendi.html"
---

## 1. Dijital Gözetim Toplumu ve Veri Sömürgeciliği

Shoshana Zuboff, *Gözetim Kapitalizmi Çağı* adlı eserinde, insan deneyiminin bedelsiz bir şekilde "davranışsal veri" olarak ele geçirilip ticari amaçlarla kullanıldığını savunur. Ücretsiz olarak sunulan bulut depolama servisleri, aslında verilerimizin işlenmesi karşılığında bize sunulan birer "altın kafes"tir.

Kendi sunucumu kurma kararımın temelinde, bu veri sömürgeciliğine karşı bir duruş sergilemek yatıyor. **Jonsbo N6**kasa içerisine konumlandırdığım**Intel i5-14500** işlemcili sistem, sadece bir depolama birimi değil; verinin işlenme sürecini (data processing) merkezi otoritelerden koparıp bireysel alana taşıyan bir özgürlük aracıdır.

---

## 2. Donanım Mimarisi: Güven ve Performansın Senfonisi

Bir dijital kalenin sağlamlığı, en zayıf halkası kadardır. Bu yüzden bileşen seçiminde hem dayanıklılığı (durability) hem de veri bütünlüğünü (data integrity) ön planda tuttum.

### Depolama ve Hata Toleransı

Sistemde kullandığım 5 adet **WD Red Plus**disk, geleneksel disklerin aksine 7/24 çalışma prensibine uygun, hata düzeltme algoritmalarıyla donatılmış profesyonel ünitelerdir. Bu diskleri**TrueNAS**işletim sistemi üzerinde**ZFS (Zettabyte File System)** yapısında kurguladım.

*ZFS, sadece bir dosya sistemi değil, verinin bozulmasını (bit rot) kendi kendine teşhis edip düzeltebilen bir mimaridir. İki adet **Samsung 990 Pro SSD** ise "Read Cache" (L2ARC) ve "Write Log" (ZIL) görevlerini üstlenerek, ağ üzerindeki dosya erişim hızını fiziksel sınırların ötesine taşımaktadır.*

### Güç ve Esneklik

**Intel 14500** işlemci, 14 çekirdekli yapısıyla aynı anda hem ailemin medya sunucusu (Nextcloud) görevini üstleniyor hem de arka planda sanallaştırma katmanlarını yönetiyor. Bu, donanımın sadece pasif bir depo değil, aktif bir hesaplama merkezi (computing hub) olduğu anlamına geliyor.

---

## 3. Yazılım Katmanı: TrueNAS, Nextcloud ve Dijital Özerklik

Yazılım tercihimdeki temel kriter, **açık kaynak kodlu (Open Source)** olmasıydı. Kapalı devre sistemlerin arka kapılar (backdoor) barındırma riski, "güvenlik" kavramıyla çelişir.

-

**Nextcloud:** Bu platform, sadece bir dosya paylaşım aracı değil; takvimden notlara, rehberden fotoğraf yedeklemeye kadar Google ve Apple ekosistemine olan bağımlılığımızı sıfırlayan bir "Collaboration Suite"dir. Tüm aile üyelerim, verilerinin dünyanın neresinde, hangi disk sektöründe yazılı olduğunu bilmenin huzuruyla bu bulutu kullanıyor.

-

**Ollama ve Yerel Yapay Zeka:**Günümüzde yapay zeka (AI) kullanımı kaçınılmazdır. Ancak sorgularımızı buluta göndermek, düşüncelerimizi bir veri bankasına teslim etmektir.**Ollama** entegrasyonu ile LLM (Large Language Models) yapılarını kendi işlemcim üzerinde koşturuyorum. Bu, "Veri Gizliliği 2.0" dönemidir; yapay zeka ile konuşurken verilerim evimin duvarları dışına çıkmıyor.

---

## 4. Ağ Güvenliği: OPNsense ve Dijital Filtreleme

Kalenin kapısı, yani internet çıkışı, en büyük risk alanıdır. Bu riski yönetmek için **Techstorm Mini PC**üzerinde**OPNsense** yapılandırmasını hayata geçirdim.

Standart bir modem, sadece trafiği yönlendirir; ancak OPNsense, trafiği analiz eder. Kurduğum bu sistem sayesinde:

-

**DNS Düzeyinde Engelleme:** Reklam ve takip (tracking) ağları daha bilgisayarlarımıza ulaşmadan engelleniyor.

-

**Intrusion Detection System (IDS):** Dışarıdan gelebilecek olası saldırıları gerçek zamanlı olarak saptıyor.

-

**Deep Packet Inspection (DPI):** Veri paketlerinin içeriği analiz edilerek, zararlı yazılımların ev ağına sızması engelleniyor.

İnternet eve girdiği anda bu filtreden geçer. Bu, evdeki her cihazın (akıllı TV'den telefonlara kadar) ek bir yazılıma ihtiyaç duymadan "temiz internet" kullanması demektir.

---

## 5. Geleceği Korumak: Çocuklarımızı Dijital Dünyada Nasıl Savunuruz?

Bir ebeveyn olarak en büyük sorumluluğumuz, çocuklarımızı dijital dünyanın vahşi dinamiklerinden korumaktır. Algoritmalar, çocukların dikkat sürelerini sömürmek ve onları tüketim odaklı profillere dönüştürmek üzerine tasarlanmıştır.

### Algoritma Esaretinden Kurtuluş

YouTube veya Instagram gibi platformların öneri algoritmaları, çocukları manipülasyona açık hale getirir. Kendi sunucumda barındırdığım içerikler ve kontrol ettiğim erişim ağları sayesinde, çocuklarım "tüketilecek bir veri" değil, "öğrenen bir birey" olarak internetle tanışıyor.

### Dijital Ayak İzi Yönetimi

Çocuklarımızın fotoğraflarını ticari bulut servislerine yüklemek, onlara ait biyometrik verileri ve çocukluk anılarını daha onlar reşit olmadan şirketlerin eline teslim etmektir. **ozanozdil.com** altyapısındaki kişisel sunucumda:

1.

Çocuklarımın fotoğrafları asla yüz tanıma algoritmalarıyla işlenip reklam hedeflemesi için kullanılmaz.

1.

Zararlı içeriklere erişim, OPNsense üzerindeki filtrelerle (kategorik bazlı engelleme) merkezi olarak yönetilir.

1.

Onlara kendi dosyalarını yönetme sorumluluğu vererek, dijital okuryazarlığı "mülkiyet bilinciyle" öğrenmeleri sağlanır.

---

## Sonuç: Neden Şimdi?

Edward Snowden’ın dediği gibi: *"Gizlilik hakkını savunmamak, söyleyecek bir şeyim yok diyerek ifade özgürlüğünü savunmamak gibidir."*

Kişisel sunucu kurmak, sadece teknik bir kurulum değil, bir yaşam biçimidir. **Jonsbo N6**, **TrueNAS**, **OPNsense**ve**Ollama** bir araya gelerek benim dijital kalemimi oluşturuyor. Bu kale, ailemin mahremiyetini koruyan, çocuklarımı algoritma saldırılarından savunan ve verilerimin gerçek mülkiyetini bana veren tek yoldur.

Kendi verinizin efendisi olmadığınız bir dünyada, hürriyetinizden söz edemezsiniz. Bu yüzden, herkesin küçük ya da büyük, kendi dijital kalesini inşa etmeye başlaması gerektiğine inanıyorum.

---

*Bu yazı, ozanozdil.com altyapısında barındırılan ve yerel sunucumda hazırlanan bir makaledir.*
