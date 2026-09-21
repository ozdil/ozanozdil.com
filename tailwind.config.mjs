/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        pcb: {
          base: '#3b0508',
          dark: '#260204',
          deep: '#190102',
          surface: '#2e0306',
          card: '#44060a',
          cardHover: '#52080d',
          border: 'rgba(229, 193, 88, 0.25)',
          trace: 'rgba(229, 193, 88, 0.12)',
        },
        gold: {
          DEFAULT: '#e5c158',
          light: '#f3e5ab',
          dark: '#c5a059',
          muted: '#a88a38',
        },
        silver: {
          DEFAULT: '#c5cbd3',
          light: '#f1f5f9',
          dark: '#94a3b8',
          muted: '#64748b',
        }
      },
      fontFamily: {
        sans: ['"JetBrainsMono Nerd Font"', '"JetBrains Mono"', 'monospace'],
        serif: ['"Bradford LL"', '"Newsreader"', '"Iowan Old Style"', 'Palatino', 'Georgia', 'serif'],
        mono: ['"JetBrainsMono Nerd Font"', '"JetBrains Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
};
