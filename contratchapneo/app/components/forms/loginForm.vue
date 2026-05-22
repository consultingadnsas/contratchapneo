<template>
  <form @submit.prevent="handleLogin">
    <h3>Connexion</h3>
    
    <BaseInputVue 
      v-model="credentials.username" 
      label="Email ou Nom d'utilisateur" 
      name="username" 
      type="text" 
      placeholder="Entrez votre email ou pseudo" 
      :errorMessage="errorMessage.username"
      required
    />
    
    <BaseInputVue 
      v-model="credentials.password" 
      label="Mot de passe" 
      name="password" 
      type="password" 
      placeholder="Entrez votre mot de passe" 
      :errorMessage="errorMessage.password"
      required
    />
    
    <formButtonVue 
      label="Connexion" 
      type="submit" 
      :isLoading="authStore.isLoading"
    />

    <div class="err-message-wrapper" v-if="authStore.error">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
        <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
      </svg>
      <p class="error-message">
        {{ authStore.error }}
      </p>
    </div>
  </form>
</template>

<script lang="ts">
import { ref } from 'vue'
import formButtonVue from '../buttons/formButton.vue'
import BaseInputVue from '../input/BaseInput.vue'
import { useAuthStore } from '../../stores/authStore'
import { useRouter } from 'vue-router'

interface ErrorMessage {
  username: string
  password: string
}

export default {
  components: {
    BaseInputVue,
    formButtonVue
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const credentials = ref({
      username: '',
      password: '',
      email:''
    })
    
    const errorMessage = ref<ErrorMessage>({
      username: '',
      password: ''
    })

    // Fonction de validation locale avant soumission
    const validateForm = (): boolean => {
      // On réinitialise les messages d'erreur à chaque vérification
      errorMessage.value.username = ''
      errorMessage.value.password = ''
      
      let isValid = true

      if (!credentials.value.username.trim()) {
        errorMessage.value.username = "Veuillez entrer un email ou un nom d'utilisateur."
        isValid = false
      } else if (credentials.value.username.length < 3) {
        errorMessage.value.username = "L'identifiant doit contenir au moins 3 caractères."
        isValid = false
      }

      if (!credentials.value.password) {
        errorMessage.value.password = "Veuillez entrer votre mot de passe."
        isValid = false
      }

      return isValid
    }

    const handleLogin = async () => {
      // 1. On lance la validation locale
      if (!validateForm()) return

      try {
        // 2. Si c'est valide, on tente la connexion (Correction de l'envoi de l'email ici)
        await authStore.login({
          email: credentials.value.email,
          username: credentials.value.username,
          password: credentials.value.password
        })
        router.push('/profile/profile') 
      } catch (error) {
        console.log('[Login] Erreur capturée', error)
      }
    }

    return {
      authStore,
      credentials,
      errorMessage, // Pensez à bien le retourner pour l'utiliser dans le template
      handleLogin
    }
  }
}
</script>

<style scoped>
.err-message-wrapper {
  padding: 10px;
  border-radius: 10px;
  width: 100%;
  background-color: #f8d7da;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 15px; /* Petit espace visuel */
}

.err-message-wrapper svg {
  color: #eb4d5d;
  flex-shrink: 0;
}

.error-message {
  color: red;
  font-size: 0.9em;
  font-weight: 600;
}
</style>