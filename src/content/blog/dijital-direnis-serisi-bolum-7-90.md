---
title: "Dijital Direniş Serisi - Bölüm 7: 90 Günlük Dijital Arınma Yol Haritası"
description: "'Büyük yolculuklar tek bir adımla başlar, ancak dijital bağımsızlık yolculuğu doğru sırayla atılan adımlarla tamamlanır."
pubDate: "2026-04-22T11:18:00.002+03:00"
updatedDate: "2026-04-22T11:18:15.243+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/04/dijital-direnis-serisi-bolum-7-90.html"
---

"Büyük yolculuklar tek bir adımla başlar, ancak dijital bağımsızlık yolculuğu doğru sırayla atılan adımlarla tamamlanır. İşte teoriyi pratiğe, bilgiyi eyleme dönüştürecek 90 günlük stratejik planınız."

## Giriş: Bilgiden Eyleme Geçiş

Buraya kadar okuduklarınız size gözetimin derinliğini ve direnişin imkanlarını gösterdi. Ancak dijital bağımsızlık bir gecede kazanılmaz. Bu son bölümde, hayatınızı Big Tech kuşatmasından aşama aşama nasıl kurtaracağınızı gösteren, 3 ana evreye ayrılmış bir uygulama planı sunuyoruz. Bu plan, teknik karmaşayı minimize ederek maksimum güvenliği hedeflemektedir.

## 1. Evre: İlk Savunma Hattı ve Veri Temizliği (1-30. Gün)

İlk ayın hedefi, veri sızıntısını durdurmak ve mevcut enkazı temizlemektir. Bu evre, büyük donanım yatırımları gerektirmez; sadece alışkanlık ve yazılım değişikliğine odaklanır.

- **Tarayıcı ve DNS Değişimi:**Chrome/Edge kullanımını bırakıp**LibreWolf**veya sertleştirilmiş**Firefox**'a geçin. DNS seviyesinde engelleme için cihazlarınıza **NextDNS**veya**ControlD** kurun.

- **Şifre Yöneticisi Geçişi:**Tüm şifrelerinizi tarayıcılardan silin ve bir şifre yöneticisine (Self-host yapana kadar Bitwarden Cloud veya yerel olarak KeePassXC) taşıyın.**2FA**(İki Faktörlü Doğrulama) için SMS yerine**Aegis**veya**Ente Auth** kullanmaya başlayın.

- **E-posta ve Arama Motoru:**Google/Bing yerine**DuckDuckGo**veya**SearXNG**kullanın. Hassas yazışmalar için**Proton Mail**veya**Tuta** gibi şifreli servislerde bir "köprü" hesap açın.

## 2. Evre: Kendi Kaleni İnşa Et (31-60. Gün)

Veri sızıntısını kontrol altına aldıktan sonra, mülkiyeti geri alma vaktidir. Bu evrede 3. bölümde detaylandırdığımız donanım mimarisi devreye girer.

### 2.1. Homelab Kurulumu ve İlk Servisler

Intel i5-14500 işlemcili sunucunuzu ayağa kaldırın ve sırasıyla şu servisleri **Docker** üzerinde yapılandırın:

1. **Vaultwarden:** Şifrelerinizi buluttan kendi sunucunuza taşıyın.

1. **Nextcloud:** Rehber, takvim ve dökümanlarınızı senkronize edin.

1. **Immich:** Fotoğraf yedeklemesini Google Photos'tan kendi diskinize yönlendirin.

1. **Pi-hole:** Tüm ev ağınızdaki reklam ve telemetriyi kesin.

## 3. Evre: Uç Nokta Güvenliği ve Tam Bağımsızlık (61-90. Gün)

Son evre, en yakınımızdaki casusları ehilleştirme ve dış dünyaya karşı görünmez olma evresidir.

### 3.1. Mobil ve Masaüstü Dönüşümü

- **GrapheneOS Geçişi:**Telefonunuza GrapheneOS yükleyin. Uygulamalarınızı**Aurora Store**(Play Store muadili anonim mağaza) ve**F-Droid** üzerinden yönetin.

- **Linux Masaüstü:**Ana bilgisayarınızda Windows'u tamamen silip (veya oyunlar için bir sanal makineye hapsedip)**Fedora KDE**veya**Debian** gibi özgür bir işletim sistemine geçin.

- **Uzak Erişim:**Sunucunuza dışarıdan erişmek için**Tailscale**veya**WireGuard** tünelinizi aktif edin.

## 4. Sürekli Bakım: Dijital Hijyen Disiplini

90 günü tamamladığınızda artık dijital dünyada "şeffaf bir kurban" değil, "görünmez bir aktör" olacaksınız. Ancak bu disiplini korumak için:

- Her ay sistem güncellemelerini (OS ve Docker imajları) kontrol edin.

- ZFS snapshot'larınızı ve off-site (başka bir lokasyona) yedeklerinizi periyodik olarak test edin.

- Yeni çıkan "akıllı" (IoT) cihazları yerel ağınıza almadan önce **No-Internet** VLAN'lerine hapsedin.

## Son Söz: Bir Yaşam Biçimi Olarak Mahremiyet

Bu makale serisi boyunca anlattıklarımız teknik birer tavsiyeden öte, bir duruş temsilidir. *"Saklayacak bir şeyim yok"* demekle *"Mahremiyet hakkım yok"* demek arasında fark yoktur. Bu 90 günlük planı tamamladığınızda, sadece teknik bir kurulum yapmış olmayacak; kendiniz, aileniz ve gelecek nesiller için özgür bir dijital sığınak inşa etmiş olacaksınız.

#### DİRENiŞİN TEKNiK ÖZETİ (CHEAT SHEET)

**İşlemci:**Intel i5-14500 (14 Cores)
**Sunucu OS:**Proxmox / Debian / TrueNAS
**Mobil OS:**GrapheneOS (Android Hardened)
**Haberleşme:**Signal / Matrix / SimpleX
**Dosya Sistemi:**ZFS (RAID-Z1 / Mirror)

"Kod yazmak, dünyayı değiştirmektir. Kendi kodunu çalıştırmak ise, dünyayı yönetmektir."

**Seri Sonu Kaynakçası ve Teşekkür:**

- PrivacyGuides.org Topluluğu

- GrapheneOS Geliştirici Ekibi

- Özgür Yazılım Derneği (ÖYD)

- Kendi sunucusunda özgürleşen tüm direnişçiler.
