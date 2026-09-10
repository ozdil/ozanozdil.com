---
title: "Quickshell ile Özelleştirilmiş Kilit Ekranı ve Bildirim Merkezi"
description: "PAM kimlik doğrulama entegrasyonu, akıcı açılış animasyonları ve gruplandırılmış Wayland bildirim merkezi mimarisi."
pubDate: 2026-09-02
heroImage: "/images/quickshell/quickshell-lockscreen.svg"
tags: ["quickshell", "guvenlik", "arayuz", "wayland", "qml"]
draft: false
---

Masaüstünün güvenliği ve bildirim yönetimi, kullanıcı deneyiminin en hassas parçalarındandır. Harici bir kilit ekranı kullanıldığında yaşanan ekran titremeleri veya bildirimlerin kilit ekranının arkasında kaybolması, bütünsel bir masaüstü hissini zedeler.

**Quickshell**, Wayland `ext-session-lock-v1` protokolünü ve Linux PAM (Pluggable Authentication Modules) altyapısını yerel olarak destekleyerek şık, güvenli ve bütünleşik bir kilit ekranı sağlar.

---

## 1. Wayland Session Lock Protokolü

Quickshell, ekran kilitlendiğinde diğer tüm pencerelerin üzerine geçen ve hiçbir girdi olayının arkaya sızmasına izin vermeyen güvenli bir yüzey oluşturur:

```qml
import QtQuick 2.15
import Quickshell 1.0
import Quickshell.Wayland 1.0

SessionLock {
    id: lockSurface
    
    Rectangle {
        anchors.fill: parent
        color: "#08090b"
        
        // Dijital Saat
        Text {
            anchors.centerIn: parent
            anchors.verticalCenterOffset: -60
            text: Qt.formatDateTime(new Date(), "hh:mm")
            font.pixelSize: 64
            font.bold: true
            color: "#ffffff"
        }
        
        // Şifre Giriş Alanı
        TextInput {
            id: passwordField
            anchors.centerIn: parent
            anchors.verticalCenterOffset: 40
            echoMode: TextInput.Password
            color: "#00ffcc"
            font.pixelSize: 18
            focus: true
            
            onAccepted: {
                PamAuth.authenticate(passwordField.text);
            }
        }
    }
}
```

---

## 2. Gruplandırılmış Bildirim Merkezi

Quickshell'in bildirim sunucusu (`org.freedesktop.Notifications`), gelen bildirimleri uygulama adına göre otomatik gruplandırır. Kullanıcı isterse geçmiş bildirimleri yan panelden listeleyebilir ya da tek tıkla temizleyebilir.
