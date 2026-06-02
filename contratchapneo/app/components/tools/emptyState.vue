<template>
    <div class="empty-state-container">
        <div class="illustration">
            <slot name="image">
                <svg width="140" height="140" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <ellipse cx="60" cy="105" rx="45" ry="5" fill="#f0f2f5"/>
                    <path d="M40 35 h35 a4 4 0 0 1 4 4 v20 h-43 z" fill="#e2e6eb"/>
                    <path d="M50 30 h30 a4 4 0 0 1 4 4 v20 h-38 z" fill="#f8f9fa"/>
                    <path d="M15 45 h40 l8 10 h42 v40 h-90 z" fill="#e8eaed"/>
                    <path d="M10 55 h100 v35 a5 5 0 0 1 -5 5 h-90 a5 5 0 0 1 -5 -5 z" fill="#f4f6f8"/>
                    
                    <path d="M45 70 l5 4 l-5 4" stroke="#8a92a6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M75 70 l-5 4 l5 4" stroke="#8a92a6" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M53 85 q 7 -7 14 0" stroke="#8a92a6" stroke-width="2.5" stroke-linecap="round"/>
                    
                    <path d="M85 45 q 5 -5 10 0 q -5 5 -10 0" fill="#e2e6eb"/>
                    <path d="M95 40 q 5 10 -10 10" stroke="#e2e6eb" stroke-width="1" fill="none" stroke-dasharray="2 2"/>
                </svg>
            </slot>
        </div>

        <h2 class="title">{{ title }}</h2>

        <p class="description">
            <slot name="description">{{ description }}</slot>
        </p>
    </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    default: 'Error'
  },
  description: {
    type: String,
    default: "According to local regulations, you are temporarily unable to register through a third-party account. Please return and click 'Register Now' to create account."
  }
})
</script>

<style scoped>
.empty-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 64px 24px;
  text-align: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #ffffff;
  width: 100%;
  box-sizing: border-box;
}

.illustration {
  margin-bottom: 24px;
  animation: float 3s ease-in-out infinite;
}

.title {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a; /* Gris très foncé / noir */
  margin: 0 0 16px 0;
}

.description {
  font-size: 15px;
  line-height: 1.6;
  color: #6b7280; /* Gris moyen */
  max-width: 650px;
  margin: 0;
}

/* Petite animation subtile pour rendre le SVG moins statique (optionnel) */
@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0px); }
}
</style>