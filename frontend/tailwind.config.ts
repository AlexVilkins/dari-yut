import type { Config } from 'tailwindcss'

// Дизайн-токены лендинга «Дари Уют» (палитра + шрифты).
export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        cream: '#f7f1e6',
        bg: '#fbf7ef',
        'bg-deep': '#f1e8d8',
        fg: '#1e1a17',
        line: '#e8e0d4',
        muted: '#8a8175',
        forest: '#1f4d43',
        'forest-muted': '#356a5d',
        accent: '#b84a3c',
        'accent-hover': '#a23f33',
      },
      fontFamily: {
        heading: ['"Playfair Display"', 'serif'],
        body: ['Onest', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 18px 40px -16px rgba(31, 77, 67, 0.25)',
        card: '0 4px 20px -8px rgba(30, 26, 23, 0.12)',
        glow: '0 12px 30px -10px rgba(184, 74, 60, 0.45)',
      },
      borderRadius: {
        xl2: '1.25rem',
        xl3: '1.75rem',
      },
      transitionTimingFunction: {
        soft: 'cubic-bezier(0.22, 1, 0.36, 1)',
      },
    },
  },
}
