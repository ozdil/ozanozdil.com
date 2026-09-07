# 🐺 ozanozdil.com

> **Ozan Özdil (@ozdil)** — Kişisel Marka, Blog ve Dijital Karargâh Altyapısı.  
> GitHub arayüzünden ilham alan, minimalist, ultra hızlı ve modern Astro + Tailwind CSS mimarisi.

🌐 **Canlı Site:** [ozanozdil.com](https://ozanozdil.com)  
⚡ **Barındırma & CDN:** Cloudflare Pages  
🛠️ **Teknoloji:** Astro v5 + Tailwind CSS + TypeScript + Markdown  
📈 **SEO & Performans:** 100/100 Google PageSpeed, Dahili RSS ve Sitemap  

---

## 📂 Proje Yapısı

```text
├── public/
│   └── avatar.jpg                 # Profil görseli
├── src/
│   ├── components/                # GitHub arayüz bileşenleri (Header, Footer, ProfileSidebar, vb.)
│   ├── content/
│   │   ├── config.ts              # Tip güvenli içerik şeması (Zod)
│   │   └── blog/                  # Markdown (.md) formatında makaleler ve yazılar
│   ├── layouts/
│   │   └── BaseLayout.astro       # Evrensel layout ve SEO meta etiketleri
│   ├── pages/
│   │   ├── index.astro            # Overview / Pinned projeler & profil
│   │   ├── hakkimda.astro         # README.md detaylı özgeçmiş
│   │   ├── projeler.astro         # Repositories (Açık kaynak araçlar)
│   │   ├── rss.xml.ts             # Otomatik RSS beslemesi
│   │   └── blog/
│   │       ├── index.astro        # Yazılar listesi
│   │       └── [...slug].astro    # Makale detay sayfası
│   └── styles/
│       └── global.css             # GitHub Dark/Light tasarım değişkenleri
├── astro.config.mjs               # Astro & Cloudflare/Sitemap yapılandırması
├── tailwind.config.mjs            # GitHub renk paleti ve tipografi
└── package.json
```

---

## ✍️ Yeni Blog Yazısı Nasıl Eklenir?

Yeni bir yazı yayınlamak için tek yapmanız gereken `src/content/blog/` klasörünün altına yeni bir Markdown (`.md`) dosyası oluşturmaktır:

```markdown
---
title: "Yazının Başlığı"
description: "Arama motorlarında ve kartlarda görünecek kısa açıklama."
pubDate: 2026-09-07
tags: ["linux", "siber-güvenlik", "yapay-zeka"]
---

Yazınızın içeriğini buraya Markdown formatında yazabilirsiniz...
```

Dosyayı ekleyip depoya push ettiğinizde, Cloudflare Pages **10-15 saniye içinde** siteyi otomatik olarak derleyip canlıya alır.

---

## 💻 Yerel Geliştirme (Local Development)

```bash
# Bağımlılıkları yükleyin
npm install

# Geliştirme sunucusunu başlatın (http://localhost:4321)
npm run dev

# Üretim derlemesi oluşturun
npm run build

# Derlemeyi önizleyin
npm run preview
```

---

## ☁️ Cloudflare Pages Bağlantısı

1. Cloudflare Dashboard'da **Compute (Workers & Pages)** > **Create application** > **Pages** > **Connect to Git** seçin.
2. `ozdil/ozanozdil.com` deposunu seçin.
3. Derleme ayarları:
   - **Framework preset:** `Astro`
   - **Build command:** `npm run build`
   - **Build output directory:** `dist`
4. **Custom domain** kısmından `ozanozdil.com` alan adınızı ekleyin.
