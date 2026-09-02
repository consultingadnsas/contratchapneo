// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  
  compatibilityDate: '2025-07-15',
  
  devtools: { enabled: true },
  
  css: ['~/assets/css/main.css'],
  
  vite: {
    optimizeDeps: {
      include: [
        '@vue/devtools-core',
        '@vue/devtools-kit',
        'vue-pdf-embed',
        '@stripe/stripe-js',
      ]
    }
  },
  
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {},
      autoprefixer: {},
    },
  },

  modules: ['@pinia/nuxt','pinia-plugin-persistedstate/nuxt'],

  runtimeConfig: {
    public: {
      // Tout ce qui est ici sera accessible côté frontend
      stripePublicKey: process.env.STRIPE_PUBLIC_KEY,
      // URL de base de l'API Django (ex: http://localhost:8000)
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  }
})