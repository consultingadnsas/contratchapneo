<template>
    <form @submit.prevent="submitForm" class="profile-form">
        
        <h3>Votre profil</h3>

        <div class="form-grid">

            <BaseInput
                label="Nom de famille"
                v-model="registrationForm.last_name"
                placeholder="Ex: Doe"
                :disabled="isSubmitting"
            />

            <BaseInput
                label="Prénoms"
                v-model="registrationForm.first_name"
                placeholder="Ex: John"
                :disabled="isSubmitting"
            />

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

        </div>

        <div class="form-actions">
            <mainButton 
                type="submit" 
                label="Mettre à jour"
                :isloading="isSubmitting"
            />
        </div>

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

        const isSubmitting = ref(false);

        // ⚡️ AJOUT : first_name et last_name dans le formulaire initial
        const registrationForm = ref<User>({
            username: "",
            first_name: "",
            last_name: "",
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
            if (!registrationForm.value.username?.trim()) {
                errors.value.username = "Le nom d'utilisateur est requis.";
                isValid = false;
            } else if (!usernameRegex.test(registrationForm.value.username)) {
                errors.value.username = "Pas d'espaces autorisés (utilisez _ ou -).";
                isValid = false;
            }

            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!registrationForm.value.email?.trim()) {
                errors.value.email = "L'email est requis.";
                isValid = false;
            } else if (!emailRegex.test(registrationForm.value.email)) {
                errors.value.email = "Veuillez entrer une adresse email valide.";
                isValid = false;
            }

            if (!registrationForm.value.phone_number?.trim()) {
                errors.value.phone_number = "Le numéro de téléphone est requis.";
                isValid = false;
            }

            // ⚡️ CORRECTION LOGIQUE : Pour une mise à jour de profil, le mot de passe est souvent optionnel !
            if (registrationForm.value.password && registrationForm.value.password.length < 8) {
                errors.value.password = "Le mot de passe doit contenir au moins 8 caractères.";
                isValid = false;
            }

            return isValid;
        }

        const submitForm = async () => {
            if (validate()) {
                
                isSubmitting.value = true; 
                
                try {
                    // Si le mot de passe est vide, on l'enlève de l'objet pour ne pas l'écraser côté serveur
                    const payload = { ...registrationForm.value };
                    if (!payload.password) {
                        delete payload.password;
                    }

                    // ⚠️ Ici, tu appelles register(), 
                    // mais tu devras créer une fonction updateProfile() dans ton store pour gérer l'API PUT/PATCH !
                    await authStore.updateProfile(payload); // <--- À adapter selon ton store
                    
                } catch (error) {
                    console.error("La mise à jour a échoué.");
                } finally {
                    isSubmitting.value = false;
                }
            }
        }

        // ⚡️ CORRECTION CRUCIALE ICI : L'utilisation de `async/await`
        onMounted(async () => {
            try {
                // On attend que les données du profil soient récupérées
                await authStore.getProfile();
                
                // ⚡️ CORRECTION : On vérifie une donnée qu'on est SÛR de recevoir (ex: email ou username)
                if (authStore.user && (authStore.user.email || authStore.user.username)) {
                    
                    // On mappe explicitement chaque champ pour forcer la réactivité Vue.js
                    registrationForm.value = {
                        username: authStore.user.username || "",
                        first_name: authStore.user.first_name || "", // ⚠️ Vérifie que ton backend n'envoie pas 'firstName'
                        last_name: authStore.user.last_name || "",   // ⚠️ Idem pour 'lastName'
                        email: authStore.user.email || "",
                        phone_number: authStore.user.phone_number || "",
                        password: "" // Toujours vide par sécurité
                    };
                    
                    console.log("Formulaire rempli avec :", registrationForm.value);
                }
            } catch(e) {
                console.error("Impossible de charger les infos utilisateur :", e);
            }
        })

        return {
            authStore,
            registrationForm,
            errors,
            submitForm,
            isSubmitting 
        }
    }
}
</script>

<style scoped>
/* Le formulaire prend toute la place disponible */
.profile-form {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 1.5rem; /* Espace global entre le titre, la grille et le bouton */
}

/* 📱 Mobile-first : 1 seule colonne */
.form-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 1rem;
    width: 100%;
}

/* 💻 Écrans larges (Laptop / Tablette) : on passe à 2 colonnes */
@media (min-width: 768px) {
    .form-grid {
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem; /* On aère un peu plus sur grand écran */
    }
}

.form-actions {
    width: 100%;
    display: flex;
    justify-content: flex-start; /* ou 'center' / 'flex-end' selon tes goûts */
    margin-top: 0.5rem;
}

.error-message {
    background: #fef2f2;
    color: #dc2626;
    border: 1px solid #f87171;
    padding: 0.75rem;
    border-radius: 0.5rem;
    margin-top: 1rem;
    text-align: center;
    font-size: 0.9rem;
    width: 100%;
}
</style>