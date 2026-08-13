<template>
    <article class="pro-card">
        <div :class="['card-header', `header-${planType}`]">
            <h4 class="pro-title">{{ title }}</h4>

            <div class="price-section">
                <span class="price-main">{{ price}} FCFA</span>
                <span class="price-suffix">/an</span>
            </div>

            <p class="description">{{ description }}</p>

            <!-- ⚡️ NOUVEAU : Condition pour afficher soit le badge, soit le bouton -->
            <div v-if="isActive" class="active-pack-badge">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="check-icon-large">
                    <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd" />
                </svg>
                Pack Actif
            </div>
            
            <mainButton v-else :label="buttonLabel" class="btn-dark" @click="$emit('buy')"/>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import mainButton from '../buttons/mainButton.vue';
import {useRouter} from 'vue-router';

export default defineComponent({
    name: 'LegendaryCard',
    components: { mainButton },
    props: {
        planType: {
            type: String as PropType<'basique' | 'business' | 'business-pro'>,
            default: 'basique',
            validator: (value: string) => ['basique', 'business', 'business-pro'].includes(value)
        },
        title: { 
            type: String, 
            default: 'Pack basique' 
        },
        description: { 
            type: String, 
            default: 'Découvrez notre pack basique et profitez de 10 contrats jurdiques.' 
        },
        price: { 
            type: String, 
            default: '25000.00 FCFA' 
        },   
        buttonLabel: { 
            type: String, 
            default: 'Acheter' 
        },
        // ⚡️ NOUVEAU : La prop pour déterminer si le pack est déjà acheté
        isActive: {
            type: Boolean,
            default: false
        }
    },
    emits:['buy'],
    setup(){
        const router = useRouter();
        return{
            router,
        }
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
    border-radius: 20px;
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

.price-section {
    display: flex;
    align-items: baseline;
    gap: 0;
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
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
    color: #1f2937;
    font-weight: 500;
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
}

/* --- NOUVEAU : STYLE DU BADGE ACTIF --- */
.active-pack-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    width: 100%;
    box-sizing: border-box;
    background: rgba(22, 163, 74, 0.1); /* Fond vert transparent */
    color: #16a34a; /* Texte vert Contratchap */
    font-weight: 700;
    border-radius: 999px;
    padding: 14px 28px;
    font-size: 1rem;
    border: 1px solid rgba(22, 163, 74, 0.2);
}

.check-icon-large {
    width: 22px;
    height: 22px;
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