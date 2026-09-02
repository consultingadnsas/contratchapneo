<template>
    <aside class="stepper-sidebar">
        <div class="sidebar-content">
            <h1 class="hero-title">Rejoignez<br>nous</h1>
            <p class="hero-subtitle">Complétez ces étapes simples pour créer votre compte.</p>

            <div class="stepper-cards">
                <div class="step-card" :class="{ 'active': currentStep === 1, 'completed': currentStep > 1 }">
                    <div class="step-icon">1</div>
                    <div class="step-text">
                        <h4>Informations de base</h4>
                        <p>Identité et contact</p>
                    </div>
                </div>
                <div class="step-card" :class="{ 'active': currentStep === 2, 'completed': currentStep > 2 }">
                    <div class="step-icon">2</div>
                    <div class="step-text">
                        <h4>Détails du compte</h4>
                        <p>Profil utilisateur</p>
                    </div>
                </div>
                <div class="step-card" :class="{ 'active': currentStep === 3 }">
                    <div class="step-icon">3</div>
                    <div class="step-text">
                        <h4>Sécurité</h4>
                        <p>Mot de passe</p>
                    </div>
                </div>
            </div>
        </div>
    </aside>
</template>

<script lang="ts">
export default {
    props: {
        currentStep: { type: Number, required: true }
    }
}
</script>

<style scoped>
.stepper-sidebar {
    width: 45%;
    background: transparent;
    padding: 4rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    border-right: 1px solid rgba(255,255,255,0.05);
}
.hero-title { font-size: 3.5rem; font-weight: 700; line-height: 1.1; margin-bottom: 1rem; }
.hero-subtitle { color: #a3a3a3; font-size: 1.1rem; margin-bottom: 3rem; max-width: 80%; }
.stepper-cards { display: flex; gap: 1.5rem; }
.step-card {
    flex: 1; background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px; padding: 1.5rem 1rem; display: flex; flex-direction: column; gap: 1rem; transition: all 0.3s ease;
}
.step-card.active { background: #ffffff; color: #000000; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
.step-card.completed { opacity: 0.6; }
.step-icon { width: 32px; height: 32px; border-radius: 50%; background: rgba(255, 255, 255, 0.1); display: flex; align-items: center; justify-content: center; font-weight: 600; font-size: 0.9rem; }
.active .step-icon { background: #000000; color: #ffffff; }
.step-text h4 { margin: 0 0 0.3rem 0; font-size: 0.95rem; font-weight: 600; }
.step-text p { margin: 0; font-size: 0.75rem; color: #888; }
.active .step-text p { color: #555; }

@media (max-width: 1024px) {
    .stepper-sidebar { width: 100%; padding: 2rem; border-right: none; border-bottom: 1px solid rgba(255,255,255,0.05); }
    .hero-title { font-size: 2.5rem; }
}
@media (max-width: 640px) {
    .stepper-cards { flex-direction: column; }
}
</style>