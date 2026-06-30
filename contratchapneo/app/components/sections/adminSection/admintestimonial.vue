<template>
  <div class="testimonials-wrapper">
    
    <!-- EN-TÊTE -->
    <div class="header-section">
      <div class="title-row">
        <h3 class="section-title">Gestion des Témoignages</h3>
        <div class="global-rating">
          <span class="rating-number">4.8</span>
          <div class="stars">
            <component :is="StarIconSolid" class="icon-sm text-yellow" v-for="n in 5" :key="n" />
          </div>
          <span class="gray-text text-sm">(128 avis globaux)</span>
        </div>
      </div>

      <!-- FILTRES -->
      <div class="filters-row">
        <div class="tabs-group">
          <button class="tab-btn" :class="{ active: activeTab === 'En attente' }" @click="activeTab = 'En attente'">
            En attente <span class="badge-count bg-orange" v-if="pendingCount > 0">{{ pendingCount }}</span>
          </button>
          <button class="tab-btn" :class="{ active: activeTab === 'Publiés' }" @click="activeTab = 'Publiés'">Publiés</button>
          <button class="tab-btn" :class="{ active: activeTab === 'Rejetés' }" @click="activeTab = 'Rejetés'">Rejetés</button>
        </div>
      </div>
    </div>

    <!-- GRILLE DES AVIS -->
    <div class="reviews-grid">
      <div 
        class="review-card" 
        v-for="review in filteredReviews" 
        :key="review.id"
        :class="{'card-rejected': review.status === 'Rejetés'}"
      >
        
        <!-- Haut : Étoiles & Date -->
        <div class="card-header">
          <div class="stars">
            <component 
              :is="n <= review.rating ? StarIconSolid : StarIconOutline" 
              class="icon-xs text-yellow" 
              v-for="n in 5" 
              :key="n" 
            />
          </div>
          <span class="gray-text text-xs">{{ review.date }}</span>
        </div>

        <!-- Corps : Le message -->
        <div class="card-body">
          <h4 class="dark-text font-bold mb-1">{{ review.contractPurchased }}</h4>
          <p class="review-text">"{{ review.message }}"</p>
        </div>

        <!-- Auteur & Statut -->
        <div class="author-section">
          <div class="author-info">
            <div class="avatar-circle">{{ review.author.charAt(0) }}</div>
            <div>
              <div class="dark-text font-bold text-sm">{{ review.author }}</div>
              <div class="gray-text text-xs">{{ review.company }}</div>
            </div>
          </div>
          <span class="status-pill" :class="getStatusClass(review.status)">{{ review.status }}</span>
        </div>

        <!-- Bas : Actions (Validation) -->
        <div class="card-footer">
          <template v-if="review.status === 'En attente'">
            <button class="action-btn btn-approve" @click="changeStatus(review, 'Publiés')">
              <component :is="CheckCircleIcon" class="icon-sm" /> Approuver
            </button>
            <button class="action-btn btn-reject" @click="changeStatus(review, 'Rejetés')">
              <component :is="XCircleIcon" class="icon-sm" /> Rejeter
            </button>
          </template>
          
          <template v-else-if="review.status === 'Publiés'">
            <button class="action-btn btn-outline" @click="changeStatus(review, 'En attente')">
              Masquer du site
            </button>
          </template>
          
          <template v-else>
            <button class="action-btn btn-delete" @click="deleteReview(review.id)">
              <component :is="TrashIcon" class="icon-sm" /> Supprimer définitivement
            </button>
          </template>
        </div>

      </div>
    </div>

    <!-- ÉTAT VIDE -->
    <div v-if="filteredReviews.length === 0" class="empty-state">
      <h4 class="dark-text">Aucun témoignage dans cette catégorie.</h4>
    </div>

  </div>
</template>

<script lang="ts">
import { ref, computed, markRaw } from 'vue';
import { 
  StarIcon as StarIconOutline, 
  CheckCircleIcon, 
  XCircleIcon, 
  TrashIcon 
} from '@heroicons/vue/24/outline';
import { StarIcon as StarIconSolid } from '@heroicons/vue/24/solid';

