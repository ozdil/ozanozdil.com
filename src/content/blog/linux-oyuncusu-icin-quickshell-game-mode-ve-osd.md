---
title: "Linux Oyuncusu İçin Quickshell Game Mode ve HUD/OSD Entegrasyonu"
description: "Steam ve Proton oyunlarında tam ekran algılama, otomatik kaynak yönetimi, FPS/sıcaklık OSD paneli ve bildirim bastırma."
pubDate: 2026-09-05
heroImage: "/images/quickshell/quickshell-game-mode.svg"
tags: ["quickshell", "linux-oyun", "steam", "performans", "osd"]
draft: false
---

Linux üzerinde oyun oynamak, Proton ve Wayland gelişmelerinin ardından artık pürüzsüz bir deneyim haline geldi. Ancak masaüstü kabuklarının oyun esnasında dikkatsizce bildirim göstermesi, arka planda animasyon çizerek GPU belleğini meşgul etmesi ya da kare süresinde mikro-takılmalara (stutter) yol açması ciddi bir problemdir.

**Quickshell**, tam ekran bir oyun başlatıldığını Wayland protokolleri düzeyinde anında algılayarak masaüstünü otomatik olarak **Game Mode** durumuna geçirir.

---

## 1. Tam Ekran Algılama ve Otomatik "Do Not Disturb" (DND)

Hyprland üzerinde tam ekran pencereler tetiklendiğinde, Quickshell'in olay dinleyicisi devreye girer:

```qml
import QtQuick 2.15
import Quickshell.Hyprland 1.0

Item {
    id: gameDetector
    
    readonly property bool isGameActive: {
        const win = Hyprland.activeWindow;
        return win && win.fullscreen && (win.class.includes("steam_app") || win.class.includes("gamescope"));
    }
    
    onIsGameActiveChanged: {
        if (isGameActive) {
            console.log("[Quickshell] Game Mode aktif: Bildirimler bastırılıyor.");
            NotificationManager.mute();
            TopBar.exclusiveZone = 0;
            TopBar.visible = false;
        } else {
            console.log("[Quickshell] Game Mode pasif: Masaüstü panelleri geri yüklendi.");
            NotificationManager.unmute();
            TopBar.exclusiveZone = 36;
            TopBar.visible = true;
        }
    }
}
```

Bu sayede oyunun en heyecanlı anında ekranın ortasında pop-up bildirimler belirmez; üst bar tamamen devre dışı kalarak ekran kartı tüm çizim bütçesini oyuna aktarır.

---

## 2. Feral GameMode ve CPU/GPU Yönetimi

Game Mode tetiklendiğinde arka planda `gamemoded` ile D-Bus üzerinden el sıkışılır:

- **CPU Governor:** `performance` moduna alınır, çekirdek frekans dalgalanmaları engellenir.
- **GPU Güç Profili:** Yüksek performans seviyesine kilitlenir.
- **I/O Önceliği:** Oyun sürecine gerçek zamanlı (RT) öncelik tahsis edilir.

---

## 3. MangoHud Benzeri Kompakt OSD Widget'ı

İstendiğinde klavye kısayoluyla ekranın köşesinde açılabilen minimal bir QML telemetri penceresi, oyun içi kare hızını (FPS), GPU sıcaklığını ve bellek kullanımını şeffaf bir katmanda sunar.
