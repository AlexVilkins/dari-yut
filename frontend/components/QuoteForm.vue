<script setup lang="ts">
// Форма «Запросить опт-прайс»: сохраняет заявку через POST /quotes.
// Заявки видит менеджер в админке (раздел «Заявки на прайс»).
const toast = useToast()
const api = useApi()

const form = reactive({
  name: '',
  phone: '',
  company: '',
  product: '',
  quantity: '',
  comment: '',
})

const file = ref<File | null>(null)
const dragOver = ref(false)
const submitting = ref(false)
const errorMsg = ref('')
const consent = ref(false)

const products = [
  'Банные полотенца',
  'Кухонные полотенца',
  'Махровые халаты',
  'Махровые простыни',
  'Гостиничный текстиль',
  'Подарочные наборы',
  'Смешанный ассортимент',
]

function onFileChange(e: Event) {
  const input = e.target as HTMLInputElement
  setFile(input.files?.[0] ?? null)
}

function onDrop(e: DragEvent) {
  dragOver.value = false
  setFile(e.dataTransfer?.files?.[0] ?? null)
}

function setFile(f: File | null) {
  if (!f) return
  // Лимит 10 МБ, изображения и PDF.
  if (f.size > 10 * 1024 * 1024) {
    errorMsg.value = 'Файл больше 10 МБ.'
    return
  }
  errorMsg.value = ''
  file.value = f
}

function humanSize(bytes: number) {
  if (bytes < 1024) return `${bytes} Б`
  if (bytes < 1024 * 1024) return `${Math.round(bytes / 1024)} КБ`
  return `${(bytes / 1024 / 1024).toFixed(1)} МБ`
}

async function submit() {
  errorMsg.value = ''
  if (!form.name || !form.phone) {
    errorMsg.value = 'Укажите имя и телефон — без них не сможем перезвонить.'
    return
  }
  if (!consent.value) {
    errorMsg.value = 'Подтвердите согласие на обработку персональных данных.'
    return
  }
  submitting.value = true
  try {
    await api('/quotes', {
      method: 'POST',
      body: {
        name: form.name,
        phone: form.phone,
        company: form.company,
        product: form.product,
        quantity: form.quantity,
        comment: form.comment,
      },
    })
    toast.success('Заявка на опт-прайс отправлена — перезвоним в течение дня')
    form.name = ''
    form.phone = ''
    form.company = ''
    form.product = ''
    form.quantity = ''
    form.comment = ''
    file.value = null
    consent.value = false
  } catch (e: any) {
    errorMsg.value =
      e?.data?.detail?.[0]?.msg ||
      e?.data?.detail ||
      'Не удалось отправить заявку. Попробуйте ещё раз или позвоните нам.'
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <form class="card p-6 sm:p-8" @submit.prevent="submit">
    <div class="grid gap-5 sm:grid-cols-2">
      <div>
        <label class="label" for="q-name">Имя <span class="text-accent">*</span></label>
        <input id="q-name" v-model="form.name" class="field" type="text" autocomplete="name" />
      </div>
      <div>
        <label class="label" for="q-phone">Телефон <span class="text-accent">*</span></label>
        <input id="q-phone" v-model="form.phone" v-phone class="field" type="tel" inputmode="tel" autocomplete="tel" placeholder="+7 ___ ___-__-__" />
      </div>
      <div>
        <label class="label" for="q-company">Компания</label>
        <input id="q-company" v-model="form.company" class="field" type="text" autocomplete="organization" placeholder="Отель, магазин, ИП…" />
      </div>
      <div>
        <label class="label" for="q-qty">Объём партии, шт.</label>
        <input id="q-qty" v-model="form.quantity" class="field" type="number" min="1" inputmode="numeric" placeholder="например, 200" />
      </div>
      <div class="sm:col-span-2">
        <label class="label" for="q-product">Интересующий ассортимент</label>
        <AppSelect
          id="q-product"
          v-model="form.product"
          :options="products"
          placeholder="Не выбрано"
          aria-label="Интересующий ассортимент"
        />
      </div>
    </div>

    <div class="mt-5">
      <label class="label" for="q-comment">Комментарий</label>
      <textarea id="q-comment" v-model="form.comment" class="field min-h-20" placeholder="Позиции, плотность, цвета, сроки, требования к упаковке…" />
    </div>

    <!-- Вложение: список позиций / бриф -->
    <div class="mt-5">
      <span class="label">Список или бриф (необязательно)</span>
      <label
        class="flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl2 border-2 border-dashed px-4 py-7 text-center transition-colors"
        :class="dragOver ? 'border-forest bg-forest/5' : 'border-line bg-bg-deep/40 hover:border-forest/40'"
        @dragover.prevent="dragOver = true"
        @dragleave.prevent="dragOver = false"
        @drop.prevent="onDrop"
      >
        <span class="flex h-11 w-11 items-center justify-center rounded-full bg-forest/10 text-forest">
          <AppIcon name="send" :size="22" />
        </span>
        <template v-if="file">
          <span class="inline-flex items-center gap-2 text-sm font-medium text-fg">
            <AppIcon name="check" :size="16" class="text-forest" /> {{ file.name }}
          </span>
          <span class="text-xs text-muted">{{ humanSize(file.size) }} · нажмите, чтобы заменить</span>
        </template>
        <template v-else>
          <span class="text-sm text-fg">Перетащите файл сюда или <span class="text-forest underline">выберите</span></span>
          <span class="text-xs text-muted">PDF, XLSX, DOCX, изображения — до 10 МБ</span>
        </template>
        <input type="file" class="sr-only" accept="image/*,.pdf,.xlsx,.xls,.doc,.docx,.csv" @change="onFileChange" />
      </label>
    </div>

    <p v-if="errorMsg" role="alert" class="mt-4 flex items-center gap-2 rounded-xl bg-accent/10 px-4 py-3 text-sm text-accent">
      <AppIcon name="close" :size="16" /> {{ errorMsg }}
    </p>

    <div class="mt-6">
      <ConsentCheckbox v-model="consent" />
    </div>

    <button class="btn-accent btn-lg mt-5 w-full" type="submit" :disabled="submitting || !consent">
      <AppIcon v-if="!submitting" name="send" :size="18" />
      {{ submitting ? 'Отправляем…' : 'Запросить опт-прайс' }}
    </button>
  </form>
</template>
