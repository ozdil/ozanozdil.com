---
title: "Xiaomi, Poco ve Redmi'de Reklamları ve Gereksiz Uygulamaları Güvenle Kaldırma Rehberi (HyperOS / MIUI, Root'suz)"
description: "Xiaomi, Poco ve Redmi telefonlarda root veya bootloader kilidi açmadan reklamları kapatma ve gereksiz sistem uygulamalarını ADB ile güvenle kaldırma rehberi. Adım adım yöntem, güvenli ve riskli paket listesi, geri alma komutu."
pubDate: 2026-10-05
tags: ["xiaomi", "poco", "redmi", "hyperos", "miui", "adb", "debloat", "reklam-engelleme", "android", "gizlilik"]
---

**Kısa cevap:** Xiaomi, Poco ve Redmi telefonlarda reklamları ve gereksiz uygulamaları, **root yapmadan, bootloader kilidini açmadan ve garantiyi bozmadan** kaldırabilirsiniz. Yöntem iki katmanlıdır: (1) ayarlardan reklam ve öneri servislerini kapatmak, (2) ADB ile gereksiz sistem uygulamalarını yalnızca **mevcut kullanıcı için** (`--user 0`) kaldırmak. Bu işlem sistem bölümünü değiştirmez, her paket tek komutla geri getirilebilir.

Bu rehber HyperOS (Xiaomi 13 ve sonrası, Redmi Note 13 ve sonrası, Poco F6/X6 ve sonrası) ile MIUI 12-14 çalıştıran cihazlar için geçerlidir. Komutlar Linux, macOS ve Windows'ta aynıdır.

---

## İçindekiler

1. Neden Xiaomi cihazlarda reklam var?
2. Başlamadan önce: yedek ve güvenlik kuralları
3. Adım 1: Ayarlardan reklam ve öneri servislerini kapatma
4. Adım 2: ADB kurulumu ve telefonu hazırlama
5. Adım 3: Paketleri listeleme ve kaldırma
6. Güvenle kaldırılabilen paketler
7. Asla kaldırılmaması gereken paketler
8. Bir paketi geri getirme
9. Sık karşılaşılan sorunlar
10. Sık sorulan sorular

---

## 1. Neden Xiaomi cihazlarda reklam var?

Xiaomi donanımı düşük kâr marjıyla satar; gelirin bir kısmı yazılım içi reklam ve öneri servislerinden gelir. Bu servisler özellikle şu bileşenlerde görünür:

- **MSA (MIUI System Ads):** Sistem uygulamalarına reklam sağlayan servis (`com.miui.msa.global`, Çin sürümlerinde `com.miui.systemAdSolution`).
- **Mi Analytics:** Kullanım telemetrisi toplayan servis (`com.miui.analytics`).
- **Güvenlik, Temalar, Müzik, Dosya Yöneticisi, Mi Tarayıcı, GetApps:** İçlerinde öneri kartı ve reklam bulunan sistem uygulamaları.
- **Bildirim önerileri:** "Önerilen uygulamalar" ve kampanya bildirimleri.

Bölgeye (Global, Türkiye, Çin, Hindistan) ve ROM sürümüne göre reklamın yoğunluğu değişir. Türkiye için global ROM kullanılır.

## 2. Başlamadan önce: yedek ve güvenlik kuralları

> **Önemli:** ADB ile kaldırma işlemi yanlış pakette cihazı açılış döngüsüne sokabilir. Aşağıdaki kuralları uygulayın.

1. **Yedek alın.** Ayarlar > Hakkında > Yedekle ve geri yükle (veya Mi Cloud / Google Yedekleme) ile verilerinizi yedekleyin.
2. **Önce kapatın, sonra kaldırın.** Bir uygulamayı kaldırmak yerine önce `pm disable-user` ile devre dışı bırakıp birkaç gün deneyin.
3. **Paketleri tek tek kaldırın.** Toplu listeyi bir betikle körlemesine çalıştırmayın.
4. **Sistem çekirdeği paketlerine dokunmayın** (7. bölüme bakın).
5. **Yalnızca `--user 0` kullanın.** Bu bayrak uygulamayı sistem bölümünden silmez, yalnızca ana kullanıcı için gizler. Fabrika ayarlarına dönüşte paketler geri gelir.
6. Kaldırmadan önce paket adını **internetteki rastgele listelerden değil, cihazınızdan** doğrulayın (`pm list packages`).

