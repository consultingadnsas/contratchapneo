<template>
    <form @submit.prevent="handleLogin">
        <h3>Connexion</h3>
        
        <BaseInputVue 
            v-model="credentials.email" 
            label="Email" 
            name="email" 
            type="email" 
            placeholder="Entrez votre email" 
            required
        />
        
        <BaseInputVue 
            v-model="credentials.password" 
            label="Mot de passe" 
            name="password" 
            type="password" 
            placeholder="Entrez votre mot de passe" 
            required
        />
        
        <formButtonVue 
            label="Connexion" 
            type="submit" 
            :disabled="authStore.isLoading"
        />

        <p v-if="authStore.error" class="error-message">
            {{ authStore.error }}
        </p>
    </form>
</template>

<script lang="ts">
import { ref } from 'vue'
import formButtonVue from '../buttons/formButton.vue'
import BaseInputVue from '../input/BaseInput.vue'
import { useAuthStore } from '../../stores/authStore'
import { useRouter } from 'vue-router'

export default {
    components: {
        BaseInputVue,
        formButtonVue
    },
    setup() {
        const authStore = useAuthStore()
        const router = useRouter() // Utile pour rediriger après connexion

        // État réactif local pour le formulaire
        const credentials = ref({
            email: '',
            password: ''
        })

        // Méthode de soumission
        const handleLogin = async () => {
            try {
                await authStore.login({
                    email: credentials.value.email,
                    password: credentials.value.password
                })
                
                // Redirection après succès (ajuste la route selon tes besoins)
                router.push('/dashboard') 
            } catch (error) {
                // L'erreur est déjà gérée dans le store et affichée via authStore.error
                console.error("Échec de la connexion", error)
            }
        }

        return {
            authStore,
            credentials,
            handleLogin
        }
    }
}
</script>

<style scoped>
.error-message {
    color: red;
    margin-top: 10px;
    font-size: 0.9em;
}
</style>