<template>
  <div class="main-container">
      <form @submit.prevent="handleLogin">
        <h3>Connexion Administrateur</h3>
        
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
          :isLoading="adminAuthStore.isLoading"
        />

        <div class="err-message-wrapper" v-if="adminAuthStore.error">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v3.75m9-.75a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9 3.75h.008v.008H12v-.008Z" />
          </svg>
          <p class="error-message">
            {{ adminAuthStore.error }}
          </p>
        </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import formButtonVue from '../buttons/formButton.vue'
import BaseInputVue from '../input/BaseInput.vue'

// ⚡️ Importation de ton NOUVEAU store admin
import { useAdminAuthStore } from '../../stores/adminAuthStore'

interface ErrorMessage {
  username: string
  password: string
}

const router = useRouter()
const adminAuthStore = useAdminAuthStore()

const credentials = ref({
  username: '',
  password: ''
})

const errorMessage = ref<ErrorMessage>({
  username: '',
  password: ''
})

// Fonction de validation locale avant soumission
const validateForm = (): boolean => {
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
  // 1. Validation locale
  if (!validateForm()) return

  try {
    // 2. Appel au store admin avec (identifiant, mot de passe)
    const success = await adminAuthStore.login(
      credentials.value.username, 
      credentials.value.password
    )
    
    // 3. Redirection si succès
    if (success) {
      router.push('/admin') 
    }
  } catch (error) {
    console.log('[Admin Login] Erreur capturée', error)
  }
}
</script>

<style scoped>
.main-container {
  width: 100%;
  max-width: 400px;
  margin: auto;
  padding: 2rem;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}
.err-message-wrapper {
  padding: 10px;
  border-radius: 10px;
  width: 100%;
  background-color: #f8d7da;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 15px;
}

.err-message-wrapper svg {
  color: #eb4d5d;
  flex-shrink: 0;
  width: 24px;
  height: 24px;
}

.error-message {
  color: red;
  font-size: 0.9em;
  font-weight: 600;
  margin: 0;
}
</style>