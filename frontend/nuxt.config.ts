// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-01-01',
  devtools: { enabled: true },

  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    'pinia-plugin-persistedstate/nuxt',
  ],

  css: ['~/assets/css/main.css'],

  // Источник данных — бэкенд FastAPI. Переопределяется переменной окружения
  // NUXT_PUBLIC_API_BASE (например, адрес прод-бэкенда при деплое).
  runtimeConfig: {
    public: {
      apiBase: 'http://localhost:8000',
    },
  },

  app: {
    // Плавный переход между страницами (CSS в assets/css/main.css).
    pageTransition: { name: 'page', mode: 'out-in' },
    head: {
      htmlAttrs: { lang: 'ru' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Махровый Мир — махровые изделия оптом от производителя: банные и кухонные полотенца, халаты, махровые простыни. Опт для отелей, спа, ресторанов и маркетплейсов. Отгрузка по всей России.',
        },
        { name: 'theme-color', content: '#136a63' },
        { property: 'og:site_name', content: 'Махровый Мир' },
        { property: 'og:locale', content: 'ru_RU' },
      ],
      link: [
        { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Onest:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap',
        },
      ],
      script: [
        {
          type: 'application/ld+json',
          innerHTML: JSON.stringify({
            '@context': 'https://schema.org',
            '@type': 'Organization',
            name: 'Махровый Мир',
            description:
              'Оптовый поставщик махровых изделий: банные и кухонные полотенца, халаты, махровые простыни. Опт для отелей, спа, ресторанов и маркетплейсов.',
            url: 'https://махровый-мир.рф',
            telephone: '+7 (921) 579-78-76',
            email: 'dari_yut@mail.ru',
            address: {
              '@type': 'PostalAddress',
              streetAddress: 'пр-т Обуховской обороны 86 лит.3',
              addressLocality: 'Санкт-Петербург',
              addressCountry: 'RU',
            },
            geo: { '@type': 'GeoCoordinates', latitude: 59.8867, longitude: 30.4691 },
            image: 'https://махровый-мир.рф/favicon.svg',
            priceRange: '₽₽',
          }),
        },
      ],
    },
  },
})
