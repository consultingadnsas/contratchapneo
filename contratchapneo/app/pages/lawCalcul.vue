<template>
    <div class="page-wrapper">
        <main class="law-calcul-page">
            <Navbar />
            
            <section class="hero-section">
                <h1 class="main-title">
                    Vos simulations juridiques <br>
                    <span class="text-accent">claires, rapides et précises.</span>
                </h1>
                <p class="hero-description muted-text">
                    Sélectionnez la nature de votre calcul pour évaluer instantanément vos droits ou obligations selon la législation ivoirienne et l'espace OHADA.
                </p>
            </section>

            <section class="selector-section" v-if="!selectedType">
                <div class="options-grid">
                    <div 
                        v-for="option in simulationTypes" 
                        :key="option.id" 
                        class="option-card"
                        @click="selectType(option)"
                    >
                        <div class="option-icon" v-html="option.icon"></div>
                        <h3>{{ option.title }}</h3>
                        <p class="muted-text">{{ option.description }}</p>
                        <span class="action-link">Démarrer <span class="arrow">→</span></span>
                    </div>
                </div>
            </section>

            <section class="workspace-section" v-else>
                <button class="back-btn" @click="resetSelection">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" width="16" height="16"><polyline points="15 18 9 12 15 6"></polyline></svg>
                    Changer de simulateur
                </button>

                <div class="workspace-title-area">
                    <h2>{{ selectedType.title }}</h2>
                    <p class="muted-text">{{ selectedType.extendedDescription }}</p>
                </div>

                <div class="calculator-layout">
                    
                    <div class="form-pane">
                        
                        <div v-if="selectedType.formLayout === 'single'" class="single-step-form">
                            <div class="form-group">
                                <label>Salaire mensuel brut global (FCFA)</label>
                                <input type="number" v-model.number="singleForm.salaire" class="clean-input" placeholder="Ex: 450000" />
                            </div>
                            <div class="form-group">
                                <label>Statut du salarié</label>
                                <select v-model="singleForm.statut" class="clean-input custom-select">
                                    <option value="ouvrier">Ouvrier / Employé payé au mois</option>
                                    <option value="tam">Technicien / Agent de Maîtrise</option>
                                    <option value="cadre">Cadre / Ingénieur / Assimilé</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Ancienneté dans l'entreprise</label>
                                <select v-model="singleForm.ancienneteRange" class="clean-input custom-select">
                                    <option value="moins_de_1">Moins de 1 an</option>
                                    <option value="1_a_5">De 1 à 5 ans</option>
                                    <option value="plus_de_5">Plus de 5 ans</option>
                                </select>
                            </div>
                        </div>

                        <div v-if="selectedType.formLayout === 'multi'" class="multi-step-form">
                            <div class="steps-indicator">
                                <span :class="{ 'is-active': multiStep === 1 }">1. Contrat</span>
                                <span :class="{ 'is-active': multiStep === 2 }">2. Dates & Salaire</span>
                            </div>

                            <div v-if="multiStep === 1" class="step-content">
                                <div class="form-group">
                                    <label>Quel est le motif de rupture envisagé ?</label>
                                    <select v-model="multiForm.motif" class="clean-input custom-select">
                                        <option value="eco">Licenciement pour motif économique</option>
                                        <option value="perso">Licenciement pour motif personnel</option>
                                        <option value="faute">Faute lourde ou disciplinaire</option>
                                    </select>
                                </div>
                                <button class="btn-primary mt-4" @click="multiStep = 2">Continuer</button>
                            </div>

                            <div v-if="multiStep === 2" class="step-content">
                                <div class="form-group">
                                    <label>Salaire de base moyen (FCFA)</label>
                                    <input type="number" v-model.number="multiForm.salaire" class="clean-input" placeholder="Ex: 600000" />
                                </div>
                                <div class="form-group">
                                    <label>Nombre d'années complètes d'ancienneté</label>
                                    <input type="number" v-model.number="multiForm.annees" class="clean-input" placeholder="Ex: 4" />
                                </div>
                                <div class="form-actions mt-4">
                                    <button class="btn-outline" @click="multiStep = 1">Retour</button>
                                    <button class="btn-primary" @click="calculerMulti">Générer le rapport complet</button>
                                </div>
                            </div>
                        </div>

                    </div>

                    <div class="result-pane">
                        <div class="result-sticky-card">
                            <h3>Estimation en temps réel</h3>
                            
                            <div class="amount-display">
                                <span class="amount-number">{{ formatFCFA(currentLiveResult) }}</span>
                                <span class="amount-label" v-if="currentLiveResult > 0">Montant brut estimé</span>
                            </div>

                            <div class="summary-details">
                                <h4>Résumé des indicateurs</h4>
                                <ul>
                                    <template v-if="selectedType.id === 'preavis'">
                                        <li><span>Durée du préavis légal :</span> <strong>{{ preavisResult.dureeText }}</strong></li>
                                        <li><span>Base mensuelle de calcul :</span> <strong>{{ formatFCFA(singleForm.salaire || 0) }}</strong></li>
                                    </template>
                                    <template v-if="selectedType.id === 'licenciement'">
                                        <li><span>Statut du dossier :</span> <strong>{{ multiForm.motif === 'faute' ? 'Non éligible' : 'Éligible' }}</strong></li>
                                        <li><span>Mode de calcul :</span> <strong>Tranches progressives</strong></li>
                                    </template>
                                </ul>
                            </div>

                            <div class="result-notice">
                                <p>Calcul effectué conformément au décret n° 96-202 et au Code du Travail de Côte d'Ivoire.</p>
                            </div>
                        </div>
                    </div>

                </div>
            </section>
          
        </main>
    </div>
     <Footer />
