<template>
    <div class="view-modale" @click.self="$emit('close')">
        <div class="modal-content">
            
            <button class="close-btn" @click="$emit('close')" aria-label="Fermer">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>

            <div class="modal-header">
                <span class="modal-badge">Aperçu du document</span>
                <h2 class="modal-title">Contrat de travail CDD</h2>
                <p class="modal-subtitle"></p>
            </div>

            <div class="modal-body">
                
                <!-- 📄 ESPACE APERÇU DU PDF NÉO-MORPHIQUE -->
                <div class="document-pdf-wrapper">
                    <!-- 
                       L'attribut src pointe vers votre PDF. 
                       Dans Nuxt/Vue, placez le fichier dans le dossier 'public'.
                       Le "#toolbar=0&navpanes=0" cache le menu natif (imprimer, zoom) du navigateur pour un rendu plus propre.
                    -->
                    <iframe 
                        src="/lettre de motivation Angui.pdf#toolbar=0&navpanes=0" 
                        class="pdf-preview" 
                        title="Aperçu du contrat CDD"
                        type="application/pdf">
                        <!-- Message de secours si le navigateur du mobile ne supporte pas l'affichage PDF -->
                    </iframe>
                </div>

                <div class="description-box">
                    <h3>Description du contrat</h3>
                    <p>
                        Ce contrat de travail à durée déterminée (CDD) est conclu entre ABC Entreprise et Jean Dupont pour une période de six mois. Le contrat précise les obligations de l'employeur et de l'employé, ainsi que les conditions de travail, la rémunération et les modalités de résiliation.
                    </p>
                </div>
            </div>

            <div class="modal-footer">
                <button class="btn-secondary" @click="$emit('close')">Fermer</button>
                <button class="btn-primary">Télécharger le PDF</button>
            </div>

        </div>
    </div>
</template>

<script>
export default {
    name: 'ViewModale',
    props: {
        isViewOpen: {
            type: Boolean,
            default: false
        }
    },
    emits: ['close'],
    setup(props, { emit }) {
        return {};
    }
}
</script>

<style scoped>
.view-modale {
    --color-primary: #156ca9;
    --color-success: #4db562;
    --color-dark: #294F62;
    --color-bg-light: #f4f7f9;
    --color-text-muted: #6b7280;
    
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(41, 79, 98, 0.6); 
    backdrop-filter: blur(4px); 
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 1rem;
    
    animation: fadeIn 0.3s ease-out;
}

.modal-content {
    background-color: #ffffff;
    border-radius: 16px;
    width: 100%;
    max-width: 600px; /* J'ai légèrement élargi (550 -> 600) pour donner plus de place à la lecture du PDF */
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
    box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    
    animation: slideUp 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-content::-webkit-scrollbar {
    width: 8px;
}
.modal-content::-webkit-scrollbar-track {
    background: #f1f1f1; 
    border-radius: 0 16px 16px 0;
}
.modal-content::-webkit-scrollbar-thumb {
    background: #c1c1c1; 
    border-radius: 8px;
}
.modal-content::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8; 
}

.close-btn {
    position: absolute;
    top: 16px;
    right: 16px;
    background: var(--color-bg-light);
    color: var(--color-text-muted);
    border: none;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease;
    z-index: 10;
}

.close-btn svg {
    width: 20px;
    height: 20px;
}

.close-btn:hover {
    background-color: #fee2e2;
    color: #ef4444;
    transform: rotate(90deg);
}

.modal-header {
    padding: 32px 32px 24px;
    border-bottom: 1px solid #e5e7eb;
}

.modal-badge {
    display: inline-block;
    background-color: rgba(21, 108, 169, 0.1);
    color: var(--color-primary);
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 4px 10px;
    border-radius: 20px;
    margin-bottom: 12px;
}

.modal-title {
    margin: 0;
    color: var(--color-dark);
    font-size: 1.5rem;
    font-weight: 800;
    line-height: 1.2;
}

.modal-subtitle {
    margin: 8px 0 0;
    color: var(--color-text-muted);
    font-size: 0.9rem;
}

.modal-body {
    padding: 24px 32px;
}

/* ── NOUVEAU : Wrapper pour l'iframe PDF ─────────────────────── */
.document-pdf-wrapper {
    width: 100%;
    height: 350px; /* Plus haut que l'image pour que le texte soit lisible */
    background-color: var(--color-bg-light);
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin-bottom: 24px;
    overflow: hidden; 
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.05); /* Petite ombre interne pour faire ressortir la feuille PDF */
}

.pdf-preview {
    width: 100%;
    height: 100%;
    border: none; /* Supprime la vilaine bordure 3D native des iframes */
    display: block;
}

.info-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin-bottom: 24px;
}

.info-item {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.info-label {
    font-size: 0.8rem;
    color: var(--color-text-muted);
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.info-value {
    color: var(--color-dark);
    font-size: 1.05rem;
    font-weight: 600;
}

.text-sm {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    font-weight: 400;
}

.highlight-amount {
    color: var(--color-success);
    font-size: 1.2rem;
    font-weight: 800;
}

.description-box {
    background-color: var(--color-bg-light);
    border-left: 4px solid var(--color-primary);
    padding: 20px;
    border-radius: 0 8px 8px 0;
}

.description-box h3 {
    margin: 0 0 10px 0;
    color: var(--color-dark);
    font-size: 1rem;
    font-weight: 700;
}

.description-box p {
    margin: 0;
    color: #4b5563;
    font-size: 0.95rem;
    line-height: 1.6;
}

.modal-footer {
    padding: 20px 32px;
    background-color: #f9fafb;
    border-top: 1px solid #e5e7eb;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
}

.modal-footer button {
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
    border: none;
}

.btn-secondary {
    background-color: transparent;
    color: var(--color-text-muted);
}

.btn-secondary:hover {
    background-color: #e5e7eb;
    color: var(--color-dark);
}

.btn-primary {
    background-color: var(--color-primary);
    color: white;
    box-shadow: 0 4px 6px rgba(21, 108, 169, 0.25);
}

.btn-primary:hover {
    background-color: #0f5282;
    transform: translateY(-1px);
    box-shadow: 0 6px 8px rgba(21, 108, 169, 0.3);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideUp {
    from { opacity: 0; transform: translateY(30px) scale(0.95); }
    to { opacity: 1; transform: translateY(0) scale(1); }
}

@media (max-width: 480px) {
    .modal-header, .modal-body, .modal-footer {
        padding: 20px;
    }
    .info-grid {
        grid-template-columns: 1fr; 
    }
    .document-pdf-wrapper {
        height: 250px; /* Sur téléphone on réduit un peu la hauteur du lecteur PDF */
    }
}
</style>