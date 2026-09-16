---
title: "Omarchy Linux İçin NetRadar: Ultra Hızlı, Unprivileged Yerel Ağ Tarayıcısı ve Cihaz Radarı"
description: "Root yetkisine ihtiyaç duymadan, Linux çekirdeğinin unprivileged arayüzleri ve POSIX getnameinfo ile yerel ağı saniyeler içinde haritalayan, Quickshell ve Rust çekirdekli NetRadar eklentisinin çıkışı."
pubDate: 2026-09-16
heroImage: "/images/quickshell/netradar-preview.png"
tags: ["omarchy", "quickshell", "rust", "ağ-güvenliği", "açık-kaynak", "linux", "siber-savunma"]
---

Modern ev ve ofis ağlarında onlarca akıllı cihaz, telefon, tablet, televizyon, tek kart bilgisayar ve IoT ekipmanı aynı anda bağlı çalışıyor. Ancak çoğu Linux kullanıcısı için "Şu anda yerel ağımda hangi cihazlar var, ağ geçidim nerede ve bu cihazlar hangi donanım üreticilerine ait?" sorusuna yanıt bulmak genellikle zahmetli bir süreçtir.

Geleneksel olarak bu ihtiyaç için terminal açıp `sudo nmap -sn 192.168.1.0/24` veya benzeri ham paket (raw socket) oluşturan, `CAP_NET_RAW` gerektiren ve sistem yetkilerini zorlayan ağır CLI araçlarına başvurulur. Masaüstü ortamında, üst panelden (bar widget) tek tıkla ağ durumunu, bağlı cihaz sayısını, IP/MAC eşleşmelerini ve donanım üreticilerini anında sunan hafif, güvenli ve zarif bir çözüm eksikliği hissediliyordu.

Bu ihtiyacı karşılamak üzere, Omarchy Linux masaüstü ekosistemi için tasarladığımız **NetRadar** projesini duyurmaktan memnuniyet duyuyorum.

NetRadar; **Quickshell 4.0'ın akıcı Wayland arayüzü**, **Rust çekirdekli yüksek başarımlı motoru (`netradar-engine`)**, **sıfır root/unprivileged çalışma prensibi** ve **dahili IEEE OUI donanım üretici tespit veritabanı** ile yerel ağınızı tek tıkla görünür kılan modern bir masaüstü radarıdır.

---

## 1. Unprivileged (Rootsuz) Keşif Mimarisi

Bir ağ tarayıcısının masaüstü ortamında güvenle çalışabilmesi için en temel kural, sistemde herhangi bir yetki yükseltme (`sudo`, `pkexec`, `setuid` veya `CAP_NET_RAW`) gerektirmemesidir.

NetRadar, çekirdeğin unprivileged kullanıcı alanı arayüzlerinden azami derecede faydalanır:

* **Kernel Komşuluk Tablosu (`ip -j neigh` & `/proc/net/arp`):** Linux çekirdeğinin ağ arayüzleri üzerinden çözümlediği ARP ve komşuluk kayıtları JSON formatında ayrıştırılır.
* **Zararsız mDNS / UDP Tetiklemesi:** Ağdaki cihazların komşuluk tablosunda güncel kalmasını sağlamak için standart yerel çok noktaya yayın (5353 mDNS / 137 NetBIOS) portlarına unprivileged UDP paketleri gönderilerek çekirdeğin ARP çözümlemesi tetiklenir.
* **POSIX getnameinfo ile Güvenli Ters DNS:** Cihazların alan adları (hostname), libc düzeyinde `getnameinfo` ve yerel `/etc/hosts` önbelleği taranarak saniyeler içinde çözümlenir.

---

## 2. Dahili IEEE OUI Üretici Tespiti

Ağdaki cihazları yalnızca karmaşık IP (`192.168.1.42`) veya MAC (`AC:71:2E:...`) adresleriyle listelemek kullanıcı deneyimi açısından yetersizdir.

NetRadar, motor içerisine gömülü yüksek hızlı OUI (Organizationally Unique Identifier) önek tablosu barındırır:

* MAC adresinin ilk 3 baytını anında eşleştirerek cihazın üreticisini (Apple, Samsung, Intel, Google, Xiaomi, Huawei, Amazon, Raspberry Pi, Espressif IoT, TP-Link, MikroTik, Cisco, VMware vb.) tespit eder.
* Donanım türünü otomatik olarak kategorize eder: Yönlendirici (Router), Bilgisayar (PC), Akıllı Telefon (Phone), Nesnelerin İnterneti (IoT) veya Akıllı Televizyon (TV).
* Arayüz üzerinde kategoriye özel görsel ikonlar ve renk vurguları atar.

---

## 3. Beyaz Şapka Servis Yoklaması ve Hızlı Erişim

NetRadar, yalnızca pasif bir izleyici olmakla kalmaz, aynı zamanda yerel ağ yönetimini kolaylaştıran pratik özellikler sunar:

