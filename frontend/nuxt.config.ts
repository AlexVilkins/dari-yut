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

  // Источник данных. Сейчас указывает на встроенные mock-роуты Nitro (/api/*).
  // Когда появится FastAPI — поменять apiBase на его адрес.
  runtimeConfig: {
    public: {
      apiBase: '/api',
    },
  },

  app: {
    head: {
      htmlAttrs: { lang: 'ru' },
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            'Профессиональная машинная вышивка в Санкт-Петербурге: корпоративная символика, подарки, домашний текстиль. Опыт 5+ лет, тираж и единичные заказы.',
        },
      ],
      link: [
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
            '@type': 'LocalBusiness',
            name: 'Дари Уют',
            description:
              'Профессиональная машинная вышивка в Санкт-Петербурге. Корпоративная символика, подарки, текстиль, шевроны. Опыт 5+ лет.',
            url: 'https://дари-уют.рф',
            telephone: '+7 (921) 579-78-76',
            email: 'dari_yut@mail.ru',
            address: {
              '@type': 'PostalAddress',
              streetAddress: 'пр-т Обуховской обороны 86 лит.3',
              addressLocality: 'Санкт-Петербург',
              addressCountry: 'RU',
            },
            geo: { '@type': 'GeoCoordinates', latitude: 59.8867, longitude: 30.4691 },
            image: 'https://дари-уют.рф/logo/logo.png',
            priceRange: '₽₽',
          }),
        },
      ],
    },
  },
})
