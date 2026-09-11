import { defineConfig, passthroughImageService } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import sitemap from '@astrojs/sitemap';

import legacyRedirects from './src/data/redirects.json';

export default defineConfig({
  site: 'https://ozanozdil.com',
  redirects: legacyRedirects,
  image: {
    service: passthroughImageService(),
  },
  integrations: [
    tailwind(),
    sitemap({
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      serialize(item) {
        const url = item.url.replace(/\/$/, '');
        if (url === 'https://ozanozdil.com') {
          item.changefreq = 'daily';
          item.priority = 1.0;
        } else if (url === 'https://ozanozdil.com/blog') {
          item.changefreq = 'daily';
          item.priority = 0.9;
        } else if (url.startsWith('https://ozanozdil.com/blog/')) {
          item.changefreq = 'monthly';
          item.priority = 0.8;
        } else if (url === 'https://ozanozdil.com/projeler' || url === 'https://ozanozdil.com/galeri') {
          item.changefreq = 'weekly';
          item.priority = 0.8;
        } else if (url === 'https://ozanozdil.com/hakkimda') {
          item.changefreq = 'monthly';
          item.priority = 0.7;
        }
        return item;
      }
    })
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true
    }
  }
});
