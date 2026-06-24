<template>
    <div class="main-wrapper">
        <failForm @timeout="handleRedirect" />
        <footerSection/>
    </div>
</template>

<script lang="ts">
import { useRouter } from 'vue-router';
import footerSection from '../../components/sections/footerSection.vue';
import failForm from '../../components/forms/failForm.vue';

export default {
    name: 'FailPage',
    components: {
        footerSection,
        failForm
    },
    setup() {
        const router = useRouter();

        // Fonction appelée quand le compte à rebours de failForm arrive à 0
        const handleRedirect = () => {
            // Par défaut, on renvoie vers la page du panier pour réessayer
            router.push('/'); 
        };

        return {
            handleRedirect
        }
    }
}
</script>

<style scoped>
.main-wrapper {
    width: 100%;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f7fafc; /* Fond très légèrement gris pour contraster avec l'écran blanc */
}
</style>