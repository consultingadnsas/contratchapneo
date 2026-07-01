<template>
  <div class="testimonials-wrapper">
    
    <!-- EN-TÊTE -->
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Témoignages Clients</h3>
        <button class="btn-primary" @click="openModal()">
          <component :is="PlusIcon" class="icon-sm" /> Ajouter un témoignage
        </button>
      </div>
      <p class="gray-text text-sm">Gérez les avis affichés sur votre page d'accueil pour renforcer la confiance de vos visiteurs.</p>
    </div>

    <!-- GRILLE DES TÉMOIGNAGES -->
    <div class="reviews-grid">
      <div class="review-card" v-for="testimonial in testimonials" :key="testimonial.id">
        
        <!-- Corps : Le message -->
        <div class="card-body">
          <div class="quote-icon">"</div>
          <p class="review-text">{{ testimonial.message }}</p>
        </div>

        <!-- Auteur & Actions (Modifié pour inclure Photo et Poste) -->
        <div class="card-footer">
          <div class="author-info">
            <!-- Affichage Photo ou Initiale -->
            <img v-if="testimonial.avatarUrl" :src="testimonial.avatarUrl" class="avatar-image" alt="Photo" />
            <div v-else class="avatar-circle">{{ testimonial.author.charAt(0) }}</div>
            
            <div class="author-details">
              <div class="dark-text font-bold text-sm">{{ testimonial.author }}</div>
              <!-- Affichage conditionnel Poste + Entreprise -->
              <div class="gray-text text-xs">
                <span v-if="testimonial.role">{{ testimonial.role }}</span>
                <span v-if="testimonial.role && testimonial.company"> • </span>
                <span v-if="testimonial.company">{{ testimonial.company }}</span>
              </div>
            </div>
          </div>
          
          <div class="actions-group">
            <button class="action-icon-btn edit-btn" title="Modifier" @click="openModal(testimonial)">
              <component :is="PencilSquareIcon" class="icon-sm" />
            </button>
            <button class="action-icon-btn delete-btn" title="Supprimer" @click="deleteTestimonial(testimonial.id)">
              <component :is="TrashIcon" class="icon-sm" />
            </button>
          </div>
        </div>

      </div>
      
      <!-- Carte "Ajouter" (Raccourci visuel) -->
      <div class="review-card add-card" @click="openModal()">
        <div class="add-circle">
          <component :is="PlusIcon" class="icon-lg" />
        </div>
        <h4 class="dark-text mt-3">Nouveau témoignage</h4>
        <span class="gray-text text-sm">Saisir manuellement</span>
      </div>
    </div>

    <!-- MODALE -->
    <TestimonialModal 
      v-if="isModalOpen" 
      :testimonial="selectedTestimonial" 
      @close="closeModal" 
      @save="saveTestimonial" 
    />

  </div>
</template>

<script lang="ts">
import { ref, markRaw } from 'vue';
import { PlusIcon, TrashIcon, PencilSquareIcon } from '@heroicons/vue/24/outline';
import TestimonialModal from '../../modale/testimonialModal.vue'; // Assure-toi du chemin

export default {
  name: 'AdminTestimonials',
  components: { TestimonialModal },
  setup() {
    const testimonials = ref([
      { 
        id: 1, 
        author: 'Sylla Awa', 
        role: 'Fondatrice',
        company: 'Startup Tech Abidjan', 
        message: 'Modèles très complets et parfaitement conformes à la réglementation OHADA. J\'ai pu immatriculer ma société sans aucun souci en quelques jours.',
        avatarUrl: '' // Laissé vide pour tester l'initiale
      },
      { 
        id: 2, 
        author: 'Kouassi Jean', 
        role: 'Consultant Indépendant',
        company: '', 
        message: 'Un excellent document de base. Il est clair, précis et protège bien les intérêts du prestataire.',
        avatarUrl: '' 
      },
      { 
        id: 3, 
        author: 'Bamba L.', 
        role: 'Gérante',
        company: 'Agence Immobilière', 
        message: 'Le service client a été très réactif pour m\'orienter vers le bon modèle. Le contrat est solide et prêt à l\'emploi.',
        avatarUrl: ''
      }
    ]);

    const isModalOpen = ref(false);
    const selectedTestimonial = ref<any>(null);

    const openModal = (testimonial: any = null) => {
      selectedTestimonial.value = testimonial;
      isModalOpen.value = true;
    };

    const closeModal = () => {
      isModalOpen.value = false;
      selectedTestimonial.value = null;
    };

    const saveTestimonial = (testimonialData: any) => {
      if (testimonialData.id) {
        // Mode édition : on met à jour l'élément existant
        const index = testimonials.value.findIndex(t => t.id === testimonialData.id);
        if (index !== -1) testimonials.value[index] = testimonialData;
      } else {
        // Mode création : on génère un faux ID et on ajoute
        testimonialData.id = Date.now();
        testimonials.value.unshift(testimonialData); // unshift l'ajoute au début de la liste
      }
      closeModal();
    };

    const deleteTestimonial = (id: number) => {
      if (confirm('Êtes-vous sûr de vouloir supprimer ce témoignage ?')) {
        testimonials.value = testimonials.value.filter(t => t.id !== id);
      }
    };

    return {
      testimonials,
      deleteTestimonial,
      isModalOpen,
      selectedTestimonial,
      openModal,
      closeModal,
      saveTestimonial,
      PlusIcon: markRaw(PlusIcon),
      TrashIcon: markRaw(TrashIcon),
      PencilSquareIcon: markRaw(PencilSquareIcon)
    };
  }
}
</script>

