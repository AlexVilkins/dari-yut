<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const cart = useCartStore()
const auth = useAuthStore()
const orders = useOrdersStore()
const toast = useToast()
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

const steps = [
  { n: 1, label: 'Корзина' },
  { n: 2, label: 'Оформление' },
  { n: 3, label: 'Готово' },
]

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
    const order = await orders.create({
      contact_name: form.contact_name,
      phone: form.phone,
      delivery_address: form.delivery_address,
      comment: form.comment,
      items: [...cart.items],
    })
    cart.clear()
    toast.success('Заявка отправлена — мы свяжемся с вами')
    await navigateTo(`/account/orders?created=${order.id}`)
  } catch (e) {
    const detail = (e as { data?: { detail?: string } })?.data?.detail
    errorMsg.value = detail || 'Не удалось отправить заявку. Попробуйте ещё раз.'
    toast.error(errorMsg.value)
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="container-x py-8 sm:py-12">
    <h1 class="font-heading text-[clamp(2rem,5vw,3rem)]">Оформление заявки</h1>

    <!-- Stepper -->
    <ol class="mt-6 flex items-center gap-2 text-sm">
      <li v-for="(s, i) in steps" :key="s.n" class="flex items-center gap-2">
        <span
          class="inline-flex h-7 w-7 items-center justify-center rounded-full text-xs font-medium"
          :class="s.n <= 2 ? 'bg-forest text-cream' : 'bg-bg-deep text-muted'"
        >
          {{ s.n }}
        </span>
        <span :class="s.n === 2 ? 'font-medium text-fg' : 'text-muted'">{{ s.label }}</span>
        <span v-if="i < steps.length - 1" class="mx-1 h-px w-6 stitch sm:w-10" />
      </li>
    </ol>

    <ClientOnly>
      <div v-if="cart.isEmpty" class="card mt-8 p-12 text-center sm:p-16">
        <span class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-bg-deep text-muted">
          <AppIcon name="cart" :size="28" />
        </span>
        <p class="mt-5 font-heading text-xl">Корзина пуста — нечего оформлять</p>
        <NuxtLink to="/catalog" class="btn-primary mt-6">В каталог</NuxtLink>
      </div>

      <form v-else class="mt-8 grid gap-8 lg:grid-cols-[1fr_340px]" @submit.prevent="submit">
        <div class="card space-y-5 p-6 sm:p-8">
          <div>
            <p class="font-heading text-lg">Контактные данные</p>
            <p class="mt-1 text-sm text-muted">Свяжемся с вами для подтверждения заявки.</p>
          </div>
          <div class="grid gap-5 sm:grid-cols-2">
            <div>
              <label class="label" for="name">Имя получателя <span class="text-accent">*</span></label>
              <input id="name" v-model="form.contact_name" class="field" type="text" autocomplete="name" />
            </div>
            <div>
              <label class="label" for="phone">Телефон <span class="text-accent">*</span></label>
              <input id="phone" v-model="form.phone" class="field" type="tel" autocomplete="tel" placeholder="+7 ___ ___-__-__" />
            </div>
          </div>
          <div>
            <label class="label" for="address">Адрес доставки <span class="text-accent">*</span></label>
            <input id="address" v-model="form.delivery_address" class="field" type="text" placeholder="Город, улица, дом, квартира" />
          </div>
          <div>
            <label class="label" for="comment">Комментарий к заказу</label>
            <textarea id="comment" v-model="form.comment" class="field min-h-24" placeholder="Пожелания по макету, срокам и т.п." />
          </div>

          <p v-if="errorMsg" role="alert" class="flex items-center gap-2 rounded-xl bg-accent/10 px-4 py-3 text-sm text-accent">
            <AppIcon name="close" :size="16" /> {{ errorMsg }}
          </p>
        </div>

        <aside class="card h-fit p-6 lg:sticky lg:top-24">
          <h2 class="font-heading text-lg">Ваш заказ</h2>
          <ul class="mt-4 space-y-3 text-sm">
            <li
              v-for="item in cart.items"
              :key="item.line_id"
              class="flex items-start justify-between gap-3"
            >
              <span class="text-muted">
                {{ item.name }}<span v-if="item.size" class="text-muted/70"> · {{ item.size }}</span>
                <span class="text-muted/70"> × {{ item.quantity }}</span>
              </span>
              <span class="tnum shrink-0">{{ formatPrice(item.price * item.quantity) }}</span>
            </li>
          </ul>
          <div class="mt-4 flex justify-between border-t border-line pt-4 text-lg">
            <span>Итого</span>
            <span class="tnum font-semibold">{{ formatPrice(cart.total) }}</span>
          </div>
          <button class="btn-accent mt-6 w-full" type="submit" :disabled="submitting">
            <AppIcon v-if="!submitting" name="send" :size="18" />
            {{ submitting ? 'Отправляем…' : 'Отправить заявку' }}
          </button>
          <NuxtLink to="/cart" class="btn-ghost mt-3 w-full">Вернуться в корзину</NuxtLink>
        </aside>
      </form>
    </ClientOnly>
  </div>
</template>