</template>

<script lang="ts">
import { ref, computed } from 'vue';
import Navbar from '../components/navigation/navbar.vue';
import Footer from '../components/sections/footerSection.vue';

export default {
    name: 'LawCalculPage',
    components: { Navbar, Footer },
    setup() {
        const selectedType = ref<any>(null);
        const multiStep = ref(1);

        // Données du formulaire étape unique (ex: préavis)
        const singleForm = ref({
            salaire: null as number | null,
            statut: 'ouvrier',
            ancienneteRange: '1_a_5'
        });

        // Données du formulaire multi-étapes (ex: licenciement complet)
        const multiForm = ref({
            motif: 'eco',
            salaire: null as number | null,
            annees: null as number | null
        });

        // Les différents simulateurs disponibles
        const simulationTypes = ref([
            {
                id: 'preavis',
                title: 'Indemnité de préavis',
                description: 'Calculez la durée légale du préavis et l\'indemnité compensatrice correspondante.',
                extendedDescription: 'Ce simulateur évalue la période de préavis obligatoire ou la compensation financière en cas de dispense, selon votre catégorie pro.',
                formLayout: 'single', // Formulaire en une étape
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>'
            },
            {
                id: 'licenciement',
                title: 'Indemnité globale de licenciement',
                description: 'Estimation complète de vos droits de fin de contrat avec application des tranches légales.',
                extendedDescription: 'Calculez l\'indemnité de licenciement légale due après au moins un an d\'ancienneté, hors faute lourde.',
                formLayout: 'multi', // Formulaire multi-étapes
                icon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line></svg>'
            }
        ]);

        const selectType = (type: any) => {
            selectedType.value = type;
            multiStep.value = 1;
        };

        const resetSelection = () => {
            selectedType.value = null;
        };

        // --- MOTEUR DE CALCULS JURIDIQUES COMPUTE (Live) ---

        // Logique Préavis (Étape unique)
        const preavisResult = computed(() => {
            const sal = singleForm.value.salaire || 0;
            const range = singleForm.value.ancienneteRange;
            const statut = singleForm.value.statut;
            let moisPreavis = 0;

            if (statut === 'ouvrier') {
                moisPreavis = range === 'moins_de_1' ? 1 : range === '1_a_5' ? 1 : 2;
            } else if (statut === 'tam') {
                moisPreavis = range === 'moins_de_1' ? 1 : range === '1_a_5' ? 2 : 3;
            } else if (statut === 'cadre') {
                moisPreavis = range === 'moins_de_1' ? 3 : range === '1_a_5' ? 3 : 4;
            }

            return {
                montant: moisPreavis * sal,
                dureeText: `${moisPreavis} mois`
            };
        });

        // Logique Licenciement global (Multi-étapes)
        const licenciementResult = computed(() => {
            if (multiForm.value.motif === 'faute') return 0;
            const sal = multiForm.value.salaire || 0;
            const annees = multiForm.value.annees || 0;
            let total = 0;

            // Barème officiel de Côte d'Ivoire
            const t1 = Math.min(annees, 5);
            total += t1 * 0.30 * sal;

            if (annees > 5) {
                const t2 = Math.min(annees - 5, 5);
                total += t2 * 0.35 * sal;
            }
            if (annees > 10) {
                const t3 = annees - 10;
                total += t3 * 0.40 * sal;
            }

            return total;
        });

        // Sortie unifiée pour le panneau de droite selon le contexte actif
        const currentLiveResult = computed(() => {
            if (!selectedType.value) return 0;
            if (selectedType.value.id === 'preavis') return preavisResult.value.montant;
            if (selectedType.value.id === 'licenciement') return licenciementResult.value;
            return 0;
        });

        const formatFCFA = (valeur: number) => {
            return new Intl.NumberFormat('fr-FR').format(Math.round(valeur)) + ' FCFA';
        };

        const calculerMulti = () => {
            alert(`Simulation enregistrée ! Montant calculé : ${formatFCFA(licenciementResult.value)}`);
        };

        return {
            selectedType,
            multiStep,
            simulationTypes,
            singleForm,
            multiForm,
            currentLiveResult,
            preavisResult,
            selectType,
            resetSelection,
            formatFCFA,
            calculerMulti
        };
    }
}
</script>

