---
title: "Omarchy 4.0.4 ve Yeni Nesil Yapay Zekâ Ekosistemi: Çekirdek Düzeyinde Ajanlar, Akıllı Çökme Teşhisi ve Voxtype"
description: "16 Eylül 2026'da yayımlanan Omarchy 4.0.4 sürümüyle Linux masaüstü otonom bir AI çalışma ortamına dönüştü: 13 farklı kodlama ajanı, systemd-coredump destekli akıllı çökme teşhisi, yerel ses diktesi Voxtype ve yeni linux-omarchy çekirdeğiyle yapılabilecek her şey."
pubDate: "2026-09-16T11:35:00.000+03:00"
updatedDate: "2026-09-16T11:35:00.000+03:00"
heroImage: "/images/omarchy-4-0-4-ai-ecosystem-hero.webp"
tags: ["omarchy", "yapay zeka", "linux", "ajanlar", "sistem mimarisi", "hyprland", "voxtype"]
draft: false
toc: true
---

> **Yönetici Özeti:** Arch Linux tabanlı, Hyprland ve Quickshell mimarisi üzerine kurulu **Omarchy 4.0.4** sürümü 16 Eylül 2026 itibarıyla kararlı kanalda yayımlandı. Bu güncelleme, işletim sistemini yapay zekâ araçlarının sadece üzerinde çalıştığı pasif bir platform olmaktan çıkarıp; 13 farklı otonom ajanı koordine eden, `systemd-coredump` üzerinden uygulama çökmelerini otomatik teşhis eden, Vulkan destekli yerel ses diktesi (Voxtype) sunan ve özel `linux-omarchy` çekirdeğiyle donatılmış tam teşekküllü bir **yapay zekâ işletim ortamına** dönüştürüyor.

---

## Giriş: Pasif İşletim Sistemlerinden Otonom Yapay Zekâ Platformuna

Geleneksel işletim sistemleri (Windows, macOS ve klasik Linux dağıtımları), yapay zekâyı hâlâ harici bir misafir gibi ağırlar. Ya tarayıcı sekmesindeki bir sohbet arayüzüne mahkûmsunuzdur ya da editörünüze gömülü eklentilerle sınırlı kalırsınız. Yapay zekânın işletim sisteminin belleğiyle, hata ayıklama günlükleriyle (journal), donanım hızlandırma katmanlarıyla ve pencere yöneticisiyle doğrudan haberleşebildiği entegre bir zemin bugüne kadar bulunmuyordu.

David Heinemeier Hansson (DHH) ve topluluk tarafından geliştirilen **Omarchy**, 4.0.4 sürümüyle birlikte bu paradigmayı kökten yıktı.

Omarchy 4.0.4; klavye odaklı Hyprland Wayland kompozitörü, reaktif Quickshell kabuğu ve UNIX domain soketleri üzerine inşa edilmiş deterministik yapısını, doğrudan yapay zekâ ajanlarının (AI Agents) ana kumanda merkezine dönüştürüyor. Bu yazıda, yeni sürümle birlikte sistemimize eklenen tüm AI yeteneklerini, terminal komutlarını ve donanım düzeyindeki entegrasyonları en ince teknik detayına kadar masaya yatırıyoruz.

---

## 1. Çoklu Ajan Matrisi (Multi-Agent Subsystem): `omarchy agent`

