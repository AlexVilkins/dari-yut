export function useFormat() {
  const formatPrice = (value: number) =>
    `${new Intl.NumberFormat('ru-RU').format(value)} ₽`

  const formatDate = (iso: string) =>
    new Intl.DateTimeFormat('ru-RU', {
      day: '2-digit',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(new Date(iso))

  return { formatPrice, formatDate }
}
