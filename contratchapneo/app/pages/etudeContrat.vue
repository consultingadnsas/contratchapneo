<template>
    <section class="study-section">
        <navbar/>
        <div class="bg-huge-text">CONTRAT</div>

        <div class="contact-container">
            
            <div class="left-panel">

                <h1>Faites analyser <span>votre contrat</span></h1>
                <p>Confiez vos documents à nos experts juridiques en vue d'une révision complète, confidentielle et sécurisée pour la protection de vos intérêts.</p>

                <div class="info-cards-container">
                    <div class="info-card">
                        <div class="icon-box">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
                        </div>
                        <div class="info-texts">
                            <h4>Expertise OHADA</h4>
                            <span>Avocats et juristes qualifiés</span>
                        </div>
                    </div>

                    <div class="info-card">
                        <div class="icon-box">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                        </div>
                        <div class="info-texts">
                            <h4>Confidentialité absolue</h4>
                            <span>Vos données sont chiffrées</span>
                        </div>
                    </div>

                    <div class="info-card">
                        <div class="icon-box">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
                        </div>
                        <div class="info-texts">
                            <h4>Réponse rapide</h4>
                            <span>Sous 48h à 72h ouvrées</span>
                        </div>
                    </div>
                </div>
            </div>

            <div class="right-panel">
                <div class="form-wrapper">
                    <form @submit.prevent="handleSubmit" class="study-form">
                        
                        <BaseInput
                            v-model="formData.name"
                            id="name"
                            label="Nom complet"
                            placeholder="Ex: Yvan Pascal..."
                            required
                        />

                        <BaseInput
                            v-model="formData.email"
                            id="email"
                            type="email"
                            label="Adresse e-mail"
                            placeholder="votre.email@exemple.com"
                            required
                        />

                        <div class="custom-input-group">
                            <label class="custom-label">Numéro de téléphone <span class="required-mark">*</span></label>
                            <div class="phone-inputs">
                                <BaseSelect
                                    v-model="formData.phonePrefix"
                                    id="phonePrefix"
                                    :options="ohadaCountries"
                                    placeholder="Ind."
                                    class="prefix-select"
                                />
                                <BaseInput
                                    v-model="formData.phoneNumber"
                                    id="phoneNumber"
                                    type="tel"
                                    placeholder="01 23 45 67 89"
                                    required
                                    class="number-input"
                                />
                            </div>
                        </div>

                        <BaseArea
                            v-model="formData.description"
                            id="description"
                            label="Message / Contexte"
                            placeholder="Décrivez brièvement votre besoin (ex: Vérification des clauses de confidentialité...)"
                            rows="4"
                            required
                        />

                        <div class="form-group custom-upload-group">
                            <label class="custom-label">Votre document (PDF ou Word) <span class="required-mark">*</span></label>
                            <div class="file-upload-container" :class="{ 'has-file': selectedFile }">
                                <input 
                                    type="file" 
                                    id="file-upload" 
                                    @change="handleFileUpload" 
                                    accept=".pdf, .doc, .docx, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
                                    required 
                                    class="file-input-hidden"
                                />
                                <label for="file-upload" class="file-upload-label">
                                    <div class="upload-icon">
                                        <svg v-if="!selectedFile" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                                            <polyline points="17 8 12 3 7 8"></polyline>
                                            <line x1="12" y1="3" x2="12" y2="15"></line>
                                        </svg>
                                        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#32f459" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                                            <polyline points="14 2 14 8 20 8"></polyline>
                                            <line x1="16" y1="13" x2="8" y2="13"></line>
                                            <line x1="16" y1="17" x2="8" y2="17"></line>
                                            <polyline points="10 9 9 9 8 9"></polyline>
                                        </svg>
                                    </div>
                                    <span v-if="!selectedFile" class="upload-text">Cliquez pour choisir un fichier</span>
                                    <span v-else class="upload-text file-name">{{ selectedFile.name }}</span>
                                </label>
                            </div>
                            <small class="file-hint">Taille maximale : 10 Mo. Formats acceptés : .pdf, .docx</small>
                        </div>

                        <div v-if="successMessage" class="alert success">{{ successMessage }}</div>
                        <div v-if="errorMessage" class="alert error">{{ errorMessage }}</div>

                        <form-button
                            label="Envoyer la demande"
                            :isLoading="isSubmitting"
                            type="submit"
                            class="submit-btn"
                        />
                    </form>
                </div>
            </div>
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import BaseInput from '../components/input/BaseInput.vue';
import BaseSelect from '../components/input/BaseSelect.vue';
import BaseArea from '../components/input/BaseArea.vue';
import navbar from '../components/navigation/navbar.vue';
import formButton from '../components/buttons/formButton.vue';

