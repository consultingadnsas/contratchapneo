<template>
    
    <form @submit.prevent="submitForm">
        
        <h3>Ouvrir un compte</h3>

        <BaseInput
            label="Nom d'utilisateur/nom entreprise"
            v-model="registrationForm.username"
            placeholder="Entrer votre nom d'utilisateur"
            :errorMessage="errors.username"
        />

        <BaseInput
            label="Votre email"
            v-model="registrationForm.email"
            placeholder="Entrer votre email"
            :errorMessage="errors.email"
        />

        <BaseInput
            label="N° de téléphone"
            v-model="registrationForm.phone_number"
            placeholder="Entrer un mot de passe"
            :errorMessage="errors.password"
        />

        <BaseInput
            label="Mot de passe"
            v-model="registrationForm.password"
            placeholder="Entrer un mot de passe"
            :errorMessage="errors.password"
            type="password"
        />

        <mainButton 
            type="submit" 
            label="S'inscrire"
            :isLoading="useAuthStore.isLoading"
        />

        <div class="error-message" v-if="useAuthStore.error">
            <p>{{ useAuthStore.error }}</p>
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

        const registrationForm = ref<User>({
            username: "",
            password: "",
            email: "",
            phone_number: ""
        });

        // 1. On crée un objet réactif pour stocker nos erreurs
        const errors = ref({
            username: "",
            email: "",
            phone_number:"",
            password: "",
        });

        // 2. La fonction de validation
        function validate(): boolean {
            
            let isValid = true;
            
            // On réinitialise les erreurs à chaque validation
            errors.value = {
                username: "",
                email: "",
                password: "",
                phone_number:"  "
            };

            // Validation du Nom d'utilisateur
            if (!registrationForm.value.username.trim()) {
                errors.value.username = "Le nom d'utilisateur est requis.";
                isValid = false;
            }

            // Validation de l'Email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!registrationForm.value.email.trim()) {
                errors.value.email = "L'email est requis.";
                isValid = false;
            } else if (!emailRegex.test(registrationForm.value.email)) {
                errors.value.email = "Veuillez entrer une adresse email valide.";
                isValid = false;
            }

            // Validation du Mot de passe
            if (!registrationForm.value.password) {
                errors.value.password = "Le mot de passe est requis.";
                isValid = false;
            } else if (registrationForm.value.password.length < 8) {
                errors.value.password = "Le mot de passe doit contenir au moins 8 caractères.";
                isValid = false;
            }

            return isValid;
        }

        // 3. Soumission du formulaire
        const submitForm = async () => {
            // On appelle validate() en premier
            if (validate()) {
                console.log("Les données sont valides, on envoie au backend :", registrationForm.value);
                
                try {
                    // Exemple d'appel à ton store
                    await authStore.register(registrationForm.value);
                    
                } catch (error) {
                    console.error("Erreur lors de l'inscription", error);
                }
            } else {
                console.log("Le formulaire contient des erreurs.");
            }
        }

        onMounted(() => {
            console.log("Registration form monté", registrationForm.value)
        })

        return {
            authStore,
            registrationForm,
            errors,
            submitForm
        }
    }
}
</script>

<style scoped>
.error-message{
    background: #ef4c4c;
    color: red;
    padding: 0.5rem;
    border-radius: 0.5rem;
}
</style>