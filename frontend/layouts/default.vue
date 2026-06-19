<template>
  <div class="grain flex min-h-dvh flex-col">
    <a
      href="#main"
      class="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[120] focus:rounded-full focus:bg-forest focus:px-4 focus:py-2 focus:text-sm focus:text-cream"
    >
      К основному содержимому
    </a>
    <AppHeader />
    <main id="main" class="relative z-10 flex-1">
      <slot />
    </main>
    <AppFooter />
    <CartDrawer />
    <AppToaster />
  </div>
</template>