<style scoped>
/* --- MISE EN PAGE ET INTEGRATION D.A. --- */
.page-wrapper {
    background-color: #ffffff; /* Gris extérieur protecteur */
    padding: 3rem 1rem;
    min-height: 100vh;
    display: flex;
    justify-content: center;
}

.law-calcul-page {
    background-color: #ffffff; /* Page blanche épurée */
    width: 100%;
    max-width: 1200px;
    border-radius: 40px;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.05); /* Ombre douce de la D.A. */
    color: #0f172a;
    overflow: hidden;
    display: flex;
    flex-direction: column;
}

/* --- TEXTES & ACCENTS --- */
.muted-text { color: #64748b; }
.text-accent { color: #34d399; }

.pill-badge {
    display: inline-block;
    background-color: rgba(52, 211, 153, 0.1);
    color: #34d399;
    padding: 6px 18px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 1.5rem;
}

/* --- 1. HERO SECTION --- */
.hero-section {
    padding: 6rem 2rem 3rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
    border-bottom: 1px solid #f1f5f9;
}

.main-title {
    font-size: clamp(2.2rem, 4vw, 3.5rem);
    font-weight: 800;
    line-height: 1.15;
    margin: 0 0 1rem 0;
}

.hero-description {
    font-size: 1.1rem;
    line-height: 1.6;
    max-width: 700px;
}

/* --- 2. GRILLE DE SELECTION ÉTAPE 1 --- */
.selector-section {
    padding: 5rem 3rem;
}

.options-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
    gap: 2rem;
}

.option-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 20px;
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    cursor: pointer;
    transition: all 0.3s ease;
}

.option-card:hover {
    transform: translateY(-5px);
    border-color: #34d399;
    box-shadow: 0 15px 30px rgba(0,0,0,0.02);
}

.option-icon {
    width: 46px;
    height: 46px;
    color: #34d399;
    background: rgba(52, 211, 153, 0.1);
    padding: 10px;
    border-radius: 12px;
    margin-bottom: 1.5rem;
}

.option-card h3 {
    font-size: 1.3rem;
    font-weight: 700;
    margin: 0 0 0.8rem 0;
}

.option-card p {
    font-size: 0.95rem;
    line-height: 1.5;
    margin-bottom: 2rem;
    flex-grow: 1;
}

