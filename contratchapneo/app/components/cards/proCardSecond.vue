<template>
    <article class="pro-card">
        <!-- Zone supérieure : Photo de profil -->
        <div 
            class="card-bg" 
            :style="{ backgroundImage: `url(${image})` }"
        ></div>

        <!-- Zone inférieure : Informations style Badge -->
        <div class="card-info">
            <!-- La forme de découpe asymétrique en SVG pour un rendu parfait et fluide -->
            <div class="badge-cutout">
                <svg viewBox="0 0 100 20" preserveAspectRatio="none">
                    <path d="M0,20 L100,20 L100,0 C80,0 70,18 45,18 L0,18 Z" fill="#ffffff" />
                </svg>
            </div>
            
            <div class="info-content">
                <h4 class="pro-name">
                    <!-- Permet de séparer proprement le prénom et le nom si nécessaire -->
                    {{ formatName(title).first }} <br />
                    <span class="last-name">{{ formatName(title).last }}</span>
                </h4>
                
                <div class="badge-footer">
                    <p class="pro-specialty">{{ subtitle }}</p>
                    <span class="badge-id">ID #{{ idNumber }}</span>
                </div>
            </div>
        </div>
    </article>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import defaultImg from '@/assets/pictures/ContratChap/pexels-thirdman-5060819.jpg'; // cite: 1

export default defineComponent({
    name: 'ProCards',
    props: {
        title: {
            type: String,
            default: 'Constance Kelly'
        },
        subtitle: {
            type: String,
            default: 'Data Analyst'
        },
        image: {
            type: String,
            default: defaultImg // cite: 1
        },
        idNumber: {
            type: String,
            default: '000761'
        }
    },
    methods: {
        // Petite fonction utilitaire pour scinder le nom en deux lignes comme sur le badge
        formatName(fullName: string) {
            const parts = fullName.split(' ');
            if (parts.length > 1) {
                return { first: parts[0], last: parts.slice(1).join(' ') };
            }
            return { first: fullName, last: '' };
        }
    }
});
</script>

<style scoped>
.pro-card {
    position: relative;
    width: 100%;
    /* Ratio vertical typique d'un badge d'identification */
    aspect-ratio: 1 / 1.4; 
    border-radius: 16px; /* Des angles plus arrondis et doux */
    overflow: hidden;
    cursor: pointer;
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.08);
    background-color: #f4f4f5;
    display: flex;
    flex-direction: column;
}

/* Photo centrée en haut */
.card-bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 65%; /* Occupe la majeure partie supérieure */
    background-size: cover;
    background-position: center top;
    transition: transform 0.5s ease;
    z-index: 1;
}

.pro-card:hover .card-bg {
    transform: scale(1.04);
}

/* Bloc d'infos blanc en bas */
.card-info {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 42%; /* Légère superposition sur l'image */
    z-index: 2;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
}

/* Vague de découpe asymétrique moderne */
.badge-cutout {
    position: absolute;
    top: -18px; /* Aligné avec la hauteur du tracé SVG */
    left: 0;
    width: 100%;
    height: 20px;
    overflow: hidden;
}

.badge-cutout svg {
    width: 100%;
    height: 100%;
}

/* Contenu textuel interne */
.info-content {
    padding: 0 1.25rem 1.25rem 1.25rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    flex-grow: 1;
}

.pro-name {
    margin: -5px 0 0 0;
    font-size: 1.4rem;
    font-weight: 600;
    line-height: 1.15;
    color: #18181b;
    letter-spacing: -0.01em;
}

.last-name {
    font-weight: 600;
}

/* Aligné tout en bas du badge */
.badge-footer {
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    margin-top: auto;
}

.pro-specialty {
    margin: 0;
    font-size: 0.75rem;
    font-weight: 500;
    color: #71717a;
    letter-spacing: 0.02em;
}

.badge-id {
    font-size: 0.75rem;
    font-weight: 500;
    color: #a1a1aa;
    font-variant-numeric: tabular-nums;
}
</style>