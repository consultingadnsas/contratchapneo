<template>
    <transition name="modal-fade">
        <div v-if="isOpen && service" class="details-overlay" @click.self="$emit('close')">
            <div class="details-modal glass-effect">
                
                <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>
                </button>

                <div class="modal-layout">
                    <div class="modal-visual" :style="{ 
                        backgroundImage: `linear-gradient(to bottom, rgba(15, 23, 42, 0.2), rgba(15, 23, 42, 0.85)), url(${service.image})`,
                        backgroundSize: 'cover',
                        backgroundPosition: 'center'
                    }">
                        <div class="modal-icon-large" v-html="service.icon"></div>
                    </div>

                    <div class="modal-info">
                        <h2 class="modal-title">{{ service.title }}</h2>
                        
                        <div class="scrollable-body">
                            <p class="long-description muted-text">{{ service.longDescription }}</p>                        
                            
                            <div class="features-section">
                                <h4>Ce qui est inclus :</h4>
                                <ul class="features-list">
                                    <li v-for="(feature, idx) in service.features" :key="idx">
                                        <svg viewBox="0 0 24 24" fill="none" stroke="#34d399" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg>
                                        {{ feature }}
                                    </li>
                                </ul>
                            </div>
                        </div>
                        
                        <div class="modal-actions">
                            <button class="btn-primary" @click="$emit('quote', service.title)">
                                Générer un devis
                                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </button>
                            <button class="btn-secondary" @click="$emit('close')">Retour</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </transition>
</template>

<script lang="ts">
export default {
    name: 'ServiceModale',
    props: {
        isOpen: { type: Boolean, required: true },
        service: { type: Object, default: null }
    },
    emits: ['close', 'quote']
}
</script>

<style scoped>
/* L'overlay sombre et flou */
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

/* --- MODIFICATIONS PRINCIPALES ICI --- */
.details-modal {
    width: 100%;
    max-width: 950px;
    border-radius: 32px;
    position: relative;
    overflow: hidden;
    animation: modalSlideIn 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    
    /* On force la modale à ne pas dépasser 90% de la hauteur de l'écran */
    max-height: 90vh; 
    display: flex;
    flex-direction: column;
}

@keyframes modalSlideIn {
    from { opacity: 0; transform: translateY(30px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

.close-btn {
    position: absolute; top: 1.5rem; right: 1.5rem;
    background: rgba(15, 23, 42, 0.05); border: none; color: #0f172a;
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    cursor: pointer; z-index: 10; transition: background 0.2s;
}
.close-btn:hover { background: rgba(15, 23, 42, 0.1); }
.close-btn svg { width: 18px; height: 18px; }

.modal-layout {
    display: grid; grid-template-columns: 1fr 1.6fr; 
    min-height: 550px;
    height: 100%; /* S'assure de prendre toute la place dispo */
}

/* Visuel Gauche */
.modal-visual {
    padding: 4rem; display: flex; flex-direction: column;
    justify-content: space-between; align-items: center;
    color: #ffffff;
    position: relative; /* Sécurité pour le layout */
}

.modal-icon-large {
    width: 120px; height: 120px; color: #ffffff;
    background: rgba(255, 255, 255, 0.2);
    padding: 30px; border-radius: 30px; margin: auto 0;
}

.price-tag {
    width: 100%; padding: 1.5rem; border-radius: 16px;
    display: flex; flex-direction: column; text-align: center;
    background: rgba(255, 255, 255, 0.1) !important; border: 1px solid rgba(255,255,255,0.2);
}

/* Contenu Droite */
.modal-info {
    /* Padding réduit en haut et en bas pour maximiser l'espace du scroll */
    padding: 3rem 3rem 3rem 4rem; 
    background: #ffffff;
    display: flex; flex-direction: column; align-items: flex-start;
    
    /* Structure pour le scroll interne */
    height: 100%;
    overflow: hidden; 
}

/* Le titre ne doit pas bouger */
.modal-title { 
    font-size: 2.2rem; font-weight: 800; color: #0f172a; 
    margin: 0 0 1.5rem 0; line-height: 1.1; 
    flex-shrink: 0; 
}

/* --- LA ZONE MAGIQUE DE DÉFILEMENT --- */
.scrollable-body {
    flex-grow: 1; /* Prend l'espace libre au centre */
    overflow-y: auto; /* Active le scroll vertical */
    padding-right: 1.5rem; /* Écarte le texte de la scrollbar */
    margin-bottom: 1.5rem; /* Écarte le texte des boutons */
    width: 100%;
}

/* Design Premium pour la Scrollbar sur mesure (Webkit Chrome/Safari) */
.scrollable-body::-webkit-scrollbar { width: 6px; }
.scrollable-body::-webkit-scrollbar-track { background: #f8fafc; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 10px; }
.scrollable-body::-webkit-scrollbar-thumb:hover { background: #94a3b8; }

.long-description { font-size: 1.05rem; line-height: 1.6; color: #64748b; margin-bottom: 2rem; }

/* Liste Features */
.features-section { margin-bottom: auto; width: 100%; }
.features-section h4 { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; color: #94a3b8; margin-bottom: 1rem; }
.features-list { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.features-list li { display: flex; align-items: flex-start; gap: 0.8rem; font-size: 0.95rem; font-weight: 600; color: #334155; line-height: 1.4;}
.features-list svg { width: 20px; height: 20px; flex-shrink: 0; margin-top: 2px;}

/* Actions en bas */
.modal-actions { 
    display: flex; gap: 1rem; width: 100%; 
    margin-top: auto; 
    flex-shrink: 0; /* Empêche les boutons d'être écrasés */
}
.btn-primary { background-color: #34d399; color: #0f172a; font-weight: 700; border: none; padding: 1rem 2rem; border-radius: 12px; cursor: pointer; display: flex; align-items: center; gap: 0.5rem; transition: transform 0.2s;}
.btn-primary:hover { transform: translateY(-2px); }
.btn-primary svg { width: 18px; height: 18px; }
.btn-secondary { background-color: #f1f5f9; color: #0f172a; font-weight: 600; border: none; padding: 1rem 2rem; border-radius: 12px; cursor: pointer; }
.btn-secondary:hover { background-color: #e2e8f0; }

.modal-fade-enter-active, .modal-fade-leave-active { transition: opacity 0.3s; }
.modal-fade-enter-from, .modal-fade-leave-to { opacity: 0; }

/* =============================================
   RESPONSIVE MOBILE 
   ============================================= */
@media (max-width: 768px) {
    .details-modal { 
        max-height: 95vh; 
        display: block; /* Annule le flex global */
        overflow-y: auto; /* Fait scroller toute la fenêtre nativement */
    }
    .modal-layout { 
        grid-template-columns: 1fr; 
        min-height: auto;
        display: block;
    }
    .modal-visual { padding: 3rem 2rem; min-height: 250px; }
    
    .modal-info { 
        padding: 2rem; 
        height: auto;
        overflow: visible; /* Annule la contrainte */
    }
    
    /* Sur mobile on désactive la boite de scroll interne (inutile) */
    .scrollable-body {
        overflow-y: visible;
        padding-right: 0;
        margin-bottom: 0;
    }
    
    .modal-title { font-size: 1.8rem; margin-bottom: 1rem; }
    .features-list { grid-template-columns: 1fr; }
    
    .modal-actions { flex-direction: column; margin-top: 2rem; }
    .details-overlay { padding: 1rem; }
}
</style>