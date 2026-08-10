// middleware/auth.global.ts
import { defineNuxtRouteMiddleware, navigateTo } from '#app'
import { useAuthStore } from '~/stores/authStore'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // 1. OPTIMISATION : Ignorer si c'est juste une modification d'ancre (ex: #faq) sur la même page
  if (to.path === from.path && to.hash !== from.hash) {
    return
  }

  // 2. DÉFINITION DES ROUTES PROTÉGÉES
  // Ajoute ici tous les préfixes d'URL de ton espace client
  const protectedRoutes = ['/dashboard', '/profile']
  const isProtectedRoute = protectedRoutes.some(route => to.path.startsWith(route))

  // 3. DÉFINITION DES ROUTES D'AUTHENTIFICATION
  // Pages strictement réservées aux utilisateurs non connectés
  const authRoutes = ['/auth/login', '/auth/registration']
  const isAuthRoute = authRoutes.some(route => to.path.startsWith(route))

  // Performance maximale : on ne déclenche aucune logique si c'est une page publique classique (ex: /)
  if (!isProtectedRoute && !isAuthRoute) {
    return
  }

  const authStore = useAuthStore()

  // 4. HYDRATATION SÉCURISÉE AU CHARGEMENT (SSR & F5)
  // Si ton computed isAuthenticated vaut false, on tente un unique appel silencieux à getProfile()
  if (!authStore.isAuthenticated) {
    try {
      await authStore.getProfile()
    } catch (error) {
      // Échec silencieux : absence de token, expiration ou erreur 401.
      // Le catch empêche l'application Nuxt d'afficher une page d'erreur blanche ou de crasher.
      console.warn(`[Auth Middleware] Session inactive lors du passage de ${from.path} vers ${to.path}`)
    }
  }

  // 5. BLOQUER L'ACCÈS AUX PAGES PROTÉGÉES SI L'UTILISATEUR EST DÉCONNECTÉ
  if (isProtectedRoute && !authStore.isAuthenticated) {
    console.warn(`[Auth Middleware] Accès refusé pour ${to.path}. Redirection vers le login.`)
    // On conserve l'URL d'origine afin de le rediriger au bon endroit après sa connexion
    return navigateTo(`/auth/login?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  // 6. ANTI-BOUCLE : EMPÊCHER UN UTILISATEUR CONNECTÉ D'ALLER SUR LOGIN / INSCRIPTION
  if (isAuthRoute && authStore.isAuthenticated) {
    console.log(`[Auth Middleware] Utilisateur déjà connecté. Redirection automatique vers le dashboard.`)
    return navigateTo('/profile/dashboard')
  }

  // Si toutes les conditions passent, on ne retourne rien : le routeur continue sa navigation normalement
})