<script setup lang="ts">
const auth = useAuthStore()
const route = useRoute()

useSeoMeta({ title: 'Регистрация', robots: 'noindex' })

const form = reactive({ full_name: '', email: '', phone: '', password: '' })
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
  <div class="container-x flex justify-center py-14">
    <div class="card w-full max-w-md p-8">
      <h1 class="font-heading text-2xl">Регистрация</h1>
      <p class="mt-1 text-sm text-muted">Создайте аккаунт, чтобы отправлять заявки.</p>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="label" for="name">Имя</label>
          <input id="name" v-model="form.full_name" class="field" type="text" autocomplete="name" />
        </div>
        <div>
          <label class="label" for="email">Email</label>
          <input id="email" v-model="form.email" class="field" type="email" autocomplete="email" />
        </div>
        <div>
          <label class="label" for="phone">Телефон</label>
          <input id="phone" v-model="form.phone" class="field" type="tel" autocomplete="tel" />
        </div>
        <div>
          <label class="label" for="password">Пароль</label>
          <input
            id="password"
            v-model="form.password"
            class="field"
            type="password"
            autocomplete="new-password"
          />
        </div>

        <p v-if="errorMsg" class="text-sm text-accent">{{ errorMsg }}</p>

        <button class="btn-primary w-full" type="submit" :disabled="submitting">
          {{ submitting ? 'Создаём…' : 'Зарегистрироваться' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        Уже есть аккаунт?
        <NuxtLink
          :to="{ path: '/login', query: route.query }"
          class="text-forest hover:underline"
        >
          Войти
        </NuxtLink>
      </p>
    </div>
  </div>
</template>