Omarchy 4.0.4'ün en çarpıcı yeniliği, masaüstü düzeyinde standartlaştırılmış ve soyutlanmış **kodlama ajanı altyapısıdır**. İşletim sistemi artık tek bir şirketin veya modelin tekeline bağlı kalmak yerine, piyasadaki en yetkin 13 farklı yapay zekâ ajanını tek bir çatı altında toplar:

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
    <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
      Omarchy 4.0.4 Çoklu Ajan Dağıtım Mimarisi
    </div>
    <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">UWSM İzolasyonu</span>
  </div>

  <!-- Trigger & Dispatcher -->
  <div class="max-w-md mx-auto space-y-3 mb-6 font-mono text-center">
    <div class="p-3 rounded-xl border border-[#8b3a2b]/30 bg-[#8b3a2b]/10 dark:bg-[#8b3a2b]/20">
      <div class="text-[11px] uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372] font-semibold">Global Masaüstü Kısayolu</div>
      <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mt-0.5">SUPER + SHIFT + CTRL + A</div>
      <div class="text-xs text-[#5c4033] dark:text-[#a8a29e] mt-1">omarchy agent --pick</div>
    </div>
    <div class="text-[#8b3a2b] dark:text-[#d48372] text-xs font-bold font-mono">| (Yönlendirme)</div>
    <div class="p-2.5 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/80 dark:bg-[#1c1917]/80 text-xs font-bold text-[#1c1917] dark:text-[#f5f5f4]">
      omarchy default agent (Akıllı Dağıtıcı)
    </div>
    <div class="text-[#8b3a2b] dark:text-[#d48372] text-xs font-bold font-mono">| (Ajan Seçimi)</div>
  </div>

  <!-- Agent Engines Grid -->
  <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 font-mono text-xs mb-6">
    <div class="p-3 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/50 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4] text-sm">Hermes</div>
        <div class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mt-1">Yerel TUI</div>
      </div>
      <div class="mt-3 px-2 py-1 rounded bg-stone-100 dark:bg-stone-900 text-[#8b3a2b] dark:text-[#d48372] text-[10px] font-semibold break-all">
        --yolo --tui
      </div>
    </div>

    <div class="p-3 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/50 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4] text-sm">Claude Code</div>
        <div class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mt-1">Anthropic Native</div>
      </div>
      <div class="mt-3 px-2 py-1 rounded bg-stone-100 dark:bg-stone-900 text-[#8b3a2b] dark:text-[#d48372] text-[10px] font-semibold break-all">
        --permission auto
      </div>
    </div>

    <div class="p-3 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/50 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4] text-sm">Gemini</div>
        <div class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mt-1">Google CLI</div>
      </div>
      <div class="mt-3 px-2 py-1 rounded bg-stone-100 dark:bg-stone-900 text-[#8b3a2b] dark:text-[#d48372] text-[10px] font-semibold break-all">
        --yolo --interactive
      </div>
    </div>

    <div class="p-3 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/50 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4] text-sm">Codex</div>
        <div class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mt-1">OpenAI CLI</div>
      </div>
      <div class="mt-3 px-2 py-1 rounded bg-stone-100 dark:bg-stone-900 text-[#8b3a2b] dark:text-[#d48372] text-[10px] font-semibold break-all">
        --approve-for-me
      </div>
    </div>

    <div class="p-3 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/50 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4] text-sm">OpenClaw</div>
        <div class="text-[11px] text-[#5c4033] dark:text-[#a8a29e] mt-1">Gateway Hub</div>
      </div>
      <div class="mt-3 px-2 py-1 rounded bg-stone-100 dark:bg-stone-900 text-[#8b3a2b] dark:text-[#d48372] text-[10px] font-semibold break-all">
        --gateway --tui
      </div>
    </div>
  </div>

  <!-- Scope Footer -->
  <div class="p-3.5 rounded-xl border border-emerald-300 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/30 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 font-mono text-xs">
    <div class="flex items-center gap-2">
      <span class="px-2 py-0.5 rounded bg-emerald-200 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 font-bold text-[10px]">ÇALIŞTIRMA KATMANI</span>
      <span class="text-[#1c1917] dark:text-[#f5f5f4] font-semibold">UWSM Session Scope</span>
    </div>
    <span class="text-emerald-700 dark:text-emerald-400 text-[11px]">app-id: org.omarchy.agent (İzole Wayland Oturumu)</span>
  </div>
</div>

### Desteklenen Ajan Motorları ve Otomasyon Bayrakları

Bir ajanı terminalden veya masaüstü kısayolundan çağırdığınızda en büyük problem, her işlemde sizden onay istemesidir. Omarchy, `omarchy-agent` komutu üzerinden her ajanın "kesintisiz çalışma" (unattended execution) bayraklarını arka planda otomatik haritalandırır:

