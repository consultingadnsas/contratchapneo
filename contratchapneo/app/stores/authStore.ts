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
  });

  const isLoading = ref(false);
  const error = ref<string | null>(null);

  const { $api } = useNuxtApp();

  // --- Getters ---
  // Fonction utilitaire interne pour extraire l'objet utilisateur quelle que soit l'imbrication de l'API
  const getSafeUser = () => {
    if (user.value && (user.value as any).user) {
      return (user.value as any).user;
    }
    return user.value || {};
  };

  // ⚡️ Source unique de vérité : Vérifie si le compte est authentifié et ignore "AnonymousUser"
  const isAuthenticated = computed(() => {
    const u = getSafeUser();
    return Boolean(
      (u.username && u.username !== '' && u.username !== 'AnonymousUser') ||
      (u.email && u.email !== '')
    );
  });

  // ⚡️ Calcul automatique des initiales pour la Navbar et le Dashboard
  const userInitials = computed(() => {
    const u = getSafeUser();
    if (u.first_name && u.last_name) {
      return (u.first_name.charAt(0) + u.last_name.charAt(0)).toUpperCase();
    } else if (u.username && u.username !== 'AnonymousUser') {
      return u.username.substring(0, 2).toUpperCase();
    }
    return 'DB';
  });

  // --- Actions ---
  const register = async (payload: Omit<User, 'id'>) => {
    isLoading.value = true;
    error.value = null;

    try {
      const response = await $api('/account/register/', {
        method: 'POST',
        body: payload
      });

      if (response) {
        console.log('Réponse de création', response);
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
  };

  const login = async (credentials: Pick<User, 'email' | 'username' | 'password'>) => {
    isLoading.value = true;
    error.value = null;

    console.log('[AuthStore] login() → credentials envoyés :', credentials);

    try {
      const response = await $api('/account/login/', {
        method: 'POST',
        body: credentials,
      });

      if (response) {
        console.log('[AuthStore] login() → réponse reçue :', response);
        user.value = (response as any).data?.user || {};
        return response;
      } else {
        console.log('[AuthStore] login() → erreur :', response);
        error.value = "Identifiants incorrects";
        throw new Error("Identifiants incorrects");
      }

    } catch (err: any) {
      console.error('[AuthStore] login() → erreur :', err);
      error.value = err.message;
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const getProfile = async () => {
    isLoading.value = true;

    try {
      const response = await $api<User>('/account/me/', {
        method: 'GET',
      });

      if (response) {
        user.value = response;
        console.log(user.value);
      }
    } catch (err: any) {
      throw err;
    } finally {
      isLoading.value = false;
    }
  };

  const updateProfile = async (payload:User) => {

    isLoading.value = true;

    try {

      const response = await $api('/account/me/',{
        method:'PATCH',
        body:payload
      })

      if(response){

        console.log("Mise à jour résussie", response)
      }

    } catch(err:any){
      console.error("Une erreur esrt survenue lors de la mise à jour", err)
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

  const resetPassword = async(payload: ForgotPasswordPayload) => {
    
    isLoading.value = true;

    try{

      const response = await $api('/account/password-reseting/', {
        method:'POST',
        body:{email: payload},
      })

      if(response){
        console.log("Votre reponse", response)
      }

    } catch(err:any) {

      console.log("Erreur survenue", err)

    } finally {
      isLoading.value = false;
    }

  }

  const ConfirmToken = async(payload:VerifyTokenPayload) => {
    
    isLoading.value = true;

    try{

      const response = await $api('/account/password-reset/verify-token/', {
        method:'POST',
        body:{token: payload},
      })

      if(response){
        console.log("Votre reponse", response)
      }

    } catch(err:any) {

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
    register,
    login,
    getProfile,
    logout,
    updateProfile,
    resetPassword,
    ConfirmToken,
    ChangePassword
  };
});