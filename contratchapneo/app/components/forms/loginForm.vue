<template>
    <form @submit.prevent="handleLogin">
        <h3>Connexion</h3>
        
        <BaseInputVue 
            v-model="credentials.username" 
            label="Email ou Nom d'utilisateur" 
            name="username" 
            type="text" 
            placeholder="Entrez votre email ou pseudo" 
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
        const router = useRouter()

        // Utilisation d'une clé générique 'username' pour stocker l'identifiant saisi
        const credentials = ref({
            username: '',
            password: ''
        })

        const handleLogin = async () => {
            try {
                await authStore.login({
                    username: credentials.value.username,
                    password: credentials.value.password,
                    email: credentials.value.password
                })
                router.push('/profile/profile') 
            } catch (error) {
                print('[Login] Erreur capturée', error)
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