| Ajan Adı | Entegrasyon Türü | Varsayılan Çalışma Bayrağı / Komut | Açıklama |
| :--- | :--- | :--- | :--- |
| **Hermes** | Doğal TUI & Desktop | `hermes chat --yolo --tui` | Nous Hermes yerel TUI oturumu |
| **Claude Code** | Anthropic Native | `claude --permission-mode auto` | Onaysız tam yetkili kodlama oturumu |
| **Google Gemini** | Gemini CLI | `gemini --yolo --prompt-interactive` | Yüksek bağlam pencereli interaktif akış |
| **OpenAI Codex** | Codex CLI | `codex --approve-for-me` | Otomatik onaylı terminal ajanı |
| **OpenCode** | Açık Kaynak CLI | `opencode --auto` | Çoklu sağlayıcı destekli otonom ajan |
| **Cursor Agent** | Mise Wrapper | `cursor-agent --yolo --trust` | Cursor ekosisteminin bağımsız CLI ajanı |
| **xAI Grok** | Grok CLI | `grok --permission-mode bypassPermissions` | Grok motoru ile doğrudan sistem mühendisliği |
| **Charm Crush** | Charmbracelet TUI | `crush --yolo` | Şık TUI arayüzlü Go tabanlı ajan |
| **OpenClaw** | Agent Platformu | `omarchy-launch-openclaw --tui` | Arka plan gateway bağlı sürekli ajan |
| **Meta Muse** | Mise Wrapper | `muse --approval-mode never` | Meta AI kodlama ortamı |
| **Copilot** | GitHub CLI | `copilot --allow-all` | GitHub Copilot CLI terminal oturumu |
| **Omp & Pi** | Minimalist TUI | `omp --auto-approve` / `pi` | Düşük kaynak tüketen hafif ajanlar |

### Hızlı Kullanım ve Global Kısayol

Masaüstünün herhangi bir yerindeyken `SUPER + SHIFT + CTRL + A` tuş kombinasyonuna bastığınızda, Omarchy anında varsayılan ajanınızı özel bir Wayland pencere sınıfıyla (`org.omarchy.agent`) ekrana getirir.

Varsayılan ajanınızı belirlemek veya anlık komut çalıştırmak son derece basittir:

```bash
# Varsayılan ajanı Hermes veya Claude olarak ayarla
omarchy default agent hermes
omarchy default agent claude

# Doğrudan bir görev vererek ajanı başlat
omarchy agent prompt "Bu dizindeki Rust projesinin bellek sızıntılarını tara ve düzelt"

# Komut satırı içinde satır içi (inline) çalıştır
omarchy agent --inline
```

Tüm bu süreç `setsid uwsm-app` üzerinden Universal Wayland Session Manager korumasında yürütülür; yani bir ajan terminali kilitlense veya çökse bile masaüstü oturumunuz hiçbir şekilde etkilenmez.

---

## 2. Otonom Sistem Çökme Teşhisi: `omarchy-crash-watch` & `systemd-coredump`

Omarchy 4.0.4 ile birlikte gelen ve işletim sistemleri tarihinde eşine az rastlanan bir diğer özellik ise **yapay zekâ destekli çökme teşhisidir (AI Crash Diagnostics)**.

Bir C++, Rust veya Python uygulaması segfault (SIGSEGV) ya da abort (SIGABRT) aldığında geleneksel olarak ne yaparsınız? Çoğu kullanıcı terminal çıktısındaki karmaşık bellek adreslerine bakar ve hiçbir şey anlamadan uygulamayı yeniden başlatır. 

