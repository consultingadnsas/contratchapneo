<template>
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

                <!-- ZONE D'UPLOAD MULTIPLE -->
                <div class="form-group custom-upload-group">
                    <label class="custom-label">Vos documents (Max : 5) <span class="required-mark">*</span></label>
                    
                    <div class="file-upload-container" :class="{ 'has-file': selectedFiles.length > 0 }">
                        <input 
                            type="file" 
                            id="file-upload" 
                            @change="handleFileUpload" 
                            accept=".pdf, .doc, .docx, application/msword, application/vnd.openxmlformats-officedocument.wordprocessingml.document" 
                            multiple
                            class="file-input-hidden"
                            :disabled="selectedFiles.length >= 5"
                        />
                        <label for="file-upload" class="file-upload-label" :class="{ 'disabled': selectedFiles.length >= 5 }">
                            <div class="upload-icon">
                                <svg v-if="selectedFiles.length === 0" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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
                            <span v-if="selectedFiles.length === 0" class="upload-text">Cliquez pour choisir vos fichiers</span>
                            <span v-else-if="selectedFiles.length < 5" class="upload-text">Ajouter un autre fichier ({{ selectedFiles.length }}/5)</span>
                            <span v-else class="upload-text">Limite de 5 fichiers atteinte</span>
                        </label>
                    </div>

                    <!-- Affichage de la liste des fichiers sélectionnés -->
                    <ul v-if="selectedFiles.length > 0" class="selected-files-list">
                        <li v-for="(file, index) in selectedFiles" :key="index" class="file-item">
                            <span class="file-name" :title="file.name">{{ file.name }}</span>
                            <button type="button" class="remove-file-btn" @click="removeFile(index)" aria-label="Retirer ce fichier">
                                &times;
                            </button>
                        </li>
                    </ul>

                    <small class="file-hint">Taille maximale : 10 Mo par fichier. Formats acceptés : .pdf, .docx</small>
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
</template>

<script lang="ts">
import { ref } from 'vue';
import BaseInput from '../../input/BaseInput.vue';
import BaseSelect from '../../input/BaseSelect.vue';
import BaseArea from '../../input/BaseArea.vue';
import formButton from '../../buttons/formButton.vue';

export default {
    name: 'EtudeContratRight',
    components: {
        BaseInput,
        BaseSelect,
        BaseArea,
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

        // Remplacement de `selectedFile` par un tableau de fichiers
        const selectedFiles = ref<File[]>([]);
        
        const isSubmitting = ref<boolean>(false);
        const successMessage = ref<string>('');
        const errorMessage = ref<string>('');

        const handleFileUpload = (event: Event) => {
            const target = event.target as HTMLInputElement;
            if (target.files && target.files.length > 0) {
                
                const newFiles = Array.from(target.files);
                
                // 1. Vérifier si on dépasse la limite globale de 5 fichiers
                if (selectedFiles.value.length + newFiles.length > 5) {
                    errorMessage.value = `Vous ne pouvez sélectionner que 5 fichiers maximum. Il vous reste ${5 - selectedFiles.value.length} place(s).`;
                    target.value = ''; // Réinitialiser l'input
                    return;
                }

                // 2. Traiter chaque nouveau fichier
                let hasSizeError = false;

                newFiles.forEach(file => {
                    if (file.size > 10 * 1024 * 1024) {
                        hasSizeError = true;
                    } else {
                        // On évite d'ajouter le même fichier deux fois (optionnel mais propre)
                        const isDuplicate = selectedFiles.value.some(f => f.name === file.name && f.size === file.size);
                        if (!isDuplicate) {
                            selectedFiles.value.push(file);
                        }
                    }
                });

                if (hasSizeError) {
                    errorMessage.value = "Certains fichiers ont été ignorés car ils dépassent 10 Mo.";
                } else {
                    errorMessage.value = ''; 
                }

                target.value = ''; // Reset de l'input pour pouvoir resélectionner le même fichier si on l'a supprimé entre temps
            }
        };

        const removeFile = (index: number) => {
            selectedFiles.value.splice(index, 1);
            if (selectedFiles.value.length === 0) {
                errorMessage.value = ''; // On vide l'erreur s'il n'y a plus de fichiers
            }
        };

        const handleSubmit = async () => {
            if (selectedFiles.value.length === 0) {
                errorMessage.value = "Veuillez joindre au moins un document à analyser.";
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
                
                // 🪄 NOUVEAU : On ajoute tous les fichiers à la même clé 'documents'
                selectedFiles.value.forEach((file) => {
                    payload.append('documents', file);
                });

                // Simulation API
                await new Promise(resolve => setTimeout(resolve, 1500)); 

                successMessage.value = "Votre demande a été envoyée avec succès ! Nos experts vous contacteront rapidement.";
                
                // Reset form
                formData.value = { name: '', email: '', type: '', description: '', phonePrefix: '+225', phoneNumber: '' };
                selectedFiles.value = [];

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
            selectedFiles,
            isSubmitting,
            successMessage,
            errorMessage,
            handleFileUpload,
            removeFile,
            handleSubmit
        };
    }
};
</script>

<style scoped>
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

.file-upload-label:hover:not(.disabled) {
    background: rgba(50, 244, 89, 0.05);
    border-color: rgba(50, 244, 89, 0.4);
}

.file-upload-label.disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

.has-file .file-upload-label {
    background: rgba(50, 244, 89, 0.05);
    border-color: #32f459;
    border-style: solid;
}

.upload-icon {
    color: #a0aec0;
    transition: color 0.3s ease;
}

.file-upload-label:hover:not(.disabled) .upload-icon {
    color: #32f459;
}

.upload-text {
    font-size: 0.95rem;
    color: #e2e8f0;
    font-weight: 500;
}

.file-hint {
    font-size: 0.8rem;
    color: #718096;
    margin-top: 0.5rem;
    margin-left: 0.4rem;
}

/* ── Liste des fichiers sélectionnés ── */
.selected-files-list {
    list-style: none;
    padding: 0;
    margin: 0.8rem 0 0 0;
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.file-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.6rem 1rem;
    border-radius: 10px;
    transition: background 0.2s;
}

.file-item:hover {
    background: rgba(255, 255, 255, 0.08);
}

.file-name {
    font-size: 0.85rem;
    color: #32f459;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 85%;
}

.remove-file-btn {
    background: transparent;
    border: none;
    color: #fca5a5;
    font-size: 1.4rem;
    line-height: 1;
    cursor: pointer;
    padding: 0 0.5rem;
    transition: color 0.2s ease, transform 0.2s ease;
}

.remove-file-btn:hover {
    color: #ef4444;
    transform: scale(1.1);
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
    .right-panel {
        justify-content: center;
        width: 100%;
    }
}

@media (max-width: 480px) {
    .form-wrapper {
        padding: 1.5rem;
    }
    .file-upload-label {
        padding: 1.5rem 1rem;
    }
}
</style>