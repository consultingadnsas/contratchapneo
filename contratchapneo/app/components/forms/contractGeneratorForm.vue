<template>
    
    <form @submit.prevent="submitForm" class="contrat-form">
    
        <div v-if="store.isLoading" class="loading-state">
          <p>Analyse du document et extraction des balises en cours...</p>
        </div>

        <div v-else-if="store.error" class="error-state">
            <p>🚨 Erreur : {{ store.error }}</p>
        </div>

        <div v-else-if="store.tags && store.tags.length > 0" class="contract-prev-form">
        
          <BaseInputContract
            v-for="tag in store.tags"
            :key="tag"
            v-model="formData[tag]"
            :label="formatLabel(tag)"
            :type="getInputType(tag)"
            :placeholder="'Entrez : ' + formatLabel(tag).toLowerCase()"
            :disabled="store.isLoading"
          />

          <button type="submit" class="submit-btn" :disabled="store.isLoading">
            Valider les informations
          </button>
        </div>

        <div v-else>
          <p>Ce contrat ne nécessite aucune information à remplir.</p>
        </div>
    
    </form>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import BaseInput from '../input/BaseInput.vue'
import { useContratStore } from '../../stores/contratStore' // Correction du nom d'import
import {useRoute} from 'vue-router'
import BaseInputContract from '../input/BaseInputContract.vue'

// 1. Définition des Props (on a besoin de l'ID du contrat pour chercher ses tags)


// 2. Définition des événements (pour envoyer les réponses au parent)
const emit = defineEmits(['submit-data'])

// 3. Initialisation du store et de l'objet de données
const store = useContratStore()
const formData = ref({}) // Va contenir les valeurs tapées par l'utilisateur (ex: { nom_client: "Jean", montant: 5000 })
const route = useRoute() // On initialise le routeur pour lire l'URL
// 4. Initialisation : Récupérer les tags au montage du composant
onMounted(async () => {
  try {

    if (!store.currentContratId){
      console.log('Id déterminé au montage', store.currentContratId)
      return
    }
    // On appelle l'action de ton store Pinia
    await store.fetchContractTags(store.currentContratId)

    // On pré-remplit l'objet formData avec des chaînes vides pour chaque tag
    if (store.tags && store.tags.length > 0) {
      store.tags.forEach(tag => {
      formData.value[tag] = ''
      })
    }
  } catch {
    console.log("Erreur lors du montage du composant")
  }
})

// --- FONCTIONS UTILITAIRES (L'astuce UX de Contratchap !) ---

// Rend le nom de la balise propre pour l'affichage (ex: "nom_client" -> "Nom client")
const formatLabel = (tag) => {
  return tag.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())
}

// Détermine le type de champ HTML en fonction du préfixe de la balise
const getInputType = (tag) => {
  if (tag.startsWith('date_')) return 'date'
  if (tag.startsWith('num_')) return 'number'
  if (tag.startsWith('email_')) return 'email'
  return 'text' // Par défaut, c'est du texte
}

// --- SOUMISSION ---
const submitForm = () => {
  console.log("Données prêtes à être envoyées :", formData.value)
  // On envoie le dictionnaire rempli au composant parent (la page)
  // pour qu'il lance l'appel API de génération du PDF final !
  emit('submit-data', formData.value)
}
</script>

<style scoped>
.contrat-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  max-width: 600px;
  margin: 0 auto;
}

.contract-prev-form{
  width: 100%;
}

.loading-state, .error-state {
  padding: 1rem;
  border-radius: 8px;
  text-align: center;
}
.error-state {
  background-color: #ffebee;
  color: #c62828;
}
.submit-btn {
  padding: 0.75rem 1.5rem;
  background-color: #202b4a; /* Les couleurs Contratchap ! */
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: bold;
}
.submit-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}
</style>