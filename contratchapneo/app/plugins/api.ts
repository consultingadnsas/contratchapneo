export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig()

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',
    credentials: 'include', // ✅ Le navigateur enverra ton cookie HttpOnly tout seul !

    onRequest({ options }) {
      const method = options.method?.toUpperCase() || 'GET'
      if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        const csrfFromBrowser = useCookie('csrftoken').value;
        if (csrfFromBrowser) {
          options.headers = {
            ...options.headers,
            'X-CSRFToken': csrfFromBrowser
          }
        } else {
           console.warn("🚨 Aucun cookie CSRF trouvé dans le navigateur !")
        }
      }
    },

    onResponseError({ response }) {
      if (response.status === 403) throw new Error('Erreur serveur')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  // ✅ CORRECTION : Initialiser le token CSRF uniquement côté serveur (SSR)
  // Le navigateur héritera automatiquement des cookies générés lors de la première phase.
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