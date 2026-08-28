<template>
    <div class="split-register-container">
        
        <!-- 🟩 PANNEAU GAUCHE : Stepper visuel -->
        <aside class="stepper-sidebar">
            <div class="sidebar-content">
                <h1 class="hero-title">Rejoignez<br>nous</h1>
                <p class="hero-subtitle">Complétez ces étapes simples pour créer votre compte.</p>

                <div class="stepper-cards">
                    <!-- Étape 1 -->
                    <div class="step-card" :class="{ 'active': currentStep === 1, 'completed': currentStep > 1 }">
                        <div class="step-icon">1</div>
                        <div class="step-text">
                            <h4>Informations de base</h4>
                            <p>Identité et contact</p>
                        </div>
                    </div>
                    <!-- Étape 2 -->
                    <div class="step-card" :class="{ 'active': currentStep === 2, 'completed': currentStep > 2 }">
                        <div class="step-icon">2</div>
                        <div class="step-text">
                            <h4>Détails du compte</h4>
                            <p>Profil utilisateur</p>
                        </div>
                    </div>
                    <!-- Étape 3 -->
                    <div class="step-card" :class="{ 'active': currentStep === 3 }">
                        <div class="step-icon">3</div>
                        <div class="step-text">
                            <h4>Sécurité</h4>
                            <p>Mot de passe</p>
                        </div>
                    </div>
                </div>
            </div>
        </aside>

        <!-- ⬛️ PANNEAU DROIT : Formulaire -->
        <main class="form-section">
            <div class="form-wrapper">
                <div class="form-header">
                    <h2>Créer un compte</h2>
                    <p>Entrez vos données personnelles pour commencer.</p>
                </div>

                <form @submit.prevent="submitForm" class="step-form">
                    
                    <!-- 📦 ÉTAPE 1 : Identité -->
                    <div v-show="currentStep === 1" class="form-step">
                        <div class="input-row">
                            <BaseInput
                                label="Prénom"
                                v-model="registrationForm.first_name"
                                placeholder="Ex: John"
                                :errorMessage="errors.first_name"
                            />
                            <BaseInput
                                label="Nom"
                                v-model="registrationForm.last_name"
                                placeholder="Ex: Doe"
                                :errorMessage="errors.last_name"
                            />
                        </div>
                        <BaseInput
                            label="Email"
                            v-model="registrationForm.email"
                            placeholder="Ex: john.doe@gmail.com"
                            :errorMessage="errors.email"
                        />
                    </div>

                    <!-- 📦 ÉTAPE 2 : Compte -->
                    <div v-show="currentStep === 2" class="form-step">
                        <BaseInput
                            label="Nom d'utilisateur"
                            v-model="registrationForm.username"
                            placeholder="Ex: john_doe99"
                            :errorMessage="errors.username"
                        />
                        <BaseInput
                            label="N° de téléphone"
                            v-model="registrationForm.phone_number"
                            placeholder="Ex: +225 0102030405"
                            :errorMessage="errors.phone_number"
                        />
                    </div>

                    <!-- 📦 ÉTAPE 3 : Sécurité -->
                    <div v-show="currentStep === 3" class="form-step">
                        <BaseInput
                            label="Mot de passe"
                            v-model="registrationForm.password"
                            placeholder="Entrez un mot de passe"
                            :errorMessage="errors.password"
                            type="password"
                        />
                        <BaseInput
                            label="Confirmer le mot de passe"
                            v-model="registrationForm.confirm_password"
                            placeholder="Répétez le mot de passe"
                            :errorMessage="errors.confirm_password"
                            type="password"
                        />
                    </div>

                    <!-- Erreur globale backend -->
                    <div class="error-message" v-if="authStore.error">
                        <p>{{ authStore.error }}</p>
                    </div>

                    <!-- 🔘 BOUTONS D'ACTION -->
                    <div class="form-actions">
                        <button 
                            type="button" 
                            class="btn-back" 
                            v-if="currentStep > 1" 
                            @click="prevStep"
                            :disabled="isSubmitting"
                        >
                            Précédent
                        </button>
                        
                        <!-- Si on n'est pas à la dernière étape, bouton "Suivant" -->
                        <mainButton 
                            v-if="currentStep < 3" 
                            type="button" 
                            label="Suivant"
                            @click="nextStep"
                            class="btn-next"
                        />
                        
                        <!-- Si on est à la dernière étape, bouton "S'inscrire" -->
                        <mainButton 
                            v-if="currentStep === 3" 
                            type="submit" 
                            label="S'inscrire"
                            :isloading="isSubmitting"
                            class="btn-submit"
                        />
                    </div>

                    <div class="login-link">
                        <p>Vous avez déjà un compte ? <router-link to="/login">Connectez-vous</router-link></p>
                    </div>

                </form>
            </div>
        </main>

    </div>
</template>

<script lang="ts">
import { ref } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'
import { useAuthStore } from '../../stores/authStore'

