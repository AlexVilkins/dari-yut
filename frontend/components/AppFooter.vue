<script setup lang="ts">
const { site } = useAppConfig()
const year = new Date().getFullYear()
</script>

<template>
  <footer class="relative z-10 mt-20">
    <!-- CTA-полоса -->
    <div class="container-x">
      <div
        class="relative overflow-hidden rounded-xl3 bg-forest px-6 py-12 text-cream shadow-soft sm:px-12 sm:py-14"
      >
        <div
          class="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-accent/20 blur-3xl"
          aria-hidden="true"
        />
        <div
          class="pointer-events-none absolute -bottom-20 left-1/4 h-56 w-56 rounded-full bg-cream/10 blur-3xl"
          aria-hidden="true"
        />
        <div class="relative grid gap-6 sm:grid-cols-[1.4fr_1fr] sm:items-center">
          <div>
            <p class="font-heading text-[clamp(1.6rem,3.5vw,2.4rem)] leading-tight">
              Оптовые поставки махровых изделий
            </p>
            <p class="mt-3 max-w-md text-cream/70">
              Полотенца, халаты и махровые простыни от производителя. Запросите
              актуальный опт-прайс — подберём ассортимент под ваш объём.
            </p>
          </div>
          <div class="flex flex-wrap gap-3 sm:justify-end">
            <a :href="site.phoneHref" class="btn-accent btn-lg">
              <AppIcon name="phone" :size="18" /> Позвонить
            </a>
            <a :href="site.telegram" target="_blank" rel="noopener" class="btn-ghost btn-lg bg-cream/10 text-cream hover:bg-cream/20">
              <AppIcon name="telegram" :size="18" /> Telegram
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Линки -->
    <div class="mt-14 border-t border-line bg-bg-deep/60">
      <div class="container-x grid gap-8 py-12 sm:grid-cols-2 lg:grid-cols-4">
        <div>
          <div class="text-forest">
            <AppLogo variant="full" :size="40" />
          </div>
          <p class="mt-4 text-sm text-muted">Махровые изделия оптом · Санкт-Петербург</p>
          <p class="mt-3 text-sm italic text-muted">«{{ site.slogan }}»</p>
        </div>

        <div class="text-sm">
          <p class="eyebrow mb-4">Навигация</p>
          <ul class="space-y-2.5">
            <li><NuxtLink to="/services" class="text-muted transition-colors hover:text-forest">Оптовикам</NuxtLink></li>
            <li><NuxtLink to="/catalog" class="text-muted transition-colors hover:text-forest">Каталог</NuxtLink></li>
            <li><NuxtLink to="/delivery" class="text-muted transition-colors hover:text-forest">Доставка и оплата</NuxtLink></li>
            <li><NuxtLink to="/#contact" class="text-muted transition-colors hover:text-forest">Контакты</NuxtLink></li>
          </ul>
        </div>

        <div class="text-sm">
          <p class="eyebrow mb-4">Контакты</p>
          <ul class="space-y-2.5 text-muted">
            <li>
              <a :href="site.phoneHref" class="inline-flex items-center gap-2 transition-colors hover:text-forest">
                <AppIcon name="phone" :size="16" /> {{ site.phone }}
              </a>
            </li>
            <li>
              <a :href="`mailto:${site.email}`" class="inline-flex items-center gap-2 transition-colors hover:text-forest">
                <AppIcon name="mail" :size="16" /> {{ site.email }}
              </a>
            </li>
            <li>
              <a :href="site.telegram" target="_blank" rel="noopener" class="inline-flex items-center gap-2 transition-colors hover:text-forest">
                <AppIcon name="telegram" :size="16" /> Telegram
              </a>
            </li>
          </ul>
        </div>

        <div class="text-sm">
          <p class="eyebrow mb-4">Адрес</p>
          <p class="inline-flex items-start gap-2 text-muted">
            <AppIcon name="mapPin" :size="16" class="mt-0.5" /> {{ site.address }}
          </p>
        </div>
      </div>

      <div class="border-t border-line/70">
        <div class="container-x py-5 text-xs text-muted">
          © {{ year }} {{ site.name }} · Махровые изделия оптом
        </div>
      </div>
    </div>
  </footer>
</template>
