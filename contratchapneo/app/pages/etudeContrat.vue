<template>
    <section class="study-section">
        <div class="bg-shape shape-bottom-right"></div>
        <div class="bg-shape shape-top-left"></div>

        <div class="study-header">
            <h1>Faites analyser votre contrat</h1>
            <p>Confiez vos documents à nos experts juridiques OHADA pour une révision complète, confidentielle et sécurisée.</p>
        </div>

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

                <BaseSelect
                    v-model="formData.type"
                    id="type"
                    label="Catégorie du contrat"
                    placeholder="Sélectionnez le type de contrat"
                    required
                />

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

                <button type="submit" class="submit-btn" :disabled="isSubmitting">
                    <span v-if="!isSubmitting">Envoyer la demande</span>
                    <span v-else>Envoi en cours...</span>
                </button>
            </form>
        </div>
    </section>
</template>

<script lang="ts">
import { ref } from 'vue';
import BaseInput from '../components/input/BaseInput.vue';
import BaseSelect from '../components/input/BaseSelect.vue';
import BaseArea from '../components/input/BaseArea.vue';

export default {
    name: 'EtudeContratPage',
    components: {
        BaseInput,
        BaseSelect,
        BaseArea
    },
    setup() {
        const formData = ref({
            name: '',
            email: '',
            type: '',
            description: ''
        });

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
                payload.append('type', formData.value.type);
                payload.append('description', formData.value.description);
                payload.append('document', selectedFile.value);

                // Simulation API
                await new Promise(resolve => setTimeout(resolve, 1500)); 

                successMessage.value = "Votre demande a été envoyée avec succès ! Nos experts vous contacteront rapidement.";
                
                // Reset form
                formData.value = { name: '', email: '', type: '', description: '' };
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
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 8rem 1rem 4rem 1rem;
    background: radial-gradient(circle, #202b4a 30%, #0f0f0f 100%);
    color: var(--my-white, #ffffff);
    overflow-x: hidden;
}

.study-header {
    text-align: center;
    max-width: 600px;
    margin-bottom: 3rem;
    z-index: 2;
}

.study-header h1 {
    font-size: clamp(2rem, 5vw, 3rem);
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--my-white, #ffffff);
}

.study-header p {
    font-size: clamp(1rem, 2vw, 1.15rem);
    color: #a0aec0;
    line-height: 1.6;
}

/* ── Conteneur du formulaire (Glassmorphism) ── */
.form-wrapper {
    width: 100%;
    max-width: 650px;
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 2.5rem;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
    z-index: 2;
}

.study-form {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

/* ── SURCHARGE DES COMPOSANTS BASE (Glassmorphism) ── */
:deep(.form-input),
:deep(.form-textarea),
:deep(.form-select) {
    background-color: rgba(0, 0, 0, 0.2) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: white !important;
    border-radius: 12px !important;
    padding: 1rem 1.2rem !important;
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
    margin-left: 0.2rem !important;
    font-size: 0.95rem !important;
}

/* Adapter l'icône de la flèche du Select pour fond sombre */
:deep(.form-select) {
    background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23ffffff' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e") !important;
}

/* ── Zone d'Upload Personnalisée ── */
.custom-upload-group {
    display: flex;
    flex-direction: column;
    margin-bottom: 0.5rem;
}

.custom-label {
    font-size: 0.95rem;
    font-weight: 500;
    color: #e2e8f0;
    margin-bottom: 0.5rem;
    margin-left: 0.2rem;
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
    padding: 2.5rem 2rem;
    background: rgba(50, 244, 89, 0.05);
    border: 2px dashed rgba(50, 244, 89, 0.3);
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-align: center;
}

.file-upload-label:hover {
    background: rgba(50, 244, 89, 0.1);
    border-color: #32f459;
}

.has-file .file-upload-label {
    background: rgba(50, 244, 89, 0.15);
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
    font-size: 1rem;
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
    margin-left: 0.2rem;
}

/* ── Alertes ── */
.alert {
    padding: 1rem;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 500;
    text-align: center;
    margin-top: 1rem;
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

/* ── Bouton Soumettre ── */
.submit-btn {
    width: 100%;
    padding: 1.1rem;
    background: #32f459;
    color: #0f0f0f;
    border: none;
    border-radius: 12px;
    font-size: 1.05rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-top: 1rem;
}

.submit-btn:hover:not(:disabled) {
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(50, 244, 89, 0.2);
}

.submit-btn:disabled {
    background: #4a5568;
    color: #a0aec0;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
}

/* ── Décorations de fond ── */
.bg-shape {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    z-index: 1;
    opacity: 0.5;
}

.shape-top-left {
    top: -10%;
    left: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, #32f459 0%, transparent 70%);
}

.shape-bottom-right {
    bottom: -10%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, #068cec 0%, transparent 70%);
}

/* ── Reponsive Mobile ── */
@media (max-width: 768px) {
    .study-section {
        padding: 6rem 1rem 3rem 1rem;
    }
    .form-wrapper {
        padding: 1.5rem;
    }
    .file-upload-label {
        padding: 1.5rem 1rem;
    }
}
</style>