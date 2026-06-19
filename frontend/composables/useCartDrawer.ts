// Глобальное состояние выезжающей корзины.
export function useCartDrawer() {
  const isOpen = useState<boolean>('cart-drawer-open', () => false)

  const open = () => (isOpen.value = true)
  const close = () => (isOpen.value = false)
  const toggle = () => (isOpen.value = !isOpen.value)

  return { isOpen, open, close, toggle }
}
