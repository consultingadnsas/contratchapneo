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
                <span v-if="discount" class="discount-tag">-{{ discount }}%</span>
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
        price: { type: String, default: '$120' },
        oldPrice: { type: String, default: '150' },
        discount: { type: String, default: '20' },
        dateRange: { type: String, default: 'Aug 2024 to Jan 2025' },
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
    background: #ffffff;
    border-radius: 12px;
    padding: 2rem 1.5rem;
    display: flex;
    flex-direction: column;
    position: relative;
    border: 1px solid #e5e7eb;
    transition: all 0.3s ease;
    width: 100%;
    min-width: 300px;
    min-height: 450px;
}

/* Style spécifique pour la carte mise en avant (Everyday Pass dans ton image) */
.pro-card.is-popular {
    border: 2px solid #10b981; /* Vert émeraude */
}

.badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    background: #10b981;
    color: white;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
}

.pro-title {
    font-size: 1.25rem;
    font-weight: 700;
    color: #111827;
    margin: 0 0 1.5rem 0;
}

.price-section {
    margin-bottom: 1.5rem;
}

.price-row {
    display: flex;
    align-items: center;
    gap: 8px;
}

.current-price {
    font-size: 2rem;
    font-weight: 800;
    color: #111827;
}

.old-price {
    font-size: 0.875rem;
    text-decoration: line-through;
    color: #9ca3af;
}

.discount-tag {
    background: #fee2e2;
    color: #ef4444;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 2px 6px;
    border-radius: 4px;
}

.date-range {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 4px;
}

.divider {
    height: 1px;
    background: #f3f4f6;
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
    color: #374151;
    font-weight: 500;
}

.check-icon {
    width: 20px;
    height: 20px;
    background: #10b981;
    color: white;
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

/* Styles pour les boutons selon l'état de la carte */
:deep(.btn-light button) {
    background: #f3f4f6 !important;
    color: #111827 !important;
    width: 100%;
}

:deep(.btn-dark button) {
    background: #030712 !important; /* Noir profond comme dans l'image */
    color: #ffffff !important;
    width: 100%;
}
</style>