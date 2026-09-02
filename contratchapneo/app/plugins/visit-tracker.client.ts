export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const router = useRouter();

  const apiBase = config.public.apiBase || '';
  const endpoint = `${apiBase.replace(/\/$/, '')}/stats/visit/`;

  const callVisit = async () => {
    try {
      // Obtenir le CSRF token via un GET (le middleware Django créera le cookie)
      await $fetch(endpoint, { method: 'GET', credentials: 'include' });

      // Lire le cookie CSRF (document.cookie côté client)
      const getCsrfFromCookie = () => {
        const match = document.cookie.match(/(^|;)\s*csrftoken=([^;]+)/);
        return match ? decodeURIComponent(match[2]) : null;
      };

      const csrf = getCsrfFromCookie();

      await $fetch(endpoint, {
        method: 'POST',
        credentials: 'include',
        headers: {
          'X-CSRFToken': csrf || ''
        }
      });
    } catch (e) {
      // Ne pas interrompre l'app si le tracker échoue
      console.error('Visit tracker error:', e);
    }
  };

  // Appel initial au chargement client
  callVisit();

  // Appel après chaque navigation côté client
  router.afterEach(() => {
    callVisit();
  });
});
