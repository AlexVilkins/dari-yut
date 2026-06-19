export type ToastType = 'success' | 'error' | 'info'

export interface Toast {
  id: number
  message: string
  type: ToastType
}

// Глобальное состояние тостов (общее на всё приложение).
export function useToast() {
  const toasts = useState<Toast[]>('toasts', () => [])
  const counter = useState<number>('toasts-counter', () => 0)

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  function notify(message: string, type: ToastType = 'success', timeout = 3500) {
    const id = ++counter.value
    toasts.value = [...toasts.value, { id, message, type }]
    if (import.meta.client && timeout > 0) {
      setTimeout(() => dismiss(id), timeout)
    }
    return id
  }

  return {
    toasts,
    notify,
    dismiss,
    success: (m: string) => notify(m, 'success'),
    error: (m: string) => notify(m, 'error'),
    info: (m: string) => notify(m, 'info'),
  }
}
