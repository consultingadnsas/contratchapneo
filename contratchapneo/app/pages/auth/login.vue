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
          
          <div class="input-group">
            <label for="email">Adresse Email</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="cabinet@exemple.com" 
              required 
            />
          </div>

          <div class="input-group">
            <label for="password">Mot de passe d'accès</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="••••••••" 
              required 
            />
          </div>

          <div class="form-options">
            <label class="checkbox-container">
              <input type="checkbox" v-model="rememberMe" />
              <span class="checkmark"></span>
              Se souvenir de moi
            </label>
            
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
          <p>Vous n'avez pas de pack ?</p>
          <a href="#" @click.prevent="$router.push('/achat-pack')" class="buy-link">Achetez-en un !</a>
        </div>

      </div>
    </div>

  </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export default {
  name: 'LoginPack',
  setup() {
    const router = useRouter();
    const email = ref('');
    const password = ref('');
    const rememberMe = ref(false);
    const isLoading = ref(false);
    
    const loginFailed = ref(false);

    const handleLogin = async () => {
      isLoading.value = true;
      loginFailed.value = false;

      // Simulation d'un appel API pour la connexion
      setTimeout(() => {
        isLoading.value = false;
        loginFailed.value = true; 
        console.log('Échec de la connexion pour', email.value);
      }, 1500);
    };

    return {
      email,
      password,
      rememberMe,
      isLoading,
      loginFailed,
      handleLogin,
      router
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
  padding: 1rem; /* Padding réduit */
  font-family: 'Inter', sans-serif;
  
  background: 
    linear-gradient(rgba(30, 41, 59, 0.45), rgba(30, 41, 59, 0.65)),
    url('/AA.jpg') center/cover no-repeat;
}

/* --- WRAPPER DU DOSSIER --- */
.dossier-wrapper {
  width: 100%;
  max-width: 440px; /* Légèrement réduit pour être plus proportionné sans scroll */
  position: relative;
  z-index: 10;
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
  padding: 0.8rem 0.8rem 0.8rem 0.8rem; /* 👈 Marges internes réduites pour gagner de la place */
  position: relative;
  z-index: 1;
}

.floating-shadow {
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.25), 0 0 0 1px rgba(255,255,255,0.1);
}

/* --- EN-TÊTE DU FORMULAIRE --- */
.dossier-header {
  margin-bottom: 1.5rem; /* Réduit */
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
  gap: 0.85rem; /* Réduit (était à 1rem) */
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
  flex-direction: row; /* 👈 Changé de column à row pour être sur 1 seule ligne */
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