## 3. Adım 1: Ayarlardan reklam ve öneri servislerini kapatma

ADB'den önce bu ayarları yapın. Çoğu reklam burada kapanır ve hiçbir risk taşımaz.

**Kişiselleştirilmiş reklamlar ve MSA**
1. Ayarlar > Şifreler ve güvenlik > Gizlilik > **Reklam hizmetleri** > *Kişiselleştirilmiş reklam önerileri* seçeneğini kapatın.
2. Ayarlar > Şifreler ve güvenlik > Gizlilik > **Yetkilendirme ve iptal** > **msa** iznini iptal edin (geri sayımı bekleyin).

**Uygulama bazlı öneriler**
- **Güvenlik uygulaması:** Ayarlar (sağ üst dişli) > *Önerileri al* ve *Reklamları al* seçeneklerini kapatın.
- **Temalar:** Ayarlar > *Önerileri göster* kapalı olsun.
- **Müzik / Video / Dosya Yöneticisi:** Her birinin ayarlarında *Önerileri göster* ve *Kişiselleştirilmiş öneriler* kapatılır.
- **Mi Tarayıcı:** Ayarlar > *Gelişmiş* > *Önerileri göster* kapatılır (veya uygulama devre dışı bırakılır).
- **Klasör önerileri:** Ana ekranda bir klasör açın, klasör adına dokunun ve *Önerilen uygulamaları göster* seçeneğini kapatın.
- **GetApps (Mi Picks):** Ayarlar > Uygulamalar > İzinler bölümünden bildirimleri kapatın.

**Telemetri**
- Ayarlar > Şifreler ve güvenlik > Gizlilik > **Kullanım ve tanılama** kapatılır.
- Aynı bölümde **Kullanıcı deneyimi programı** kapatılır.

## 4. Adım 2: ADB kurulumu ve telefonu hazırlama

ADB (Android Debug Bridge), Google'ın resmi Android Platform Tools paketinin parçasıdır.

**Bilgisayarda kurulum**

```bash
# Arch / Omarchy
sudo pacman -S android-tools

# Debian / Ubuntu
sudo apt install adb

# macOS (Homebrew)
brew install android-platform-tools
```

Windows'ta [developer.android.com/tools/releases/platform-tools](https://developer.android.com/tools/releases/platform-tools) adresinden resmi paketi indirip açın.

