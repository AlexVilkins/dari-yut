<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const cart = useCartStore()
const auth = useAuthStore()
const orders = useOrdersStore()
const { formatPrice } = useFormat()

useSeoMeta({ title: 'Оформление заявки', robots: 'noindex' })

const form = reactive({
  contact_name: auth.user?.full_name ?? '',
  phone: auth.user?.phone ?? '',
  delivery_address: '',
  comment: '',
})

const submitting = ref(false)
const errorMsg = ref('')

async function submit() {
  errorMsg.value = ''
  if (cart.isEmpty) {
    errorMsg.value = 'Корзина пуста.'
    return
  }
  if (!form.contact_name || !form.phone || !form.delivery_address) {
    errorMsg.value = 'Заполните имя, телефон и адрес доставки.'
    return
  }

  submitting.value = true
  try {
    // MOCK: создаём заявку локально. Заменить на POST /orders через useApi().
    await new Promise((r) => setTimeout(r, 300))
    const order = orders.create({
      contact_name: form.contact_name,
      phone: form.phone,
      delivery_address: form.delivery_address,
      comment: form.comment,
      items: [...cart.items],
    })
    cart.clear()
    await navigateTo(`/account/orders?created=${order.id}`)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="container-x py-10 sm:py-14">
    <h1 class="mb-8 font-heading text-3xl sm:text-4xl">Оформление заявки</h1>

    <ClientOnly>
      <div v-if="cart.isEmpty" class="card p-10 text-center">
        <p class="text-muted">Корзина пуста — нечего оформлять.</p>
        <NuxtLink to="/catalog" class="btn-primary mt-5">В каталог</NuxtLink>
      </div>

      <form v-else class="grid gap-8 lg:grid-cols-[1fr_320px]" @submit.prevent="submit">
        <div class="card space-y-4 p-6">
          <div>
            <label class="label" for="name">Имя получателя</label>
            <input id="name" v-model="form.contact_name" class="field" type="text" />
          </div>
          <div>
            <label class="label" for="phone">Телефон</label>
            <input id="phone" v-model="form.phone" class="field" type="tel" placeholder="+7 ___ ___-__-__" />
          </div>
          <div>
            <label class="label" for="address">Адрес доставки</label>
            <input id="address" v-model="form.delivery_address" class="field" type="text" />
          </div>
          <div>
            <label class="label" for="comment">Комментарий (необязательно)</label>
            <textarea id="comment" v-model="form.comment" class="field min-h-24" />
          </div>

          <p v-if="errorMsg" class="text-sm text-accent">{{ errorMsg }}</p>
        </div>

        <aside class="card h-fit p-6">
          <h2 class="font-heading text-lg">Ваш заказ</h2>
          <ul class="mt-4 space-y-2 text-sm">
            <li
              v-for="item in cart.items"
              :key="item.product_id"
              class="flex justify-between gap-2"
            >
              <span class="text-muted">{{ item.name }} × {{ item.quantity }}</span>
              <span>{{ formatPrice(item.price * item.quantity) }}</span>
            </li>
          </ul>
          <div class="mt-4 flex justify-between border-t border-line pt-4 text-lg">
            <span>Итого</span>
            <span class="font-semibold">{{ formatPrice(cart.total) }}</span>
          </div>
          <button class="btn-accent mt-6 w-full" type="submit" :disabled="submitting">
            {{ submitting ? 'Отправляем…' : 'Отправить заявку' }}
          </button>
        </aside>
      </form>
    </ClientOnly>
  </div>
</template>
