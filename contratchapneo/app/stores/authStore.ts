import { defineStore } from "pinia";
import { ref } from "vue";
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

  const { $api } = useNuxtApp()

 // Actions
  const register = async (payload: Omit<User, 'id'>) => {
    
    isLoading.value = true;
    error.value = null; // ⚡️ On réinitialise l'erreur proprement

    try {
      const response = await $api('/account/register/', {
        method: 'POST',
        body: payload
      })

      if (response) {
        // Debuging
        console.log('Réponse de création', response)
        await navigateTo('/auth/login'); // ⚡️ N'oublie pas le await pour la navigation
      }

    } catch (err: any) {
      console.error("Détails de l'erreur backend :", err.response?._data);
      
      // ⚡️ CORRECTION : Extraction des vraies erreurs renvoyées par Django
      if (err.response && err.response._data) {
          const data = err.response._data;
          if (data.errors) {
              // Récupère la première erreur (ex: username déjà pris)
              const firstKey = Object.keys(data.errors)[0];
              error.value = data.errors[firstKey][0];
          } else {
              error.value = data.message || "Erreur lors de l'inscription.";
          }
      } else {
          error.value = "Impossible de joindre le serveur.";
      }
      
      // On lève l'erreur pour que le formulaire puisse arrêter son traitement si besoin
      throw err; 

    } finally {
      // ⚡️ Ça arrête le spinner quoi qu'il arrive
      isLoading.value = false;
    }
  }

  // Nouvelle action pour le Login
  const login = async (credentials: Pick<User, 'email' | 'username' | 'password'>) => {
    isLoading.value = true
    error.value = null

    console.log('[AuthStore] login() → credentials envoyés :', credentials)

    try {
      // Ajuste l'URL '/auth/login' selon la structure de ton backend
      const response = await $api('/account/login/', {
        method: 'POST',
        body: credentials,
      })

      if (response){
        console.log('[AuthStore] login() → réponse reçue :', response)

        // Met à jour l'utilisateur (ou gère le stockage du token ici si nécessaire)
        user.value = (response as any).data?.user || {}

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
      // 1. Avertir le backend de fermer la session (invalider le token côté serveur)
      await $api('/account/logout/', {
        method: 'POST'
      });
    } catch (err: any) {
      // On capture l'erreur mais on ne bloque pas la suite. 
      // Si le backend échoue (ex: token déjà expiré), on DOIT quand même déconnecter l'utilisateur localement.
      console.error('❌ Erreur lors de la déconnexion backend :', err);
    } finally {
      // 2. Vider le state utilisateur localement (CRUCIAL)
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

      // 3. Supprimer le(s) cookie(s) d'authentification
      const token = useCookie('token');
      token.value = null; 
      
      //4. Vider les autres stores (Panier et Profil)
      // Importe ces stores en haut de ton fichier si ce n'est pas fait
      const cartStore = useCartStore();
      const profileStore = useProfileStore();
      
      // On utilise nos nouvelles fonctions personnalisées !
      cartStore.clearLocalCart();
      profileStore.clearLocalProfile();

      console.log('✅ Déconnexion locale réussie et state purgé !');
      isLoading.value = false;

      // 5. Rediriger l'utilisateur vers la page de connexion
      await navigateTo('/auth/login', { replace: true }); 
    }
  };

  const resetPassword = async(payload: ForgotPasswordPayload) => {
    
    isLoading.value = true;

    try{

      const response = await $api('/account/password-reseting/', {
        method:'POST',
        body: payload,
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
        body: payload,
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