<style scoped>
.testimonials-wrapper {
  --bg-panel: #ffffff;
  --text-dark: #1e293b;
  --text-gray: #94a3b8;
  --accent-blue: #2563eb;
  
  display: flex; flex-direction: column; gap: 2rem;
  font-family: 'Inter', sans-serif; padding-bottom: 2rem;
}

/* UTILITAIRES */
.dark-text { color: var(--text-dark); }
.gray-text { color: var(--text-gray); }
.font-bold { font-weight: 700; }
.text-sm { font-size: 0.85rem; }
.text-xs { font-size: 0.75rem; }
.mt-3 { margin-top: 0.8rem; }

.icon-sm { width: 18px; height: 18px; }
.icon-lg { width: 24px; height: 24px; }

/* EN-TÊTE */
.header-section { display: flex; flex-direction: column; gap: 0.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 800; margin: 0; }

.btn-primary { background: var(--text-dark); color: white; border: none; padding: 0.7rem 1.2rem; border-radius: 8px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: 0.2s; }
.btn-primary:hover { background: #000000; transform: translateY(-2px); }

/* GRILLE DES AVIS */
.reviews-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1.5rem; }

.review-card {
  background: var(--bg-panel); border-radius: 20px; padding: 1.8rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.03); border: 1px solid #e2e8f0;
  display: flex; flex-direction: column; justify-content: space-between; gap: 1.5rem;
  transition: 0.3s ease; position: relative;
}
.review-card:hover { transform: translateY(-3px); box-shadow: 0 10px 25px rgba(0,0,0,0.06); }

/* Message / Citation */
.card-body { position: relative; padding-top: 0.5rem; flex-grow: 1; }
.quote-icon { position: absolute; top: -20px; left: -10px; font-size: 4rem; color: #eff6ff; font-family: serif; font-weight: 900; line-height: 1; z-index: 0; user-select: none; }
.review-text { color: var(--text-dark); font-size: 0.95rem; line-height: 1.6; font-style: italic; margin: 0; position: relative; z-index: 1; }

/* Auteur & Actions */
.card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 1.2rem; border-top: 1px solid #f1f5f9; }
.author-info { display: flex; align-items: center; gap: 0.8rem; }
.avatar-circle { width: 40px; height: 40px; border-radius: 50%; background: #f3e8ff; color: #a855f7; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1.1rem; flex-shrink: 0; }
.avatar-image { width: 40px; height: 40px; border-radius: 50%; object-fit: cover; flex-shrink: 0; border: 1px solid #e2e8f0; }
.author-details { display: flex; flex-direction: column; justify-content: center; }

/* Boutons d'édition/suppression */
.actions-group { display: flex; gap: 0.5rem; }
.action-icon-btn { background: #f8fafc; border: 1px solid #e2e8f0; color: #64748b; width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: 0.2s; }
.action-icon-btn:hover { background: #e2e8f0; color: var(--text-dark); }
.delete-btn:hover { background: #fee2e2; border-color: #fecaca; color: #ef4444; }

/* Carte Ajout rapide */
.add-card { border: 2px dashed #cbd5e1; background: transparent; box-shadow: none; align-items: center; justify-content: center; text-align: center; cursor: pointer; min-height: 220px; }
.add-card:hover { border-color: var(--accent-blue); background: #f8fafc; }
.add-circle { width: 50px; height: 50px; border-radius: 50%; background: #eff6ff; color: var(--accent-blue); display: flex; align-items: center; justify-content: center; }
</style>