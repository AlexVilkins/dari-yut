<script setup lang="ts">
const cart = useCartStore()
const auth = useAuthStore()
const route = useRoute()
const cartDrawer = useCartDrawer()

const mobileOpen = ref(false)
const scrolled = ref(false)

// Разделы: главная (логотип), каталог, доставка, контакты.
const navLinks = [
  { label: 'Каталог', to: '/catalog' },
  { label: 'Доставка', to: '/delivery' },
  { label: 'Контакты', to: '/#contact' },
]

// Подсветка активного раздела по текущему пути.
function isActive(to: string) {
  if (to === '/catalog') return route.path.startsWith('/catalog')
  if (to === '/delivery') return route.path.startsWith('/delivery')
  return false
}

function onScroll() {
  scrolled.value = window.scrollY > 8
}
onMounted(() => {
  onScroll()
  window.addEventListener('scroll', onScroll, { passive: true })
})
onUnmounted(() => window.removeEventListener('scroll', onScroll))

async function onLogout() {
  auth.logout()
  mobileOpen.value = false
  await navigateTo('/')
}
</script>

<template>
  <header
    class="sticky top-0 z-40 border-b transition-all duration-300"
    :class="
      scrolled
        ? 'border-line bg-bg/85 shadow-card backdrop-blur'
        : 'border-transparent bg-bg/60 backdrop-blur-sm'
    "
  >
    <div class="container-x flex h-16 items-center justify-between gap-4">
      <NuxtLink to="/" class="group text-forest" aria-label="Дари Уют — на главную" @click="mobileOpen = false">
        <AppLogo variant="full" :size="44" class="transition-transform duration-300 group-hover:-rotate-3" />
      </NuxtLink>

      <!-- Desktop nav -->
      <nav class="hidden items-center gap-1 lg:flex" aria-label="Основная">
        <NuxtLink
          v-for="link in navLinks"
          :key="link.to"
          :to="link.to"
          class="relative rounded-full px-3.5 py-2 text-sm transition-colors"
          :class="
            isActive(link.to)
              ? 'text-forest'
              : 'text-muted hover:bg-line/60 hover:text-fg'
          "
        >
          {{ link.label }}
          <span
            v-if="isActive(link.to)"
            class="absolute inset-x-3.5 -bottom-px h-0.5 rounded-full bg-accent"
          />
        </NuxtLink>
      </nav>

      <div class="flex items-center gap-1 sm:gap-1.5">
        <ClientOnly>
          <NuxtLink
            v-if="auth.isAuthenticated"
            to="/account/orders"
            class="hidden items-center gap-2 rounded-full px-3 py-2 text-sm text-muted transition-colors hover:bg-line/60 hover:text-fg sm:inline-flex"
          >
            <AppIcon name="package" :size="18" />
            Мои заявки
          </NuxtLink>
        </ClientOnly>

        <button
          type="button"
          class="relative inline-flex h-10 w-10 items-center justify-center rounded-full text-fg transition-colors hover:bg-line/60"
          aria-label="Открыть корзину"
          @click="cartDrawer.open()"
        >
          <AppIcon name="cart" :size="21" />
          <ClientOnly>
            <span
              v-if="cart.count > 0"
              class="absolute -right-0.5 -top-0.5 inline-flex h-5 min-w-5 items-center justify-center rounded-full bg-accent px-1.5 text-xs font-medium text-cream shadow-sm"
            >
              {{ cart.count }}
            </span>
          </ClientOnly>
        </button>

        <ClientOnly>
          <button
            v-if="auth.isAuthenticated"
            class="hidden h-10 w-10 items-center justify-center rounded-full text-muted transition-colors hover:bg-line/60 hover:text-fg sm:inline-flex"
            aria-label="Выйти"
            title="Выйти"
            @click="onLogout"
          >
            <AppIcon name="logout" :size="19" />
          </button>
          <NuxtLink v-else to="/login" class="btn-ghost ml-1 hidden sm:inline-flex">
            <AppIcon name="user" :size="18" />
            Войти
          </NuxtLink>
        </ClientOnly>

        <!-- Mobile toggle -->
        <button
          type="button"
          class="inline-flex h-10 w-10 items-center justify-center rounded-full border border-line bg-cream/60 text-fg lg:hidden"
          :aria-expanded="mobileOpen"
          aria-controls="mobile-menu"
          @click="mobileOpen = !mobileOpen"
        >
          <span class="sr-only">Меню</span>
          <AppIcon :name="mobileOpen ? 'close' : 'menu'" :size="22" />
        </button>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="-translate-y-2 opacity-0"
      leave-active-class="transition duration-150 ease-in"
      leave-to-class="-translate-y-2 opacity-0"
    >
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
          <div class="my-2 h-px stitch" />
          <ClientOnly>
            <NuxtLink
              v-if="auth.isAuthenticated"
              to="/account/orders"
              class="flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
              @click="mobileOpen = false"
            >
              <AppIcon name="package" :size="18" /> Мои заявки
            </NuxtLink>
            <button
              v-if="auth.isAuthenticated"
              class="flex items-center gap-2 rounded-lg px-3 py-2.5 text-left text-sm text-muted hover:bg-bg-deep"
              @click="onLogout"
            >
              <AppIcon name="logout" :size="18" /> Выйти
            </button>
            <NuxtLink
              v-else
              to="/login"
              class="flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
              @click="mobileOpen = false"
            >
              <AppIcon name="user" :size="18" /> Войти
            </NuxtLink>
          </ClientOnly>
        </div>
      </nav>
    </Transition>
  </header>
</template>