export default {
    name: 'EtudeContratPage',
    components: {
        BaseInput,
        BaseSelect,
        BaseArea,
        navbar,
        formButton
    },
    setup() {
        const formData = ref({
            name: '',
            email: '',
            type: '',
            description: '',
            phonePrefix: '+225',
            phoneNumber: ''
        });

        const ohadaCountries = [
            { name: "🇨🇮 (+225)", value: "+225" },
            { name: "🇸🇳 (+221)", value: "+221" },
            { name: "🇲🇱 (+223)", value: "+223" },
            { name: "🇧🇫 (+226)", value: "+226" },
            { name: "🇹🇬 (+228)", value: "+228" },
            { name: "🇧🇯 (+229)", value: "+229" },
            { name: "🇳🇪 (+227)", value: "+227" },
            { name: "🇬🇼 (+245)", value: "+245" }
        ];

        const selectedFile = ref<File | null>(null);
        
        const isSubmitting = ref<boolean>(false);
        const successMessage = ref<string>('');
        const errorMessage = ref<string>('');

        const handleFileUpload = (event: Event) => {
            const target = event.target as HTMLInputElement;
            if (target.files && target.files.length > 0) {
                const file = target.files[0];
                
                if (file.size > 10 * 1024 * 1024) {
                    errorMessage.value = "Le fichier est trop volumineux (Max: 10 Mo).";
                    selectedFile.value = null;
                    target.value = ''; 
                    return;
                }

                selectedFile.value = file;
                errorMessage.value = ''; 
            }
        };

        const handleSubmit = async () => {
            if (!selectedFile.value) {
                errorMessage.value = "Veuillez joindre un document à analyser.";
                return;
            }

            isSubmitting.value = true;
            errorMessage.value = '';
            successMessage.value = '';

            try {
                const payload = new FormData();
                payload.append('name', formData.value.name);
                payload.append('email', formData.value.email);
                payload.append('phone', `${formData.value.phonePrefix} ${formData.value.phoneNumber}`);
                payload.append('description', formData.value.description);
                payload.append('document', selectedFile.value);

                // Simulation API
                await new Promise(resolve => setTimeout(resolve, 1500)); 

                successMessage.value = "Votre demande a été envoyée avec succès ! Nos experts vous contacteront rapidement.";
                
                // Reset form
                formData.value = { name: '', email: '', type: '', description: '', phonePrefix: '+225', phoneNumber: '' };
                selectedFile.value = null;
                
                const fileInput = document.getElementById('file-upload') as HTMLInputElement;
                if (fileInput) fileInput.value = '';

            } catch (error) {
                errorMessage.value = "Une erreur est survenue lors de l'envoi. Veuillez réessayer.";
                console.error(error);
            } finally {
                isSubmitting.value = false;
            }
        };

        return {
            formData,
            ohadaCountries,
            selectedFile,
            isSubmitting,
            successMessage,
            errorMessage,
            handleFileUpload,
            handleSubmit
        };
    }
};
</script>

