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
      <!-- Le texte d'action devient cliquable -->
      <a href="#" class="action-link" @click.prevent="handleAction">
        {{ textAction }}
      </a>
    </p>
  </div>
</template>

<script>
import { useRouter } from 'vue-router'

export default {
  name: 'EmptyState',
  props: {
    title: {
      type: String,
      default: 'Aucun résultat'
    },
    description: {
      type: String,
      default: "Nous n'avons trouvé aucun résultat correspondant à votre recherche."
    },
    textAction: {
      type: String,
      default: "Cliquez ici pour une demande spécifique"
    },
    // NOUVEAU : On ajoute un 'type' pour savoir où on se trouve
    type: {
      type: String,
      default: 'contrat', // Peut être 'contrat' ou 'pro'
      validator: (value) => ['contrat', 'pro'].includes(value)
    }
  },
  emits: ['go-to'],
  
  setup(props, { emit }) {
    const router = useRouter()

    const handleAction = () => {
      // Si le parent veut gérer lui-même l'action (optionnel)
      emit('go-to')

      // Routage automatique basé sur le type
      if (props.type === 'contrat') {
        router.push('/contractBank/customContrat')
      } else if (props.type === 'pro') {
        // Redirige vers la page services juridiques avec un petit délai pour permettre au composant de se monter,
        // puis on cible l'ancre #contact-section.
        router.push('/services').then(() => {
          setTimeout(() => {
            const contactSection = document.getElementById('contact-section');
            if (contactSection) {
              contactSection.scrollIntoView({ behavior: 'smooth' });
            }
          }, 300); // 300ms laisse le temps à la page de se charger avant de scroller
        });
      }
    }

    return {
      handleAction
    }
  }
}
</script>

<style scoped>
.empty-state-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 3rem 1rem; /* Un peu plus de padding vertical pour respirer */
  text-align: center;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: #fff;
  width: 100%;
  box-sizing: border-box;
  border-radius: 16px; /* Optionnel : léger arrondi */
}

.illustration {
  margin-bottom: 12px;
  animation: float 3s ease-in-out infinite;
}

.title {
  font-size: 26px;
  font-weight: 700;
  color: #1a1a1a; 
  margin: 0 0 8px 0;
}

.description {
  font-size: 15px;
  line-height: 1.6;
  color: #6b7280; 
  max-width: 650px;
  margin: 0;
}

/* Le texte cliquable repensé */
.action-link {
  font-weight: 600;
  color: #10507e; /* Utilisation de ton bleu ou primary-color */
  text-decoration: none;
  margin-left: 4px;
  border-bottom: 1px dashed transparent;
  transition: all 0.3s ease;
  cursor: pointer;
}

.action-link:hover {
  color: #32f459; /* Ton vert d'accentuation */
  border-bottom-color: #32f459;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-5px); }
  100% { transform: translateY(0px); }
}
</style>