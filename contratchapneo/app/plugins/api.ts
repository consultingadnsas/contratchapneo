export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const token = useCookie('token') // Ne fonctionnera que si le cookie n'est PAS HttpOnly
  const csrfToken = useCookie('csrftoken')

  const api = $fetch.create({
    baseURL: config.public.apiBase || 'http://localhost:8000',

    // ✅ INDISPENSABLE : Autorise l'échange de cookies (cart_session_id, tokens...)
    credentials: 'include',

    onRequest({ options }) {
      // ✅ Garde ceci uniquement si tes tokens ne sont pas en HttpOnly
      if (token.value) {
        options.headers = {
          ...options.headers,
          Authorization: `Bearer ${token.value}`,
        }
      }

      /*
      const method = options.method?.toUpperCase() || 'GET'
      if (csrfToken.value && ['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
        options.headers = {
          ...options.headers,
          'X-CSRFToken': csrfToken.value
        }
      }*/

    },

    onResponseError({ response }) {
      if (response.status === 403) navigateTo('auth/login')
      if (response.status === 500) throw new Error('Erreur serveur')
    },
  })

  return {
    provide: { api }
  }
})