**Telefonda geliştirici seçeneklerini açma**
1. Ayarlar > Telefon hakkında > **OS sürümü** (MIUI'de *MIUI sürümü*) satırına 7 kez dokunun.
2. Ayarlar > Ek ayarlar > Geliştirici seçenekleri > **USB hata ayıklama** seçeneğini açın.
3. Telefonu USB ile bağlayın, bildirimdeki *Dosya aktarımı* modunu seçin.
4. Çıkan "USB hata ayıklamaya izin ver" penceresinde bilgisayarın parmak izini kontrol edip onaylayın.

> **Not:** Paket kaldırma için "USB hata ayıklama (Güvenlik ayarları)" seçeneği **gerekmez**; bu seçenek yalnızca ADB ile dokunma simülasyonu içindir. Gereksiz izin vermeyin ve işiniz bitince USB hata ayıklamayı kapatın.

**Bağlantıyı doğrulama**

```bash
adb devices
```

Çıktıda cihaz seri numarasının yanında `device` yazmalıdır. `unauthorized` yazıyorsa telefondaki izin penceresini onaylayın.

## 5. Adım 3: Paketleri listeleme ve kaldırma

**Cihazdaki tüm paketleri listeleme**

```bash
# Tüm paketler
adb shell pm list packages

# Yalnızca sistem paketleri
adb shell pm list packages -s

# Belirli bir marka veya kelime
adb shell pm list packages | grep -i miui
```

**Paketi ana kullanıcıdan kaldırma (önerilen yöntem)**

```bash
adb shell pm uninstall -k --user 0 <paket.adi>
```

`-k` bayrağı veri ve önbelleği korur, `--user 0` ise yalnızca ana kullanıcı için kaldırır. Başarılı olursa `Success` çıktısı verir.

**Önce devre dışı bırakma (daha güvenli)**

```bash
adb shell pm disable-user --user 0 <paket.adi>
```

Bu komut paketi kaldırmaz, yalnızca durdurur. Sorun çıkarsa tek komutla açılır:

```bash
adb shell pm enable <paket.adi>
```

**Örnek: Mi Analytics'i kaldırma**

```bash
adb shell pm uninstall -k --user 0 com.miui.analytics
```

**Hata mesajları**
- `Failure [DELETE_FAILED_INTERNAL_ERROR]`: Paket adı yanlış veya zaten kaldırılmış.
- `Failure [DELETE_FAILED_DEVICE_POLICY_MANAGER]`: Paket cihaz yönetimi tarafından korunuyor; devre dışı bırakmayı deneyin.
- `java.lang.SecurityException: ... requires android.permission.DELETE_PACKAGES`: Bazı HyperOS sürümlerinde yalnızca `pm disable-user` kullanılabilir.

## 6. Güvenle kaldırılabilen paketler

Aşağıdaki paketler yaygın olarak kaldırılır ve sistemi bozmaz. **Paket adları ROM ve bölgeye göre değişir**; yalnızca cihazınızda listelenenleri işleme alın.

| Paket adı | Uygulama / servis | Not |
|---|---|---|
| `com.miui.analytics` | Mi Analytics | Telemetri |
| `com.miui.msa.global` | MSA (sistem reklamları) | Global ROM; Çin: `com.miui.systemAdSolution` |
| `com.miui.bugreport` | Hata raporu | Telemetri |
| `com.xiaomi.mipicks` | GetApps | Uygulama mağazası ve reklam |
| `com.mi.globalbrowser` | Mi Tarayıcı | Başka tarayıcı kullanıyorsanız |
| `com.miui.player` | Mi Müzik | Öneri ve reklam içerir |
| `com.miui.videoplayer` | Mi Video | Öneri ve reklam içerir |
| `com.miui.yellowpage` | Yellow Pages / Mi Rehber servisi | Arayan kimlik reklamları |
| `com.miui.hybrid` | Hızlı uygulamalar | Kullanılmıyorsa |
| `com.xiaomi.glgm` | Oyun Merkezi (Games) | Kullanılmıyorsa |
| `com.facebook.appmanager` | Facebook App Manager | Ön yüklü |
| `com.facebook.services` | Facebook Services | Ön yüklü |
| `com.facebook.system` | Facebook System | Ön yüklü |
| `com.netflix.partner.activation` | Netflix aktivasyonu | Ön yüklü |
| `com.miui.cleaner` | Temizleyici | Yalnızca ayrı bir temizleme aracı kullanıyorsanız |
| `com.miui.notes` | Mi Notlar | Başka not uygulaması kullanıyorsanız |

> **İpucu:** Bir paketin ne olduğundan emin değilseniz önce `disable-user` ile durdurun, bir hafta kullanın, sorun yoksa kaldırın.

## 7. Asla kaldırılmaması gereken paketler

Aşağıdaki paketler arayüzün, güvenliğin ve donanım yönetiminin parçasıdır. Kaldırmak veya devre dışı bırakmak **açılış döngüsüne, kilit ekranı hatasına veya performans kaybına** yol açabilir.

| Paket adı | Neden kaldırılmamalı |
|---|---|
| `com.miui.home` | Ana ekran (launcher); kaldırılırsa arayüz açılmaz |
| `com.android.systemui` | Durum çubuğu, bildirimler, kilit ekranı |
| `com.miui.securitycenter` | Güvenlik ve izin yönetimi; birçok sistem özelliği buna bağlı |
| `com.xiaomi.joyose` | Termal ve performans yönetimi; kaldırmak oyun ve ısı davranışını bozabilir |
| `com.miui.powerkeeper` | Pil ve arka plan yönetimi |
| `com.android.phone`, `com.android.providers.*` | Arama, SMS, kişiler, veri sağlayıcıları |
| `com.miui.system`, `com.android.settings` | Çekirdek sistem ve ayarlar |
| `com.google.android.gms` | Google Play Hizmetleri; bildirimler ve birçok uygulama bağımlı |
| `com.xiaomi.finddevice` / `com.miui.cloudservice` | Cihazımı bul ve bulut senkronizasyonu; hesap tabanlı güvenlik |
| `com.android.vending` | Google Play Store |

> **Uyarı:** `com.xiaomi.joyose` internette sık "gereksiz telemetri" olarak önerilir. Ancak termal ve performans profillerini yönetir. Kaldırmadan önce yan etkilerini araştırın; önerimiz **dokunmamaktır**.

## 8. Bir paketi geri getirme

Yanlışlıkla kaldırdığınız bir paketi fabrika ayarına dönmeden geri yükleyebilirsiniz:

```bash
adb shell cmd package install-existing <paket.adi>
```

Alternatif eski yöntem:

```bash
adb shell pm install-existing --user 0 <paket.adi>
```

Telefon açılmıyorsa Recovery'den *Önbelleği sil* (Wipe cache) deneyin; veri silmez. Bu da işe yaramazsa fabrika ayarına dönüş, `--user 0` ile kaldırılan tüm sistem paketlerini geri getirir.

## 9. Sık karşılaşılan sorunlar

**Güncellemeden sonra uygulamalar geri geldi.**
Sistem güncellemeleri (OTA) bazen kaldırılan paketleri mevcut kullanıcı için yeniden etkinleştirir. Kaldırma komutlarını bir betik dosyasına kaydedip güncellemeden sonra yeniden çalıştırın.

**`adb devices` boş görünüyor.**
Kabloyu değiştirin, *Dosya aktarımı* modunu seçin, geliştirici seçeneklerinde *USB yapılandırması* bölümünü kontrol edin, Linux'ta `udev` kurallarının yüklü olduğundan emin olun.

**Reklamlar kaldırmadan sonra da görünüyor.**
Ayarlardaki kişiselleştirilmiş reklam seçeneğinin kapalı olduğunu, MSA iznini iptal ettiğinizi ve ilgili uygulamaların kendi öneri ayarlarını kapattığınızı kontrol edin. Tarayıcı ve üçüncü taraf uygulama reklamları sistem seviyesinde kaldırılamaz.

**Garanti ve güvenlik güncellemeleri etkilenir mi?**
Hayır. Bootloader kilidi açılmadığı, root yapılmadığı ve sistem bölümü değiştirilmediği için garanti, SafetyNet / Play Integrity ve bankacılık uygulamaları etkilenmez.

## 10. Sık sorulan sorular

### Xiaomi telefonlarda reklamları tamamen kapatabilir miyim?
Sistem reklamlarının büyük bölümünü kapatabilirsiniz. Ayarlardan kişiselleştirilmiş reklamları ve MSA iznini kapatmak, ardından ADB ile MSA ve Analytics paketlerini kaldırmak sistem genelindeki reklamları büyük ölçüde ortadan kaldırır. Üçüncü taraf uygulamalardaki reklamlar bu yöntemle kaldırılmaz.

### Root veya bootloader kilidi açmak gerekir mi?
Hayır. `adb shell pm uninstall -k --user 0` komutu root gerektirmez ve bootloader kilidini açmaya gerek yoktur.

### Bu işlem garantiyi bozar mı?
Hayır. Sistem bölümünü değiştirmez ve cihaz yazılımını kalıcı olarak değiştirmez. Fabrika ayarına dönüş her şeyi eski haline getirir.

### Kaldırdığım uygulamayı nasıl geri getiririm?
`adb shell cmd package install-existing <paket.adi>` komutunu çalıştırın.

### HyperOS ile MIUI arasında fark var mı?
Yöntem aynıdır. Bazı paket adları ve ayar menü konumları değişebilir; paketleri her zaman `pm list packages` ile doğrulayın.

### Hangi paketlere kesinlikle dokunmamalıyım?
`com.miui.home`, `com.android.systemui`, `com.miui.securitycenter`, `com.xiaomi.joyose`, `com.miui.powerkeeper`, `com.google.android.gms` ve telefon/SMS sağlayıcıları. Bunlar sistemin çalışması için gereklidir.

### Bu yöntem Poco ve Redmi cihazlarda da çalışır mı?
Evet. Poco, Redmi ve Xiaomi aynı MIUI / HyperOS tabanını kullanır. Poco cihazlarda ek olarak Poco Launcher paketlerine dikkat edin; launcher kaldırmadan önce alternatif bir ana ekran kurun.

### Aynı işlem için ADB'ye alternatif var mı?
Telefondan çalışan Shizuku tabanlı araçlar da aynı `pm` komutlarını kullanır, ancak yetkiyi üçüncü taraf bir uygulamaya verdiğiniz için bilgisayardan resmi ADB kullanmak daha şeffaf ve güvenlidir.

---

## Özet işlem sırası

1. Yedek alın.
2. Ayarlardan kişiselleştirilmiş reklamları, MSA iznini, kullanım ve tanılama ile uygulama içi önerileri kapatın.
3. Android Platform Tools kurun, USB hata ayıklamayı açın, `adb devices` ile bağlantıyı doğrulayın.
4. `adb shell pm list packages` ile cihazdaki gerçek paket adlarını görün.
5. Önce `pm disable-user --user 0`, sorun yoksa `pm uninstall -k --user 0` uygulayın.
6. Çekirdek paketlere (6. ve 7. bölümdeki tablolar) dokunmayın.
7. Sorun olursa `cmd package install-existing` ile geri getirin.
8. İşiniz bitince USB hata ayıklamayı kapatın.

*Bu rehber, cihaz üreticisinin resmi Android araçlarını kullanır ve yazılımı kalıcı olarak değiştirmez. Paket adları ROM sürümüne göre farklılık gösterebilir; işlem sorumluluğu kullanıcıdadır. Son güncelleme: 05/10/2026.*

<script type="application/ld+json">{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": "Xiaomi telefonlarda reklamları tamamen kapatabilir miyim?", "acceptedAnswer": {"@type": "Answer", "text": "Sistem reklamlarının büyük bölümünü kapatabilirsiniz. Ayarlardan kişiselleştirilmiş reklamları ve MSA iznini kapatıp ADB ile MSA ve Analytics paketlerini kaldırmak sistem genelindeki reklamları büyük ölçüde ortadan kaldırır. Üçüncü taraf uygulama reklamları bu yöntemle kaldırılmaz."}}, {"@type": "Question", "name": "Root veya bootloader kilidi açmak gerekir mi?", "acceptedAnswer": {"@type": "Answer", "text": "Hayır. adb shell pm uninstall -k --user 0 komutu root gerektirmez ve bootloader kilidini açmaya gerek yoktur."}}, {"@type": "Question", "name": "Bu işlem garantiyi bozar mı?", "acceptedAnswer": {"@type": "Answer", "text": "Hayır. Sistem bölümü değiştirilmez; fabrika ayarına dönüş tüm kaldırılan paketleri geri getirir."}}, {"@type": "Question", "name": "Kaldırdığım uygulamayı nasıl geri getiririm?", "acceptedAnswer": {"@type": "Answer", "text": "adb shell cmd package install-existing <paket.adi> komutunu çalıştırın."}}, {"@type": "Question", "name": "Hangi paketlere kesinlikle dokunmamalıyım?", "acceptedAnswer": {"@type": "Answer", "text": "com.miui.home, com.android.systemui, com.miui.securitycenter, com.xiaomi.joyose, com.miui.powerkeeper, com.google.android.gms ve telefon/SMS sağlayıcıları sistemin çalışması için gereklidir."}}]}</script>
