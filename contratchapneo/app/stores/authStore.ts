import { defineStore } from "pinia";
import { ref } from "vue";

export interface User {
  id?: string | number;
  username: string;
  first_name?: string;
  last_name?: string;
  password: string;
  email: string;
  phone_number: string;
  user_type: string;
}

export const useAuthStore = defineStore('auth', () => {

  // State
  const user = ref<User>({
    id: '',
    username: '',
    first_name: '',
    last_name: '',
    password: '',
    email: '',
    phone_number: '',
    user_type: ''
  })

  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // $api accessible dans Pinia via useNuxtApp()
  const { $api } = useNuxtApp()

  // Actions
  const register = async (payload: Omit<User, 'id'>) => {
    isLoading.value = true
    error.value = null

    console.log('[AuthStore] register() → payload envoyé :', payload)

    try {
      const response = await $api('/auth/register', {
        method: 'POST',
        body: payload,
      })

      console.log('[AuthStore] register() → réponse reçue :', response)

      user.value = response.user // adapte selon ta structure de réponse
      
      return response

    } catch (err: any) {
      console.error('[AuthStore] register() → erreur :', err)
      console.error('[AuthStore] status :', err?.response?.status)
      console.error('[AuthStore] message :', err?.data?.message ?? err.message)

      error.value = err?.data?.message ?? 'Erreur inconnue'
      throw err

    } finally {
      isLoading.value = false
      console.log('[AuthStore] register() → terminé, isLoading =', isLoading.value)
    }
  }

  return {
    user,
    isLoading,
    error,
    register,
  }
})