.action-link {
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.option-card:hover .action-link {
    color: #34d399;
}

/* --- 3. LOGIQUE DOUBLE COLONNE WORKSPACE --- */
.workspace-section {
    padding: 3rem;
    animation: fadeIn 0.4s ease;
}

.back-btn {
    background: none;
    border: none;
    color: #64748b;
    font-weight: 600;
    font-size: 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    cursor: pointer;
    padding: 0;
    margin-bottom: 2rem;
}

.back-btn:hover { color: #0f172a; }

.workspace-title-area {
    margin-bottom: 3rem;
}

.workspace-title-area h2 {
    font-size: 2rem;
    font-weight: 800;
    margin: 0 0 0.5rem 0;
}

/* Structure Master-Detail */
.calculator-layout {
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 3rem;
    align-items: start;
}

/* Formulaires Rentrée (Gauche) */
.form-pane {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 2.5rem;
    border-radius: 24px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-bottom: 1.5rem;
}

.form-group label {
    font-size: 0.9rem;
    font-weight: 700;
    color: #334155;
}

.clean-input {
    width: 100%;
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 1rem;
    color: #0f172a;
    font-size: 1rem;
    box-sizing: border-box;
    transition: all 0.2s ease;
}

.clean-input:focus {
    outline: none;
    border-color: #34d399;
    box-shadow: 0 0 0 4px rgba(52, 211, 153, 0.1);
}

select.custom-select {
    appearance: none;
    background-image: url("data:image/svg+xml;charset=US-ASCII,%3Csvg%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20width%3D%2224%22%20height%3D%2224%22%20fill%3D%22none%22%20stroke%3D%22%2364748b%22%20stroke-width%3D%222%22%3E%3Cpolyline%20points%3D%226%209%2012%2015%2018%209%22%3E%3C%2Fpolyline%3E%3C%2Fsvg%3E");
    background-repeat: no-repeat;
    background-position: right 1rem center;
    background-size: 1.2rem;
}

/* Progression multi-étapes */
.steps-indicator {
    display: flex;
    gap: 1.5rem;
    border-bottom: 1px solid #e2e8f0;
    padding-bottom: 1rem;
    margin-bottom: 2rem;
}

.steps-indicator span {
    font-size: 0.85rem;
    font-weight: 700;
    color: #94a3b8;
}

.steps-indicator span.is-active {
    color: #34d399;
}

/* Panneau Résultat Flottant (Droite) */
.result-pane {
    position: sticky;
    top: 100px; /* S'accroche lors du défilement */
}

.result-sticky-card {
    background-color: #0f172a; /* Contraste sombre chic */
    color: #ffffff;
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.result-sticky-card h3 {
    margin: 0 0 2rem 0;
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: #94a3b8;
    font-weight: 600;
}

.amount-display {
    margin-bottom: 2.5rem;
}

.amount-number {
    font-size: clamp(2.2rem, 3vw, 3rem);
    font-weight: 800;
    color: #34d399;
    display: block;
    line-height: 1;
}

.amount-label {
    font-size: 0.85rem;
    color: #64748b;
    margin-top: 0.5rem;
    display: block;
}

.summary-details h4 {
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #94a3b8;
    margin: 0 0 1rem 0;
}

.summary-details ul {
    list-style: none;
    padding: 0;
    margin: 0 0 2.5rem 0;
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

.summary-details li {
    display: flex;
    justify-content: space-between;
    font-size: 0.9rem;
    border-bottom: 1px dashed rgba(255, 255, 255, 0.08);
    padding-bottom: 0.6rem;
}

.summary-details li span { color: #94a3b8; }

.result-notice {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    padding: 1rem;
    border-radius: 12px;
}

.result-notice p {
    font-size: 0.75rem;
    color: #64748b;
    margin: 0;
    line-height: 1.4;
}

/* Boutons standardisés */
.btn-primary {
    background-color: #34d399;
    color: #0f172a;
    font-weight: 700;
    padding: 1rem 2rem;
    border-radius: 12px;
    border: none;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.btn-outline {
    background-color: transparent;
    color: #ffffff;
    font-weight: 600;
    padding: 1rem 2rem;
    border-radius: 12px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
}

.btn-primary:hover, .btn-outline:hover {
    transform: translateY(-2px);
}

.mt-4 { margin-top: 1rem; }
.form-actions { display: flex; gap: 1rem; }

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(8px); }
    to { opacity: 1; transform: translateY(0); }
}

/* --- RESPONSIVE --- */
@media (max-width: 960px) {
    .calculator-layout {
        grid-template-columns: 1fr; /* Passage sur une colonne sur tablette/mobile */
        gap: 2rem;
    }
    .workspace-section { padding: 1.5rem; }
    .selector-section { padding: 3rem 1.5rem; }
}
</style>