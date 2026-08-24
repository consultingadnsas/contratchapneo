// middleware/admin-auth.global.ts
import { defineNuxtRouteMiddleware, navigateTo } from '#app'
import { useAdminAuthStore } from '~/stores/adminAuthStore'

export default defineNuxtRouteMiddleware(async (to, from) => {
  // 1. OPTIMISATION : Ignorer si c'est juste une modification d'ancre (ex: #faq) sur la même page
  if (to.path === from.path && to.hash !== from.hash) {
    return
  }

  // 2. DÉFINITION DES ROUTES PROTÉGÉES (ADMIN)
  // Ajoute ici tous les préfixes d'URL réservés aux administrateurs
  const protectedAdminRoutes = ['/admin']
  const isProtectedAdminRoute = protectedAdminRoutes.some(route => to.path.toLowerCase().startsWith(route.toLowerCase()))

  // 3. DÉFINITION DES ROUTES D'AUTHENTIFICATION (ADMIN)
  // Page strictement réservée aux administrateurs non connectés
  const adminAuthRoutes = ['/auth/adminlogin']
  const isAdminAuthRoute = adminAuthRoutes.some(route => to.path.toLowerCase().startsWith(route.toLowerCase()))

  // Performance maximale : on ne déclenche aucune logique si c'est une page client classique (ex: /, /auth/login, etc.)
  if (!isProtectedAdminRoute && !isAdminAuthRoute) {
    return
  }

  const adminAuthStore = useAdminAuthStore()

  // 4. HYDRATATION SÉCURISÉE AU CHARGEMENT (SSR & F5)
  if (!adminAuthStore.isAuthenticated) {
    try {
      await adminAuthStore.fetchProfile()
    } catch (error) {
      console.warn(`[Admin Middleware] Session inactive lors du passage de ${from.path} vers ${to.path}`)
    }
  }

  // ⚡️ VÉRIFICATION DES DROITS STRICTS
  const isAdmin = adminAuthStore.isAuthenticated && 
                  (adminAuthStore.user?.is_staff || adminAuthStore.user?.is_superuser)

  // 5. BLOQUER L'ACCÈS AUX PAGES PROTÉGÉES SI L'UTILISATEUR EST DÉCONNECTÉ OU NON-ADMIN
  if (isProtectedAdminRoute && !isAdmin) {
    console.warn(`[Admin Middleware] Accès refusé pour ${to.path}. Redirection vers le login admin.`)
    
    // Par sécurité, on nettoie le store si un client normal a essayé d'entrer
    adminAuthStore.user = null
    adminAuthStore.isAuthenticated = false

    // On conserve l'URL d'origine afin de le rediriger au bon endroit après sa connexion
    return navigateTo(`/auth/adminlogin?redirect=${encodeURIComponent(to.fullPath)}`)
  }

  // 6. ANTI-BOUCLE : EMPÊCHER UN ADMIN CONNECTÉ D'ALLER SUR LA PAGE DE LOGIN ADMIN
  if (isAdminAuthRoute && isAdmin) {
    console.log(`[Admin Middleware] Admin déjà connecté. Redirection automatique vers le dashboard.`)
    return navigateTo('/admin')
  }

  // Si toutes les conditions passent, le routeur continue sa navigation normalement
})