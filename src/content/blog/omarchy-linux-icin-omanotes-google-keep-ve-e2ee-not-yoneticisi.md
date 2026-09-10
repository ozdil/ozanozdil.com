---
title: "Omarchy Linux İçin OmaNotes: Google Keep Tarzında, Zero-Knowledge E2EE Not ve Görev Yöneticisi"
description: "Tamamen Quickshell arayüzlü, Rust motorlu, klavyesiz (mouse-first) kullanımlı ve Google Drive ile Git'e uçtan uca şifreli (AES-256-GCM) yedekleme sunan OmaNotes'un mimarisi ve çıkışı."
pubDate: 2026-09-10
heroImage: "/images/quickshell/omanotes-preview.png"
tags: ["omarchy", "quickshell", "rust", "e2ee", "siber-güvenlik", "açık-kaynak", "verimlilik", "google-keep"]
---

Linux masaüstünde günlük akış esnasında aklımıza gelen bir fikri, linki veya yapılacaklar listesini hızla not almak çoğu zaman iki uç nokta arasında sıkışır: Ya büyük teknoloji şirketlerinin tüm verilerimizi tarayıp yapay zeka modellerini eğittiği tescilli bulut not uygulamalarına teslim oluruz ya da metin tabanlı, grafiksel arayüz zarafetinden uzak, yavaş çalışan yerel araçlarla yetinmek zorunda kalırız.

Bu ikilemi ortadan kaldırmak amacıyla, Omarchy Linux masaüstü ekosistemi için tasarladığımız **OmaNotes**'u duyurmaktan mutluluk duyuyorum.

OmaNotes; **Google Keep tarzında renkli kartlar ve to-do listesi ergonomisini**, **Quickshell 4.0'ın akıcı Wayland arayüzü**, **Rust çekirdekli sistem motoru** ve **Zero-Knowledge AES-256-GCM uçtan uca şifreleme (E2EE)** mimarisiyle birleştiren bağımsız, açık kaynaklı bir masaüstü eklentisidir.

---

## 🎯 Klavyesiz (Mouse & Touch-First) Ergonomi

OmaNotes, günlük kullanımda klavyeye hiç dokunmadan masaüstünün sağ üst barından tek tıkla yönetilebilecek şekilde kurgulandı:

1. **📋 Panodan Tek Tıkla Not Oluşturma:** Panoya kopyaladığınız herhangi bir metin, link veya görev listesini yazma zahmetine girmeden tek tıkla karta dönüştüren `Paste from Clipboard` butonu (`wl-paste` entegrasyonu).
2. **➕ Hazır Hızlı Şablonlar:**
   * `🛒 Groceries` (Örnek maddelerle hazır alışveriş listesi)
   * `📅 Priorities` (Günlük öncelikler ve odak görevleri)
   * `💡 Idea` (Fikir karalama şablonu)
3. **🎨 Canlı Filtre Çipleri (Zero Typing):** Not aramak için arama çubuğuna yazmak yerine; `All`, `📌 Pinned`, `󰄲 Checklist` ve pastel renk noktalarına (`🟡`, `🟢`, `🔵`, `🟣`, `🔴`, `🪨`) tıklayarak kartları anında filtreleme.
4. **🖱️ Kart Üzeri Hızlı Aksiyonlar:** Tek tıkla onay kutusu işaretleme (üstü çizilir), alt paletten tek tıkla kart rengini değiştirme, sabitleme (`󰤱`), çoğaltma/kopya (`󰆏`) ve güvenli silme (`󰅖`).

---

## 🔒 Sıfır Bilgi Uçtan Uca Şifreleme (Zero-Knowledge E2EE)

OmaNotes'un kalbinde, verilerinize sizden başka kimsenin (bulut sağlayıcısı dahil) erişemeyeceğini garanti eden matematiksel bir şifreleme katmanı bulunur:

* **Kriptografik Anahtar Türetimi:** Belirleyeceğiniz ana parola, **PBKDF2-HMAC-SHA256** standardı üzerinden 10.000 iterasyon ve 16-baytlık kriptografik rastgele tuz (salt) ile 256-bit şifreleme anahtarına dönüştürülür.
* **AES-256-GCM Kimlik Doğrulamalı Şifreleme (AEAD):** Her şifreleme işleminde 12-baytlık tek seferlik rastgele nonce üretilir. Veriler şifrelenirken aynı zamanda kimlik doğrulama etiketi (auth tag) üretilerek bulutta bayt seviyesinde kurcalamalara (bit-flipping saldırıları) karşı tam koruma sağlanır.
* **Sıfır Düz Metin Sızıntısı:** Bulut kasasına aktarılan `notes.enc` paketinde hiçbir başlık, içerik veya etiket şifresiz (plaintext) olarak bulunmaz.

---

## ☁️ Çoklu Bulut Yedekleme & Disaster Recovery

Notlarınızı ister Google Drive'da, ister kendi özel Git deponuzda tutun:

