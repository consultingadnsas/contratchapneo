import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { useCartStore } from './cartStore';
import { useProfileStore } from './profileStore';

export interface User {
  id?: string | number;
  username: string;
  first_name?: string;
  last_name?: string;
  password: string;
  email: string;
  phone_number: string;
  user_type?: string;
}

interface ForgotPasswordPayload {
  email: string
}

export interface VerifyTokenPayload {
  email: string
  token: string
}

export interface ChangePasswordPayload {
  email: string
  token: string
  new_password: string
  confirm_password: string
}

export const useAuthStore = defineStore('auth', () => {

  // --- State ---
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

  const { $api } = useNuxtApp()

  // --- Getters (Réintégrés pour le Middleware, la Navbar et le Dashboard) ---
  const getSafeUser = () => {
    if (user.value && (user.value as any).user) {
      return (user.value as any).user;
    }
    return user.value || {};
  };

  const isAuthenticated = computed(() => {
    const u = getSafeUser();
    return Boolean(
      (u.username && u.username !== '' && u.username !== 'AnonymousUser') ||
      (u.email && u.email !== '')
    );
  });

  const userInitials = computed(() => {
    const u = getSafeUser();
    if (u.first_name && u.last_name) {
      return (u.first_name.charAt(0) + u.last_name.charAt(0)).toUpperCase();
    } else if (u.username && u.username !== 'AnonymousUser') {
      return u.username.substring(0, 2).toUpperCase();
    }
    return 'DB';
  });

  const displayName = computed(() => {
    const u = getSafeUser();
    if (u.first_name && u.first_name !== '') {
      return u.first_name;
    } else if (u.username && u.username !== '' && u.username !== 'AnonymousUser') {
      return u.username;
    } else if (u.email && u.email !== '') {
      return u.email.split('@')[0];
    }
    return 'invité';
  });

  // --- Actions ---
  const register = async (payload: Omit<User, 'id'>) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api('/account/register/', {
        method: 'POST',
        body: payload
      })

      if (response) {
        console.log('Réponse de création', response)
        await navigateTo('/auth/login');
      }

    } catch (err: any) {
      console.error("Détails de l'erreur backend :", err.response?._data);
      
      if (err.response && err.response._data) {
          const data = err.response._data;
          if (data.errors) {
              const firstKey = Object.keys(data.errors)[0];
              error.value = data.errors[firstKey][0];
          } else {
              error.value = data.message || "Erreur lors de l'inscription.";
          }
      } else {
          error.value = "Impossible de joindre le serveur.";
      }
      
      throw err; 

    } finally {
      isLoading.value = false;
    }
  }

  // Action pour le Login avec enregistrement du token + chargement du profil
  const login = async (credentials: Pick<User, 'email' | 'username' | 'password'>) => {
    isLoading.value = true
    error.value = null

    console.log('[AuthStore] login() → credentials envoyés :', credentials)

    try {
      const response = await $api('/account/login/', {
        method: 'POST',
        body: credentials,
      })

      if (response) {
        console.log('[AuthStore] login() → réponse reçue :', response)

        // 1. Enregistrer le token dans les cookies Nuxt (Indispensable pour le SSR & Middleware)
        const resData = (response as any).data || response;
        const tokenCookie = useCookie('token', {
          maxAge: 60 * 60 * 24 * 7, // 7 jours
          sameSite: 'lax'
        });
        
        tokenCookie.value = resData.token || resData.access || resData.key;
        console.log('[AuthStore] ✅ Cookie token enregistré :', tokenCookie.value);

        // 2. Charger directement le profil complet via getProfile()
        await getProfile();

        return response
      } else {
        console.log('[AuthStore] login() → erreur :', response)
        error.value = "Identifiants incorrects"
        throw new Error("Identifiants incorrects")
      }

    } catch (err: any) {
      console.error('[AuthStore] login() → erreur :', err)
      error.value = err.message
      throw err
    } finally {
      isLoading.value = false
    }
  }

  // Ton getProfile fusionné et respecté à 100% (avec le { user: User })
  const getProfile = async () => {
    isLoading.value = true;

    try {
      const response = await $api<{ user: User }>('/account/me/', {
        method: 'GET',
      });

      console.log("Réponse brute", response);

      if (response?.user) {
        user.value = response.user; // ✅ extrait l'objet user
        console.log('Vos informations utilisateurs', user.value);
      }
    } catch (err: any) {
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateProfile = async (payload: User) => {
    isLoading.value = true;

    try {
      const response = await $api('/account/me/', {
        method: 'PATCH',
        body: payload
      })

      if (response) {
        console.log("Mise à jour réussie", response)
      }

    } catch (err: any) {
      console.error("Une erreur est survenue lors de la mise à jour", err)
    } finally {
      isLoading.value = false;
    }
  }

  const logout = async () => {
    isLoading.value = true;

    try {
      await $api('/account/logout/', {
        method: 'POST'
      });
    } catch (err: any) {
      console.error('❌ Erreur lors de la déconnexion backend :', err);
    } finally {
      user.value = {
        id: '',
        username: '',
        first_name: '',
        last_name: '',
        password: '',
        email: '',
        phone_number: '',
        user_type: ''
      };

      const token = useCookie('token');
      token.value = null; 
      
      const cartStore = useCartStore();
      const profileStore = useProfileStore();
      
      cartStore.clearLocalCart();
      profileStore.clearLocalProfile();

      console.log('✅ Déconnexion locale réussie et state purgé !');
      isLoading.value = false;

      await navigateTo('/auth/login', { replace: true }); 
    }
  };

  const resetPassword = async (payload: ForgotPasswordPayload) => {
    isLoading.value = true;

    try {
      const response = await $api('/account/password-reseting/', {
        method: 'POST',
        body: payload,
      })

      if (response) {
        console.log("Votre reponse", response)
      }

    } catch (err: any) {
      console.log("Erreur survenue", err)
    } finally {
      isLoading.value = false;
    }
  }

  const ConfirmToken = async (payload: VerifyTokenPayload) => {
    isLoading.value = true;

    try {
      const response = await $api('/account/password-reset/verify-token/', {
        method: 'POST',
        body: payload,
      })

      if (response) {
        console.log("Votre reponse", response)
      }

    } catch (err: any) {
      console.log("Erreur survenue", err)
    } finally {
      isLoading.value = false;
    }
  }

  const ChangePassword = async (payload: ChangePasswordPayload) => {
    isLoading.value = true
    try {
      const response = await $api('/account/password-reset/confirm/', {
        method: 'POST',
        body: payload   // déjà au bon format, pas de ré-enveloppement
      })
      if (response) {
        console.log("Votre reponse", response)
      }
      return response
    } catch (err: any) {
      console.log("Erreur survenue", err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    userInitials,
    displayName,
    register,
    login,
    getProfile,
    logout,
    updateProfile,
    resetPassword,
    ConfirmToken,
    ChangePassword
  }
})