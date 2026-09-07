/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        gh: {
          bg: 'var(--color-gh-bg)',
          subtle: 'var(--color-gh-subtle)',
          border: 'var(--color-gh-border)',
          borderMuted: 'var(--color-gh-border-muted)',
          text: 'var(--color-gh-text)',
          textMuted: 'var(--color-gh-text-muted)',
          link: 'var(--color-gh-link)',
          green: '#238636',
          greenHover: '#2ea043',
          badge: 'var(--color-gh-badge)',
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', '"Noto Sans"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      }
    },
  },
  plugins: [],
};
