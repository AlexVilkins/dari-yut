<script setup lang="ts">
import type { OrderStatus } from '~/types'

definePageMeta({ middleware: 'auth' })

const orders = useOrdersStore()
const route = useRoute()
const { formatPrice, formatDate } = useFormat()

useSeoMeta({ title: 'Мои заявки', robots: 'noindex' })

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
  <div class="container-x py-10 sm:py-14">
    <h1 class="mb-8 font-heading text-3xl sm:text-4xl">Мои заявки</h1>

    <ClientOnly>
      <div
        v-if="justCreatedId"
        class="mb-6 rounded-xl border border-forest/30 bg-forest/5 px-4 py-3 text-sm text-forest"
      >
        Заявка №{{ justCreatedId }} принята. Мы свяжемся с вами для подтверждения.
      </div>

      <div v-if="!orders.orders.length" class="card p-10 text-center">
        <p class="text-muted">У вас пока нет заявок.</p>
        <NuxtLink to="/catalog" class="btn-primary mt-5">В каталог</NuxtLink>
      </div>

      <ul v-else class="flex flex-col gap-4">
        <li v-for="order in orders.orders" :key="order.id" class="card p-6">
          <div class="flex flex-wrap items-center justify-between gap-3">
            <div>
              <span class="font-heading text-lg">Заявка №{{ order.id }}</span>
              <span class="ml-3 text-sm text-muted">{{ formatDate(order.created_at) }}</span>
            </div>
            <span
              class="rounded-full px-3 py-1 text-xs font-medium"
              :class="statusClass[order.status]"
            >
              {{ statusLabel[order.status] }}
            </span>
          </div>

          <ul class="mt-4 space-y-1 text-sm text-muted">
            <li
              v-for="item in order.items"
              :key="item.product_id"
              class="flex justify-between gap-2"
            >
              <span>{{ item.product_name }} × {{ item.quantity }}</span>
              <span>{{ formatPrice(item.price * item.quantity) }}</span>
            </li>
          </ul>

          <div class="mt-4 flex justify-between border-t border-line pt-3">
            <span class="text-sm text-muted">{{ order.delivery_address }}</span>
            <span class="font-semibold">{{ formatPrice(order.total) }}</span>
          </div>
        </li>
      </ul>
    </ClientOnly>
  </div>
</template>
