import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const siteUrl = context.site ? context.site.toString().replace(/\/$/, '') : 'https://ozanozdil.com';
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const lines = [
    `# Ozan Özdil`,
    ``,
    `> Ozan Özdil (@ozdil) resmi web sitesi ve bilgi tabanı. YZ Kodcusu, açık kaynak sistemler ve dağıtım okuryazarlığı (Omarchy, CachyOS, Arch Linux), Steam Deck odaklı Linux oyunculuğu ve orta format mimari/doğa fotoğrafçılığı.`,
    ``,
    `## Ana Sayfalar & Portfolyo`,
    `- [Ana Sayfa](${siteUrl}/): Ozan Özdil biyografisi, sistem okuryazarlığı, yerel ve bulut YZ çalışma modelleri, kamu koordinasyonu deneyimi.`,
    `- [Yazılar & Notlar](${siteUrl}/blog): Linux sistemleri, Wayland mimarisi, donanım optimizasyonu, siber güvenlik ve dijital egemenlik üzerine teknik makaleler.`,
    `- [Açık Kaynak Projeler](${siteUrl}/projeler): Açık kaynak sistem yapılandırmaları, QuickShell modülleri, Wayland araçları ve güvenlik yazılımları.`,
    `- [Fotoğraf Galerisi](${siteUrl}/galeri): Fujifilm GFX 50R ve GFX 100 ile çekilmiş UNESCO ahşap camileri, Ağlı Kalesi ve Karadeniz rotaları.`,
    `- [RSS Beslemesi](${siteUrl}/rss.xml): Güncel içerik bildirimleri için RSS 2.0 XML kaynağı.`,
    ``,
    `## Yazılar & Makale Kütüphanesi`,
  ];

  for (const post of sortedPosts) {
    const dateStr = post.data.pubDate.toISOString().split('T')[0];
    const desc = post.data.description ? post.data.description.replace(/\n+/g, ' ').trim() : '';
    lines.push(`- [${post.data.title}](${siteUrl}/blog/${post.slug}): (${dateStr}) ${desc}`);
  }

  lines.push(``);
  lines.push(`## İsteğe Bağlı & Ek Kaynaklar`);
  lines.push(`- [llms-full.txt](${siteUrl}/llms-full.txt): Sitedeki tüm makalelerin tam metinlerini içeren birleşik dosya.`);
  lines.push(`- [GitHub: @ozdil](https://github.com/ozdil): Açık kaynak depolar, dotfiles ve sistem betikleri.`);
  lines.push(`- [Steam Topluluğu](https://steamcommunity.com/id/ozanozdil): Linux ve Steam Deck oyuncu profili.`);

  return new Response(lines.join('\n') + '\n', {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
