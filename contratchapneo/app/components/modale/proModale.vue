<template>
    <transition name="modal-fade">
        <div v-if="isOpen && professional" class="details-overlay" @click.self="$emit('close')">
            <div class="details-modal glass-effect">
                
                <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>

                <div class="modal-layout">

                    <!-- ── COLONNE GAUCHE : Photo complète ── -->
                    <div class="modal-visual">
                        <!-- Photo de profil couvrant tout l'espace -->
                        <img
                            v-if="professional.profile_picture"
                            :src="professional.profile_picture"
                            :alt="`${professional.first_name} ${professional.last_name}`"
                            class="pro-cover-image"
                        />
                        <!-- Fallback si pas de photo -->
                        <div v-else class="pro-cover-fallback">
                            {{ initials }}
                        </div>

                    </div>

                    <!-- ── COLONNE DROITE : Infos détaillées ── -->
                    <div class="modal-info">
                        <div class="header-titles">
                            <h2 class="modal-title">
                                {{ professional.first_name }} {{ professional.last_name }} 
                                <span v-if="professional.is_verified" class="verified-badge-floating" title="Professionnel vérifié">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
                                        <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                </span>
                            </h2>
                               
                            <p class="pro-role-subtitle">{{ professional.title_display }} </p>
                        </div>

                        <div class="scrollable-body">

                            <!-- Bio -->
                            <p class="long-description muted-text">{{ professional.bio }}</p>

                            <!-- Grille d'informations (Expérience, N°, Ordre, Localisation) -->
                            <div class="meta-grid">
                                
                                <div class="meta-item">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2">
                                        <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"/>
                                    </svg>
                                    <div>
                                        <span class="meta-label">Expérience</span>
                                        <span class="meta-value">{{ professional.years_of_experience }} ans</span>
                                    </div>
                                </div>

                                <div class="meta-item">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2">
                                        <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                                    </svg>
                                    <div>
                                        <span class="meta-label">N° d'inscription</span>
                                        <span class="meta-value">{{ professional.registration_number }}</span>
                                    </div>
                                </div>

                                <div class="meta-item" v-if="professional.professional_order">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2">
                                        <path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"/>
                                    </svg>
                                    <div>
                                        <span class="meta-label">Ordre professionnel</span>
                                        <span class="meta-value">{{ professional.professional_order }}</span>
                                    </div>
                                </div>

                                <!-- NOUVEAU : Localisation sur la même ligne que l'ordre pro -->
                                <div class="meta-item" v-if="professional.city || professional.country?.name">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2">
                                        <path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/>
                                        <path d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/>
                                    </svg>
                                    <div>
                                        <span class="meta-label">Localisation</span>
                                        <span class="meta-value">
                                            {{ professional.city }}<template v-if="professional.city && professional.country?.name">, </template>{{ professional.country?.name }}
                                        </span>
                                    </div>
                                </div>

                                <div class="meta-item" v-if="professional.website">
                                    <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2">
                                        <path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9"/>
                                    </svg>
                                    <div>
                                        <span class="meta-label">Site web</span>
                                        <a :href="professional.website" target="_blank" class="meta-link">
                                            Lien vers le site
                                        </a>
                                    </div>
                                </div>
                            </div>

                            <!-- Domaines d'expertise -->
                            <div class="features-section" v-if="professional.domains?.length">
                                <h4>Domaines d'expertise</h4>
                                <ul class="features-list">
                                    <li v-for="domain in professional.domains" :key="domain.id">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5">
                                            <polyline points="20 6 9 17 4 12"/>
                                        </svg>
                                        {{ domain.name }}
                                    </li>
                                </ul>
                            </div>

                        </div>

                        <!-- Actions -->
                        <div class="modal-actions">
                            <checkout-button 
                                @click="$emit('pay-consultation', professional)" 
                                label="Payer la consultation"
                            />
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts">
import { computed } from 'vue'
import type { LegalProfessional } from '../../../stores/proStore'
import checkoutButton from '../buttons/checkoutButton.vue'

export default {
    name: 'ProModale',

    props: {
        isOpen:       { type: Boolean, required: true },
        professional: { type: Object as () => LegalProfessional | null, default: null }
    },

    emits: ['close', 'pay-consultation'],

    components:{
        checkoutButton
    },

    setup(props) {
        // Initiales pour le fallback avatar
        const initials = computed(() => {
            if (!props.professional) return ''
            const f = props.professional.first_name?.[0] ?? ''
            const l = props.professional.last_name?.[0] ?? ''
            return (f + l).toUpperCase()
        })

        return { initials }
    }
}
</script>

<style scoped>
/* ── Overlay ── */
.details-overlay {
    position: fixed;
    inset: 0;
    background-color: rgba(15, 23, 42, 0.7);
    z-index: 9999;
    display: flex; justify-content: center; align-items: center;
    padding: 2rem;
    backdrop-filter: blur(8px);
}

.glass-effect {
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.2);
    box-shadow: 0 25px 50px rgba(0, 0, 0, 0.1);
}

.details-modal {
    width: 100%;
    max-width: 950px;
    border-radius: 32px;
    position: relative;
    overflow: hidden;
    animation: modalSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    max-height: 90vh;
    display: flex;
    flex-direction: column;
}

