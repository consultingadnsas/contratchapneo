<template>
    <article class="pro-card">
        <div :class="['card-header', `header-${planType}`]">
            <h4 class="pro-title">{{ title }}</h4>

            <div class="price-section">
                <!-- ⚡️ AFFICHAGE DYNAMIQUE DU PRIX (Avec ou sans promo) -->
                <template v-if="promoPrice && Number(promoPrice) > 0">
                    <span class="price-old">{{ price }}</span>
                    <span class="price-main">{{ promoPrice }}</span>
                </template>
                <template v-else>
                    <span class="price-main">{{ price }} </span>
                </template>
                <span class="price-suffix">FCFA</span>
            </div>

            <p class="description">{{ description }}</p>

            <mainButton :label="buttonLabel" class="btn-dark" @click="()=>{router.push('/auth/login')}"/>
        </div>

        <div class="card-body">
            <ul class="features-list">
                <!-- ⚡️ BOUCLE SUR LES AVANTAGES CALCULÉS DYNAMIQUEMENT -->
                <li v-for="(feature, index) in computedFeatures" :key="index">
                    <span class="check-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clip-rule="evenodd" />
                        </svg>
                    </span>
                    {{ feature }}
                </li>
            </ul>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent, PropType, computed } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import { useRouter } from 'vue-router';

export default defineComponent({
    name: 'LegendaryCard',
    components: { mainButton },
    props: {
        planType: {
            type: String as PropType<'basique' | 'business' | 'business-pro'>,
            default: 'basique',
            validator: (value: string) => ['basique', 'business', 'business-pro'].includes(value)
        },
        title: { type: String, required: true },
        description: { type: String, default: '' },
        
        // ⚡️ PRIX
        price: { type: [Number, String], required: true },
        promoPrice: { type: [Number, String], default: null },

        // ⚡️ NOUVELLES PROPS (Directement liées à ta base de données)
        nombreCredits: { type: Number, default: 0 },
        nombreCustomedContract: { type: Number, default: 0 },
        nombreCartesPro: { type: Number, default: 0 },
        dureeValiditeJours: { type: Number, default: 30 },
        
        buttonLabel: { type: String, default: 'Commencer' }
    },
    setup(props) {
        
        const router = useRouter();

        // ⚡️ LOGIQUE DE CRÉATION DE LA LISTE :
        // Si le backend renvoie un chiffre > 0, on ajoute la phrase correspondante à la liste.
        const computedFeatures = computed(() => {
            const list = [];
            
            if (props.nombreCredits > 0) {
                list.push(`Accès à ${props.nombreCredits} document(s) juridique(s) payant(s)`);
            }
            
            if (props.nombreCustomedContract > 0) {
                list.push(`Rédaction sur-mesure de ${props.nombreCustomedContract} document(s)`);
            }
            
            if (props.nombreCartesPro > 0) {
                list.push(`Suivi juriste : ${props.nombreCartesPro} consultation(s) incluse(s)`);
            }
            
            if (props.dureeValiditeJours > 0) {
                list.push(`Validité du pack : ${props.dureeValiditeJours} jours`);
            }

            // Fallback au cas où le pack serait vide
            if (list.length === 0) {
                list.push("Aucun avantage spécifique inclus");
            }
            
            return list;
        });

        return {
            router,
            computedFeatures
        };
    }
});
</script>

<style scoped>
/* --- STYLE ÉPURÉ ET BLANC --- */
.pro-card {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: auto;
    max-width: 420px;
    padding: 0.5rem;
    border-radius: 28px;
    box-sizing: border-box;
    background: #ffffff;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
}

.pro-card:hover {
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
    transform: translateY(-10px);
    transition: all 0.2s ease;
}

/* --- STRUCTURE DU HEADER --- */
.card-header {
    margin-bottom: 1rem;
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem; 
    border-radius: 1.5rem;
    transition: background 0.3s ease;
}

/* --- DÉCLINAISONS DE COULEURS DU HEADER --- */
.header-basique {
    background: #f3f4f6; 
}

.header-business {
    background: #e0f2fe; 
}

.header-business-pro {
    background: linear-gradient(135deg, #e0f2fe 0%, #65e17e 100%);
}

/* --- TYPOGRAPHIES ET ÉLÉMENTS --- */
.pro-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #1f2937;
    margin: 0;
    text-transform: capitalize;
}

.card-body {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    padding: 0 1rem 1rem 1rem; 
}

/* ⚡️ NOUVEAU STYLE POUR LES PRIX BARRÉS */
.price-section {
    display: flex;
    align-items: baseline;
    gap: 0;
    flex-wrap: wrap; 
}

.price-old {
    font-size: 1.1rem;
    color: #9ca3af;
    text-decoration: line-through;
    margin-right: 0.6rem;
    font-weight: 600;
}

.price-main {
    font-size: 1.8rem; 
    font-weight: 800;
    color: #111827;
    line-height: 1;
}

.price-suffix {
    font-size: 0.95rem;
    color: #4b5563; 
    margin-left: 4px;
    font-weight: 500;
}

.description {
    font-size: 0.95rem;
    color: #4b5563;
    line-height: 1.5;
    margin: 0;
}

.features-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 0.85rem;
}

.features-list li {
    display: flex;
    align-items: flex-start; /* Aligné en haut si le texte passe sur 2 lignes */
    gap: 12px;
    font-size: 0.95rem;
    color: #1f2937;
    font-weight: 500;
    line-height: 1.4;
}

.check-icon {
    width: 20px;
    height: 20px;
    background: #16a34a;
    color: #ffffff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
    flex-shrink: 0;
    margin-top: 2px;
}

/* --- BOUTONS --- */
.btn-dark {
    width: 100%;
    box-sizing: border-box;
}

:deep(.btn-dark button) {
    box-sizing: border-box; 
    background: #111827 !important;
    color: #ffffff !important;
    font-weight: 600;
    width: 100%;
    border-radius: 999px;
    padding: 14px 28px;
    font-size: 1rem;
    border: none;
    transition: background 0.4s ease;
}

:deep(.btn-dark button:hover) {
    background: #1f2937 !important;
    transition: background 0.2s ease;
}
</style>