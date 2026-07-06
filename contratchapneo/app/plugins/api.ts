export default defineNuxtPlugin(async () => {
  const config = useRuntimeConfig()

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',
    credentials: 'include', // ✅ Le navigateur enverra ton cookie HttpOnly tout seul !

    onRequest({ options }) {
      // ❌ Plus besoin d'injecter manuellement Authorization: Bearer !

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
      if (response.status === 403) navigateTo('/auth/login')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  // Initialiser le token CSRF au chargement de l'app
  try {
    await api('/account/csrf/')
    console.log('✅ Token CSRF initialisé')
  } catch (err) {
    console.warn('⚠️ Erreur lors de l\'initialisation du token CSRF:', err)
  }

  return { provide: { api } }
})