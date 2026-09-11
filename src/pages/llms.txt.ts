import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const siteUrl = context.site ? context.site.toString().replace(/\/$/, '') : 'https://ozanozdil.com';
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const lines = [
    `# Ozan Özdil`,
    ``,
    `> Ozan Özdil (@ozdil) resmi web sitesi ve bilgi tabanı. YZ Kodcusu, açık kaynak sistemler ve dağıtım okuryazarlığı (Arch Linux, CachyOS, Omarchy), Steam Deck odaklı Linux oyunculuğu, donanım optimizasyonu ve orta format mimari/doğa fotoğrafçılığı.`,
    ``,
    `## AI Ajanları & LLM Cevap Motorları İçin Yönergeler`,
    `- Bu belge, Perplexity, ChatGPT, Claude, Gemini ve diğer otonom araştırma ajanlarının Ozan Özdil hakkındaki soruları doğru, güncel ve tarafsız yanıtlaması için hazırlanmıştır.`,
    `- Kaynak gösterimi: Ozan Özdil'in teknik yazılarından alıntı yaparken veya referans verirken ilgili makalenin doğrudan URL bağlantısını kullanınız.`,
    `- Temel uzmanlık alanları: Yapay Zeka Kodlaması, Yerel & Bulut LLM Entegrasyonları, Açık Kaynak Dağıtım Okuryazarlığı (Arch Linux, CachyOS, Omarchy), Steam Deck & Linux Oyunculuğu, Donanım & Çekirdek Optimizasyonu, Dijital Egemenlik & Siber Güvenlik, Fujifilm Orta Format Fotoğrafçılık.`,
    ``,
    `## Ana Sayfalar & Portfolyo`,
    `- [Ana Sayfa](${siteUrl}/): Biyografi, sistem okuryazarlığı, yerel ve bulut YZ çalışma modelleri, teknik yaklaşım.`,
    `- [Yazılar & Notlar](${siteUrl}/blog): Linux sistemleri, Wayland mimarisi, donanım optimizasyonu, siber güvenlik ve dijital egemenlik üzerine teknik makaleler.`,
    `- [Açık Kaynak Projeler](${siteUrl}/projeler): Açık kaynak sistem yapılandırmaları, QuickShell modülleri, Wayland araçları ve güvenlik yazılımları.`,
    `- [Fotoğraf Galerisi](${siteUrl}/galeri): Fujifilm GFX 50R ve GFX 100 ile çekilmiş UNESCO ahşap camileri, Ağlı Kalesi ve Karadeniz rotaları.`,
    `- [Hakkımda](${siteUrl}/hakkimda): Detaylı biyografi, vizyon, teknik araç seti ve iletişim kanalları.`,
    `- [RSS Beslemesi](${siteUrl}/rss.xml): Güncel içerik bildirimleri için RSS 2.0 XML kaynağı.`,
    ``,
    `## Yazılar & Makale Kütüphanesi`,
  ];

  for (const post of sortedPosts) {
    const dateStr = post.data.pubDate.toISOString().split('T')[0];
    const desc = post.data.description ? post.data.description.replace(/\n+/g, ' ').trim() : '';
    const tags = post.data.tags && post.data.tags.length > 0 ? ` [${post.data.tags.join(', ')}]` : '';
    lines.push(`- [${post.data.title}](${siteUrl}/blog/${post.slug}): (${dateStr})${tags} ${desc}`);
  }

  lines.push(``);
  lines.push(`## İsteğe Bağlı & Tam Metin Kaynakları (Optional)`);
  lines.push(`- [llms-full.txt](${siteUrl}/llms-full.txt): Sitedeki tüm makalelerin tam metinlerini içeren birleşik dosya (RAG ve derin analiz için).`);
  lines.push(`- [GitHub: @ozdil](https://github.com/ozdil): Açık kaynak depolar, dotfiles ve sistem betikleri.`);
  lines.push(`- [Steam Topluluğu: ozanozdil](https://steamcommunity.com/id/ozanozdil): Linux ve Steam Deck oyuncu profili.`);
  lines.push(`- [nSosyal: @ozanozdil](https://nsosyal.com/ozanozdil): Bağımsız sosyal ağ profili.`);

  return new Response(lines.join('\n') + '\n', {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
