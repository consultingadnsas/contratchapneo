<template>
    <main class="form-section">
        <div class="form-wrapper">
            <div class="form-header">
                <h2>Créer un compte</h2>
                <p></p>
            </div>

            <form @submit.prevent="submitForm" class="step-form">
                
                <!-- 📦 ÉTAPE 1 : Identité -->
                <div v-show="currentStep === 1" class="form-step">
                    <div class="input-row">
                        <BaseInput label="Prénom" v-model="registrationForm.first_name" placeholder="Ex: John" :errorMessage="errors.first_name" />
                        <BaseInput label="Nom" v-model="registrationForm.last_name" placeholder="Ex: Doe" :errorMessage="errors.last_name" />
                    </div>
                    <BaseInput label="Email" v-model="registrationForm.email" placeholder="Ex: john.doe@gmail.com" :errorMessage="errors.email" />
                </div>

                <!-- 📦 ÉTAPE 2 : Compte -->
                <div v-show="currentStep === 2" class="form-step">
                    <BaseInput label="Nom d'utilisateur" v-model="registrationForm.username" placeholder="Ex: john_doe99" :errorMessage="errors.username" />
                    
                    <div class="input-wrapper custom-phone-group">
                        <label class="input-label">N° de téléphone</label>
                        <div class="phone-flex-container">
                            <select v-model="registrationForm.countryCode" class="country-select">
                                <option value="+229">🇧🇯 +229</option>
                                <option value="+226">🇧🇫 +226</option>
                                <option value="+237">🇨🇲 +237</option>
                                <option value="+236">🇨🇫 +236</option>
                                <option value="+269">🇰🇲 +269</option>
                                <option value="+242">🇨🇬 +242</option>
                                <option value="+225">🇨🇮 +225</option>
                                <option value="+241">🇬🇦 +241</option>
                                <option value="+224">🇬🇳 +224</option>
                                <option value="+245">🇬🇼 +245</option>
                                <option value="+240">🇬🇶 +240</option>
                                <option value="+223">🇲🇱 +223</option>
                                <option value="+227">🇳🇪 +227</option>
                                <option value="+243">🇨🇩 +243</option>
                                <option value="+221">🇸🇳 +221</option>
                                <option value="+235">🇹🇩 +235</option>
                                <option value="+228">🇹🇬 +228</option>
                            </select>
                            
                            <input type="tel" v-model="registrationForm.phone_number" class="form-input phone-input" placeholder="Ex: 0102030405" />
                        </div>
                        <span v-if="errors.phone_number" class="error-message">{{ errors.phone_number }}</span>
                    </div>
                </div>

                <!-- 📦 ÉTAPE 3 : Sécurité -->
                <div v-show="currentStep === 3 && !isSuccess" class="form-step">
                    <BaseInput label="Mot de passe" v-model="registrationForm.password" placeholder="Entrez un mot de passe" :errorMessage="errors.password" type="password" showPasswordToggle />
                    <BaseInput label="Confirmer le mot de passe" v-model="registrationForm.confirm_password" placeholder="Répétez le mot de passe" :errorMessage="errors.confirm_password" type="password" showPasswordToggle />
                </div>

                <!-- 📦 ÉTAPE 4 : Succès -->
                <div v-if="isSuccess" class="form-step success-step">
                    <div class="success-icon">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                            <polyline points="22 4 12 14.01 9 11.01"></polyline>
                        </svg>
                    </div>
                    <h3>Inscription réussie !</h3>
                    <p>Votre compte a été créé avec succès. Vous allez être redirigé vers la page de connexion dans quelques instants...</p>
                </div>

                <div class="error-message-block" v-if="authStore.error && !isSuccess">
                    <p>{{ authStore.error }}</p>
                </div>

                <div class="form-actions" v-if="!isSuccess">
                    <button type="button" class="btn-back" v-if="currentStep > 1" @click="prevStep" :disabled="isSubmitting">Précédent</button>
                    <mainButton v-if="currentStep < 3" type="button" label="Suivant" @click="nextStep" class="btn-next" />
                    <mainButton v-if="currentStep === 3" type="submit" label="S'inscrire" :isloading="isSubmitting" class="btn-submit" />
                </div>

                <div class="login-link" v-if="!isSuccess">
                    <p>Vous avez déjà un compte ? <router-link to="/auth/login">Connectez-vous</router-link></p>
                </div>
            </form>
        </div>
    </main>
</template>

<script lang="ts">
import { ref } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'
import { useAuthStore } from '../../stores/authStore'

