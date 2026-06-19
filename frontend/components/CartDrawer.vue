<script setup lang="ts">
const cart = useCartStore()
const { isOpen, close } = useCartDrawer()
const { formatPrice } = useFormat()

// Закрываем по Esc и блокируем прокрутку фона, пока открыта панель.
watch(isOpen, (v) => {
  if (!import.meta.client) return
  document.body.style.overflow = v ? 'hidden' : ''
})

function onKey(e: KeyboardEvent) {
  if (e.key === 'Escape') close()
}
onMounted(() => window.addEventListener('keydown', onKey))
onUnmounted(() => {
  window.removeEventListener('keydown', onKey)
  if (import.meta.client) document.body.style.overflow = ''
})

function goCheckout() {
  close()
  navigateTo('/checkout')
}
function goCart() {
  close()
  navigateTo('/cart')
}
</script>

<template>
  <ClientOnly>
    <Teleport to="body">
      <!-- Затемнение -->
      <Transition
        enter-active-class="transition-opacity duration-300"
        enter-from-class="opacity-0"
        leave-active-class="transition-opacity duration-200"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isOpen"
          class="fixed inset-0 z-[90] bg-fg/40 backdrop-blur-sm"
          aria-hidden="true"
          @click="close"
        />
      </Transition>

      <!-- Панель -->
      <Transition
        enter-active-class="transition-transform duration-300 ease-soft"
        enter-from-class="translate-x-full"
        leave-active-class="transition-transform duration-200 ease-in"
        leave-to-class="translate-x-full"
      >
        <aside
          v-if="isOpen"
          class="fixed inset-y-0 right-0 z-[95] flex w-full max-w-md flex-col bg-bg shadow-soft"
          role="dialog"
          aria-modal="true"
          aria-label="Корзина"
        >
          <header class="flex items-center justify-between border-b border-line px-5 py-4">
            <div class="flex items-center gap-2">
              <AppIcon name="cart" :size="20" class="text-forest" />
              <h2 class="font-heading text-lg">Корзина</h2>
              <span v-if="cart.count" class="tnum text-sm text-muted">· {{ cart.count }}</span>
            </div>
            <button
              type="button"
              class="inline-flex h-9 w-9 items-center justify-center rounded-full text-muted transition-colors hover:bg-bg-deep hover:text-fg"
              aria-label="Закрыть корзину"
              @click="close"
            >
              <AppIcon name="close" :size="20" />
            </button>
          </header>

          <!-- Пусто -->
          <div v-if="cart.isEmpty" class="flex flex-1 flex-col items-center justify-center gap-4 px-6 text-center">
            <span class="flex h-16 w-16 items-center justify-center rounded-full bg-bg-deep text-muted">
              <AppIcon name="cart" :size="28" />
            </span>
            <p class="font-heading text-lg">Пока пусто</p>
            <p class="max-w-xs text-sm text-muted">Добавьте товары из каталога — они появятся здесь.</p>
            <button class="btn-primary mt-2" @click="goCart">В каталог</button>
          </div>

          <!-- Список -->
          <template v-else>
            <ul class="flex-1 space-y-3 overflow-y-auto px-5 py-4">
              <li v-for="item in cart.items" :key="item.line_id" class="flex gap-3">
                <NuxtLink :to="`/catalog/${item.slug}`" class="shrink-0 overflow-hidden rounded-xl" @click="close">
                  <img :src="item.image_url" :alt="item.name" class="h-20 w-20 object-cover" />
                </NuxtLink>
                <div class="flex flex-1 flex-col">
                  <NuxtLink
                    :to="`/catalog/${item.slug}`"
                    class="text-sm font-medium leading-snug hover:text-forest"
                    @click="close"
                  >
                    {{ item.name }}
                  </NuxtLink>
                  <span v-if="item.size" class="mt-0.5 text-xs text-muted">Размер: {{ item.size }}</span>
                  <div class="mt-auto flex items-center justify-between pt-2">
                    <div class="inline-flex items-center rounded-full border border-line">
                      <button class="inline-flex h-8 w-9 items-center justify-center text-fg" aria-label="Уменьшить" @click="cart.decrement(item.line_id)">
                        <AppIcon name="minus" :size="15" />
                      </button>
                      <span class="tnum w-7 text-center text-xs">{{ item.quantity }}</span>
                      <button class="inline-flex h-8 w-9 items-center justify-center text-fg" aria-label="Увеличить" @click="cart.increment(item.line_id)">
                        <AppIcon name="plus" :size="15" />
                      </button>
                    </div>
                    <span class="tnum text-sm font-semibold">{{ formatPrice(item.price * item.quantity) }}</span>
                  </div>
                </div>
                <button
                  type="button"
                  class="inline-flex h-8 w-8 shrink-0 items-center justify-center self-start rounded-full text-muted transition-colors hover:bg-accent/10 hover:text-accent"
                  :aria-label="`Удалить ${item.name}`"
                  @click="cart.remove(item.line_id)"
                >
                  <AppIcon name="trash" :size="16" />
                </button>
              </li>
            </ul>

            <footer class="border-t border-line bg-white px-5 py-4">
              <div class="flex items-center justify-between text-base">
                <span>Итого</span>
                <span class="tnum font-semibold">{{ formatPrice(cart.total) }}</span>
              </div>
              <button class="btn-accent mt-4 w-full" @click="goCheckout">
                Оформить заявку <AppIcon name="arrowRight" :size="18" />
              </button>
              <button class="btn-ghost mt-2 w-full" @click="goCart">Открыть корзину</button>
            </footer>
          </template>
        </aside>
      </Transition>
    </Teleport>
  </ClientOnly>
</template>
