---
title: "Quickshell Eklenti Ekosistemi: Topluluk Eklentileri ve Modüler Yapı"
description: "Omarchy ve Quickshell için bağımsız eklenti yazımı, dizin hiyerarşisi, QML modül yükleme ve güvenli çalıştırma pratikleri."
pubDate: 2026-09-04
heroImage: "/images/quickshell/quickshell-plugins.svg"
tags: ["quickshell", "eklentiler", "qml", "moduler", "omarchy"]
draft: false
---

Bir masaüstü kabuğunu gerçekten güçlü kılan şey, yalnızca çekirdek geliştiricilerinin sunduğu özellikler değil; topluluğun kolayca katkıda bulunabileceği esnek bir eklenti (plugin) mimarisidir. **Omarchy Shell** ve **Quickshell**, modüler bileşen yapısı sayesinde eklenti geliştirmeyi çocuk oyuncağı haline getiriyor.

Omarchy Plugin Kataloğu ([plugins.omarchy.org](https://plugins.omarchy.org)) üzerinde binlerce topluluk eklentisi paylaşılmakta ve kullanıcılar bunları tek bir komutla masaüstlerine entegre edebilmektedir.

---

## 1. Bir Quickshell Eklentisinin Anatomisi

Her eklenti, kendi bağımsız dizininde bir bildirim dosyası (`metadata.json`) ve ana QML dosyasından oluşur:

```text
~/.config/quickshell/plugins/badusb-shield/
├── metadata.json
├── Plugin.qml
└── assets/
    └── icon.svg
```

### `metadata.json` Manifest Örneği

```json
{
  "name": "BadUSB Shield",
  "id": "org.omarchy.badusb-shield",
  "version": "1.2.0",
  "author": "Ozan Özdil",
  "description": "USB veri yollarını anlık izleyen donanım güvenlik eklentisi",
  "entryPoint": "Plugin.qml",
  "category": "security"
}
```

---

## 2. Eklentinin Dinamik Yüklenmesi

Quickshell, `Instantiator` veya `Loader` bileşenlerini kullanarak kurulu eklentileri çalışma anında keşfeder ve panele yerleştirir:

```qml
import QtQuick 2.15
import Quickshell 1.0

Row {
    spacing: 6
    
    Repeater {
        model: PluginManager.installedPlugins
        
        Loader {
            source: modelData.entryPointUrl
        }
    }
}
```

Eklenti kodunda bir hata meydana gelse bile, Quickshell'in izolasyon mekanizması sayesinde tüm masaüstü çökmez; yalnızca ilgili eklenti güvenli modda durdurulur.

---

## 3. Topluluk Eklentilerimiz

Omarchy ekosistemine kazandırdığımız siber güvenlik ve sistem araçları (BadUSB Shield, CVE Radar, DNS Leak Guard, Ghost MAC vb.), Quickshell'in modüler eklenti mimarisinin en somut örneklerindendir.
