import type { Config } from 'tailwindcss'

// Дизайн-токены бренда «Махровый Мир» — махровые изделия оптом (палитра + шрифты).
// Тёплый хлопковый фон + спа-бирюза как основной цвет + мягкий терракотовый акцент.
// Имена токенов (forest/accent/cream) сохранены из прошлого макета, чтобы не
// переписывать все классы — поменялись только значения цветов.
export default <Partial<Config>>{
  theme: {
    extend: {
      colors: {
        cream: '#fbf6ee',
        bg: '#fbf7f1',
        'bg-deep': '#f0e9dd',
        fg: '#1f1c19',
        line: '#e9e0d2',
        muted: '#8b8377',
        // «forest» → спа-бирюза (основной цвет бренда).
        forest: '#136a63',
        'forest-muted': '#1f877d',
        // мягкий тёплый терракот (акцент, CTA, распродажи).
        accent: '#c96a48',
        'accent-hover': '#b1573a',
      },
      fontFamily: {
        heading: ['"Playfair Display"', 'serif'],
        body: ['Onest', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        soft: '0 18px 40px -16px rgba(19, 106, 99, 0.28)',
        card: '0 4px 20px -8px rgba(31, 28, 25, 0.12)',
        glow: '0 12px 30px -10px rgba(201, 106, 72, 0.45)',
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
