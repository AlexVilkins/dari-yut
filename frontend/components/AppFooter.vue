<script setup lang="ts">
const { site } = useAppConfig()
const year = new Date().getFullYear()
</script>

<template>
  <footer class="mt-16 border-t border-line bg-bg-deep">
    <div class="container-x grid gap-8 py-12 sm:grid-cols-2 lg:grid-cols-4">
      <div>
        <p class="font-heading text-lg text-forest">{{ site.name }}</p>
        <p class="mt-1 text-sm text-muted">Мастерская машинной вышивки · Санкт-Петербург</p>
        <p class="mt-3 text-sm italic text-muted">«{{ site.slogan }}»</p>
      </div>

      <div class="text-sm">
        <p class="eyebrow mb-3">Навигация</p>
        <ul class="space-y-2">
          <li><NuxtLink to="/catalog" class="text-muted hover:text-forest">Каталог</NuxtLink></li>
          <li><NuxtLink to="/#about" class="text-muted hover:text-forest">О компании</NuxtLink></li>
          <li><NuxtLink to="/#services" class="text-muted hover:text-forest">Услуги и прайс</NuxtLink></li>
          <li><NuxtLink to="/#contact" class="text-muted hover:text-forest">Контакты</NuxtLink></li>
        </ul>
      </div>

      <div class="text-sm">
        <p class="eyebrow mb-3">Контакты</p>
        <ul class="space-y-2 text-muted">
          <li><a :href="site.phoneHref" class="hover:text-forest">{{ site.phone }}</a></li>
          <li><a :href="`mailto:${site.email}`" class="hover:text-forest">{{ site.email }}</a></li>
          <li><a :href="site.telegram" class="hover:text-forest" target="_blank" rel="noopener">Telegram</a></li>
        </ul>
      </div>

      <div class="text-sm">
        <p class="eyebrow mb-3">Адрес</p>
        <p class="text-muted">{{ site.address }}</p>
      </div>
    </div>

    <div class="border-t border-line/70">
      <div class="container-x py-5 text-xs text-muted">
        ИП Черноземов М.О. · © {{ year }} {{ site.name }}
      </div>
    </div>
  </footer>
</template>