* **Google Drive / Nextcloud / WebDAV (`rclone`):** Sistemdeki rclone uzak bağlantıları üzerinden tek tıkla şifreli senkronizasyon.
* **Özel Git Kasası (`git`):** Şifrelenmiş `notes.enc` dosyasını kendi özel Git deponuza `git commit & push` ile versiyonlayarak yedekleme.
* **Afet Kurtarma (`--pull`):** Bilgisayarınızı formatlasanız veya yeni bir cihaza geçseniz bile, tek tıkla buluttan şifreli paketi indirip ana parolanızla tüm kartlarınızı saniyeler içinde geri yükleyebilirsiniz.

---

## 🛡️ Güvenlik Mimarisi & Omarcom Standartları (`AGENTS.md`)

OmaNotes, Omarchy Linux ekosisteminin resmi güvenlik yönergelerine (`AGENTS.md`) istisnasız tam uyum sağlayacak biçimde inşa edildi:

| Güvenlik Alanı | Uygulanan Mimari Kural |
| :--- | :--- |
| **İzole Süreç Grupları** | Alt süreçler bağımsız süreç grubunda (`cmd.process_group(0)`) çalıştırılır. |
| **Non-Blocking I/O** | `O_NONBLOCK` + POSIX `poll()` ile borular kilitlenmeden okunur. |
| **Monotonic Deadlines** | 30 saniyelik mutlak zaman aşımı denetimi ile donmalar engellenir. |
| **Koşulsuz SIGKILL** | Zaman aşımında SIGTERM -> 5ms -> SIGKILL ile arka planda torun süreç bırakılmaz. |
| **0600 / 0700 Atomik Yazım** | Dosyalar `.tmp_*` üzerinden yazılıp `sync_all` sonrasında atomik `rename` ile `0600` izinleriyle taşınır; symlink'ler reddedilir. |
| **Düz Metin Güvencesi** | QML tarafındaki tüm kullanıcı ve pano metinlerinde `textFormat: Text.PlainText` zorunlu tutularak XSS/HTML enjeksiyonu engellenmiştir. |

---

## 🧪 15/15 Otomatik Test Paketi

OmaNotes, Rust test altyapısı altında **15 farklı birim, güvenlik, stres ve kaos testinin tamamından** tam not almıştır:

* **Birim Testleri (5/5):** 0600 atomik depolama, buffer overrun engelleme, monotonic deadline, kripto round-trip, yanlış parola reddi.
* **İleri Düzey Güvenlik & Kaos Testleri (6/6):**
  1. *Bit-Flipping Testi:* Şifreli pakette tek bir bayt tahrif edildiğinde AEAD doğrulamasının veriyi reddetmesi.
  2. *Shell Injection & Fuzzing:* Not başlığına `; rm -rf / ; touch /tmp/pwned` gibi komutlar enjekte edildiğinde sistem komutlarının engellenmesi.
  3. *Bozuk Dosya Kurtarma:* `notes.json` içine yarım kesik JSON yazılarak ani güç kesintisinin simüle edilmesi ve motorun çökmeden kendini onarması.
  4. *Stres Testi:* 1.000 adet notun < 50ms içinde taranması ve 64 KB büyük veri aktarımı.
  5. *Eşzamanlılık:* 10 ayrı iş parçacığının aynı anda not eklemesi ve yarış durumu oluşmaması.
  6. *Ağ Kesintisi:* Ulaşılamayan Git/rclone hedeflerinde askıda kalmadan temiz hata dönülmesi.
* **Entegrasyon Testleri (4/4):** Symlink saldırı reddi, inatçı torun süreç temizliği, CLI dayanıklılığı, uçtan uca Git bulut döngüsü.

---

## 🚀 Kurulum ve Kullanım

Omarchy Linux kurulu sisteminizde tek bir komutla depoyu ekleyip kullanmaya başlayabilirsiniz:

```bash
# 1. Eklentiyi sisteme ekleyin
omarchy plugin add https://github.com/ozdil/omarchy-omanotes.git

# 2. Güvenli kaynaktan yerel derlemeyi yapın
cd ~/.config/omarchy/plugins/ozdil.omanotes
cargo build --release --locked
install -m 755 target/release/omanotes-engine ./omanotes-engine

# 3. Omarchy barınıza ekleyin (~/.config/omarchy/shell.json içine)
# "bar.layout.right" altına: { "id": "ozdil.omanotes" }

# 4. Shell'i yenileyin
omarchy-restart-shell
```

Terminalden hızlı durum kontrolü için:
```bash
~/.config/omarchy/plugins/ozdil.omanotes/omanotes-status
```

---

### 🔗 Bağlantılar ve Kaynak Kod
* **GitHub Deposu:** [ozdil/omarchy-omanotes](https://github.com/ozdil/omarchy-omanotes)
* **Lisans:** MIT Lisansı
* **Küratör & Standart:** Omarchy Linux (`AGENTS.md`) & HANCORE Plugin Marketplace Baseline
