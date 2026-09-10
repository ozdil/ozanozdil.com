---
title: "Quickshell ile Sıfırdan QML Bar ve Panel Geliştirme"
description: "Quickshell bileşenleri kullanarak Wayland için hafif, animasyonlu ve modüler bir üst bar (panel) ve durum widget'ı oluşturma rehberi."
pubDate: 2026-09-08
heroImage: "/images/quickshell/quickshell-bar-widget.svg"
tags: ["quickshell", "qml", "widget", "arayuz", "omarchy"]
draft: false
---

Wayland ortamında kişisel bir üst bar (panel) geliştirmek istediğinizde geleneksel olarak karşınıza iki seçenek çıkardı: Statik yapılandırma dosyalarıyla sınırlı GTK tabanlı paneller ya da tarayıcı motoru çalıştıran aşırı ağır JavaScript çözümleri. **Quickshell**, QML'in güçlü deklaratif yapısını doğrudan Wayland protokollerine bağlayarak her iki dünyanın da en iyi yönlerini bir araya getiriyor.

Bu yazıda, Quickshell kullanarak Omarchy stilinde hafif, modüler ve akıcı animasyonlara sahip bir üst barı nasıl inşa edebileceğinizi adım adım inceleyeceğiz.

---

## 1. Dizin Yapısı ve Temel Konfigürasyon

Quickshell yapılandırmaları varsayılan olarak `~/.config/quickshell/` dizininde konumlanır. Temiz bir mimari için bileşenleri modüllere ayırmak en sağlıklı yaklaşımdır:

```text
~/.config/quickshell/
├── shell.qml               # Ana giriş noktası
├── components/
│   ├── Workspaces.qml      # Çalışma alanları modülü
│   ├── WindowTitle.qml     # Aktif pencere başlığı
│   └── SystemTray.qml      # Sistem tepsisi ve göstergeler
└── theme/
    └── Theme.qml           # Global renk ve tipografi tanımları
```

---

## 2. Ana Kabuk: `shell.qml`

`shell.qml` dosyası ekran katmanını ve ana çerçevenin boyutlarını belirler:

```qml
import QtQuick 2.15
import QtQuick.Layouts 1.15
import Quickshell 1.0
import Quickshell.Wayland 1.0
import "components"
import "theme"

Scope {
    PanelWindow {
        id: bar
        
        anchors {
            top: true
            left: true
            right: true
        }
        height: 36
        
        WlrLayershell.layer: WlrLayer.Top
        WlrLayershell.exclusiveZone: 36
        
        color: Theme.background
        
        RowLayout {
            anchors.fill: parent
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            spacing: 8
            
            // Sol: Çalışma Alanları
            Workspaces {
                Layout.alignment: Qt.AlignLeft
            }
            
            // Orta: Aktif Pencere
            WindowTitle {
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignCenter
            }
            
            // Sağ: Sistem Durumu
            SystemTray {
                Layout.alignment: Qt.AlignRight
            }
        }
    }
}
```

---

## 3. Çalışma Alanı Göstergesi: `Workspaces.qml`

Hyprland çalışma alanlarını dinamik butonlar olarak listelemek ve fare ile tıklanabilir hale getirmek oldukça basittir:

```qml
import QtQuick 2.15
import QtQuick.Layouts 1.15
import Quickshell.Hyprland 1.0
import "../theme"

RowLayout {
    spacing: 4
    
    Repeater {
        model: 5
        
        Rectangle {
            id: wsButton
            property int wsId: index + 1
            property bool isActive: Hyprland.activeWorkspace.id === wsId
            
            width: 24
            height: 24
            radius: 4
            color: isActive ? Theme.accent : Theme.surface
            border.color: isActive ? Theme.accent : Theme.border
            
            Text {
                anchors.centerIn: parent
                text: wsId
                font.family: "JetBrains Mono"
                font.pixelSize: 11
                font.bold: isActive
                color: isActive ? Theme.background : Theme.textMuted
            }
            
            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: Hyprland.dispatch("workspace " + wsId)
            }
            
            Behavior on color {
                ColorAnimation { duration: 120 }
            }
        }
    }
}
```

---

## 4. Akıcı Geçişler ve Hover Efektleri

QML'in en büyük avantajı, CSS animasyonlarının ötesinde donanım destekli ve fizik tabanlı interpolasyon sunmasıdır. Örneğin, fare üzerine geldiğinde butonun yumuşakça parlaması `Behavior on ...` bloklarıyla tek satırda çözülür.

Quickshell ile geliştirilen bileşenler bağımsız pencereler olarak değil, GPU üzerinde tek bir yüzeyde çizildiği için kare atlaması yaşanmaz.
