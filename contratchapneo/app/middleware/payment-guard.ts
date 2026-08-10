// middleware/payment-guard.ts
import { defineNuxtRouteMiddleware, navigateTo } from '#app'
import { useOrderStore } from '~/stores/orderStore'

export default defineNuxtRouteMiddleware((to, from) => {
  const orderStore = useOrderStore()
  const order = orderStore.currentOrder

  // 1. Si aucune commande en mémoire ou si elle est marquée en échec
  if (!order || ['FAILED', 'CANCELLED', 'CANCELED', 'REJECTED'].includes(String(order.status).toUpperCase())) {
    console.warn("[Payment Guard] 🚨 Accès interdit à /orderSucces. Redirection vers /orderFails")
    return navigateTo('/order/orderFails', { replace: true })
  }

  // 2. Si la commande est encore PENDING, on l'envoie sur la page de vérification intermédiaire
  if (String(order.status).toUpperCase() === 'PENDING') {
    console.warn("[Payment Guard] ⏳ Commande PENDING. Redirection vers /orderVerifying")
    return navigateTo(`/order/orderVerifying?ref=${order.id}`, { replace: true })
  }

  // 3. Si order.status === 'PAID' / 'SUCCESS' -> Le middleware laisse entrer sur /orderSucces !
})