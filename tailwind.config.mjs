/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: {
          light: '#f8fafc',
          dark: '#08090b',
        },
        surface: {
          light: '#ffffff',
          dark: '#0e1116',
        },
        qs: {
          black: '#08090b',
          panel: '#0e1116',
          surface: '#141820',
          hover: '#1b202a',
          border: 'rgba(255, 255, 255, 0.08)',
          'border-bright': 'rgba(255, 255, 255, 0.16)',
          accent: '#00ffcc',
          'accent-dim': '#00ffcc22',
          muted: '#707880',
          foreground: '#cacccc',
          emerald: '#10b981',
          cyan: '#06b6d4',
          amber: '#f59e0b',
          rose: '#f43f5e',
        },
        mai: {
          oat: '#fef9ed',
          linen: '#F5F0E4',
          sand: '#FBF4E5',
          cocoa: '#5D524B',
          'cocoa-soft': '#8C7E74',
          peach: '#FBD3BE',
          terracotta: '#E1734B',
          sage: '#D7E6D6',
          mint: '#EAEFE1',
          'mint-ink': '#2E4D4D',
          plum: '#4D2A33',
          taupe: '#D1CABB',
          bronze: '#A67C52',
          dark: {
            bg: '#141210',
            surface: '#1f1a17',
            card: '#26201c',
            border: '#2d2521',
            text: '#fef9ed',
            muted: '#a89f91',
          }
        }
      },
      fontFamily: {
        sans: ['Inter', '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', '"Noto Sans"', 'sans-serif'],
        serif: ['"Bradford LL"', '"Newsreader"', '"Iowan Old Style"', 'Palatino', 'Georgia', 'serif'],
        mono: ['"Red Hat Mono"', '"JetBrains Mono"', 'ui-monospace', 'SFMono-Regular', 'Menlo', 'monospace'],
      }
    },
  },
  plugins: [],
};
