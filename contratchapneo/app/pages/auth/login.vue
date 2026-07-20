<template>
  <div class="login-hero-page">
    
    <div class="dossier-wrapper">
      
      <div class="dossier-tab">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="tab-icon">
          <path stroke-linecap="round" stroke-linejoin="round" d="M16.5 10.5V6.75a4.5 4.5 0 1 0-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 0 0 2.25-2.25v-6.75a2.25 2.25 0 0 0-2.25-2.25H6.75a2.25 2.25 0 0 0-2.25 2.25v6.75a2.25 2.25 0 0 0 2.25 2.25Z" />
        </svg>
        <span>Accès Client</span>
      </div>

      <div class="dossier-body floating-shadow">
        
        <div class="dossier-header">
          <h2>Ouvrir votre compte</h2>
          <p>Connectez-vous pour accéder à votre pack de services juridiques.</p>
        </div>

        <form @submit.prevent="handleLogin" class="dossier-form">
          
          <BaseInput 
            label="Email/username" 
            placeholder="Entrer username/email"
            v-model="loginForm.identifier"
            :errorMessage="errors.identifier"
        />

        <BaseInput 
            label="Mot de passe" 
            placeholder="Entrer un mot de passe"
            type="password"
            v-model="loginForm.password"
            :errorMessage="errors.password"
        />


          <div class="form-options">
            <a href="#" v-if="loginFailed" class="forgot-link fade-in">Code perdu ?</a>
          </div>

          <p v-if="loginFailed" class="error-message fade-in">
            Identifiants incorrects. Veuillez réessayer ou récupérer votre code.
          </p>

          <button type="submit" class="btn-dossier" :disabled="isLoading">
            <span v-if="isLoading" class="loader"></span>
            <span v-else>Accéder à mon compte</span>
          </button>

        </form>

        <div class="purchase-section">
          <p>Vous n'avez pas de compte ?</p>
          <a href="#" @click.prevent="$router.push('/achat-pack')" class="buy-link">créez-en un !</a>
        </div>

      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/authStore'
import { validateForm } from '../../utils/validators'

import BaseInput from '../../components/input/BaseInput.vue'

export default {
  name: 'LoginPack',
  components: {
    BaseInput,
  },
  setup() {
    const router = useRouter();
    const authStore = useAuthStore();
    
    // 1. On utilise "identifier" au lieu de séparer email et username
    const loginForm = ref({ 
        identifier: "", 
        password: "" 
    });

    const errors = ref<Record<string, string>>({});
    const loginFailed = ref(false);
    const isLoading = ref(false); // Pour ton bouton de chargement

    const handleLogin = async () => {
      // On réinitialise l'état d'erreur général
      loginFailed.value = false;

      // 2. On valide les deux champs (ça va vérifier s'ils ne sont pas vides)
      const validation = validateForm(loginForm.value);
      errors.value = validation.errors;
      
      if (validation.isValid) {
        isLoading.value = true;
        
        try {
          // 3. LA MAGIE EST ICI 🪄 : On détecte s'il y a un '@'
          const isEmail = loginForm.value.identifier.includes('@');

          // 4. On construit l'objet exactement comme ton backend l'attend
          const payload = {
            password: loginForm.value.password,
            // Si isEmail est vrai, on crée la clé 'email', sinon on crée 'username'
            ...(isEmail 
                ? { email: loginForm.value.identifier } 
                : { username: loginForm.value.identifier }
            )
          };

          console.log("Données prêtes à être envoyées :", payload);

          // 5. On envoie au store
          await authStore.login(payload);
          
          // Redirection après succès (si non gérée dans le store)
          router.push('/profile/dashboard'); 

        } catch (error) {
          console.error("Erreur de connexion :", error);
          loginFailed.value = true;
        } finally {
          isLoading.value = false;
        }
      }
    };

    return {
      router,
      authStore,
      loginForm,
      errors,
      loginFailed,
      isLoading,
      handleLogin,
    };
  }
}
</script>

<style scoped>
/* --- FOND DE LA PAGE --- */
.login-hero-page {
  height: 100vh; /* 👈 Fixé à 100vh exactement */
  overflow: hidden; /* 👈 Empêche tout scroll sur la page */
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 0.1rem; /* Padding réduit */
  font-family: 'Inter', sans-serif;
  
  background: 
    linear-gradient(rgba(30, 41, 59, 0.45), rgba(30, 41, 59, 0.65)),
    url('/AA.jpg') center/cover no-repeat;
}

