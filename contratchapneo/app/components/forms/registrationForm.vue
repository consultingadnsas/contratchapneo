<template>
    <form @submit.prevent="submitForm">
        
        <h3>Ouvrir un compte</h3>

        <BaseInput
            label="Nom d'utilisateur"
            v-model="registrationForm.username"
            placeholder="Ex: mon_entreprise"
            :errorMessage="errors.username"
            :disabled="isSubmitting"
        />

        <BaseInput
            label="Votre email"
            v-model="registrationForm.email"
            placeholder="Entrer votre email"
            :errorMessage="errors.email"
            :disabled="isSubmitting"
        />

        <BaseInput
            label="N° de téléphone"
            v-model="registrationForm.phone_number"
            placeholder="Ex: +225 0102030405"
            :errorMessage="errors.phone_number"
            :disabled="isSubmitting"
        />

        <BaseInput
            label="Mot de passe"
            v-model="registrationForm.password"
            placeholder="Entrer un mot de passe"
            :errorMessage="errors.password"
            type="password"
            :disabled="isSubmitting"
        />

        <!-- ⚡️ CORRECTION : btn_label et isloading en minuscules, branchés sur la variable locale -->
        <mainButton 
            type="submit" 
            label="S'inscrire"
            :isloading="isSubmitting"
        />

        <!-- Affichage de l'erreur renvoyée par le backend -->
        <div class="error-message" v-if="authStore.error">
            <p>{{ authStore.error }}</p>
        </div>

    </form>
</template>

<script lang="ts">
import { ref, onMounted } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import mainButton from '../buttons/mainButton.vue'

import type { User } from '../../stores/authStore'
import { useAuthStore } from '../../stores/authStore'

export default {
    components: {
        BaseInput,
        mainButton
    },
    setup() {
        const authStore = useAuthStore();

        // ⚡️ État de chargement 100% local, initialisé à false
        const isSubmitting = ref(false);

        const registrationForm = ref<User>({
            username: "",
            password: "",
            email: "",
            phone_number: ""
        });

        const errors = ref({
            username: "",
            email: "",
            phone_number: "",
            password: "",
        });

        function validate(): boolean {
            let isValid = true;
            
            errors.value = {
                username: "",
                email: "",
                password: "",
                phone_number: ""
            };

            const usernameRegex = /^[\w.@+-]+$/; 
            if (!registrationForm.value.username.trim()) {
                errors.value.username = "Le nom d'utilisateur est requis.";
                isValid = false;
            } else if (!usernameRegex.test(registrationForm.value.username)) {
                errors.value.username = "Pas d'espaces autorisés (utilisez _ ou -).";
                isValid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!registrationForm.value.email.trim()) {
                errors.value.email = "L'email est requis.";
                isValid = false;
            } else if (!emailRegex.test(registrationForm.value.email)) {
                errors.value.email = "Veuillez entrer une adresse email valide.";
                isValid = false;
            }

            if (!registrationForm.value.phone_number.trim()) {
                errors.value.phone_number = "Le numéro de téléphone est requis.";
                isValid = false;
            }

            if (!registrationForm.value.password) {
                errors.value.password = "Le mot de passe est requis.";
                isValid = false;
            } else if (registrationForm.value.password.length < 8) {
                errors.value.password = "Le mot de passe doit contenir au moins 8 caractères.";
                isValid = false;
            }

            return isValid;
        }

        const submitForm = async () => {
            if (validate()) {
                
                isSubmitting.value = true; // Allume le bouton
                
                try {
                    await authStore.register(registrationForm.value);
                } catch (error) {
                    console.error("L'inscription a échoué.");
                } finally {
                    isSubmitting.value = false; // Éteint le bouton
                }
            }
        }

        onMounted(() => {
            console.log("Formulaire monté, prêt à l'emploi.");
        })

        return {
            authStore,
            registrationForm,
            errors,
            submitForm,
            isSubmitting // ⚡️ Très important : on l'exporte pour le template
        }
    }
}
</script>

<style scoped>
.error-message {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #f87171;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
    text-align: center;
    font-size: 0.9rem;
}
</style>