* **Canlı Gecikme (Ping) Probları:** Her cihaz için milisaniyelik gidiş-dönüş süresi (RTT) ölçülür ve erişilebilirlik durumu yeşil/turuncu göstergelerle sunulur.
* **Yönetim Servisleri Kontrolü:** Cihazların standart yönetim portları (80 HTTP, 443 HTTPS, 8080 WebUI, 22 SSH, 53 DNS, 445 SMB) 130 milisaniyelik kısa zaman aşımlı, müdahaleci olmayan TCP el sıkışmalarıyla yoklanır.
* **Tek Tıkla Web Arayüzü Açma:** Yönlendiriciniz veya modeminiz için doğrudan varsayılan tarayıcınızda web yönetim panelini açar.
* **Tek Tıkla SSH Başlatma:** Açık portu tespit edilen sunucu veya Raspberry Pi gibi cihazlara doğrudan `foot` terminali üzerinden SSH oturumu başlatır.
* **Wayland Pano Entegrasyonu:** IP veya MAC adresine tıklandığı anda `wl-copy` ile panoya aktarılır ve ekranda anlık bildirim gösterilir.

---

## 4. Güvenlik ve Savunma Standartları Uyumu

NetRadar, Omarchy Linux ve HANCORE-linux pazar yeri güvenlik mimarisine uygun olarak geliştirilmiştir:

1. **Alt Süreç İzolasyonu:** Tüm harici sistem komutları `cmd.process_group(0)` ile bağımsız süreç grubunda, temizlenmiş ortam değişkenleriyle (`PATH=/usr/bin:/bin`, `LC_ALL=C`) ve `O_NONBLOCK` boru okumalarıyla çalıştırılır.
2. **Sınırlı Arabellek ve Bellek Tavanı:** Süreç borusu okumaları 64 KiB tavan sınırla (`MAX_BUFFER_CAP = 64 * 1024`), kalıcı durum dosyaları ise 1 MiB tavan sınırla (`MAX_REGISTRY_FILE_SIZE = 1024 * 1024`) sınırlandırılmıştır. Bellek tüketimi ve DoS saldırıları engellenmiştir.
3. **Argüman Enjeksiyonu Savunması:** IP adresleri sıkı biçimde `Ipv4Addr` doğrulamasından geçirilir. `ping` ve `ssh` komutlarına bayrak manipülasyonunu engelleyen `--` argüman sonlandırıcısı iletilir.
4. **Özel Alt Ağ Sınırlandırması (CIDR Bounding):** Tarama ve port yoklama işlemleri kesin olarak RFC 1918 (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), RFC 3927 (link-local) ve geri döngü adresleriyle sınırlandırılmıştır. Kamusal internet adreslerine paket gönderimi engellenmiştir.
5. **Mode 0600 Atomik Depolama:** Cihaz takma adları (alias) ve güvenilen cihaz listesi, sembolik bağların (symlink) kesinlikle reddedildiği, `0700` izinli dizinlerde ve `0600` izinli dosyalarda `.tmp_*` üzerinden atomik olarak kaydedilir.
6. **XSS ve İşaretleme Koruması:** Quickshell/QML arayüzündeki tüm dinamik metinler `%100` oranında `textFormat: Text.PlainText` bildirimi ile işlenir.

---

## 5. Çift Modlu Kullanım

NetRadar iki farklı kullanım senaryosu için optimize edilmiştir:

* **Quickshell Top Bar Widget (`Panel.qml`):** Masaüstünün sağ üst barında aktif cihaz sayısını gösteren sayaç rozeti ve tıklandığında açılan hızlı radar menüsü.
* **Masaüstü Uygulaması (`netradar-dashboard`, `shell.qml`):** Kategori filtre çipleri (Tümü, Yönlendiriciler, Bilgisayarlar, Telefonlar, IoT), arama çubuğu ve anlık ağ trafiği (RX/TX hızları) göstergelerine sahip geniş kontrol paneli.

---

## 6. Kurulum ve Kullanım

### Kaynak Koddan Derleme

```bash
# Depoyu klonlayın
git clone https://github.com/ozdil/omarchy-netradar.git
cd omarchy-netradar

# Motoru derleyin
cargo build --release --locked

# İkili dosyaları kurun
install -Dm755 target/release/netradar-engine ~/.local/bin/netradar-engine
install -Dm755 netradar ~/.local/bin/netradar
install -Dm755 netradar-dashboard ~/.local/bin/netradar-dashboard
install -Dm755 netradar-status ~/.local/bin/netradar-status
install -Dm644 netradar.desktop ~/.local/share/applications/netradar.desktop
```

### CLI Kullanımı

```bash
# Tam JSON tarama çıktısı (otomasyon ve betikler için)
netradar-engine --scan

# Tek satır insan okunabilir durum özeti
netradar-status

# Belirli bir cihazın gecikmesini ölçme
netradar-engine --ping 192.168.1.1

# Bir cihaza kalıcı takma ad (alias) atama
netradar-engine --set-alias "AC:71:2E:95:48:56" "Ana Ofis Router"

# Grafiksel kontrol panelini başlatma
netradar
```

---

## Açık Kaynak Bağlantıları

* **GitHub Deposu:** [ozdil/omarchy-netradar](https://github.com/ozdil/omarchy-netradar)
* **Lisans:** MIT Lisansı
* **Geliştirici:** Ozan Özdil
