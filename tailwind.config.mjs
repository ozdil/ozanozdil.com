/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: '#09090b',
        surface: {
          DEFAULT: '#121215',
          subtle: '#18181b',
          card: '#121215',
          cardHover: '#18181b',
          border: '#27272a',
          borderSubtle: '#1f1f23',
          borderHover: '#3f3f46',
        }
      },
      fontFamily: {
        sans: ['"JetBrainsMono Nerd Font"', '"JetBrains Mono"', 'monospace'],
        serif: ['"JetBrainsMono Nerd Font"', '"JetBrains Mono"', 'monospace'],
        mono: ['"JetBrainsMono Nerd Font"', '"JetBrains Mono"', 'monospace'],
      }
    },
  },
  plugins: [],
};
