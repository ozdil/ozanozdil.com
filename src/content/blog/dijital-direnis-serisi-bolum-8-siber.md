---
title: "Dijital Direniş Serisi - Bölüm 8: Siber Gerilla Taktikleri ve İleri Seviye Görünmezlik"
description: "'En iyi savunma, orada olduğunuzun bile bilinmemesidir. Dijital dünyada hayalet olmak, sistemin sizi kategorize etme yeteneğini elinden almaktır."
pubDate: "2026-04-22T11:20:00.000+03:00"
updatedDate: "2026-04-22T11:20:42.239+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/04/dijital-direnis-serisi-bolum-8-siber.html"
---

"En iyi savunma, orada olduğunuzun bile bilinmemesidir. Dijital dünyada hayalet olmak, sistemin sizi kategorize etme yeteneğini elinden almaktır."

## Giriş: Pasif Savunmadan Aktif Görünmezliğe

Buraya kadar olan bölümlerde verilerimizi korumayı öğrendik. Ancak ileri seviye bir "direnişçi" için veri korumak yetmez; verinin üretim sürecinde kimliğin saptırılması gerekir. Bu bölümde, algoritmaların bizi tanımasını imkansız kılan **Obfuscation** (Yanıltma) tekniklerini ve siber gerilla taktiklerini teknik katmanlarıyla ele alacağız.

## 1. Ağ Seviyesinde Maskeleme: VPN ve Tor Köprüleri

İnternet servis sağlayıcınız (ISS), hangi sitelere girdiğinizi metadata üzerinden görebilir. Standart bir VPN bu veriyi sadece ISS'den saklar, ancak VPN sağlayıcınıza teslim eder.

### 1.1. Multi-Hop ve Onion Routing

Siber gerilla, tek bir noktaya güvenmez. **Multi-hop VPN**kullanarak trafiğinizi önce bir ülkeden, sonra başka bir ülkeden çıkararak takip edilmeyi teknik olarak imkansızlaştırır. Daha da ileri aşamada,**Tor Project**'in "meek_lite" veya "obfs4" gibi köprülerini (bridges) kullanarak, trafiğinizi sıradan bir HTTPS trafiği gibi gösterip derin paket inceleme (DPI) cihazlarını atlatabilirsiniz.

## 2. Dijital Kimlik Saptırma (Identity Obfuscation)

Algoritmalar sizi e-posta adresiniz veya telefon numaranızla değil, bu verilerin oluşturduğu "ilişki haritası" ile tanır. Bu haritayı bozmak için **Alias (Takma Ad)** mimarisi şarttır.

### 2.1. E-Posta ve Telefon Maskeleme

- **SimpleLogin / Addy.io:** Her servis için farklı bir e-posta alias'ı oluşturun. Eğer bir servis verilerinizi sızdırırsa veya spam gönderirse, sadece o alias'ı kapatarak dijital kimliğinizin geri kalanını koruyabilirsiniz.

- **VOIP ve Brülör Numaralar:** Kayıt olduğunuz servislerde gerçek telefon numaranızı kullanmak yerine, sanal (VOIP) numaralar kullanarak fiziksel SIM kartınızla dijital kimliğiniz arasındaki bağı koparın.

## 3. Dosya ve Metadata Temizliği (ExifStripper)

Kendi sunucunuzda (Nextcloud/Immich) saklasanız bile, internete yüklediğiniz bir fotoğrafın içine gömülü olan **EXIF** verileri (GPS koordinatları, kamera seri numarası, çekim saati) sizi ele verir.

- **Metadata Scrubbing:** Dosyalarınızı paylaşmadan önce *ExifTool* veya *Metadata Cleaner* gibi araçlarla temizlemek, dijital parmak izinizi silmenin temel kuralıdır.

## 4. Yerel Şifreleme: "At-Rest" Veri Güvenliği

Sunucunuzun (Homelab) fiziksel olarak ele geçirilmesi ihtimaline karşı, disklerinizin sadece ZFS ile korunması yetmez. **LUKS (Linux Unified Key Setup)**veya**VeraCrypt** kullanarak disklerinizi donanım seviyesinde şifrelemelisiniz. Sunucu her açıldığında şifreyi manuel (veya güvenli bir anahtar sunucusu üzerinden) girmeden verilerin okunması imkansız olmalıdır.

## 5. Sosyal Mühendisliğe Karşı Bölümlendirme (Compartmentalization)

En büyük açık her zaman insandır. Siber gerilla taktiği, dijital hayatı birbirinden tamamen bağımsız kompartımanlara ayırmayı gerektirir.

- **Resmi Hayat:** Devlet işleri ve bankacılık için ayrı bir tarayıcı profili / ayrı bir VM.

- **Sosyal Hayat:** Takma isimli sosyal medya hesapları için tamamen farklı bir ağ (VPN çıkışı) ve tarayıcı.

- **Teknik Hayat:** Geliştirme ve araştırmalar için izole, telemetrisi kapatılmış bir çevre.

## Sonuç: Sürekli Tetikte Kalmak

Görünmezlik bir yazılım yüklemekle biten bir durum değil, bir yaşam biçimidir. Algoritmalar her gün daha akıllı hale gelirken, bizim de taktiklerimizi güncellememiz gerekir. Unutmayın; siber dünyada en güvenli profil, hakkında veri toplanan değil, toplanan verilerin birbirine bağlanamadığı profildir.

#### 8. Bölüm Teknik Terimler Sözlüğü:

- **Obfuscation:** Veriyi anlaşılmaz veya yanıltıcı hale getirme.

- **Multi-hop:** Trafiğin birden fazla sunucu üzerinden aktarılması.

- **DPI (Deep Packet Inspection):** Paketlerin içeriğinin derinlemesine incelenmesi.

- **EXIF:** Fotoğrafların içine gömülü teknik üst veriler.

- **LUKS:** Linux için standart disk şifreleme katmanı.

- **Alias:** Gerçek kimliği gizleyen takma isim/adres.

- **Compartmentalization:** Sistemlerin birbirinden tamamen izole edilmesi.

- **Onion Routing:**Verinin katmanlı şifreleme ile iletilmesi (Tor).**Kaynakça:**

- The Art of Invisibility by Kevin Mitnick.

- Whonix OS Documentation (Advanced Anonymity).

- Tor Project: Bridges and Pluggable Transports.

- Electronic Frontier Foundation (EFF) Surveillance Self-Defense Guide.
