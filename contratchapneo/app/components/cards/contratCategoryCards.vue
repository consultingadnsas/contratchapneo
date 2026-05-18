<template>
    <div class="badge-card">
        <div class="icon-wrapper">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9.75 3.104v5.714a2.25 2.25 0 0 1-.659 1.591L5 14.5M9.75 3.104c-.251.023-.501.05-.75.082m.75-.082a24.301 24.301 0 0 1 4.5 0m0 0v5.714c0 .597.237 1.17.659 1.591L19.8 15.3M14.25 3.104c.251.023.501.05.75.082M19.8 15.3l-1.57.393A9.065 9.065 0 0 1 12 15a9.065 9.065 0 0 0-6.23-.693L5 14.5m14.8.8 1.402 1.402c1.232 1.232.65 3.318-1.067 3.611A48.309 48.309 0 0 1 12 21c-2.773 0-5.491-.235-8.135-.687-1.718-.293-2.3-2.379-1.067-3.61L5 14.5" />
            </svg>
        </div>
        <p class="badge-title">Catégorie de {{ title }}</p>
        <div class="btn-container">
            <button>
                <span>
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="arrow-svg size-6">
                        <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
                    </svg>
                </span>
            </button>
        </div>
    </div>
</template>

<script lang="ts">
export default {
    name: 'OrdinaryBadge',
    props: {
        title: {
            type: String,
            default: 'Création/cession'
        }
    }
}
</script>

<style scoped>
/* --- La Carte Badge globale --- */
.badge-card {
    z-index: 1;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    
    padding: 1.25rem 1rem;
    background: #ffffff;
    border: 1px solid rgba(0, 0, 0, 0.08);
    border-radius: 16px;
    
    /* Ombre très douce et moderne */
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.02);
    
    /* Transition pour l'animation de survol */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    user-select: none;
    height: 200px;
    width: 200px;
}

/* --- L'Écrin de l'icône --- */
.icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    
    width: 48px;
    height: 48px;
    margin-bottom: 0.75rem;
    border-radius: 12px;
    
    /* Utilise ta couleur principale avec 8% d'opacité en fond */
    background-color: rgba(74, 222, 128, 0.08); /* Exemple avec un vert, s'adaptera à ton projet */
    color: var(--primary-color);
    
    transition: all 0.3s ease;
}

.icon-wrapper svg {
    width: 24px;
    height: 24px;
    transition: transform 0.3s ease;
}

/* --- Le Texte --- */
.badge-title {
    color: #1f2937; /* Teinte sombre text-gray-800 pour un look pro */
    font-size: 0.95rem;
    font-weight: 500;
    margin: 0;
    transition: color 0.3s ease;
}

.btn-container {
    z-index: 2;
    position: absolute;
    bottom: -5px;
    right: -5px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: none;
    border-top-left-radius: 2rem;
    border-bottom-right-radius: 1.5rem;
    width: 55px;
    height: 55px;
}

.btn-container button {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    border: none;
    cursor: pointer;
    color: #ffffff;
    background: var(--primary-color);
    transition: transform 0.3s ease;
    flex-shrink: 0;
}

.badge-card button:hover {
    transform: scale(1.1) rotate(5deg);
}

.size-6 {
    width: 18px;
    height: 18px;
}

/* --- LA TOUCHE ESTHÉTIQUE : Effet Hover / Active (Tactile) --- */
@media (hover: hover) {
    .badge-card:hover {
        transform: translateY(-4px);
        border-color: var(--primary-color);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
    }

    .badge-card:hover .icon-wrapper {
        /* L'écrin s'illumine complètement au survol */
        background-color: var(--primary-color);
        color: #ffffff;
    }
    
    .badge-card:hover .icon-wrapper svg {
        transform: scale(1.1); /* Léger pop de l'icône */
    }

    .badge-card:hover .badge-title {
        color: var(--primary-color);
    }
}

/* Effet au clic (très important pour le Mobile-First) */
.badge-card:active {
    transform: scale(0.97);
    background-color: #f9fafb;
}
</style>