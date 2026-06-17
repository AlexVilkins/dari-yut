<script setup lang="ts">
const auth = useAuthStore()
const route = useRoute()

useSeoMeta({ title: 'Вход', robots: 'noindex' })

const form = reactive({ email: '', password: '' })
const submitting = ref(false)
const errorMsg = ref('')

const redirectTo = computed(() => (route.query.redirect as string) || '/account/orders')

async function submit() {
  errorMsg.value = ''
  if (!form.email || !form.password) {
    errorMsg.value = 'Введите email и пароль.'
    return
  }
  submitting.value = true
  try {
    await auth.login(form.email, form.password)
    await navigateTo(redirectTo.value)
  } catch {
    errorMsg.value = 'Не удалось войти. Попробуйте ещё раз.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <div class="container-x flex justify-center py-14">
    <div class="card w-full max-w-md p-8">
      <h1 class="font-heading text-2xl">Вход</h1>
      <p class="mt-1 text-sm text-muted">Войдите, чтобы оформить заявку.</p>

      <form class="mt-6 space-y-4" @submit.prevent="submit">
        <div>
          <label class="label" for="email">Email</label>
          <input id="email" v-model="form.email" class="field" type="email" autocomplete="email" />
        </div>
        <div>
          <label class="label" for="password">Пароль</label>
          <input
            id="password"
            v-model="form.password"
            class="field"
            type="password"
            autocomplete="current-password"
          />
        </div>

        <p v-if="errorMsg" class="text-sm text-accent">{{ errorMsg }}</p>

        <button class="btn-primary w-full" type="submit" :disabled="submitting">
          {{ submitting ? 'Входим…' : 'Войти' }}
        </button>
      </form>

      <p class="mt-6 text-center text-sm text-muted">
        Нет аккаунта?
        <NuxtLink
          :to="{ path: '/register', query: route.query }"
          class="text-forest hover:underline"
        >
          Зарегистрироваться
        </NuxtLink>
      </p>
    </div>
  </div>
</template>
