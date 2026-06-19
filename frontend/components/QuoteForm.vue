<script setup lang="ts">
// Форма «Рассчитать стоимость» с загрузкой макета.
// MOCK: ничего не отправляет на сервер — показывает тост. Заменить на POST /quotes.
const toast = useToast()

const form = reactive({
  name: '',
  phone: '',
  product: '',
  quantity: '',
  comment: '',
})

const file = ref<File | null>(null)
const dragOver = ref(false)
const submitting = ref(false)
const errorMsg = ref('')

const products = [
  'Футболка / поло',
  'Худи / свитшот',
  'Кепка',
  'Спецодежда',
  'Домашний текстиль',
  'Шоппер / сумка',
  'Другое',
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
  submitting.value = true
  try {
    // MOCK: имитируем отправку.
    await new Promise((r) => setTimeout(r, 500))
    toast.success('Заявка на расчёт отправлена — перезвоним в течение дня')
    form.name = ''
    form.phone = ''
    form.product = ''
    form.quantity = ''
    form.comment = ''
    file.value = null
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
        <input id="q-phone" v-model="form.phone" class="field" type="tel" autocomplete="tel" placeholder="+7 ___ ___-__-__" />
      </div>
      <div>
        <label class="label" for="q-product">Изделие</label>
        <select id="q-product" v-model="form.product" class="field">
          <option value="">Не выбрано</option>
          <option v-for="p in products" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
      <div>
        <label class="label" for="q-qty">Тираж, шт.</label>
        <input id="q-qty" v-model="form.quantity" class="field" type="number" min="1" inputmode="numeric" placeholder="например, 50" />
      </div>
    </div>

    <div class="mt-5">
      <label class="label" for="q-comment">Комментарий</label>
      <textarea id="q-comment" v-model="form.comment" class="field min-h-20" placeholder="Цвета, материал, сроки, пожелания по макету…" />
    </div>

    <!-- Загрузка макета -->
    <div class="mt-5">
      <span class="label">Макет (необязательно)</span>
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
          <span class="text-xs text-muted">PNG, JPG, PDF до 10 МБ</span>
        </template>
        <input type="file" class="sr-only" accept="image/*,.pdf" @change="onFileChange" />
      </label>
    </div>

    <p v-if="errorMsg" role="alert" class="mt-4 flex items-center gap-2 rounded-xl bg-accent/10 px-4 py-3 text-sm text-accent">
      <AppIcon name="close" :size="16" /> {{ errorMsg }}
    </p>

    <button class="btn-accent btn-lg mt-6 w-full" type="submit" :disabled="submitting">
      <AppIcon v-if="!submitting" name="send" :size="18" />
      {{ submitting ? 'Отправляем…' : 'Отправить заявку на расчёт' }}
    </button>
    <p class="mt-3 text-center text-xs text-muted">
      Нажимая кнопку, вы соглашаетесь на обработку персональных данных.
    </p>
  </form>
</template>
