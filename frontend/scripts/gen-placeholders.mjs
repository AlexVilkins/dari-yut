// Генерирует локальные SVG-заглушки для товаров и героя в public/.
// Зачем: внешний picsum.photos недоступен (блокируется/таймаут) → картинки
// не грузятся. Локальные SVG раздаются самим фронтом и работают офлайн.
// Запуск: node scripts/gen-placeholders.mjs
import { mkdirSync, writeFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __dirname = dirname(fileURLToPath(import.meta.url))
const PUBLIC = resolve(__dirname, '..', 'public')

// Палитра в тон бренду (cream / forest / terracotta).
const ITEMS = [
  { file: 'products/dariyut-1.svg', label: 'Полотенца', a: '#f3ede0', b: '#e3d6bf', ink: '#1f4d43' },
  { file: 'products/dariyut-2.svg', label: 'Халаты', a: '#efe7da', b: '#d9c7ad', ink: '#8a5a3c' },
  { file: 'products/dariyut-3.svg', label: 'Пледы', a: '#ede7e2', b: '#cbbfb2', ink: '#5a6b5f' },
  { file: 'products/dariyut-4.svg', label: 'Для кухни', a: '#f1ece1', b: '#ddcdb4', ink: '#b84a3c' },
  { file: 'products/dariyut-5.svg', label: 'Детям', a: '#eaf0ec', b: '#cfe0d4', ink: '#3f7a63' },
  { file: 'products/dariyut-6.svg', label: 'Подушки', a: '#f0e9e6', b: '#d8c5bd', ink: '#9a5b6b' },
  { file: 'products/dariyut-7.svg', label: 'Для кухни', a: '#f1ece1', b: '#ddcdb4', ink: '#b84a3c' },
  { file: 'products/dariyut-8.svg', label: 'Подарки', a: '#f3ede0', b: '#e3d6bf', ink: '#1f4d43' },
  { file: 'hero-1.svg', label: 'Вышивка', a: '#f3ede0', b: '#e3d6bf', ink: '#1f4d43', w: 600, h: 720 },
  { file: 'hero-2.svg', label: 'Текстиль', a: '#f1ece1', b: '#e7d8c2', ink: '#b84a3c', w: 600, h: 760 },
]

function svg({ label, a, b, ink, w = 800, h = 800 }) {
  const cx = w / 2
  const cy = h / 2
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img" aria-label="${label}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="${a}"/>
      <stop offset="1" stop-color="${b}"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.5" cy="0.42" r="0.6">
      <stop offset="0" stop-color="#ffffff" stop-opacity="0.55"/>
      <stop offset="1" stop-color="#ffffff" stop-opacity="0"/>
    </radialGradient>
    <pattern id="stitch" width="34" height="34" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
      <path d="M0 17 h12 M22 17 h12" stroke="${ink}" stroke-opacity="0.10" stroke-width="3" stroke-linecap="round"/>
    </pattern>
  </defs>
  <rect width="${w}" height="${h}" fill="url(#bg)"/>
  <rect width="${w}" height="${h}" fill="url(#stitch)"/>
  <rect width="${w}" height="${h}" fill="url(#glow)"/>
  <g transform="translate(${cx} ${cy - 30})">
    <circle r="96" fill="none" stroke="${ink}" stroke-opacity="0.35" stroke-width="2"/>
    <circle r="96" fill="none" stroke="${ink}" stroke-opacity="0.5" stroke-width="2" stroke-dasharray="2 9" stroke-linecap="round"/>
    <text x="0" y="22" text-anchor="middle" font-family="'Playfair Display', Georgia, serif" font-size="74" font-weight="600" fill="${ink}">ДУ</text>
  </g>
  <text x="${cx}" y="${cy + 120}" text-anchor="middle" font-family="'Onest', system-ui, sans-serif" font-size="30" letter-spacing="6" fill="${ink}" fill-opacity="0.85">${label.toUpperCase()}</text>
  <text x="${cx}" y="${cy + 162}" text-anchor="middle" font-family="'Onest', system-ui, sans-serif" font-size="19" letter-spacing="2" fill="${ink}" fill-opacity="0.55">ДАРИ УЮТ</text>
</svg>
`
}

mkdirSync(resolve(PUBLIC, 'products'), { recursive: true })
for (const item of ITEMS) {
  writeFileSync(resolve(PUBLIC, item.file), svg(item), 'utf8')
  console.log('wrote', item.file)
}