export default {
  name: 'AdminTestimonials',
  setup() {
    const activeTab = ref('En attente');

    // Base de données factice des avis
    const reviews = ref([
      { 
        id: 1, 
        author: 'Sylla Awa', 
        company: 'Startup Tech', 
        rating: 5, 
        date: '28 Juin 2026', 
        contractPurchased: 'Pack Création SARL',
        message: 'Modèles très complets et parfaitement conformes à la réglementation OHADA. J\'ai pu immatriculer ma société sans aucun souci.', 
        status: 'En attente' 
      },
      { 
        id: 2, 
        author: 'Kouassi Jean', 
        company: 'Indépendant', 
        rating: 4, 
        date: '25 Juin 2026', 
        contractPurchased: 'Contrat de Prestation de Services',
        message: 'Bon document de base. J\'ai dû faire quelques petites retouches pour mon secteur, mais ça m\'a fait gagner beaucoup de temps.', 
        status: 'En attente' 
      },
      { 
        id: 3, 
        author: 'Bamba L.', 
        company: 'Cabinet Immo', 
        rating: 5, 
        date: '10 Juin 2026', 
        contractPurchased: 'Contrat de Bail Commercial',
        message: 'Excellent service. Le document est clair, précis et protège bien les deux parties.', 
        status: 'Publiés' 
      },
      { 
        id: 4, 
        author: 'Anonyme', 
        company: 'Particulier', 
        rating: 1, 
        date: '05 Juin 2026', 
        contractPurchased: 'Statuts SAS',
        message: 'Spam publicitaire, à ignorer.', 
        status: 'Rejetés' 
      }
    ]);

    const filteredReviews = computed(() => {
      return reviews.value.filter(review => review.status === activeTab.value);
    });

    const pendingCount = computed(() => {
      return reviews.value.filter(r => r.status === 'En attente').length;
    });

    const changeStatus = (review: any, newStatus: string) => {
      review.status = newStatus;
    };

    const deleteReview = (id: number) => {
      if (confirm('Supprimer définitivement cet avis ?')) {
        reviews.value = reviews.value.filter(r => r.id !== id);
      }
    };

    const getStatusClass = (status: string) => {
      if (status === 'Publiés') return 'pill-green';
      if (status === 'En attente') return 'pill-yellow';
      return 'pill-gray';
    };

    return {
      activeTab,
      filteredReviews,
      pendingCount,
      changeStatus,
      deleteReview,
      getStatusClass,
      StarIconOutline: markRaw(StarIconOutline),
      StarIconSolid: markRaw(StarIconSolid),
      CheckCircleIcon: markRaw(CheckCircleIcon),
      XCircleIcon: markRaw(XCircleIcon),
      TrashIcon: markRaw(TrashIcon)
    };
  }
}
</script>

<style scoped>
.testimonials-wrapper {
  --bg-panel: #ffffff;
  --bg-panel-light: #f1f5f9;
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
.text-yellow { color: #f59e0b; }
.mb-1 { margin-bottom: 0.5rem; }

.icon-xs { width: 16px; height: 16px; }
.icon-sm { width: 18px; height: 18px; }

/* EN-TÊTE */
.header-section { display: flex; flex-direction: column; gap: 1.5rem; }
.title-row { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }
.section-title { font-size: 1.4rem; color: var(--text-dark); font-weight: 700; margin: 0; }

.global-rating { display: flex; align-items: center; gap: 0.5rem; background: var(--bg-panel); padding: 0.5rem 1rem; border-radius: 50px; border: 1px solid #f1f5f9; }
.rating-number { font-size: 1.2rem; font-weight: 800; color: var(--text-dark); }
.stars { display: flex; gap: 2px; }

/* ONGLETS ET BADGES */
.tabs-group { display: flex; background: var(--bg-panel-light); border-radius: 50px; padding: 0.3rem; width: fit-content; }
.tab-btn { position: relative; background: transparent; border: none; color: var(--text-gray); font-size: 0.85rem; font-weight: 600; padding: 0.6rem 1.2rem; border-radius: 50px; cursor: pointer; transition: all 0.2s ease; display: flex; align-items: center; gap: 0.5rem; }
.tab-btn.active { background: var(--bg-panel); color: var(--text-dark); box-shadow: 0px 2px 10px rgba(0,0,0,0.05); }

.badge-count { color: white; padding: 2px 6px; border-radius: 50px; font-size: 0.7rem; font-weight: 700; }
.bg-orange { background: #f97316; }

/* GRILLE DES AVIS */
.reviews-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 1.5rem; }

.review-card {
  background: var(--bg-panel); border-radius: 20px; padding: 1.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.03); border: 1px solid #f8fafc;
  display: flex; flex-direction: column; justify-content: space-between; gap: 1rem;
  transition: 0.3s ease;
}
.review-card:hover { transform: translateY(-2px); box-shadow: 0 15px 35px rgba(0,0,0,0.05); }
.card-rejected { opacity: 0.6; }

.card-header { display: flex; justify-content: space-between; align-items: center; }

.review-text { color: var(--text-dark); font-size: 0.95rem; line-height: 1.5; font-style: italic; margin: 0; }

.author-section { display: flex; justify-content: space-between; align-items: center; margin-top: 0.5rem; padding-top: 1rem; border-top: 1px solid #f1f5f9; }
.author-info { display: flex; align-items: center; gap: 0.8rem; }
.avatar-circle { width: 36px; height: 36px; border-radius: 50%; background: #eff6ff; color: #2563eb; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; }

/* STATUTS */
.status-pill { padding: 0.3rem 0.8rem; border-radius: 50px; font-size: 0.7rem; font-weight: 700; }
.pill-green { background: #d1fae5; color: #059669; }
.pill-yellow { background: #fef3c7; color: #d97706; }
.pill-gray { background: #f1f5f9; color: #64748b; }

/* BOUTONS D'ACTION */
.card-footer { display: flex; gap: 0.5rem; margin-top: 0.5rem; }
.action-btn { flex: 1; display: flex; justify-content: center; align-items: center; gap: 0.4rem; padding: 0.6rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; cursor: pointer; border: none; transition: 0.2s; }
.btn-approve { background: #10b981; color: white; }
.btn-approve:hover { background: #059669; }
.btn-reject { background: #fee2e2; color: #dc2626; }
.btn-reject:hover { background: #fecaca; }
.btn-outline { background: transparent; border: 1px solid #e2e8f0; color: var(--text-dark); }
.btn-outline:hover { background: #f8fafc; }
.btn-delete { background: transparent; color: #ef4444; border: 1px solid #fee2e2; }
.btn-delete:hover { background: #fee2e2; }

.empty-state { text-align: center; padding: 3rem; color: var(--text-gray); }
</style>