export default {
    components: {
        BaseInput,
        mainButton
    },
    setup() {
        const authStore = useAuthStore();
        
        const currentStep = ref(1);
        const isSubmitting = ref(false);

        // Ajout des nouveaux champs demandés
        const registrationForm = ref({
            first_name: "",
            last_name: "",
            email: "",
            username: "",
            phone_number: "",
            password: "",
            confirm_password: ""
        });

        const errors = ref({
            first_name: "",
            last_name: "",
            email: "",
            username: "",
            phone_number: "",
            password: "",
            confirm_password: ""
        });

        const clearErrors = () => {
            Object.keys(errors.value).forEach(key => {
                errors.value[key as keyof typeof errors.value] = "";
            });
        };

        // Validation par étape pour bloquer l'avancement si invalide
        const validateStep = (step: number): boolean => {
            clearErrors();
            let isValid = true;

            if (step === 1) {
                if (!registrationForm.value.first_name.trim()) { errors.value.first_name = "Requis"; isValid = false; }
                if (!registrationForm.value.last_name.trim()) { errors.value.last_name = "Requis"; isValid = false; }
                
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!registrationForm.value.email.trim()) { errors.value.email = "Requis"; isValid = false; }
                else if (!emailRegex.test(registrationForm.value.email)) { errors.value.email = "Email invalide"; isValid = false; }
            } 
            else if (step === 2) {
                const usernameRegex = /^[\w.@+-]+$/;
                if (!registrationForm.value.username.trim()) { errors.value.username = "Requis"; isValid = false; }
                else if (!usernameRegex.test(registrationForm.value.username)) { errors.value.username = "Pas d'espaces autorisés"; isValid = false; }
                
                if (!registrationForm.value.phone_number.trim()) { errors.value.phone_number = "Requis"; isValid = false; }
            } 
            else if (step === 3) {
                if (!registrationForm.value.password) { errors.value.password = "Requis"; isValid = false; }
                else if (registrationForm.value.password.length < 8) { errors.value.password = "8 caractères minimum"; isValid = false; }
                
                if (registrationForm.value.password !== registrationForm.value.confirm_password) {
                    errors.value.confirm_password = "Les mots de passe ne correspondent pas";
                    isValid = false;
                }
            }
            return isValid;
        };

        const nextStep = () => {
            if (validateStep(currentStep.value)) {
                currentStep.value++;
            }
        };

        const prevStep = () => {
            if (currentStep.value > 1) currentStep.value--;
        };

        const submitForm = async () => {
            if (validateStep(3)) {
                isSubmitting.value = true;
                try {
                    // Attention: Assure-toi que la fonction authStore.register 
                    // accepte bien les nouveaux champs (first_name, last_name, etc.)
                    await authStore.register({
                        username: registrationForm.value.username,
                        email: registrationForm.value.email,
                        phone_number: registrationForm.value.phone_number,
                        password: registrationForm.value.password,
                        first_name: registrationForm.value.first_name,
                        last_name: registrationForm.value.last_name
                    });
                } catch (error) {
                    console.error("L'inscription a échoué.", error);
                } finally {
                    isSubmitting.value = false;
                }
            }
        };

        return {
            authStore, registrationForm, errors,
            currentStep, isSubmitting,
            nextStep, prevStep, submitForm
        }
    }
}
</script>

<style scoped>
/* Conteneur principal plein écran */
.split-register-container {
    display: flex;
    width: 100%;
    min-height: 100vh;
    background-color: #050505; /* Noir profond */
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

/* --- PANNEAU GAUCHE (Stepper) --- */
.stepper-sidebar {
    width: 45%;
    background: radial-gradient(circle at top left, #1e4a3b, #050505 70%);
    padding: 4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-right: 1px solid rgba(255,255,255,0.05);
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
}

.hero-subtitle {
    color: #a3a3a3;
    font-size: 1.1rem;
    margin-bottom: 3rem;
    max-width: 80%;
}

.stepper-cards {
    display: flex;
    gap: 1.5rem;
}

.step-card {
    flex: 1;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 1.5rem 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    transition: all 0.3s ease;
}

.step-card.active {
    background: #ffffff;
    color: #000000;
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.5);
}

.step-card.completed {
    opacity: 0.6;
}

.step-icon {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 0.9rem;
}

.active .step-icon {
    background: #000000;
    color: #ffffff;
}

.step-text h4 {
    margin: 0 0 0.3rem 0;
    font-size: 0.95rem;
    font-weight: 600;
}

.step-text p {
    margin: 0;
    font-size: 0.75rem;
    color: #888;
}
.active .step-text p { color: #555; }

/* --- PANNEAU DROIT (Formulaire) --- */
.form-section {
    width: 55%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 2rem;
}

.form-wrapper {
    width: 100%;
    max-width: 480px;
}

.form-header {
    margin-bottom: 2.5rem;
    text-align: center;
}

.form-header h2 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
}

.form-header p {
    color: #a3a3a3;
    font-size: 0.9rem;
}

.step-form {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
}

.form-step {
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
    animation: fadeIn 0.4s ease-in-out;
}

.input-row {
    display: flex;
    gap: 1rem;
}
.input-row > * {
    flex: 1;
}

.form-actions {
    display: flex;
    gap: 1rem;
    margin-top: 1rem;
}

.btn-back {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 0 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.2s;
}

.btn-back:hover:not(:disabled) {
    background: rgba(255, 255, 255, 0.05);
}

.btn-next, .btn-submit {
    flex: 1;
}

.error-message {
    background: rgba(220, 38, 38, 0.1);
    color: #ef4444;
    border: 1px solid rgba(220, 38, 38, 0.3);
    padding: 0.75rem;
    border-radius: 8px;
    text-align: center;
    font-size: 0.85rem;
}

.login-link {
    text-align: center;
    margin-top: 2rem;
    font-size: 0.85rem;
    color: #888;
}

.login-link a {
    color: #ffffff;
    text-decoration: none;
    font-weight: 600;
}
.login-link a:hover { text-decoration: underline; color: var(--secondary-light-color) }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

/* RESPONSIVE DESIGN */
@media (max-width: 1024px) {
    .split-register-container { flex-direction: column; }
    .stepper-sidebar { width: 100%; padding: 2rem; border-right: none; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .hero-title { font-size: 2.5rem; }
    .form-section { width: 100%; padding: 3rem 1.5rem; }
}

@media (max-width: 640px) {
    .stepper-cards { flex-direction: column; }
    .input-row { flex-direction: column; gap: 1.2rem; }
}
</style>