/* --- WRAPPER DU DOSSIER --- */
.dossier-wrapper {
  width: 100%;
  max-width: 420px; /* Légèrement réduit pour être plus proportionné sans scroll */
  position: relative;
  z-index: 10;
  overflow: auto;
}

/* --- L'ONGLET DU DOSSIER --- */
.dossier-tab {
  background-color: #ffffff;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.5rem 0.8rem 1.5rem; /* Réduit */
  border-radius: 12px 12px 0 0;
  font-weight: 800;
  color: #156ca9;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  position: relative;
  z-index: 2;
  transform: translateY(2px); 
}

.tab-icon {
  width: 16px;
  height: 16px;
}

/* --- CORPS DU DOSSIER --- */
.dossier-body {
  background-color: #ffffff;
  border-radius: 0 20px 20px 20px;
  padding: 0.5rem 0.5rem 0.5rem 0.5rem; /* 👈 Marges internes réduites pour gagner de la place */
  position: relative;
  z-index: 1;
}

.floating-shadow {
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255,255,255,0.1);
}

/* --- EN-TÊTE DU FORMULAIRE --- */
.dossier-header {
  margin-bottom: 0.1rem; /* Réduit */
}

.dossier-header h2 {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 0.2rem 0;
  letter-spacing: -0.5px;
}

.dossier-header p {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0;
  line-height: 1.4;
}

/* --- FORMULAIRE --- */
.dossier-form {
  display: flex;
  flex-direction: column;
  gap: 0.7rem; /* Réduit (était à 1rem) */
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.input-group label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #334155;
}

.input-group input {
  padding: 0.75rem 1rem; /* 👈 Padding réduit pour des champs moins hauts */
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  background-color: #f8fafc;
  font-size: 0.95rem;
  color: #1e293b;
  outline: none;
  transition: all 0.3s ease;
}

.input-group input:focus {
  border-color: #156ca9;
  background-color: #ffffff;
  box-shadow: 0 0 0 4px rgba(21, 108, 169, 0.1);
}

/* --- OPTIONS --- */
.form-options {
  display: flex;
  flex-direction: column; /* 👈 Changé de column à row pour être sur 1 seule ligne */
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  margin-top: 0.2rem;
  min-height: 20px;
}

.checkbox-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #475569;
  font-weight: 500;
}

.forgot-link {
  color: #ef4444; 
  font-weight: 700;
  text-decoration: none;
  transition: opacity 0.2s;
}

.forgot-link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.error-message {
  font-size: 0.8rem;
  color: #ef4444;
  margin: 0;
  font-weight: 500;
}

/* Animation douce pour l'apparition */
.fade-in {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(-5px); }
  to { opacity: 1; transform: translateY(0); }
}

/* --- BOUTON D'ACTION --- */
.btn-dossier {
  background-color: #1e293b;
  color: #ffffff;
  border: none;
  border-radius: 50px;
  padding: 0.9rem; /* 👈 Réduit (était à 1.1rem) */
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 0.5rem; /* Réduit */
}

.btn-dossier:hover:not(:disabled) {
  background-color: #156ca9; 
  transform: translateY(-2px);
  box-shadow: 0 8px 15px rgba(21, 108, 169, 0.2);
}

.btn-dossier:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loader {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-top: 3px solid #ffffff;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* --- SECTION D'ACHAT --- */
.purchase-section {
  margin-top: 1.5rem; /* 👈 Réduit (était à 2.5rem) */
  padding-top: 1rem; /* 👈 Réduit (était à 1.5rem) */
  border-top: 1px solid #e2e8f0;
  text-align: center;
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.purchase-section p {
  color: #64748b;
  font-size: 0.85rem;
  margin: 0;
}

.buy-link {
  color: #156ca9;
  font-weight: 800;
  font-size: 0.95rem;
  text-decoration: none;
  transition: color 0.2s ease;
}

.buy-link:hover {
  color: #0f4c78;
  text-decoration: underline;
}

/* --- RESPONSIVE MOBILE --- */
@media (max-width: 480px) {
  /* Si l'écran est VRAIMENT trop petit sur mobile, on autorise le défilement uniquement dans la carte */
  .dossier-body {
    padding: 1.5rem 1.2rem;
    border-radius: 0 16px 16px 16px;
    max-height: 85vh;
    overflow-y: auto;
  }
  .dossier-header h2 {
    font-size: 1.3rem;
  }
}
</style>