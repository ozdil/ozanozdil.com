---
title: "Omarchy Linux Üzerinde NVIDIA PAIR ile Evde Yerel Yapay Zeka Kümesi (AI Cluster) Kurulumu"
description: "Yapay zeka modellerinin parametre boyutları hızla büyürken ve çokluajan (multiagent) iş akışları günlük yazılım geliştirme rutinim haline gelmişken, tek bir ..."
pubDate: "2026-09-04T13:18:38.306+03:00"
updatedDate: "2026-09-04T13:18:38.307+03:00"
tags: ["teknoloji", "sistem", "guvenlik"]
draft: false
legacyUrl: "/2026/09/omarchy-linux-uzerinde-nvidia-pair-ile.html"
---

Yapay zeka modellerinin parametre boyutları hızla büyürken ve **çoklu-ajan (multi-agent)** iş akışları günlük yazılım geliştirme rutinim haline gelmişken, tek bir bilgisayarın GPU belleğine (VRAM) sıkışıp kalmak en büyük darboğazlardan biriydi.

NVIDIA'nın **Eylül 2026**'da duyurduğu açık kaynaklı yeni aracı **NVIDIA PAIR (Personal AI Router)**, bu sorunu tam olarak hedef alıyor: Yerel ağınızdaki (LAN) tüm uyumlu bilgisayarları (NVIDIA GeForce RTX 20 serisi ve üzeri, RTX Workstation, DGX ve hatta Apple M-serisi Mac'ler) birbirine bağlayarak **kişisel, dağıtık bir yapay zeka çıkarım kümesi (Personal AI Cluster)** oluşturmanızı sağlıyor.

Bu yazıda, Arch Linux tabanlı modern işletim sistemimiz **Omarchy 4.0.2 (Hyprland)**üzerinde**NVIDIA PAIR**'ı nasıl kuracağınızı, yerel ağdaki diğer cihazlarla nasıl eşleyeceğinizi (pairing) ve **Ollama / LM Studio** ile çoklu ajan iş yüklerini nasıl dağıtacağınızı adım adım anlatıyorum.

---

## NVIDIA PAIR Nedir ve Nasıl Çalışır?

NVIDIA PAIR, donanımsal bir cihaz değil; yerel ağınızda çalışan hafif, akıllı bir **çıkarım yönlendiricisidir (Virtual Inference Router)**.

<div class="my-8 rounded-2xl border border-[#27272a] bg-[#121215] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#27272a] pb-3 mb-6">
  <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#ffffff]">
  Kişisel Yapay Zekâ Kümesi (AI Cluster) Topolojisi
  </div>
  <span class="text-xs font-mono text-[#71717a]">Sıfır Bulut Bağımlılığı</span>
  </div>
  <!-- Client Node -->
  <div class="max-w-md mx-auto p-4 rounded-xl border border-[#27272a] bg-[#18181b] text-center font-mono text-xs mb-3">
  <span class="text-[10px] font-bold uppercase tracking-wider text-[#ffffff]">İstemci ve Ana İstasyon</span>
  <div class="font-bold text-sm text-[#ffffff] mt-1">Omarchy Linux (İstemci / Ana PC)</div>
  <p class="text-[11px] text-[#a1a1aa] mt-1">Agentic AI / IDE / Geliştirme Ortamı</p>
  </div>
  <!-- Router Arrow & Box -->
  <div class="text-center font-mono text-xs text-[#ffffff] font-bold mb-2">| (localhost:8080/v1)</div>
  <div class="max-w-lg mx-auto p-4 rounded-xl border border-[#8b3a2b]/30 bg-[#8b3a2b]/10 dark:bg-[#8b3a2b]/20 text-center font-mono text-xs mb-6">
  <span class="text-[10px] font-bold uppercase tracking-wider text-[#ffffff]">Merkezi Sanal Yönlendirici</span>
  <div class="font-bold text-sm text-[#ffffff] mt-1">NVIDIA PAIR (Personal AI Router)</div>
  <p class="text-[11px] text-[#a1a1aa] dark:text-[#d6d3d1] mt-1">Dinamik Yük Dağıtımı, Otomatik Boş GPU Algılama ve Akıllı Yönlendirme</p>
  </div>
  <!-- Worker Nodes Grid -->
  <div class="grid grid-cols-1 md:grid-cols-2 gap-4 font-mono text-xs">
  <div class="p-4 rounded-xl border border-emerald-300 dark:border-emerald-900/60 bg-emerald-50/40 dark:bg-emerald-950/20 flex flex-col justify-between">
  <div>
  <div class="flex items-center justify-between mb-2">
  <span class="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 font-bold text-[10px]">DÜĞÜM 1</span>
  <span class="text-[10px] text-emerald-700 dark:text-emerald-400 font-semibold">Mobil Çıkarım</span>
  </div>
  <div class="font-bold text-sm text-[#ffffff] mb-1">Game Garaj (RTX 4060)</div>
  <p class="text-[11px] text-[#a1a1aa] mb-2">8GB GDDR6 VRAM, düşük gecikmeli yerel modeller.</p>
  </div>
  <div class="p-2 rounded bg-[#18181b] border border-[#27272a] text-[11px]">
  <strong>Ollama:</strong> Qwen 2.5 Coder / Llama 3.2
  </div>
  </div>
  <div class="p-4 rounded-xl border border-sky-200/80 dark:border-sky-900/40 bg-sky-50/40 dark:bg-sky-950/20 flex flex-col justify-between">
  <div>
  <div class="flex items-center justify-between mb-2">
  <span class="px-2 py-0.5 rounded bg-sky-100 dark:bg-sky-900/60 text-sky-800 dark:text-sky-300 font-bold text-[10px]">DÜĞÜM 2</span>
  <span class="text-[10px] text-sky-700 dark:text-sky-400 font-semibold">Sunucu Çıkarım</span>
  </div>
  <div class="font-bold text-sm text-[#ffffff] mb-1">Homelab Server / Mac</div>
  <p class="text-[11px] text-[#a1a1aa] mb-2">RTX 3090 (24GB VRAM) / Apple M-Serisi Birleşik Bellek.</p>
  </div>
  <div class="p-2 rounded bg-[#18181b] border border-[#27272a] text-[11px]">
  <strong>LM Studio:</strong> DeepSeek V3 / Ağır Mantık Modelleri
  </div>
  </div>
  </div>
</div>

### Öne Çıkan Özellikleri:

- **Dinamik Yük Dağıtımı:** Bir ajan ana modele sorgu atarken, alt görevleri (kod analizi, web araması özetleme vb.) ağdaki boşta duran diğer GPU'lara yönlendirir.

- **Esnek ve Kesintisiz:** Ağdaki bir bilgisayarda oyun oynanmaya veya render alınmaya başlandığında, PAIR o cihazı meşgul olarak algılar ve yükü anında ana makineye veya diğer boş düğümlere aktarır.

- **Sıfır Bulut Bağımlılığı (Zero-Trust ve Gizlilik):** Tüm promptlar, kodlar ve model ağırlıkları yalnızca evinizin yerel ağında (LAN) dolaşır.

- **Platformlar Arası:** Linux, Windows 11 ve macOS arasında sorunsuz kümeleme desteği sunar.

---

## 1. Omarchy Linux Üzerine Kurulum

Omarchy (Arch Linux) sistemimizde NVIDIA PAIR'ı kurmanın en temiz ve pratik yolu, resmi `.deb` paketini yerel dosya ağacımıza entegre etmektir.

Terminalinizi (`Super + Enter`) açın ve aşağıdaki komutları çalıştırın:


```bash
# 1. Geçici kurulum dizini oluşturun ve paketi indirin
mkdir -p /tmp/nvpair && cd /tmp/nvpair
curl -LO https://github.com/NVIDIA/Personal-AI-Router/releases/download/v0.1.1/NVPAIR-Setup-0.1.1-amd64.deb

# 2. Paketi açın ve /opt/nvpair dizinine çıkartın
ar x NVPAIR-Setup-0.1.1-amd64.deb
tar -xf data.tar.xz

# 3. İlgili dizinleri sisteme kopyalayın
sudo cp -r opt/* /opt/
sudo cp -r usr/share/applications/* ~/.local/share/applications/ 2>/dev/null || sudo cp -r usr/share/applications/* /usr/share/applications/
sudo cp -r usr/share/icons/* ~/.local/share/icons/ 2>/dev/null || true

# 4. Kolay çalıştırma için global sembolik link tanımlayın
sudo ln -sf /opt/nvpair/nvpair /usr/local/bin/nvpair 2>/dev/null || true

# 5. Temizlik
cd ~ && rm -rf /tmp/nvpair
```


Kurulum tamamlandıktan sonra terminalden `nvpair` yazarak veya Omarchy menünüzden (**Super + Space**) **NVIDIA PAIR**'ı aratarak uygulamayı başlatabilirsiniz.

---

## 2. Cihazları Eşleme (Cluster Pairing)

Yapay zeka kümenizin gücünden tam olarak yararlanabilmek için ağınızdaki ikinci bilgisayara (örneğin evdeki masaüstü PC veya homelab sunucusu) da PAIR uygulamasını yükleyin:

1. **PAIR Arayüzünü Açın:** Her iki cihazda da PAIR uygulamasını çalıştırın.

1. **Otomatik Keşif:** PAIR, yerel ağdaki diğer PAIR çalıştıran cihazları mDNS üzerinden otomatik olarak listeleyecektir.

1. **Eşleme Kodu:** Karşı cihazın üzerine tıklayıp **"Pair"** deyin ve ekranda çıkan onay kodunu doğrulayın.

1. Artık her iki cihaz tek bir sanal yapay zeka havuzu (Inference Pool) olarak senkronize oldu!

---

## 3. Ollama ve LM Studio Entegrasyonu

NVIDIA PAIR, yapay zeka istemcileriniz için standart bir **OpenAI Uyumlu API Proxy** (`http://localhost:8080/v1`) sunar.


```bash
# PAIR proxy üzerinden model sorgulama örneği
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.3:8b",
    "messages": [{"role": "user", "content": "Omarchy Linux üzerinde yapay zeka kümesi nasıl optimize edilir?"}]
  }'
```


PAIR, bu isteği ağdaki GPU bellek durumunu analiz ederek en uygun düğüme iletir ve yanıtı milisaniyeler içinde ana ekranınıza geri döndürür.

---

## Omarchy İçin Tavsiye Edilen Hyprland Pencere Kuralı

Omarchy'nin dinamik döşeme (tiling) yöneticisi Hyprland üzerinde PAIR'in şık ve sabit bir floating pencere olarak açılmasını isterseniz, pencere kurallarınıza (`~/.config/hypr/hyprland.conf`) şu satırı ekleyebilirsiniz:


```text
windowrulev2 = float, class:^(nvpair|Personal-AI-Router)$
windowrulev2 = size 900 650, class:^(nvpair|Personal-AI-Router)$
windowrulev2 = center, class:^(nvpair|Personal-AI-Router)$
```


---

## Sonuç: Kendi Donanımınızla Özgür Yapay Zeka

Bulut API'lerine servet ödemeden ve kişisel verilerinizi üçüncü taraf sunuculara göndermeden, evdeki tüm boşta duran GPU'ları tek bir devasa yapay zeka beynine dönüştürmek NVIDIA PAIR ile artık çocuk oyuncağı.

Omarchy'nin düşük kaynak tüketen akıcı Hyprland masaüstü ortamı ve Game Garaj RTX 4060 donanımımızın sunduğu saf güçle birleştiğinde, evde yapay zeka kümesi yönetmek hem son derece stabil hem de benzersiz bir keyif haline geliyor.

Teknoloji, Linux ve Açık Kaynak Notları — [ozanozdil.com](https://ozanozdil.com)
