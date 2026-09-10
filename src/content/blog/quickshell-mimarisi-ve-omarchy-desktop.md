---
title: "Quickshell Mimarisi: Modern Wayland Masaüstünün Temeli"
description: "C++ ve Qt/QML tabanlı Quickshell'in tek süreçli masaüstü kabuğu mimarisi, Hyprland entegrasyonu ve sıfır gecikmeli arayüz tasarımı."
pubDate: 2026-09-09
heroImage: "/images/quickshell/quickshell-architecture.svg"
tags: ["quickshell", "omarchy", "wayland", "qml", "mimari"]
draft: false
---

Linux masaüstü ortamları uzun yıllar boyunca parçalı, birbirleriyle sürekli IPC soketleri üzerinden haberleşmeye çalışan çok sayıda bağımsız süreçten (daemon) oluştu. Üst panel için ayrı bir süreç, bildirimler için ayrı bir daemon, ses ve parlaklık OSD göstergeleri için başka bir araç, kilit ekranı için ise bambaşka bir ikili dosya... Bu yapı yalnızca gereksiz bellek tüketimine yol açmakla kalmıyor; arayüz elemanları arasında görsel tutarsızlıklara ve gecikmelere neden oluyordu.

**Quickshell**, bu paradigmayı kökten değiştirerek tüm masaüstü kabuğunu tek bir uzun ömürlü, C++ çekirdekli ve QML deklaratif arayüzlü süreç altında topluyor. **Omarchy** masaüstünün merkezinde yer alan Quickshell mimarisi, modern Wayland protokollerini doğrudan konuşarak masaüstünü tamamen şekillendirilebilir (*malleable*) bir çalışma alanına dönüştürüyor.

---

## 1. Neden Tek Süreçli (Single-Process) Mimari?

Geleneksel Wayland masaüstlerinde panel (örneğin Waybar veya AGS) ayrı çalışır, `mako` veya `dunst` bildirimleri yönetir, `hyprlock` kilit ekranını sağlar. Quickshell mimarisinde ise:

1. **Ortak Durum Paylaşımı (Shared State):** Panel, bildirim merkezi, OSD göstergeleri ve sistem tepsisi aynı bellek alanında yaşar. Bir ses değiştiğinde veya yeni bir bildirim geldiğinde süreçler arası karmaşık soket trafiği gerekmez; QML'in reaktif bağlama (*property binding*) mekanizması sayesinde arayüz anında güncellenir.
2. **Düşük Kaynak Tüketimi:** Quickshell, Qt Quick'in donanım hızlandırmalı sahne grafiğini (Scene Graph) kullanır. Boşta bellek tüketimi 35 MB'ın altındadır ve CPU kullanımı %0'a yakındır.
3. **Anında Başlatma ve Canlı Yenileme (Live Reload):** QML dosyalarında yapılan herhangi bir değişiklik, kabuk sürecini yeniden başlatmaya gerek kalmadan anında ekrana yansır.

---

## 2. Wayland Katman Protokolleri (Layer Shell)

Quickshell, Wayland'in `zwlr_layer_shell_v1` protokolünü yerel olarak destekler. Bu protokol pencereleri 4 temel katmana ayırır:

- **Background:** Duvar kağıdı ve masaüstü zemin bileşenleri.
- **Bottom:** Masaüstü simgeleri veya arka plan widget'ları.
- **Top:** Üst panel, durum çubuğu ve dock bileşenleri.
- **Overlay:** Bildirimler, kilit ekranı ve tam ekran OSD göstergeleri.

Quickshell QML içerisinde bir pencere tanımlamak yalnızca birkaç satırdan ibarettir:

```qml
import Quickshell 1.0
import Quickshell.Wayland 1.0

Scope {
    PanelWindow {
        id: topBar
        anchors {
            top: true
            left: true
            right: true
        }
        height: 38
        
        WlrLayershell.layer: WlrLayer.Top
        WlrLayershell.keyboardFocus: WlrKeyboardFocus.None
        
        color: "#08090b"
        
        // Bar içeriği ve modülleri burada tanımlanır
    }
}
```

---

## 3. Hyprland IPC ile Doğrudan Entegrasyon

Omarchy üzerinde Hyprland olayları, `/tmp/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock` üzerinden akar. Quickshell, C++ soket dinleyicileriyle bu olayları doğrudan QML sinyallerine dönüştürür:

- `workspace>>id`: Çalışma alanı değiştiğinde paneldeki aktif numara gecikmesiz güncellenir.
- `activewindow>>title`: Aktif pencere başlığı anında üst barın merkezine yazılır.
- `fullscreen>>bool`: Tam ekrana geçildiğinde panel otomatik olarak gizlenir veya arka plana itilir.

---

## 4. Sonuç ve Gelecek

Quickshell, Linux masaüstünü hantal web teknolojilerine (Electron/Webview) teslim etmeden; C++ performansını modern, reaktif ve estetik bir QML arayüz motoruyla buluşturuyor. Omarchy masaüstünün bu denli hızlı, tepkisel ve esnek olmasının arkasındaki gerçek güç Quickshell mimarisidir.
