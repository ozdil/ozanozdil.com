---
title: "Quickshell İçin Dinamik Tema Motoru ve OLED Renk Yönetimi"
description: "Gerçek OLED siyahları, Catppuccin, Tokyo Night ve özel renk paletlerini Quickshell genelinde anında yeniden yüklemeden uygulama yöntemleri."
pubDate: 2026-09-06
heroImage: "/images/quickshell/quickshell-oled-themes.svg"
tags: ["quickshell", "temalar", "oled", "qml", "omarchy"]
draft: false
---

Masaüstü estetiğinde tema değişimi çoğunlukla yapılandırma dosyalarının düzenlenip uygulamanın yeniden başlatılmasını gerektirir. **Quickshell**, QML Singleton kalıbı ve dinamik özellik bağlama (*dynamic property binding*) sayesinde tüm masaüstünün renk şemasını tek bir komutla ve anında değiştirmeye imkan tanır.

Bu yazıda, özellikle **OLED (#000000)** paneller için optimize edilmiş yüksek kontrastlı temaların Quickshell'de nasıl yapılandırıldığını ve Omarchy tema motoruyla nasıl entegre edildiğini ele alıyoruz.

---

## 1. Global Tema Singleton'ı: `Theme.qml`

QML içerisinde `pragma Singleton` tanımlanmış bir dosya, tüm alt bileşenler tarafından doğrudan erişilebilir:

```qml
pragma Singleton
import QtQuick 2.15

QtObject {
    id: theme
    
    // Aktif tema adı
    property string current: "oled-black"
    
    // Dinamik renk paletleri
    property color background: current === "oled-black" ? "#000000" : "#0f141c"
    property color surface:    current === "oled-black" ? "#0a0a0a" : "#171d27"
    property color border:     current === "oled-black" ? "#222222" : "#2a3442"
    property color text:       "#f4f4f5"
    property color textMuted:  "#71717a"
    property color accent:     "#00ffcc"
    
    // Temayı anında değiştir
    function setTheme(name) {
        current = name;
    }
}
```

Tüm bar ve widget'lar `color: Theme.background` şeklinde tanımlandığı için, `Theme.setTheme("tokyo-night")` çağrıldığı anda tüm ekran yeniden başlatma gerekmeksizin yeni renklere bürünür.

---

## 2. Omarchy Resmi OLED Temaları

Omarchy ekosistemi için tasarladığımız ve Quickshell motoruyla kusursuz çalışan 4 temel OLED teması:

1. **Türkiye Teması:** Ay yıldız al kırmızısı (#e11d48) ve Akdeniz turkuazı (#00ffcc) dengesi.
2. **Steam Machine Edition:** Valve mirası mekanik turuncu (#f97316) ve Steam mavisi (#38bdf8).
3. **Ankara Teması:** Sıcak kehribar (#f59e0b) ve başkent laciverti (#1e3a8a).
4. **İstanbul Teması:** İznik çinisi turkuazı ve mercan kırmızısı (#fb7185).

Tüm bu temalar, OLED ekranlarda piksellerin tamamen kapanmasını sağlayarak hem güç tasarrufu sağlar hem de mutlak kontrast sunar.
