// plugins/api.ts
import { defineNuxtPlugin, useCookie, useRuntimeConfig, useRequestHeaders } from '#app'

export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig()

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',
    credentials: 'include',

    // ⚡️ CORRECTION 1 : Transmettre les cookies du navigateur au serveur Django en SSR
    // Sans ça, Node.js appelle Django en tant qu'utilisateur anonyme !
    headers: import.meta.server ? useRequestHeaders(['cookie']) : undefined,

    onRequest({ options }) {
      // ⚡️ CORRECTION 2 : Lire les cookies à l'intérieur de onRequest pour avoir la valeur la plus fraîche
      const token = useCookie('token')
      const csrfFromBrowser = useCookie('csrftoken')

      options.headers = options.headers || {}

      // 1. Injection du Token d'authentification
      if (token.value) {
        options.headers = {
          ...options.headers,
          // ⚠️ Assure-toi que ton Django attend 'Bearer' (JWT) et non 'Token' (DRF TokenAuth classique)
          Authorization: `Bearer ${token.value}`
        }
      }

      // 2. Injection du Token CSRF pour les méthodes de modification
      const method = options.method?.toUpperCase() || 'GET'
      if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        if (csrfFromBrowser.value) {
          options.headers = {
            ...options.headers,
            'X-CSRFToken': csrfFromBrowser.value
          }
        } else if (import.meta.client) {
          console.warn("🚨 Aucun cookie CSRF trouvé dans le navigateur !")
        }
      }
    },

    onResponseError({ response }) {
      if (response.status === 403) throw new Error('Erreur serveur (403 Accès refusé)')
      if (response.status === 500) throw new Error('Erreur serveur (500)')
    },
  })

  // 3. Initialisation du token CSRF côté serveur (SSR)
  if (import.meta.server) {
    try {
      await api('/account/csrf/')
      console.log('✅ Token CSRF initialisé côté serveur')
    } catch (err) {
      console.warn('⚠️ Erreur lors de l\'initialisation du token CSRF:', err)
    }
  }

  return { provide: { api } }
})