<style scoped>
/* ── Container Principal ── */
.study-section {
    position: relative;
    width: 100%;
    min-height: 100vh;
    padding: 8rem 2rem 4rem 2rem;
    background: radial-gradient(circle at center, #202b4a 0%, #0f0f0f 100%);
    color: var(--my-white, #ffffff);
    overflow-x: hidden;
    display: flex;
    justify-content: center;
}

/* ── Le grand texte en filigrane (façon "CONTACT" dans l'image) ── */
.bg-huge-text {
    position: absolute;
    top: 15%;
    left: 50%;
    transform: translateX(-50%);
    font-size: 18vw;
    font-weight: 900;
    color: rgba(255, 255, 255, 0.053);
    z-index: 0;
    pointer-events: none;
    user-select: none;
    letter-spacing: 0.05em;
    font-family: Zalando Sans SemiExpanded, sans-serif;
}

/* ── Conteneur du Layout en 2 colonnes ── */
.contact-container {
    display: flex;
    gap: 4rem;
    max-width: 1200px;
    width: 100%;
    z-index: 2;
    position: relative;
    align-items: flex-start;
}

/* ── COLONNE GAUCHE ── */
.left-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding-top: 2rem;
}

.left-panel h1 {
    font-size: clamp(3rem, 4.5vw, 4rem);
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 1rem;
    color: #ffffff;
}

.left-panel span{
    color: var(--primary-color)
}

.left-panel p {
    font-size: 1.15rem;
    color: #a0aec0;
    line-height: 1.6;
    margin-bottom: 3rem;
    max-width: 90%;
}

/* Les 3 cartes d'information */
.info-cards-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.info-card {
    display: flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 1rem 1.2rem;
    border-radius: 16px;
    transition: all 0.3s ease;
    cursor: default;
}

.icon-box {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 45px;
    height: 45px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    margin-right: 1.2rem;
    color: #a0aec0;
    flex-shrink: 0;
}

.info-card:hover .icon-box {
    color: #32f459;
}

.info-texts {
    flex: 1;
    display: flex;
    flex-direction: column;
}

.info-texts h4 {
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
}

.info-texts span {
    font-size: 0.85rem;
    color: #718096;
    margin-top: 0.2rem;
}

/* ── COLONNE DROITE (Formulaire) ── */
.right-panel {
    flex: 1.2;
    display: flex;
    justify-content: flex-end;
}

.form-wrapper {
    width: 100%;
    max-width: 600px;
    background: rgba(255, 255, 255, 0.02);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.5rem;
    box-shadow: 0 30px 60px rgba(0, 0, 0, 0.3);
}

.study-form {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

/* ── SURCHARGE DES COMPOSANTS BASE (Glassmorphism) ── */
:deep(.form-input),
:deep(.form-textarea),
:deep(.form-select) {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 1.1rem 1.2rem !important;
    font-size: 0.95rem !important;
}

:deep(.form-input:focus),
:deep(.form-textarea:focus),
:deep(.form-select:focus) {
    border-color: #32f459 !important;
    box-shadow: 0 0 0 3px rgba(50, 244, 89, 0.1) !important;
    background-color: rgba(0, 0, 0, 0.3) !important;
}

:deep(.input-label) {
    color: #e2e8f0 !important;
    margin-left: 0.4rem !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

:deep(.form-select) {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
}

/* ── Zone d'Upload Personnalisée ── */
.custom-upload-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.5rem;
    margin-top: 0.5rem;
}

.custom-label {
    font-size: 0.9rem;
    font-weight: 500;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
    margin-left: 0.4rem;
}

.required-mark {
    color: #ef4444;
    margin-left: 2px;
}

.file-upload-container {
    position: relative;
    width: 100%;
}

.file-input-hidden {
    position: absolute;
    width: 0;
    height: 0;
    opacity: 0;
    overflow: hidden;
    z-index: -1;
}

.file-upload-label {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    padding: 2rem;
    background: rgba(255, 255, 255, 0.02);
    border: 2px dashed rgba(255, 255, 255, 0.15);
    border-radius: 14px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.file-upload-label:hover {
    background: rgba(50, 244, 89, 0.05);
    border-color: rgba(50, 244, 89, 0.4);
}

.has-file .file-upload-label {
    background: rgba(50, 244, 89, 0.1);
    border-color: #32f459;
    border-style: solid;
}

.upload-icon {
    color: #a0aec0;
    transition: color 0.3s ease;
}

.file-upload-label:hover .upload-icon {
    color: #32f459;
}

.upload-text {
    font-size: 0.95rem;
    color: #e2e8f0;
    font-weight: 500;
}

.file-name {
    color: #32f459;
    word-break: break-all;
}

.file-hint {
    font-size: 0.8rem;
    color: #718096;
    margin-top: 0.5rem;
    margin-left: 0.4rem;
}

/* ── Champs Téléphone (Alignement) ── */
.custom-input-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.2rem;
    width: 100%;
}

.phone-inputs {
    display: flex;
    gap: 0.8rem;
    align-items: flex-start;
}

.prefix-select {
    flex: 0 0 35%;
    margin-bottom: 0 !important;
}

.number-input {
    flex: 1;
    margin-bottom: 0 !important;
}

:deep(.prefix-select .form-select) {
    padding-left: 1rem !important;
    padding-right: 2rem !important;
}

/* ── Alertes ── */
.alert {
    padding: 1rem;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
    margin-top: 0.5rem;
}

.alert.error {
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.alert.success {
    background: rgba(50, 244, 89, 0.1);
    color: #32f459;
    border: 1px solid rgba(50, 244, 89, 0.3);
}

:deep(.submit-btn:hover:not(:disabled)) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(255, 255, 255, 0.2);
}


/* ── Reponsive Mobile & Tablette ── */
@media (max-width: 992px) {
    .contact-container {
        flex-direction: column;
        gap: 3rem;
    }
    .left-panel {
        padding-top: 0;
        align-items: center;
        text-align: center;
    }
    .left-panel p {
        margin-bottom: 2rem;
    }
    .info-cards-container {
        width: 100%;
        max-width: 500px;
    }
    .right-panel {
        justify-content: center;
        width: 100%;
    }
}

@media (max-width: 480px) {
    .study-section {
        padding: 6rem 1rem 3rem 1rem;
    }
    .form-wrapper {
        padding: 1.5rem;
    }
    .file-upload-label {
        padding: 1.5rem 1rem;
    }
    .bg-huge-text {
        font-size: 20vw;
        top: 10%;
    }
}
</style>