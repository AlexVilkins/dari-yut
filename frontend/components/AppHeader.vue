<script setup lang="ts">
import type { Category } from "~/types";

const { site } = useAppConfig();
const cart = useCartStore();
const auth = useAuthStore();
const route = useRoute();
const cartDrawer = useCartDrawer();

const mobileOpen = ref(false);
const scrolled = ref(false);

// Категории для выпадающего меню «Каталог» (кешируются общим ключом).
const { data: categories } = await useApiFetch<Category[]>("/categories", {
  key: "categories",
});

// Разделы: оптовикам, каталог, доставка, контакты. У «Каталога» — мега-меню.
const navLinks = [
  { label: "Оптовикам", to: "/services" },
  { label: "Каталог", to: "/catalog", mega: true },
  { label: "Доставка", to: "/delivery" },
  { label: "Контакты", to: "/#contact" },
];

// Подсветка активного раздела по текущему пути / якорю.
function isActive(link: { to: string }) {
  if (link.to === "/services") return route.path.startsWith("/services");
  if (link.to === "/catalog") return route.path.startsWith("/catalog");
  if (link.to === "/delivery") return route.path.startsWith("/delivery");
  if (link.to === "/#contact")
    return route.path === "/" && route.hash === "#contact";
  return false;
}

function onScroll() {
  scrolled.value = window.scrollY > 8;
}
onMounted(() => {
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
});
onUnmounted(() => window.removeEventListener("scroll", onScroll));

// Закрываем мобильное меню при любой смене маршрута.
watch(
  () => route.fullPath,
  () => (mobileOpen.value = false),
);

async function onLogout() {
  auth.logout();
  mobileOpen.value = false;
  await navigateTo("/");
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
      <NuxtLink
        to="/"
        class="group shrink-0 text-forest"
        aria-label="Махровый Мир — на главную"
        @click="mobileOpen = false"
      >
        <AppLogo
          variant="full"
          :size="44"
          class="transition-transform duration-300 group-hover:-rotate-3"
        />
      </NuxtLink>

      <!-- Desktop nav -->
      <nav class="hidden items-center gap-1 lg:flex" aria-label="Основная">
        <template v-for="link in navLinks" :key="link.to">
          <!-- «Каталог» с выпадающим меню категорий -->
          <div v-if="link.mega" class="group relative">
            <NuxtLink
              :to="link.to"
              class="relative inline-flex items-center gap-1 rounded-full px-3.5 py-2 text-sm transition-colors"
              :class="
                isActive(link)
                  ? 'text-forest'
                  : 'text-muted hover:bg-line/60 hover:text-fg'
              "
            >
              {{ link.label }}
              <AppIcon
                name="chevronRight"
                :size="14"
                class="rotate-90 transition-transform group-hover:translate-y-0.5"
              />
              <span
                v-if="isActive(link)"
                class="absolute inset-x-3.5 -bottom-px h-0.5 rounded-full bg-accent"
              />
            </NuxtLink>

            <!-- Dropdown: появляется по hover / фокусу -->
            <div
              class="invisible absolute left-1/2 top-full z-50 w-64 -translate-x-1/2 translate-y-1 pt-2 opacity-0 transition-all duration-150 group-hover:visible group-hover:translate-y-0 group-hover:opacity-100 group-focus-within:visible group-focus-within:translate-y-0 group-focus-within:opacity-100"
            >
              <div class="card overflow-hidden p-2">
                <NuxtLink
                  to="/catalog"
                  class="flex items-center justify-between rounded-xl px-3 py-2 text-sm font-medium text-fg transition-colors hover:bg-bg-deep"
                >
                  Все товары
                  <AppIcon name="arrowRight" :size="16" class="text-muted" />
                </NuxtLink>
                <div class="my-1 h-px stitch" />
                <NuxtLink
                  v-for="c in categories"
                  :key="c.slug"
                  :to="{ path: '/catalog', query: { category: c.slug } }"
                  class="block rounded-xl px-3 py-2 text-sm text-muted transition-colors hover:bg-bg-deep hover:text-fg"
                >
                  {{ c.name }}
                </NuxtLink>
              </div>
            </div>
          </div>

          <!-- Обычная ссылка -->
          <NuxtLink
            v-else
            :to="link.to"
            class="relative rounded-full px-3.5 py-2 text-sm transition-colors"
            :class="
              isActive(link)
                ? 'text-forest'
                : 'text-muted hover:bg-line/60 hover:text-fg'
            "
          >
            {{ link.label }}
            <span
              v-if="isActive(link)"
              class="absolute inset-x-3.5 -bottom-px h-0.5 rounded-full bg-accent"
            />
          </NuxtLink>
        </template>
      </nav>

      <div class="flex items-center gap-1 sm:gap-1.5">
        <!-- Телефон + CTA «Рассчитать» -->
        <a
          :href="site.phoneHref"
          class="hidden items-center gap-2 rounded-full px-3 py-2 text-sm font-medium text-nowrap text-fg transition-colors hover:bg-line/60 xl:inline-flex"
        >
          <AppIcon name="phone" :size="17" /> {{ site.phone }}
        </a>
        <NuxtLink
          to="/services#quote"
          class="btn-accent hidden lg:inline-flex text-nowrap"
        >
          Опт-прайс
        </NuxtLink>

        <ClientOnly>
          <NuxtLink
            v-if="auth.isAuthenticated"
            to="/account/orders"
            class="ml-1 hidden h-10 w-10 items-center justify-center rounded-full text-muted transition-colors hover:bg-line/60 hover:text-fg sm:inline-flex"
            aria-label="Мои заявки"
            title="Мои заявки"
          >
            <AppIcon name="package" :size="20" />
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
          <NuxtLink
            v-else
            to="/login"
            class="btn-ghost ml-1 hidden sm:inline-flex"
          >
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
        class="max-h-[calc(100dvh-4rem)] overflow-y-auto border-t border-line bg-bg lg:hidden"
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

          <!-- Категории каталога -->
          <div
            v-if="categories?.length"
            class="mt-1 rounded-lg bg-bg-deep/40 p-2"
          >
            <p class="px-2 py-1 text-xs uppercase tracking-wider text-muted">
              Категории
            </p>
            <div class="flex flex-wrap gap-2 px-1 pt-1">
              <NuxtLink
                v-for="c in categories"
                :key="c.slug"
                :to="{ path: '/catalog', query: { category: c.slug } }"
                class="chip"
                @click="mobileOpen = false"
              >
                {{ c.name }}
              </NuxtLink>
            </div>
          </div>

          <div class="my-2 h-px stitch" />

          <a
            :href="site.phoneHref"
            class="flex items-center gap-2 rounded-lg px-3 py-2.5 text-sm hover:bg-bg-deep"
          >
            <AppIcon name="phone" :size="18" /> {{ site.phone }}
          </a>
          <NuxtLink
            to="/services#quote"
            class="btn-accent mt-2"
            @click="mobileOpen = false"
          >
            Запросить опт-прайс
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
