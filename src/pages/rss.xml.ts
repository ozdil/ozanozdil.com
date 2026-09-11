import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';

export async function GET(context: APIContext) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sortedPosts = posts.sort((a, b) => b.data.pubDate.valueOf() - a.data.pubDate.valueOf());

  return rss({
    title: 'Ozan Özdil (@ozdil) — Açık Kaynak, Sistemler & YZ',
    description: 'YZ Kodcusu. Açık kaynak sistem okuryazarlığı, Omarchy ve CachyOS takibi, Steam Deck ile Linux oyunculuğu ve orta format fotoğrafçılık.',
    site: context.site || 'https://ozanozdil.com',
    items: sortedPosts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      description: post.data.description,
      categories: post.data.tags || [],
      link: `/blog/${post.slug}/`,
    })),
    customData: `<language>tr-TR</language><managingEditor>ozdil@ozanozdil.com (Ozan Özdil)</managingEditor><webMaster>ozdil@ozanozdil.com (Ozan Özdil)</webMaster>`,
  });
}