export default {
    components: { BaseInput, mainButton },
    props: {
        currentStep: { type: Number, required: true }
    },
    emits: ['update:currentStep'], // Permet de modifier la prop via le v-model du parent
    setup(props, { emit }) {
        const authStore = useAuthStore();
        const isSubmitting = ref(false);
        const isSuccess = ref(false);

        const registrationForm = ref({
            first_name: "", last_name: "", email: "", username: "",
            countryCode: "+225", phone_number: "", password: "", confirm_password: ""
        });

        const errors = ref({
            first_name: "", last_name: "", email: "", username: "",
            countryCode: "", phone_number: "", password: "", confirm_password: ""
        });

        const clearErrors = () => {
            Object.keys(errors.value).forEach(key => {
                errors.value[key as keyof typeof errors.value] = "";
            });
        };

        const validateStep = (step: number): boolean => {
            clearErrors();
            let isValid = true;
            if (step === 1) {
                if (!registrationForm.value.first_name.trim()) { errors.value.first_name = "Requis"; isValid = false; }
                if (!registrationForm.value.last_name.trim()) { errors.value.last_name = "Requis"; isValid = false; }
                const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!registrationForm.value.email.trim()) { errors.value.email = "Requis"; isValid = false; }
                else if (!emailRegex.test(registrationForm.value.email)) { errors.value.email = "Email invalide"; isValid = false; }
            } else if (step === 2) {
                const usernameRegex = /^[\w.@+-]+$/;
                if (!registrationForm.value.username.trim()) { errors.value.username = "Requis"; isValid = false; }
                else if (!usernameRegex.test(registrationForm.value.username)) { errors.value.username = "Pas d'espaces autorisés"; isValid = false; }
                if (!registrationForm.value.phone_number.trim()) { errors.value.phone_number = "Requis"; isValid = false; }
            } else if (step === 3) {
                const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$/;
                if (!registrationForm.value.password) { errors.value.password = "Requis"; isValid = false; }
                else if (!passwordRegex.test(registrationForm.value.password)) { errors.value.password = "Min. 8 caractères, 1 maj, 1 min, 1 chiffre, 1 car. spécial"; isValid = false; }
                if (registrationForm.value.password !== registrationForm.value.confirm_password) {
                    errors.value.confirm_password = "Les mots de passe ne correspondent pas"; isValid = false;
                }
            }
            return isValid;
        };

        const nextStep = () => {
            if (validateStep(props.currentStep)) {
                emit('update:currentStep', props.currentStep + 1); // Indique au parent d'avancer
            }
        };

        const prevStep = () => {
            if (props.currentStep > 1) {
                emit('update:currentStep', props.currentStep - 1); // Indique au parent de reculer
            }
        };

        const submitForm = async () => {
            const cleanNumber = registrationForm.value.phone_number.replace(/\s+/g, '');
            const fullPhoneNumber = `${registrationForm.value.countryCode}${cleanNumber}`;
            if (validateStep(3)) {
                isSubmitting.value = true;
                try {
                    const success = await authStore.register({
                        username: registrationForm.value.username,
                        email: registrationForm.value.email,
                        phone_number: fullPhoneNumber,
                        password: registrationForm.value.password,
                        first_name: registrationForm.value.first_name,
                        last_name: registrationForm.value.last_name
                    });
                    
                    if (success) {
                        isSuccess.value = true;
                        setTimeout(() => {
                            navigateTo('/auth/login');
                        }, 3000);
                    }
                } catch (error) {
                    console.error("L'inscription a échoué.", error);
                } finally {
                    isSubmitting.value = false;
                }
            }
        };

        return {
            authStore, registrationForm, errors, isSubmitting, isSuccess,
            nextStep, prevStep, submitForm
        }
    }
}
</script>

<style scoped>
.form-section { width: 55%; display: flex; align-items: center; justify-content: center; padding: 2rem; }
.form-wrapper { width: 100%; max-width: 480px; }
.form-header { margin-bottom: 2.5rem; text-align: center; }
.form-header h2 { font-size: 1.8rem; margin-bottom: 0.5rem; }
.form-header p { color: #a3a3a3; font-size: 0.9rem; }
.step-form { display: flex; flex-direction: column; gap: 1.5rem; }
.form-step { display: flex; width: 100%; flex-direction: column; gap: 1.2rem; animation: fadeIn 0.4s ease-in-out; }
.input-row { display: flex; gap: 1rem; }
.input-row > * { flex: 1; }
.form-actions { display: flex; align-items: center; justify-content: center; width: 100%; gap: 1rem; margin-top: 1rem; }
.btn-back { background: transparent; width: 50%; height: 8vh; border: 1px solid rgba(255, 255, 255, 0.2); color: white; padding: 0 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 500; transition: all 0.2s; }
.btn-back:hover:not(:disabled) { background: rgba(255, 255, 255, 0.05); }
.btn-next, .btn-submit { width: 50%; flex: 1; }

/* Téléphone personnalisé */
.phone-flex-container { display: flex; align-items: center; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; background: #ffffff; }
.phone-flex-container:focus-within { border-color: var(--accent-blue, #2563eb); box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1); }
.country-select { background-color: #f8fafc; border: none; border-right: 1px solid #e2e8f0; padding: 0.75rem; font-size: 0.95rem; color: #475569; cursor: pointer; outline: none; }
.phone-input { border: none !important; box-shadow: none !important; width: 100%; padding: 0.75rem 1rem; outline: none; color: #475569 }
.error-message { color: #ef4444; font-size: 0.85rem; margin-top: 0.25rem; display: block; }
.error-message-block { background: rgba(220, 38, 38, 0.1); color: #ef4444; border: 1px solid rgba(220, 38, 38, 0.3); padding: 0.75rem; border-radius: 8px; text-align: center; font-size: 0.85rem; }

.login-link { text-align: center; margin-top: 2rem; font-size: 0.85rem; color: #888; }
.login-link a { color: #ffffff; text-decoration: none; font-weight: 600; }
.login-link a:hover { text-decoration: underline; color: var(--secondary-light-color); }

/* Success Step */
.success-step { text-align: center; align-items: center; padding: 2rem 0; }
.success-icon { width: 64px; height: 64px; border-radius: 50%; background: rgba(34, 197, 94, 0.1); color: #22c55e; display: flex; align-items: center; justify-content: center; margin: 0 auto 1.5rem auto; }
.success-icon svg { width: 32px; height: 32px; }
.success-step h3 { font-size: 1.5rem; margin-bottom: 0.5rem; color: #f8fafc; }
.success-step p { color: #94a3b8; line-height: 1.5; font-size: 0.95rem; }

@keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

@media (max-width: 1024px) {
    .form-section { width: 100%; padding: 3rem 1.5rem; }
}
@media (max-width: 640px) {
    .input-row { flex-direction: column; gap: 1.2rem; }
}
</style>