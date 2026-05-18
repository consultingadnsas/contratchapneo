<template>
    <article :class="['pro-card', { 'is-popular': isPopular }]">
        <div v-if="isPopular" class="badge">
            Plus populaire
        </div>

        <div class="card-header">
            <h4 class="pro-title">{{ title }}</h4>
        </div>

        <div class="price-section">
            <div class="price-row">
                <span class="current-price">{{ price }}</span>
                <span v-if="oldPrice" class="old-price">${{ oldPrice }}</span>
            </div>
            <p class="date-range">{{ dateRange }}</p>
        </div>

        <div class="divider"></div>

        <div class="card-body">
            <ul class="features-list">
                <li v-for="(feature, index) in features" :key="index">
                    <span class="check-icon">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                            <path fill-rule="evenodd" d="M16.704 4.153a.75.75 0 0 1 .143 1.052l-8 10.5a.75.75 0 0 1-1.127.075l-4.5-4.5a.75.75 0 0 1 1.06-1.06l3.894 3.893 7.48-9.817a.75.75 0 0 1 1.05-.143Z" clip-rule="evenodd" />
                        </svg>
                    </span>
                    {{ feature }}
                </li>
            </ul>
        </div>

        <div class="card-footer">
            <mainButton :label="buttonLabel" :class="isPopular ? 'btn-dark' : 'btn-light'" />
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent, PropType } from 'vue';
import mainButton from '../buttons/mainButton.vue';

export default defineComponent({
    name: 'ContratCards',
    components: { mainButton },
    props: {
        title: { type: String, default: 'Weekday Pass' },
        price: { type: String, default: '29000 FCFA' },
        oldPrice: { type: String, default: '49000 FCFA' },
        discount: { type: String, default: '20' },
        dateRange: { type: String, default: 'Valable 1 an' },
        features: {
            type: Array as PropType<string[]>,
            default: () => [
                'Utilisation sur tout support',
                'Accès 24h/24 et 7j/7',
                'Support prioritaire'
            ]
        },
        buttonLabel: { type: String, default: 'Commencer' },
        isPopular: { type: Boolean, default: false }
    }
});
</script>

<style scoped>
.pro-card {
    display: flex;
    flex-direction: column;
    position: relative;
    width: 100%;
    min-width: 300px;
    min-height: 450px;
    padding: 2rem 1.5rem;
    border-radius: 1.25rem;
    box-sizing: border-box;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    /* --- EFFET GLASSMORPHISM --- */
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.18);
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
}

.pro-card:hover {
    transform: translateY(-6px);
    border-color: rgba(255, 255, 255, 0.3);
    box-shadow: 0 12px 40px 0 rgba(0, 0, 0, 0.35);
}

/* --- VARIANTE POPULAIRE MISE EN AVANT --- */
.pro-card.is-popular {
    background: rgba(255, 255, 255, 0.12); /* Légèrement plus opaque pour se détacher */
    border: 1.5px solid rgba(16, 185, 129, 0.6); /* Bordure vert émeraude translucide */
    /* Halo lumineux vert très discret */
    box-shadow: 0 8px 32px 0 rgba(16, 185, 129, 0.15), 0 4px 12px 0 rgba(0, 0, 0, 0.2);
}

.pro-card.is-popular:hover {
    border-color: rgba(16, 185, 129, 0.9);
    box-shadow: 0 12px 40px 0 rgba(16, 185, 129, 0.25);
}

.badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: var(--secondary-light-color);
    color: #ffffff;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
}

/* --- TYPOGRAPHIES (Adaptées pour le fond en transparence) --- */
.pro-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #ffffff; /* Blanc pur pour claquer sur le verre */
    margin: 0 0 1.5rem 0;
}

.price-section {
    margin-bottom: 1.5rem;
}

.price-row {
    display: flex;
    align-items: center;
    gap: 10px;
}

.current-price {
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
}

.old-price {
    font-size: 0.9rem;
    text-decoration: line-through;
    color: rgba(255, 255, 255, 0.4); /* Translucide pour l'ancien prix */
}

.discount-tag {
    background: rgba(239, 68, 68, 0.2); /* Rouge ultra-léger pour rester dans le thème glass */
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.25);
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 6px;
}

.date-range {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
    margin-top: 6px;
}

.divider {
    height: 1px;
    background: rgba(255, 255, 255, 0.12); /* Ligne translucide */
    margin-bottom: 1.5rem;
}

.card-body {
    flex-grow: 1;
}

.features-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.features-list li {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 0.95rem;
    color: rgba(255, 255, 255, 0.85); /* Texte légèrement adouci pour le confort visuel */
    font-weight: 500;
}

.check-icon {
    width: 20px;
    height: 20px;
    background: var(--secondary-light-color);
    color: #ffffff;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 4px;
    flex-shrink: 0;
}

.card-footer {
    margin-top: 2rem;
}

/* --- BOUTONS --- */
:deep(.btn-light button) {
    background: rgba(255, 255, 255, 0.15) !important; /* Bouton givré lui aussi */
    backdrop-filter: blur(4px);
    color: #ffffff !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    width: 100%;
    transition: background 0.2s ease;
}

:deep(.btn-light button:hover) {
    background: rgba(255, 255, 255, 0.25) !important;
}

:deep(.btn-dark button) {
    background: #ffffff !important; /* Le bouton principal devient blanc uni pour attirer l'œil instantanément */
    color: #030712 !important;
    font-weight: 600;
    width: 100%;
    box-shadow: 0 4px 14px rgba(255, 255, 255, 0.2);
}
</style>