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
    sitemap()
  ],
  markdown: {
    shikiConfig: {
      theme: 'github-dark',
      wrap: true
    }
  }
});
