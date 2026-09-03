export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig();
  const router = useRouter();

  const apiBase = config.public.apiBase || '';
  const endpoint = `${apiBase.replace(/\/$/, '')}/stats/visit/`;

  const callVisit = async () => {
    try {
      // Un seul appel GET suffit pour réveiller le middleware Django
      await $fetch(endpoint, { method: 'GET', credentials: 'include' });
    } catch (e) {
      console.error('Visit tracker error:', e);
    }
  };

  // Variable pour mémoriser la page et éviter le double-ping au chargement initial
  let lastRoute = null;

  // Se déclenche à chaque changement de page (y compris le chargement initial)
  router.afterEach((to) => {
    if (lastRoute !== to.fullPath) {
      lastRoute = to.fullPath;
      callVisit();
    }
  });
});