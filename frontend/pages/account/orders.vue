<script setup lang="ts">
import type { OrderStatus } from '~/types'

definePageMeta({ middleware: 'auth' })

const orders = useOrdersStore()
const auth = useAuthStore()
const route = useRoute()
const { formatPrice, formatDate } = useFormat()

useSeoMeta({ title: 'Мои заявки', robots: 'noindex' })

// Заявки приходят из бэка (GET /orders/me). Грузим на клиенте: на сервере
// токена нет (он в localStorage), а страница и так под auth-миддлварой.
const pending = ref(true)
const loadError = ref(false)

onMounted(async () => {
  try {
    await orders.fetchMine()
  } catch {
    loadError.value = true
  } finally {
    pending.value = false
  }
})

const justCreatedId = computed(() =>
  route.query.created ? Number(route.query.created) : null,
)

const statusLabel: Record<OrderStatus, string> = {
  new: 'Новая',
  processing: 'В работе',
  done: 'Выполнена',
  cancelled: 'Отменена',
}

const statusClass: Record<OrderStatus, string> = {
  new: 'bg-forest/10 text-forest',
  processing: 'bg-accent/10 text-accent',
  done: 'bg-forest text-cream',
  cancelled: 'bg-muted/20 text-muted',
}
</script>

<template>
  <div class="container-x py-8 sm:py-12">
    <div class="flex flex-wrap items-end justify-between gap-3">
      <div>
        <h1 class="font-heading text-[clamp(2rem,5vw,3rem)]">Мои заявки</h1>
        <p v-if="auth.user" class="mt-2 text-muted">
          {{ auth.user.full_name || auth.user.email }}
        </p>
      </div>
      <NuxtLink to="/catalog" class="btn-ghost">
        <AppIcon name="plus" :size="18" /> Новый заказ
      </NuxtLink>
    </div>

    <ClientOnly>
      <Transition
        enter-active-class="transition duration-300 ease-out"
        enter-from-class="-translate-y-2 opacity-0"
      >
        <div
          v-if="justCreatedId"
          class="mt-6 flex items-start gap-3 rounded-xl2 border border-forest/30 bg-forest/5 px-5 py-4 text-sm text-forest"
        >
          <AppIcon name="check" :size="20" class="mt-0.5 shrink-0" />
          <span>
            <span class="font-medium">Заявка №{{ justCreatedId }} принята.</span>
            Мы свяжемся с вами для подтверждения.
          </span>
        </div>
      </Transition>

      <!-- Загрузка -->
      <div v-if="pending" class="mt-8 flex flex-col gap-4">
        <div v-for="n in 2" :key="n" class="card overflow-hidden">
          <div class="h-16 animate-pulse bg-bg-deep/40" />
          <div class="space-y-3 p-6">
            <div class="h-4 w-2/3 animate-pulse rounded bg-bg-deep" />
            <div class="h-4 w-1/3 animate-pulse rounded bg-bg-deep" />
          </div>
        </div>
      </div>

      <!-- Ошибка загрузки -->
      <div v-else-if="loadError" class="card mt-8 p-12 text-center">
        <p class="text-accent">Не удалось загрузить заявки.</p>
        <button class="btn-ghost mt-5" @click="$router.go(0)">Обновить</button>
      </div>

      <div v-else-if="!orders.orders.length" class="card mt-8 p-12 text-center sm:p-16">
        <span class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-bg-deep text-muted">
          <AppIcon name="package" :size="28" />
        </span>
        <p class="mt-5 font-heading text-xl">У вас пока нет заявок</p>
        <p class="mx-auto mt-2 max-w-sm text-sm text-muted">
          Оформите первый заказ — и он появится здесь со статусом обработки.
        </p>
        <NuxtLink to="/catalog" class="btn-primary mt-6">В каталог</NuxtLink>
      </div>

      <ul v-else class="mt-8 flex flex-col gap-4">
        <li v-for="order in orders.orders" :key="order.id" class="card overflow-hidden">
          <div class="flex flex-wrap items-center justify-between gap-3 border-b border-line bg-bg-deep/30 px-6 py-4">
            <div class="flex items-center gap-3">
              <span class="flex h-10 w-10 items-center justify-center rounded-full bg-forest/10 text-forest">
                <AppIcon name="package" :size="20" />
              </span>
              <div>
                <span class="font-heading text-lg">Заявка №{{ order.id }}</span>
                <span class="block text-xs text-muted">{{ formatDate(order.created_at) }}</span>
              </div>
            </div>
            <span
              class="rounded-full px-3 py-1 text-xs font-medium"
              :class="statusClass[order.status]"
            >
              {{ statusLabel[order.status] }}
            </span>
          </div>

          <div class="px-6 py-5">
            <ul class="space-y-2 text-sm text-muted">
              <li
                v-for="item in order.items"
                :key="item.product_id"
                class="flex justify-between gap-2"
              >
                <span>
                  {{ item.product_name }}<span v-if="item.size" class="text-muted/70"> · {{ item.size }}</span>
                  <span class="text-muted/70"> × {{ item.quantity }}</span>
                </span>
                <span class="tnum shrink-0">{{ formatPrice(item.price * item.quantity) }}</span>
              </li>
            </ul>

            <div class="mt-4 flex flex-wrap items-center justify-between gap-2 border-t border-line pt-4">
              <span class="inline-flex items-center gap-1.5 text-sm text-muted">
                <AppIcon name="mapPin" :size="16" /> {{ order.delivery_address }}
              </span>
              <span class="tnum font-semibold">{{ formatPrice(order.total) }}</span>
            </div>
          </div>
        </li>
      </ul>
    </ClientOnly>
  </div>
</template>
