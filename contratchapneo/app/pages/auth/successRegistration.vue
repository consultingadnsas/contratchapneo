<template>
    <div class="success-page">
        <div class="success-card">
            <div class="success-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
            </div>
            <h1>Inscription réussie !</h1>
            <p>Votre compte a été créé avec succès. Vous pouvez maintenant vous connecter pour profiter de nos services.</p>
            <button class="btn-login" @click="router.push('/auth/login')">Se connecter</button>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()
</script>

<style scoped>
.success-page {
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: radial-gradient(circle at top right, #111827, #000000);
    padding: 1rem;
}

.success-card {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 24px;
    padding: 3rem 2rem;
    max-width: 500px;
    width: 100%;
    text-align: center;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
    animation: fadeInUp 0.6s ease-out;
}

.success-icon {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: rgba(34, 197, 94, 0.1);
    color: #22c55e;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 2rem auto;
}

.success-icon svg {
    width: 40px;
    height: 40px;
}

h1 {
    font-size: 2rem;
    color: #ffffff;
    margin-bottom: 1rem;
    font-weight: 700;
}

p {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-bottom: 2.5rem;
}

.btn-login {
    display:flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto;
    background: #39acff;
    color: #ffffff;
    border: none;
    padding: 1rem 2.5rem;
    border-radius: 50px;
    font-size: 1.05rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    width: 100%;
    max-width: 300px;
}

.btn-login:hover {
    background: #2563eb;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(37, 99, 235, 0.3);
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}
</style>
