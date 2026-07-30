<template>
  <form @submit.prevent="handleSubmit">
    <!-- ÉTAPE 1 : Demande d'envoi du mail -->
    <template v-if="step === 1">
      <h3>Mot de passe oublié</h3>

      <BaseInputVue
        v-model="form.email"
        label="Email"
        name="email"
        type="text"
        placeholder="Entrez votre email"
        :errorMessage="errorMessage.email"
        required
      />

      <formButtonVue
        label="Envoyer le lien"
        type="submit"
        :isLoading="authStore.isLoading"
      />
    </template>

    <!-- ÉTAPE 2 : Vérification du token -->
    <template v-else-if="step === 2">
      <h3>Vérification du code</h3>

      <BaseInputVue
          v-model="form.token"
          label="Code de vérification"
          name="token"
          type="text"
          placeholder="Entrez le code reçu par email"
          :errorMessage="errorMessage.token"
          required
      />

      <formButtonVue
        label="Vérifier"
        type="submit"
        :isLoading="authStore.isLoading"
      />
    </template>

    <!-- ÉTAPE 3 : Réinitialisation du mot de passe -->
    <template v-else-if="step === 3">
      <h3>Nouveau mot de passe</h3>

      <BaseInputVue
          v-model="form.newPassword"
          label="Nouveau mot de passe"
          name="newPassword"
          type="password"
          placeholder="Entrez votre nouveau mot de passe"
          :errorMessage="errorMessage.newPassword"
          required
      />

      <BaseInputVue
          v-model="form.confirmPassword"
          label="Confirmer le mot de passe"
          name="confirmPassword"
          type="password"
          placeholder="Confirmez votre nouveau mot de passe"
          :errorMessage="errorMessage.confirmPassword"
          required
      />

      <formButtonVue
          label="Réinitialiser"
          type="submit"
          :isLoading="authStore.isLoading"
      />
    </template>

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
  email: string
  token: string
  newPassword: string
  confirmPassword: string
}

export default {
  components: {
    BaseInputVue,
    formButtonVue
  },
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    // Étape courante du flow (1: email, 2: token, 3: nouveau mot de passe)
    const step = ref(1)

    const form = ref({
      email: '',
      token: '',
      newPassword: '',
      confirmPassword: ''
    })

    const errorMessage = ref<ErrorMessage>({
      email: '',
      token: '',
      newPassword: '',
      confirmPassword: ''
    })

    const resetErrors = () => {
      errorMessage.value = {
        email: '',
        token: '',
        newPassword: '',
        confirmPassword: ''
      }
    }

    // --- Validation locale par étape ---
    const validateStep1 = (): boolean => {
      resetErrors()
      if (!form.value.email.trim()) {
        errorMessage.value.email = "Veuillez entrer votre email."
        return false
      }
      return true
    }

    const validateStep2 = (): boolean => {
      resetErrors()
      if (!form.value.token.trim()) {
        errorMessage.value.token = "Veuillez entrer le code reçu."
        return false
      }
      return true
    }

    const validateStep3 = (): boolean => {
      resetErrors()
      let isValid = true
      if (!form.value.newPassword) {
        errorMessage.value.newPassword = "Veuillez entrer un nouveau mot de passe."
        isValid = false
      }
      if (form.value.newPassword !== form.value.confirmPassword) {
        errorMessage.value.confirmPassword = "Les mots de passe ne correspondent pas."
        isValid = false
      }
      return isValid
    }

    // --- 1. Envoi de la requête pour l'envoi du mail ---
    const sendResetEmail = async () => {
      try {
        await authStore.resetPassword({ email: form.value.email })
      } catch (err: any) {
        console.error("erreur survenue", err)
      }
    }

    // --- 2. Vérification du token ---
    const verifyResetToken = async () => {
      try{
        await authStore.ConfirmToken({ email: form.value.email, token: form.value.token });
      } catch(err:any){
        console.error("erreur survenue", err)
      }
    }

    // --- 3. Réinitialisation du mot de passe ---
    const resetPassword = async () => {
      try {
        await authStore.ChangePassword({
        email: form.value.email,
        token: form.value.token,
        new_password: form.value.newPassword,
        confirm_password: form.value.confirmPassword
      })
      } catch (err: any) {
        console.error("erreur survenue", err)
      }
    }

    // --- Dispatch selon l'étape courante ---
    const handleSubmit = async () => {
      try {
        if (step.value === 1) {
          if (!validateStep1()) return
          await sendResetEmail()
          step.value = 2
        } else if (step.value === 2) {
          if (!validateStep2()) return
          await verifyResetToken()
          step.value = 3
        } else if (step.value === 3) {
          if (!validateStep3()) return
          await resetPassword()
          router.push('/auth/login')
        }
      } catch (error) {
        console.log('[ResetPassword] Erreur capturée', error)
      }
    }

    return {
      authStore,
      step,
      form,
      errorMessage,
      handleSubmit
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
  margin-top: 15px;
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