@keyframes modalSlideIn {
    from { opacity: 0; transform: translateY(30px) scale(0.95); }
    to   { opacity: 1; transform: translateY(0)    scale(1);    }
}

/* ── Bouton fermer ── */
.close-btn {
    position: absolute; top: 1.5rem; right: 1.5rem;
    background: rgba(15, 23, 42, 0.05); border: none; color: #0f172a;
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 10; transition: background 0.2s;
}
.close-btn:hover { background: rgba(15, 23, 42, 0.1); }
.close-btn svg   { width: 18px; height: 18px; }

/* ── Layout 2 colonnes ── */
.modal-layout {
    display: grid;
    grid-template-columns: 1fr 1.6fr;
    min-height: 550px;
    height: 100%;
    flex: 1;
    overflow: hidden;
}

/* ── Colonne gauche (Photo) ── */
.modal-visual {
    position: relative;
    width: 100%;
    height: 100%;
    background-color: #0f172a;
    overflow: hidden;
}

.pro-cover-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    object-position: center;
    display: block;
}

.pro-cover-fallback {
    width: 100%;
    height: 100%;
    background: linear-gradient(160deg, #0f172a 0%, #1e3a5f 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 5rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.5);
    letter-spacing: 2px;
}

/* Badge vérifié flottant sur l'image */
.verified-badge-floating {
    position: relative;
    top: 0.2rem;
    left: 0.9rem;
    background: #34d399;
    color: #064e3b;
    padding: 0rem 0.2rem;
    border-radius: 50px;
    font-size: 0.5rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 0.2rem;
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.verified-badge-floating svg { width: 20px; height: 20px; }

/* ── Colonne droite ── */
.modal-info {
    padding: 3rem 3rem 2.5rem 3rem;
    background: #ffffff;
    display: flex; flex-direction: column;
    height: 100%; overflow: hidden;
}

.header-titles {
    margin-bottom: 1.5rem;
    flex-shrink: 0;
}

.modal-title {
    font-size: 2rem; font-weight: 800; color: #0f172a;
    margin: 0 0 0.2rem 0; line-height: 1.1; display: flex; flex-direction: grid;
    padding: 0.2rem 0;
}
.modal-title .verified-badge-floating{
    margin: 0 0 0.5rem 0;
}


.pro-role-subtitle {
    font-size: 1.05rem;
    color: #64748b;
    font-weight: 500;
    margin: 0;
}

/* Zone scrollable */
.scrollable-body {
    flex-grow: 1;
    overflow-y: auto;
    padding-right: 1rem;
    margin-bottom: 1.5rem;
    width: 100%;
}
.scrollable-body::-webkit-scrollbar       { width: 6px; }
.scrollable-body::-webkit-scrollbar-track { background: #f8fafc; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.long-description { font-size: 1rem; line-height: 1.7; color: #64748b; margin-bottom: 1.5rem; }

/* Grille méta-infos */
.meta-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 2rem;
}
.meta-item {
    display: flex; align-items: flex-start; gap: 0.6rem;
    background: #f8fafc; border-radius: 12px; padding: 0.85rem 1rem;
}
.meta-item svg    { width: 18px; height: 18px; flex-shrink: 0; margin-top: 3px; }
.meta-item div    { display: flex; flex-direction: column; gap: 0.15rem; }
.meta-label       { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.8px; color: #94a3b8; }
.meta-value       { font-size: 0.9rem; font-weight: 600; color: #0f172a; }
.meta-link        { font-size: 0.85rem; font-weight: 500; color: #3b82f6; text-decoration: none; word-break: break-all; }
.meta-link:hover  { text-decoration: underline; }

/* Domaines */
.features-section h4 {
    font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;
    color: #94a3b8; margin: 0 0 0.85rem;
}
.features-list {
    list-style: none; padding: 0; margin: 0;
    display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;
}
.features-list li {
    display: flex; align-items: flex-start; gap: 0.6rem;
    font-size: 0.9rem; font-weight: 600; color: #334155; line-height: 1.4;
}
.features-list svg { width: 18px; height: 18px; flex-shrink: 0; margin-top: 2px; }

/* Actions */
.modal-actions {
    display: flex; justify-content: flex-start; gap: 1rem; width: 100%;
    flex-shrink: 0; margin-top: auto;
}

/* Transition */
.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s; }
.modal-fade-enter-from,   .modal-fade-leave-to     { opacity: 0; }

/* ── Mobile ── */
@media (max-width: 768px) {
    .details-modal {
        max-height: 95vh;
        display: block;
        overflow-y: auto;
    }
    .modal-layout {
        grid-template-columns: 1fr;
        min-height: auto;
        display: block;
    }
    .modal-visual { 
        height: 250px; /* Limite la hauteur de l'image sur mobile */
    }
    .modal-info   { padding: 2rem; height: auto; overflow: visible; }
    .scrollable-body { overflow-y: visible; padding-right: 0; margin-bottom: 0; }
    .modal-title  { font-size: 1.6rem; }
    .meta-grid    { grid-template-columns: 1fr; }
    .features-list { grid-template-columns: 1fr; }
    .modal-actions { flex-direction: column; margin-top: 2rem; }
    .details-overlay { padding: 0.75rem; }
}
</style>