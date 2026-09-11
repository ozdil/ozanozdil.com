import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const siteUrl = context.site ? context.site.toString().replace(/\/$/, '') : 'https://ozanozdil.com';
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  const lines = [
    `# Ozan Özdil — Tam Dokümantasyon & Makaleler (llms-full.txt)`,
    ``,
    `> Bu dosya; AI botları, LLM'ler ve otonom araştırma ajanları için Ozan Özdil web sitesindeki tüm teknik makaleleri tam metin olarak bir araya getirmektedir.`,
    `> Kaynak: ${siteUrl}`,
    ``,
    `---`,
    ``,
  ];

  for (const post of sortedPosts) {
    const dateStr = post.data.pubDate.toISOString().split('T')[0];
    lines.push(`## ${post.data.title}`);
    lines.push(``);
    lines.push(`- **URL:** ${siteUrl}/blog/${post.slug}`);
    lines.push(`- **Tarih:** ${dateStr}`);
    if (post.data.tags && post.data.tags.length > 0) {
      lines.push(`- **Etiketler:** ${post.data.tags.join(', ')}`);
    }
    if (post.data.description) {
      lines.push(`- **Özet:** ${post.data.description}`);
    }
    lines.push(``);
    lines.push(post.body.trim());
    lines.push(``);
    lines.push(`---`);
    lines.push(``);
  }

  return new Response(lines.join('\n') + '\n', {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