Omarchy 4.0.4 bunu tamamen değiştirdi.

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
    <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
      Otonom Sistem Çökme Teşhis Boru Hattı
    </div>
    <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">systemd-coredump + GDB</span>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 font-mono text-xs">
    <!-- Step 1 -->
    <div class="p-4 rounded-xl border border-red-200/80 dark:border-red-900/40 bg-red-50/40 dark:bg-red-950/20 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-red-100 dark:bg-red-900/60 text-red-800 dark:text-red-300 font-bold text-[10px]">ADIM 01</span>
          <span class="text-[10px] text-red-600 dark:text-red-400 font-bold">SIGSEGV / SIGABRT</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">Çöken Süreç</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">Uygulama bellek hatası alır ve işletim sistemi tarafından sonlandırılır.</p>
      </div>
      <div class="mt-3 text-[10px] text-red-700 dark:text-red-400 font-semibold">Core dump oluşumu tetiklenir</div>
    </div>

    <!-- Step 2 -->
    <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-[#ead9d2] dark:bg-[#2a2421] text-[#3c2a21] dark:text-[#e7e5e4] font-bold text-[10px]">ADIM 02</span>
          <span class="text-[10px] text-[#5c4033] dark:text-[#c4a482]">Journal Olayı</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">systemd-coredump</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">MESSAGE_ID=fc2e22bc... olayı üretilerek bellek dökümü journal'a kaydedilir.</p>
      </div>
      <div class="mt-3 text-[10px] text-[#8b3a2b] dark:text-[#d48372] font-semibold">mktemp izole depolama</div>
    </div>

    <!-- Step 3 -->
    <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-[#ead9d2] dark:bg-[#2a2421] text-[#3c2a21] dark:text-[#e7e5e4] font-bold text-[10px]">ADIM 03</span>
          <span class="text-[10px] text-[#5c4033] dark:text-[#c4a482]">Daemon Filtre</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">omarchy-crash-watch</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">Deduplication ve UID denetimi ile gereksiz tekrarlar elenir.</p>
      </div>
      <div class="mt-3 text-[10px] text-[#8b3a2b] dark:text-[#d48372] font-semibold">Aktif kullanıcı eşleştirme</div>
    </div>

    <!-- Step 4 -->
    <div class="p-4 rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/60 dark:bg-[#1c1917]/50 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-[#ead9d2] dark:bg-[#2a2421] text-[#3c2a21] dark:text-[#e7e5e4] font-bold text-[10px]">ADIM 04</span>
          <span class="text-[10px] text-amber-600 dark:text-amber-400 font-bold">Masaüstü Aksiyonu</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">Quickshell Bildirimi</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">"Process crashed: &lt;app&gt;. Click to diagnose" interaktif bildirimi görüntülenir.</p>
      </div>
      <div class="mt-3 text-[10px] text-amber-700 dark:text-amber-400 font-semibold">Tek tıkla tetikleme</div>
    </div>

    <!-- Step 5 -->
    <div class="p-4 rounded-xl border border-sky-200/80 dark:border-sky-900/40 bg-sky-50/40 dark:bg-sky-950/20 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-sky-100 dark:bg-sky-900/60 text-sky-800 dark:text-sky-300 font-bold text-[10px]">ADIM 05</span>
          <span class="text-[10px] text-sky-600 dark:text-sky-400 font-bold">Ajan Analizi</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">diagnose-crash Skill</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">debuginfod.archlinux.org sembolleri çekilir ve GDB yığın analizi başlatılır.</p>
      </div>
      <div class="mt-3 text-[10px] text-sky-700 dark:text-sky-400 font-semibold">omarchy agent crash &lt;pid&gt;</div>
    </div>

    <!-- Step 6 -->
    <div class="p-4 rounded-xl border border-emerald-300 dark:border-emerald-900/60 bg-emerald-50/50 dark:bg-emerald-950/30 flex flex-col justify-between">
      <div>
        <div class="flex items-center justify-between mb-2">
          <span class="px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-900/60 text-emerald-800 dark:text-emerald-300 font-bold text-[10px]">ADIM 06</span>
          <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">Çözüm Raporu</span>
        </div>
        <div class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4] mb-1">Kök Neden ve Yama</div>
        <p class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">Bellek durumu, son sistem güncellemeleri ve somut düzeltme önerisi sunulur.</p>
      </div>
      <div class="mt-3 text-[10px] text-emerald-700 dark:text-emerald-400 font-semibold">Otonom hata çözümü</div>
    </div>
  </div>
</div>

### Çalışma Mekanizması

1. **Journal Olay Takibi:** Arka planda çalışan `omarchy-crash-watch.service`, `systemd-coredump` servisinin ürettiği `MESSAGE_ID=fc2e22bc6ee647b6b90729ab34a250b1` olaylarını kesintisiz dinler.
2. **Akıllı Masaüstü Bildirimi:** Kullanıcıya ait bir işlem çöktüğünde ekrana kritik öncelikli bir Quickshell bildirimi düşer:
   ```
   Process crashed: alacritty
   Click to diagnose with AI
   ```
3. **debuginfod ve GDB Entegrasyonu:** Bildirime tıklandığında veya terminalde `omarchy agent crash <pid>` çalıştırıldığında sistem, varsayılan kodlama ajanını `diagnose-crash` becerisiyle (skill) uyandırır.
4. **Güvenli Analiz:** Bellek dökümü (core dump) geçici ve güvenli bir `mktemp` alanına alınır. Ajan, Arch Linux'un resmî `debuginfod.archlinux.org` sunucusuna bağlanarak yerel diskte olmayan sembol tablolarını anında çeker ve GDB ile yığını (stack trace) sembolize eder.
5. **Kapsamlı Korelasyon:** Ajan sadece çöken çerçeveyi (frame 0) değil; diğer tüm iş parçacıklarını, dosya sistemi değişiklik zamanlarını (`mtime`), sistem günlüklerindeki uyarıları ve son `pacman` güncellemelerini eşleştirir. Çökmenin bir bellek yetersizliği (OOM Killer) mi, kütüphane uyumsuzluğu mu yoksa bir yazılım hatası mı olduğunu saniyeler içinde raporlar.

Bu mekanizmayı dilediğiniz zaman açıp kapatabilirsiniz:
```bash
# Çökme yakalama bildirimlerini aç / kapat
omarchy toggle crash capture
```

---

## 3. Açık Kaynak Otonom Ajan Platformu: OpenClaw

Omarchy 4.0.4, bağımsız çalışan açık kaynaklı ajan platformu **OpenClaw** için tam teşekküllü sistem seviyesinde entegrasyon sunuyor:

```bash
# OpenClaw platformunu ve sistem servislerini tek komutla kur
omarchy install ai openclaw
```

### OpenClaw Mimarisi ve Gateway Yönetimi

OpenClaw, sistemde bir web gateway'i (`http://127.0.0.1:18789`) ve terminal UI katmanını birlikte koşturur. Ancak geleneksel Linux ortamlarında terminal ile arka plan servisinin port çakışmaları yaşaması yaygındır.

Omarchy, `omarchy openclaw onboard` ve `omarchy-openclaw-onboard` betikleriyle bu süreci mükemmelleştirmiştir:
- OpenClaw ağ geçidi bir systemd kullanıcı servisi (`openclaw-gateway.service`) olarak yapılandırılır.
- Kurulum sihirbazı tamamlandığı an ağ geçidi portunu (`18789`) otomatik dinler ve soket hazır olduğunda masaüstü Web App penceresini açar.
- Terminalden müdahale etmek istediğinizde `omarchy launch openclaw --tui` komutu doğrudan koşan ağ geçidine bağlanır; yetki karmaşası veya kilit dosyası (lockfile) hatası yaşanmaz.

---

## 4. Donanım Hızlandırmalı Yerel Ses Diktesi: Voxtype

Metin odaklı bir sistemde klavye hızınız bazen zihninize yetişemez. Omarchy 4.0.4, OpenAI Whisper modellerini doğrudan Wayland pencere yöneticisine entegre eden **Voxtype** altyapısını duyurdu.

```bash
# Voxtype ve ~150MB'lık Whisper yapay zekâ modelini kur
omarchy voxtype install
```

### Donanım Seviyesinde Vulkan GPU Hızlandırması

Voxtype kurulurken Omarchy donanımınızı (`omarchy-hw-vulkan`) otomatik olarak tarar. Sistemde Intel Arc, NVIDIA veya AMD Vulkan destekli bir grafik işlemci varsa, ses modelini doğrudan GPU çekirdeklerine yükler. Bu sayede sesin metne dönüştürülmesi buluta tek bir bayt dahi göndermeden, **sıfır gecikmeyle ve tamamen yerel olarak** gerçekleşir.

* **Kısayollar:** `F9` tuşuna basılı tutarak konuşun ya da `Super + Ctrl + X` kombinasyonuyla dikte modunu açıp kapatın.
* **Wayland Enjeksiyonu:** Çıkarılan metin `wtype` kütüphanesiyle doğrudan o an odaklandığınız terminale, Neovim tamponuna veya tarayıcı giriş kutusuna sanki klavyeden yazılmış gibi aktarılır.

### LLM ile Otomatik Dilbilgisi ve Dolgu Kelime Temizliği

Voxtype'ın en heyecan verici yönü, `~/.config/voxtype/config.toml` dosyası üzerinden yerel LLM boru hatlarını (post-processing pipelines) desteklemesidir:

```toml
# ~/.config/voxtype/config.toml
[output.post_process]
command = "ollama run llama3.2:1b 'Bu dikte metnini temizle. Dilbilgisini düzelt, ııı/şey gibi dolgu kelimeleri kaldır. Sadece düzeltilmiş metni yaz:'"
timeout_ms = 30000
```

Konuştuğunuz ham metin, saniyeler içinde yerel bir Llama 3.2 modeli tarafından filtrelenir; devrik cümleler ve konuşma aksaklıkları giderilerek ekranınıza tertemiz bir editoryal Türkçe veya İngilizce paragraf olarak dökülür.

---

## 5. Quickshell Bar Telemetrisi ve Tüketim Takibi: `omarchy.agents`

Geliştiricilerin en büyük kabuslarından biri, kod yazarken kullandıkları Claude veya OpenAI abonelik kotalarının aniden tükenmesidir. 

Omarchy 4.0.4, Quickshell durum çubuğuna (bar) doğrudan entegre edilen **`omarchy.agents`** bileşeniyle bu sorunu çözüme kavuşturuyor.

<div class="my-8 rounded-2xl border border-[#ead9d2] dark:border-[#2a2421] bg-white/80 dark:bg-[#141211] p-6 shadow-sm">
  <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-6">
    <div class="text-xs font-mono font-semibold uppercase tracking-wider text-[#8b3a2b] dark:text-[#d48372]">
      Quickshell Bar Telemetri Modülü: omarchy.agents
    </div>
    <div class="flex items-center gap-2">
      <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
      <span class="text-xs font-mono text-[#5c4033] dark:text-[#c4a482]">Canlı IPC Yayını</span>
    </div>
  </div>

  <div class="rounded-xl border border-[#ead9d2] dark:border-[#2a2421] bg-[#faf6f0]/70 dark:bg-[#1c1917]/70 p-5 font-mono text-xs">
    <!-- Header -->
    <div class="flex items-center justify-between border-b border-[#ead9d2] dark:border-[#2a2421] pb-3 mb-4">
      <div class="flex items-center gap-2">
        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span>
        <span class="font-bold text-sm text-[#1c1917] dark:text-[#f5f5f4]">CLAUDE CODE</span>
        <span class="text-[10px] px-2 py-0.5 rounded bg-emerald-100 dark:bg-emerald-950/60 text-emerald-800 dark:text-emerald-300 font-semibold">Max 20x Aktif</span>
      </div>
      <span class="text-[11px] text-[#5c4033] dark:text-[#a8a29e]">IPC: socket://omarchy.agents</span>
    </div>

    <!-- Limit Bars -->
    <div class="space-y-4 mb-5">
      <div>
        <div class="flex justify-between mb-1.5 text-[11px]">
          <span class="text-[#5c4033] dark:text-[#d6d3d1] font-semibold">5-Saatlik Oturum Limiti:</span>
          <span class="text-[#8b3a2b] dark:text-[#d48372] font-bold">%64 (1s 24dk içinde sıfırlanır)</span>
        </div>
        <div class="w-full h-2.5 rounded-full bg-[#ead9d2]/60 dark:bg-[#2a2421] overflow-hidden">
          <div class="h-full bg-gradient-to-r from-amber-500 to-[#8b3a2b] rounded-full" style="width: 64%"></div>
        </div>
      </div>

      <div>
        <div class="flex justify-between mb-1.5 text-[11px]">
          <span class="text-[#5c4033] dark:text-[#d6d3d1] font-semibold">Haftalık Kota Kullanımı:</span>
          <span class="text-emerald-700 dark:text-emerald-400 font-bold">%38 (Pazartesi yenilenir)</span>
        </div>
        <div class="w-full h-2.5 rounded-full bg-[#ead9d2]/60 dark:bg-[#2a2421] overflow-hidden">
          <div class="h-full bg-emerald-600 dark:bg-emerald-500 rounded-full" style="width: 38%"></div>
        </div>
      </div>
    </div>

    <!-- Daily Token Histogram -->
    <div class="border-t border-[#ead9d2] dark:border-[#2a2421] pt-4">
      <div class="text-[11px] font-bold text-[#8b3a2b] dark:text-[#d48372] uppercase tracking-wider mb-3">
        Günlük Token Tüketimi (Son 7 Gün):
      </div>
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-2 text-[11px]">
        <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-[#ead9d2]/60 dark:border-[#2a2421]">
          <div class="text-[#78716c]">Perşembe</div>
          <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4]">142k tokens</div>
        </div>
        <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-[#ead9d2]/60 dark:border-[#2a2421]">
          <div class="text-[#78716c]">Cuma</div>
          <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4]">210k tokens</div>
        </div>
        <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-[#ead9d2]/60 dark:border-[#2a2421]">
          <div class="text-[#78716c]">Cumartesi</div>
          <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4]">85k tokens</div>
        </div>
        <div class="p-2 rounded bg-white/80 dark:bg-black/40 border border-[#ead9d2]/60 dark:border-[#2a2421]">
          <div class="text-[#78716c]">Pazar</div>
          <div class="font-bold text-[#1c1917] dark:text-[#f5f5f4]">190k tokens</div>
        </div>
        <div class="p-2 rounded bg-amber-50 dark:bg-amber-950/30 border border-amber-300 dark:border-amber-900/50">
          <div class="text-amber-800 dark:text-amber-400 font-semibold">Pazartesi (Tepe)</div>
          <div class="font-bold text-[#8b3a2b] dark:text-[#d48372]">320k tokens</div>
        </div>
      </div>
      <div class="mt-3 text-[11px] text-[#5c4033] dark:text-[#a8a29e]">
        Bugün: <span class="font-bold text-[#1c1917] dark:text-[#f5f5f4]">178k tokens</span> (42 oturum, 128 istem)
      </div>
    </div>
  </div>
</div>

### Telemetri Özellikleri

1. **Çoklu Abonelik Geçişi:** Klavyeden `h` / `l` tuşlarıyla veya fareyle tıklayarak Claude, Codex ve Fireworks hesaplarınız arasında anında geçiş yapabilirsiniz.
2. **Kalan Süre Sayacı:** 5 saatlik kayan pencere ve 7 günlük kota limitlerinin dolmasına ne kadar süre kaldığını dinamik olarak hesaplar.
3. **Model Bazlı Ayrıştırma:** Hangi modelin (Opus, Sonnet, GPT-4o, Haiku) ne kadar girdi (input), çıktı (output) ve önbellek (cache read/write) tükettiğini grafik üzerinde detaylandırır.
4. **IPC Entegrasyonu:** Komut satırından çubuk widget'ını tetikleyebilirsiniz:
   ```bash
   omarchy-shell omarchy.agents toggle
   omarchy-shell omarchy.agents refresh
   ```

---

## 6. Evrensel Sistem Becerileri: `~/.agents/skills/omarchy`

Bir yapay zekâ modelini terminalde açtığınızda sisteminizi tanımazsa size genel Linux tavsiyeleri verir ve Omarchy'nin özel yapılandırmalarını bozabilir.

Omarchy 4.0.4, sistemin tüm mimari kurallarını içeren resmî bir **Agent Skill** setiyle birlikte gelir. Sistem güncellendiğinde bu beceri otomatik olarak tüm ajanların konfigürasyon dizinlerine sembolik bağ (symlink) ile bağlanır:

```bash
~/.agents/skills/omarchy -> /usr/share/omarchy/default/agents/skills/omarchy
~/.claude/skills/omarchy -> /usr/share/omarchy/default/agents/skills/omarchy
~/.codex/skills/omarchy  -> /usr/share/omarchy/default/agents/skills/omarchy
~/.pi/agent/skills/omarchy -> /usr/share/omarchy/default/agents/skills/omarchy
~/.hermes/skills/omarchy   -> /usr/share/omarchy/default/agents/skills/omarchy
```

Bu sayede çağırdığınız herhangi bir ajan:
* `/usr/share/omarchy/` dizininin salt okunur olduğunu ve asla doğrudan düzenlenmemesi gerektiğini bilir.
* Kullanıcı ayarlarının `~/.config/omarchy/` ve `~/.config/hypr/` altında olduğunu anlar.
* Monitör yenileme hızlarını, VRR ayarlarını, Quickshell bar yerleşimini ve OLED temalarını tek bir yanlış komut vermeden, deterministik olarak yönetir.

---

## 7. Donanım ve Altyapı Temeli: `linux-omarchy` Çekirdeği

Yapay zekâ iş yükleri, yüksek bellek bant genişliği ve düşük girdi gecikmesi gerektirir. Omarchy 4.0.4, Arch Linux'un standart çekirdeği yerine bu sürümle birlikte dağıtıma özel olarak derlenen **`linux-omarchy`** çekirdeğini devreye aldı.

* **Düşük Gecikme (Low-Latency Preemption):** Wayland kompozitörünün girdi gecikmelerini minimize ederken, arka planda koşan ağır LLM çıkarımlarının masaüstünü takılmaya uğratmasını engeller.
* **Limine & Snapper Güvencesi:** Sistem önyükleyicisi (bootloader) olarak modern Limine kullanılır. Yapay zekâ ajanlarına sistem seviyesinde geniş yetkiler verdiğinizde, Snapper Btrfs anlık görüntüleri sayesinde olası bir yapılandırma bozulmasında tek tuşla dünkü sistem durumuna geri dönülebilir.

---

## 8. Özet: Omarchy 4.0.4 Komut Rehberi

Yeni yapay zekâ özelliklerini hemen deneyimlemek için kullanabileceğiniz temel komut özeti:

```bash
# 1. Dağıtımı ve paketleri son sürüme güncelle
omarchy update

# 2. Varsayılan ajanını seç ve başlat
omarchy default agent hermes
omarchy agent

# 3. Voxtype yerel ses diktesini etkinleştir
omarchy voxtype install
omarchy voxtype status

# 4. OpenClaw otonom ajan platformunu kur
omarchy install ai openclaw
omarchy openclaw onboard

# 5. Çöken bir süreci AI ile derinlemesine analiz et
omarchy agent crash <PID>

# 6. Durum çubuğundaki AI token ve kota verilerini tazele
omarchy agent usage update

# 7. Ekrandaki herhangi bir bölgeden anında OCR ile metin kopyala
omarchy capture text
```

---

## Sonuç

Omarchy 4.0.4, Linux dünyasında uzun zamandır eksikliği hissedilen bir vizyonu gerçeğe dönüştürüyor: **Yapay zekâyı bir yabancı gibi izole etmek yerine, onu işletim sisteminin doğal bir uzvu haline getirmek.**

`systemd-coredump` üzerinden çökmeleri analiz eden, Vulkan çekirdekleriyle yerel dikte alan, 13 farklı kodlama ajanını tek kısayolla önünüze seren ve sistem ayarlarını yapay zekâya güvenle emanet eden bu mimari; önümüzdeki yıllarda işletim sistemlerinin nasıl evrileceğinin en somut kanıtıdır. 

Eğer siz de makinenizi saf bir mühendislik ve üretkenlik canavarına dönüştürmek istiyorsanız, terminalinizi açın ve `omarchy update` ile bu geleceğe adım atın.
