<script setup lang="ts">
const cart = useCartStore()
const auth = useAuthStore()
const { site } = useAppConfig()

const mobileOpen = ref(false)

// Якоря ведут на секции главной (работают и с других страниц через "/#...").
const navLinks = [
  { label: 'О компании', to: '/#about' },
  { label: 'Услуги и прайс', to: '/#services' },
  { label: 'Каталог', to: '/catalog' },
  { label: 'Контакты', to: '/#contact' },
]

async function onLogout() {
  auth.logout()
  mobileOpen.value = false
  await navigateTo('/')
}
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-line bg-bg/85 backdrop-blur">
    <div class="container-x flex h-16 items-center justify-between gap-4">
      <NuxtLink to="/" class="flex items-center gap-3 leading-none" @click="mobileOpen = false">
        <span
          class="flex h-11 w-11 items-center justify-center rounded-full border border-line bg-cream font-heading text-xl text-forest"
          aria-hidden="true"
        >
          Д
        </span>
        <span class="flex flex-col">
          <span class="font-heading text-xl tracking-tight text-forest">{{ site.name }}</span>
          <span class="mt-0.5 text-[0.6rem] uppercase tracking-[0.22em] text-muted">
            {{ site.tagline }}
          </span>
        </span>
      </NuxtLink>

      <!-- Desktop nav -->
      <nav class="hidden items-center gap-1 lg:flex" aria-label="Основная">
        <NuxtLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="rounded-full px-3 py-2 text-sm text-muted transition-colors hover:bg-line/80 hover:text-fg"
        >
          {{ link.label }}
        </NuxtLink>
      </nav>

      <div class="flex items-center gap-1 sm:gap-2">
        <ClientOnly>
          <NuxtLink
            v-if="auth.isAuthenticated"
            to="/account/orders"
            class="hidden rounded-full px-3 py-2 text-sm hover:bg-line/80 sm:inline-flex"
          >
            Мои заявки
          </NuxtLink>
        </ClientOnly>

        <NuxtLink
          to="/cart"
          class="relative rounded-full px-3 py-2 text-sm hover:bg-line/80"
          aria-label="Корзина"
        >
          Корзина
          <ClientOnly>
            <span
              v-if="cart.count > 0"
              class="absolute -right-1 -top-1 inline-flex h-5 min-w-5 items-center justify-center rounded-full bg-accent px-1.5 text-xs font-medium text-cream"
            >
              {{ cart.count }}
            </span>
          </ClientOnly>
        </NuxtLink>

        <ClientOnly>
          <button
            v-if="auth.isAuthenticated"
            class="hidden rounded-full px-3 py-2 text-sm text-muted hover:bg-line/80 sm:inline-flex"
            @click="onLogout"
          >
            Выйти
          </button>
          <NuxtLink v-else to="/login" class="btn-ghost ml-1 hidden sm:inline-flex">Войти</NuxtLink>
        </ClientOnly>

        <!-- Mobile toggle -->
        <button
          type="button"
          class="inline-flex items-center justify-center rounded-full border border-line bg-cream/60 p-2 text-fg lg:hidden"
          :aria-expanded="mobileOpen"
          aria-controls="mobile-menu"
          @click="mobileOpen = !mobileOpen"
        >
          <span class="sr-only">Меню</span>
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path
              :d="mobileOpen ? 'M6 6l12 12M6 18L18 6' : 'M4 7h16M4 12h16M4 17h16'"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
            />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <nav
      v-if="mobileOpen"
      id="mobile-menu"
      class="border-t border-line bg-bg lg:hidden"
      aria-label="Мобильная"
    >
      <div class="container-x flex flex-col py-3">
        <NuxtLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
          @click="mobileOpen = false"
        >
          {{ link.label }}
        </NuxtLink>
        <ClientOnly>
          <NuxtLink
            v-if="auth.isAuthenticated"
            to="/account/orders"
            class="rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
            @click="mobileOpen = false"
          >
            Мои заявки
          </NuxtLink>
          <button
            v-if="auth.isAuthenticated"
            class="rounded-lg px-3 py-2.5 text-left text-sm text-muted hover:bg-bg-deep"
            @click="onLogout"
          >
            Выйти
          </button>
          <NuxtLink
            v-else
            to="/login"
            class="rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
            @click="mobileOpen = false"
          >
            Войти
          </NuxtLink>
        </ClientOnly>
      </div>
    </nav>
  </header>
</template>
