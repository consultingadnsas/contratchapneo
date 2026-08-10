<template>
    <form @submit.prevent="submitForm" class="profile-form">
        
        <h3>Votre profil</h3>

        <!-- ⚡️ BANNIÈRE DE SUCCÈS ANIMÉE -->
        <Transition name="fade-slide">
            <div v-if="showSuccess" class="success-banner">
                <svg xmlns="http://www.w3.org/2000/svg" class="icon-success" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.857-9.809a.75.75 0 00-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 10-1.06 1.061l2.5 2.5a.75.75 0 001.137-.089l4-5.5z" clip-rule="evenodd" />
                </svg>
                <span>Vos informations ont été enregistrées avec succès.</span>
            </div>
        </Transition>

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
            <!-- ⚡️ LABEL ET STYLE DU BOUTON DYNAMIQUES -->
            <mainButton 
                type="submit" 
                :label="showSuccess ? 'Enregistré !' : 'Mettre à jour'"
                :isloading="isSubmitting"
                :class="{ 'btn-success-state': showSuccess }"
            />
            <secondButton 
                type="reset" 
                label="Réinitialiser mon mot de passe"
                :disabled="isSubmitting"
                @click.prevent="router.push('/auth/password-reset')"
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
import secondButton from '../buttons/secondButton.vue'
import { useRouter } from 'vue-router'

import type { User } from '../../stores/authStore'
import { useAuthStore } from '../../stores/authStore'

export default {
    components: {
        BaseInput,
        mainButton,
        secondButton
    },
    emits:['updated'],
    setup(props, { emit }) {
        const authStore = useAuthStore();
        const showSuccess = ref(false);
        const router = useRouter();

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
                    // 2. OPTION A (Moderne et fluide) : On refetch directement le profil pour 
                    // rafraîchir le nom dans le header et dans les champs de formulaire !
                    await authStore.getProfile();
                   
                    console.log("✅ Profil mis à jour et rafraîchi avec succès !");
                    // 3. EMIT : On notifie le parent que la mise à jour a été effectuée
                    emit('updated');
                    // 2. ⚡️ On active l'animation de succès
                    showSuccess.value = true;

                    // 3. On désactive le message après 3.5 secondes pour garder le formulaire propre
                    setTimeout(() => {
                        showSuccess.value = false;
                    }, 3500);
                    
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
            isSubmitting,
            showSuccess,
            router
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
/* ── Bannière de succès ── */
.success-banner {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    background-color: #f0fdf4;
    color: #166534;
    border: 1px solid #bbf7d0;
    padding: 0.85rem 1rem;
    border-radius: 0.75rem;
    font-size: 0.95rem;
    font-weight: 500;
    box-shadow: 0 4px 12px rgba(22, 101, 52, 0.05);
}

.icon-success {
    width: 20px;
    height: 20px;
    flex-shrink: 0;
    color: #22c55e;
}

/* ── Transitions Vue (fade + glissement vers le bas) ── */
.fade-slide-enter-active,
.fade-slide-leave-active {
    transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1);
}

.fade-slide-enter-from,
.fade-slide-leave-to {
    opacity: 0;
    transform: translateY(-10px);
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
    gap: 1.5rem;
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