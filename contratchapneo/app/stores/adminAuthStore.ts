import { defineStore } from 'pinia';
import { ref } from 'vue';
import { useNuxtApp, useRouter } from '#app';

export interface AdminUser {
    id: string;
    username: string;
    email: string;
    first_name: string;
    last_name: string;
    user_type?: string;
    is_staff?: boolean; // Hérité de AbstractUser de Django
    is_superuser?: boolean;
}

export const useAdminAuthStore = defineStore('adminAuth', () => {
    const { $api } = useNuxtApp();
    const router = useRouter();

    // --- STATE ---
    const user = ref<AdminUser | null>(null);
    const isAuthenticated = ref<boolean>(false);
    const isLoading = ref<boolean>(false);
    const error = ref<string | null>(null);

    // --- ACTIONS ---

    // 1. SE CONNECTER
    async function login(identifier: string, password: string) {
        isLoading.value = true;
        error.value = null;

        try {
            const response = await $api<any>('/account/login/', { 
                method: 'POST',
                body: { username: identifier, password: password } 
            });

            if (response && response.user) {
                // ⚡️ LE BOUCLIER DE SÉCURITÉ EST ICI
                if (!response.user.is_staff && !response.user.is_superuser) {
                    
                    // 1. L'utilisateur est un client normal. On détruit immédiatement sa session.
                    await $api<any>('/account/logout/', { method: 'POST' });
                    
                    // 2. On affiche un message d'erreur
                    error.value = "Accès refusé : Vous n'avez pas les droits d'administration.";
                    return false; // On bloque la redirection
                }

                // Si c'est un vrai admin, on valide la session
                user.value = response.user;
                isAuthenticated.value = true;
                return true; 
            }
            
            return false;
        } catch (err: any) {
            error.value = err.message || "Identifiants incorrects ou erreur de connexion.";
            console.error("Erreur de connexion Admin:", err);
            return false;
        } finally {
            isLoading.value = false;
        }
    }

    // 2. RÉCUPÉRER LE PROFIL (Vérifier la session au chargement)
    async function fetchProfile() {
        isLoading.value = true;
        
        try {
            // Appel à ton UserProfileView (GET /me/) protégé par IsAuthenticated
            const response = await $api<any>('/account/me/', { // 👈 Ajuste le chemin exact
                method: 'GET'
            });

            if (response && response.user) {
                user.value = response.user;
                isAuthenticated.value = true;
            }
        } catch (err: any) {
            // Si l'appel échoue (token expiré ou absent), on déconnecte
            user.value = null;
            isAuthenticated.value = false;
            console.warn("Session admin invalide ou expirée.");
        } finally {
            isLoading.value = false;
        }
    }

    // 3. SE DÉCONNECTER
    async function logout() {
        isLoading.value = true;
        try {
            // Appel à ton LogoutView qui blacklist le token et supprime les cookies
            await $api<any>('/account/logout/', { // 👈 Ajuste le chemin exact
                method: 'POST'
            });
        } catch (err: any) {
            console.error("Erreur lors de la déconnexion côté serveur:", err);
        } finally {
            // Même si le serveur plante, on vide le state local et on renvoie au login
            user.value = null;
            isAuthenticated.value = false;
            isLoading.value = false;
            router.push('/auth/adminlogin'); // 👈 Ajuste la route de ta page de login admin
        }
    }

    return {
        // State
        user,
        isAuthenticated,
        isLoading,
        error,
        // Actions
        login,
        fetchProfile,
        logout
    };
});