<template>
    <div class="split-register-container">
        <!-- Panneau Gauche -->
        <RegistrationStepper :currentStep="currentStep" />

        <!-- Panneau Droit -->
        <RegisterForm v-model:currentStep="currentStep" />
    </div>
</template>

<script lang="ts">
import { ref } from 'vue';
import RegistrationStepper from '../../components/tools/registrationStepper.vue'
import RegisterForm from '../../components/forms/registrationForm.vue';

export default {
    components: { RegistrationStepper, RegisterForm },
    setup() {
        const currentStep = ref(1);
        return { currentStep };
    }
}
</script>

<style scoped>
.split-register-container {
    display: flex;
    width: 100%;
    min-height: 100vh;
    background: radial-gradient(circle at 50% 15%, #18223c 0%, #0a0e1a 100%);
    color: #ffffff;
    font-family: 'Inter', sans-serif;
}

@media (max-width: 1024px) {
    .split-register-container { flex-direction: column; }
}
</style>