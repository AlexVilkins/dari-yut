<script setup lang="ts">
const auth = useAuthStore()
const route = useRoute()

useSeoMeta({ title: 'Регистрация', robots: 'noindex' })

const form = reactive({ full_name: '', email: '', phone: '', password: '' })
const showPassword = ref(false)
const submitting = ref(false)
const errorMsg = ref('')

const redirectTo = computed(() => (route.query.redirect as string) || '/account/orders')

async function submit() {
  errorMsg.value = ''
  if (!form.full_name || !form.email || !form.password) {
    errorMsg.value = 'Заполните имя, email и пароль.'
    return
  }
  submitting.value = true
  try {
    await auth.register({ ...form })
    await navigateTo(redirectTo.value)
  } catch {
    errorMsg.value = 'Не удалось зарегистрироваться. Попробуйте ещё раз.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="container-x py-10 sm:py-16">
    <div class="mx-auto grid max-w-4xl overflow-hidden rounded-xl3 border border-line shadow-soft lg:grid-cols-2">
      <!-- Бренд-панель -->
      <aside class="relative hidden flex-col justify-between overflow-hidden bg-forest p-10 text-cream lg:flex">
        <div class="pointer-events-none absolute -bottom-16 -left-12 h-56 w-56 rounded-full bg-accent/20 blur-3xl" />
        <div class="relative">
          <span class="flex h-12 w-12 items-center justify-center rounded-full border border-cream/20 bg-cream/10 font-heading text-2xl">М</span>
          <p class="mt-6 font-heading text-3xl leading-tight">Создайте аккаунт</p>
          <p class="mt-3 max-w-xs text-cream/70">
            Регистрация занимает минуту и нужна только для отправки оптовой заявки.
          </p>
        </div>
        <blockquote class="relative border-l-2 border-accent/60 pl-4 text-sm italic text-cream/85">
          «Мягкость, тепло и уют — оптом» — махровые изделия от производителя.
        </blockquote>
      </aside>

      <!-- Форма -->
      <div class="bg-white p-8 sm:p-10">
        <h1 class="font-heading text-2xl sm:text-3xl">Регистрация</h1>
        <p class="mt-1.5 text-sm text-muted">Создайте аккаунт, чтобы отправлять заявки.</p>

        <form class="mt-7 space-y-4" @submit.prevent="submit">
          <div>
            <label class="label" for="name">Имя</label>
            <input id="name" v-model="form.full_name" class="field" type="text" autocomplete="name" />
          </div>
          <div>
            <label class="label" for="email">Email</label>
            <input id="email" v-model="form.email" class="field" type="email" autocomplete="email" placeholder="you@example.com" />
          </div>
          <div>
            <label class="label" for="phone">Телефон</label>
            <input id="phone" v-model="form.phone" v-phone class="field" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 ___ ___-__-__" />
          </div>
          <div>
            <label class="label" for="password">Пароль</label>
            <div class="relative">
              <input
                id="password"
                v-model="form.password"
                class="field pr-12"
                :type="showPassword ? 'text' : 'password'"
                autocomplete="new-password"
              />
              <button
                type="button"
                class="absolute inset-y-0 right-0 inline-flex w-11 items-center justify-center text-muted hover:text-fg"
                :aria-label="showPassword ? 'Скрыть пароль' : 'Показать пароль'"
                @click="showPassword = !showPassword"
              >
                <AppIcon :name="showPassword ? 'close' : 'user'" :size="18" />
              </button>
            </div>
          </div>

          <p v-if="errorMsg" role="alert" class="flex items-center gap-2 rounded-xl bg-accent/10 px-4 py-3 text-sm text-accent">
            <AppIcon name="close" :size="16" /> {{ errorMsg }}
          </p>

          <button class="btn-primary w-full" type="submit" :disabled="submitting">
            {{ submitting ? 'Создаём…' : 'Зарегистрироваться' }}
          </button>
        </form>

        <p class="mt-6 text-center text-sm text-muted">
          Уже есть аккаунт?
          <NuxtLink :to="{ path: '/login', query: route.query }" class="font-medium text-forest hover:underline">
            Войти
          </NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>
