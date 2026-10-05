# Katkı ve Yayın Standartları (CONTRIBUTING)

Bu belge, ozanozdil.com bünyesindeki tüm blog makaleleri, dokümantasyonlar, açık kaynak duyuruları ve kod katkıları için geçerli yayın standartlarını belirler.

---

## 1. Türkçe Yazım ve Dilbilgisi Kuralları

- **Türk Dil Kurumu (TDK) Uyumu:** Tüm içerikler güncel TDK yazım kılavuzu ve dilbilgisi kurallarına eksiksiz uymak zorundadır.
- **Yazım ve Noktalama:**
  - Noktalama işaretlerinden sonra standart bir boşluk bırakılmalıdır.
  - Kesme işaretleri (`'`), bağlaç olan `de/da` ve `ki` yazımları, soru eki `mi/mı/mu/mü` ayrımları özenle yapılmalıdır.
  - Cümle yapıları açık, akıcı, düşük cümlelerden arındırılmış ve teknik olarak tutarlı olmalıdır.

---

## 2. Türkçe Terim Politikası ve Yabancı Kelime Kullanımı

- **Mümkün Olduğunca Türkçe Terimler:** İçeriklerde yabancı dildeki kavramlar yerine yerleşik veya önerilen Türkçe karşılıkları tercih edilmelidir.
- **Terim Dönüşüm Rehberi:**
  - *Pipeline* -> Dağıtım hattı / Süreç hattı
  - *Deploy / Deployment* -> Dağıtım / Yayına alma
  - *Repository / Repo* -> Depo / Kod deposu
  - *Commit* -> İşleme / Kayıt
  - *Branch* -> Dal
  - *Merge* -> Birleştirme
  - *Build* -> Derleme / İnşa
  - *Workflow* -> İş akışı
  - *Cache* -> Ön bellek
  - *Issue* -> Hata kaydı / Görev
  - *Feature* -> Özellik
  - *Bug / Fix* -> Yazılım hatası / Düzeltme
  - *Benchmark* -> Başarım ölçütü / Kıyaslama
  - *Dependency* -> Bağımlılık
  - *Runtime* -> Çalışma zamanı
  - *Framework* -> Çatı
  - *Frontend / Backend* -> Ön yüz / Arka yüz
  - *Hardware / Software* -> Donanım / Yazılım
- **Zorunlu Yabancı Kavramlar:** Özgün marka adları (Linux, Wayland, Slint, Rust, Astro, Cloudflare, Python vb.), komut adları (`git`, `npm`, `cargo`), kod değişkenleri veya teknik standart kodları (RFC, FIPS, NIST) olduğu gibi korunmalı; ancak cümle içindeki açıklamaları Türkçe yapılmalıdır.

---

## 3. Tipografi ve Yazı Tipi Standardı

- Sitedeki tüm arayüz bileşenleri, makale blokları, kod pencereleri ve panellerde varsayılan yazı tipi:
  `"JetBrainsMono Nerd Font, JetBrains Mono, monospace"` zinciridir.
- Sans-serif veya yabancı font tanımlamaları yapılmamalıdır.

---

## 4. Sıfır Emoji Politikası

- Makale başlıklarında, alt başlıklarda, metin gövdesinde, kod yorumlarında, commit mesajlarında ve sistem çıktılarında kesinlikle hiçbir unicode emoji kullanılmayacaktır.
- Vurgulamalar markdown biçimlendirmeleri (kalın, italik, alıntı blokları, uyarı kutuları) ile sağlanacaktır.

---

## 5. Makale Ön Bilgisi (Frontmatter) Şablonu

`src/content/blog/` dizinine eklenecek yeni makaleler için standart şablon:

```markdown
---
title: "Örnek Türkçe Makale Başlığı"
description: "Arama motorları ve sosyal ağlar için Türkçe ve öz açıklama."
pubDate: 2026-10-05
tags: ["linux", "acik-kaynak", "sistem-mimarisi"]
draft: false
---

Makale içeriği burada başlar...
```
