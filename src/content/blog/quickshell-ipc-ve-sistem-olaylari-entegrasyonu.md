---
title: "Quickshell IPC ve Sistem Olayları: Hyprland ve D-Bus Entegrasyonu"
description: "Soket tabanlı IPC, Hyprland olay dinleyicileri ve D-Bus sinyalleri ile anlık masaüstü bildirimleri ve OSD pencereleri yönetimi."
pubDate: 2026-09-07
heroImage: "/images/quickshell/quickshell-ipc-events.svg"
tags: ["quickshell", "hyprland", "ipc", "dbus", "wayland"]
draft: false
---

Masaüstü kabuklarının en kritik sınavı, sistemde meydana gelen olaylara ne kadar hızlı ve verimli tepki verebildiğidir. Klavyeden ses açma tuşuna bastığınızda ekranda beliren OSD göstergesinin 100 milisaniye gecikmesi bile masaüstünün hantal hissettirmesine yol açar.

**Quickshell**, olay döngüsünü (event loop) doğrudan Linux çekirdeği, D-Bus mesaj yolu ve Hyprland IPC soketlerine bağlayarak mikrosaniye seviyesinde tepki süreleri sunar.

---

## 1. D-Bus ve Medya Kontrolleri (MPRIS2)

Quickshell, `org.mpris.MediaPlayer2` protokolünü dinleyerek Spotify, Firefox veya VLC gibi uygulamaların durumunu anlık yakalar:

```qml
import QtQuick 2.15
import Quickshell.Services.Mpris 1.0

Item {
    id: mediaTracker
    
    readonly property var player: Mpris.players.values[0]
    
    Text {
        text: player ? (player.trackTitle + " — " + player.trackArtist) : "Medya çalmıyor"
        font.family: "JetBrains Mono"
        color: "#00ffcc"
    }
}
```

Uygulama şarkıyı değiştirdiği anda D-Bus sinyali Quickshell tarafından doğrudan yakalanır; herhangi bir ek sorgulama (polling) döngüsü çalıştırılmaz.

---

## 2. Ses ve Parlaklık OSD Göstergesi

Wayland üzerinde geçici OSD pencereleri için `WlrLayershell.layer: WlrLayer.Overlay` kullanılır. Ses düzeyi değiştiğinde beliren ve 1.5 saniye sonra yumuşakça kaybolan OSD yapısı:

```qml
import QtQuick 2.15
import Quickshell 1.0
import Quickshell.Wayland 1.0

PanelWindow {
    id: volumeOsd
    
    anchors {
        bottom: true
        horizontalCenter: true
    }
    anchors.bottomMargin: 80
    
    width: 240
    height: 48
    color: "#0e1117"
    radius: 10
    
    WlrLayershell.layer: WlrLayer.Overlay
    visible: false
    
    Timer {
        id: hideTimer
        interval: 1500
        onTriggered: volumeOsd.visible = false
    }
    
    function trigger(level) {
        progressBar.value = level;
        volumeOsd.visible = true;
        hideTimer.restart();
    }
}
```

---

## 3. Donanım ve Sensör Telemetrisi

Quickshell'in C++ arka yüzü, Linux `/sys/class/` dizinindeki batarya, termal sensör ve CPU frekanslarını doğrudan okuyabilen reaktif sağlayıcılar sunar. Shell süreci uykudayken kaynak tüketmez; yalnızca ilgili sensör değeri değiştiğinde arayüzü yeniler.
