import type { Category, Product } from '~/types'

// Категории каталога (mock).
export const categories: Category[] = [
  { slug: 'towels', name: 'Полотенца' },
  { slug: 'robes', name: 'Халаты' },
  { slug: 'blankets', name: 'Пледы' },
  { slug: 'kitchen', name: 'Для кухни' },
  { slug: 'kids', name: 'Детям' },
  { slug: 'pillows', name: 'Подушки' },
  { slug: 'gifts', name: 'Подарочные наборы' },
]

// Моковый каталог. Когда появится FastAPI — эти роуты удаляются,
// а фронт ходит напрямую в backend через runtimeConfig.public.apiBase.
export const mockProducts: Product[] = [
  {
    id: 1,
    name: 'Банное полотенце с вышивкой инициалов',
    slug: 'bannoe-polotence-initsialy',
    category: 'towels',
    description:
      'Плотное хлопковое полотенце 70×140 см с индивидуальной вышивкой инициалов. Идеальный подарок к свадьбе или новоселью.',
    price: 1290,
    image_url: 'https://picsum.photos/seed/dariyut-1/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 2,
    name: 'Махровый халат с именной вышивкой',
    slug: 'mahrovyy-halat-imennoy',
    category: 'robes',
    description:
      'Уютный махровый халат с вышитым именем или монограммой. Мягкий хлопок, аккуратная отделка, размеры S–XXL.',
    price: 3490,
    image_url: 'https://picsum.photos/seed/dariyut-2/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 3,
    name: 'Плед с вышитой надписью',
    slug: 'pled-vyshitaya-nadpis',
    category: 'blankets',
    description:
      'Тёплый плед 130×170 см с персональной вышитой надписью. Приятная фактура, подойдёт для дома и в подарок.',
    price: 2790,
    image_url: 'https://picsum.photos/seed/dariyut-3/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 4,
    name: 'Набор кухонных полотенец «Уют»',
    slug: 'nabor-kuhonnyh-polotenec-uyut',
    category: 'kitchen',
    description:
      'Комплект из трёх льняных полотенец с декоративной вышивкой. Практичный и стильный акцент на кухне.',
    price: 1490,
    image_url: 'https://picsum.photos/seed/dariyut-4/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 5,
    name: 'Детское полотенце с уголком и вышивкой',
    slug: 'detskoe-polotence-ugolok',
    category: 'kids',
    description:
      'Мягкое детское полотенце с капюшоном-уголком и вышивкой имени малыша. Гипоаллергенный хлопок.',
    price: 1690,
    image_url: 'https://picsum.photos/seed/dariyut-5/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 6,
    name: 'Подушка декоративная с монограммой',
    slug: 'podushka-dekorativnaya-monogramma',
    category: 'pillows',
    description:
      'Декоративная подушка 45×45 см с вышитой монограммой. Съёмный чехол, наполнитель в комплекте.',
    price: 1990,
    image_url: 'https://picsum.photos/seed/dariyut-6/800/800',
    in_stock: false,
    is_active: true,
  },
  {
    id: 7,
    name: 'Фартук с именной вышивкой',
    slug: 'fartuk-imennaya-vyshivka',
    category: 'kitchen',
    description:
      'Льняной фартук с вышивкой имени или забавной надписи. Регулируемые завязки, удобный карман.',
    price: 1390,
    image_url: 'https://picsum.photos/seed/dariyut-7/800/800',
    in_stock: true,
    is_active: true,
  },
  {
    id: 8,
    name: 'Свадебный набор полотенец с датой',
    slug: 'svadebnyy-nabor-polotenec',
    category: 'gifts',
    description:
      'Парный набор полотенец с вышитыми именами молодожёнов и датой свадьбы. Подарочная упаковка.',
    price: 2990,
    image_url: 'https://picsum.photos/seed/dariyut-8/800/800',
    in_stock: true,
    is_active: true,
  },
]

export function getActiveProducts(category?: string): Product[] {
  return mockProducts.filter(
    (p) => p.is_active && (!category || p.category === category),
  )
}

export function getProductBySlug(slug: string): Product | undefined {
  return mockProducts.find((p) => p.slug === slug && p.is_active)
}

// Только категории, в которых есть активные товары.
export function getActiveCategories(): Category[] {
  const used = new Set(getActiveProducts().map((p) => p.category))
  return categories.filter((c) => used.has(c.slug))
}
