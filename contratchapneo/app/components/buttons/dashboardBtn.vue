<template>
    <div class="profile-wrapper" ref="wrapperRef">
          <button class="profile-button" @click="toggleDropdown">
            
            <!-- ⚡️ NOUVELLE ICÔNE (Avec la classe icon-size pour garder les bonnes proportions) -->
            <img 
              class="icon-size" 
              src="https://img.icons8.com/arcade/64/coins--v1.png" 
              alt="coins--v1"
            />
            
            <!-- ⚡️ Les crédits s'affichent dynamiquement -->
            <span class="credits-text">{{ activeCredits }} Crédits</span>
          </button>

          <Transition name="fade">
            <div v-if="isOpen" class="dropdown">
              <ul class="dropdown-menu">
                
                <li>
                    <span class="menu-item">
                        <small>Contrats standards</small>
                        <strong>{{ activeCredits }} restants</strong>
                    </span>
                </li>

                <li>
                    <span class="menu-item">
                        <small>Contrats sur mesure</small>
                        <strong>{{ activeCustoms }} restants</strong>
                    </span>
                </li>
                
                <li>
                    <span class="menu-item">
                        <small>Statut du pack</small>
                        <!-- ⚡️ Pastille de couleur selon le statut -->
                        <span :class="['status-badge', activePack ? 'active' : 'inactive']">
                            {{ activePack ? 'Actif' : 'Aucun pack actif' }}
                        </span>
                    </span>
                </li>

                <li v-if="activePack?.date_expiration">
                    <span class="menu-item">
                        <small>Date d'expiration</small>
                        <strong>{{ formattedExpirationDate }}</strong>
                    </span>
                </li>

              </ul>
            </div>
          </Transition>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useProfileStore } from '~/stores/profileStore' // Vérifie que ce chemin est correct

// 1. Initialisation du store
const profileStore = useProfileStore()

// 2. Récupération dynamique du pack actif
// On cherche dans userPacks le premier pack qui a isActive = true
const activePack = computed(() => {
    // ⚡️ CORRECTION : On cherche "is_active" (Django) 
    return profileStore.userPacks.find(pack => pack.is_active === true) || null
})

// 3. Calculs des valeurs à afficher
const activeCredits = computed(() => activePack.value?.credits_restants || 0)
const activeCustoms = computed(() => activePack.value?.customs_restants || 0)

// 4. Formatage propre de la date (ex: 24 Oct 2024)
const formattedExpirationDate = computed(() => {
    if (!activePack.value?.date_expiration) return 'N/A'
    const date = new Date(activePack.value.date_expiration)
    return date.toLocaleDateString('fr-FR', { 
        day: 'numeric', 
        month: 'short', 
        year: 'numeric' 
    })
})

// === LOGIQUE DE LA MODALE DU BOUTON ===
const isOpen = ref(false)
const wrapperRef = ref(null)

const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const handleClickOutside = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  // Optionnel : Si tes packs ne sont pas encore chargés au moment où ce composant s'affiche
  if (profileStore.userPacks.length === 0) {
      profileStore.getPacks();
  }
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.profile-wrapper {
  position: relative;
  display: inline-block;
}

.profile-button {
  background-color: #000e2ddd;
  display: flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  gap: 0.5rem;
  border: none;
  border-radius: 8px; 
  cursor: pointer;
  color: #ffffff;
  padding: 0.6rem 1.2rem; 
  transition: 0.4s;
}

.profile-button:hover {
  transform: translateY(-2px);
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.icon-size {
  width: 22px;
  height: 22px;
}

.credits-text {
  font-size: 0.95rem;
  font-weight: 600;
  white-space: nowrap;
}

.dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 220px; /* Un peu plus large pour afficher les infos proprement */
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  border: 1px solid #eaeaea;
  z-index: 1000;
  overflow: hidden;
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu li {
  border-bottom: 1px solid #f0f0f0;
}

.dropdown-menu li:last-child {
  border-bottom: none;
}

.menu-item {
  display: flex;
  flex-direction: column;
  padding: 12px 16px;
  color: #333;
  text-align: left;
}

.menu-item small {
    color: #6b7280;
    font-size: 0.75rem;
    margin-bottom: 4px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.menu-item strong {
    font-size: 0.95rem;
    color: #111827;
}

/* ⚡️ STYLE DU STATUT DYNAMIQUE */
.status-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 50px;
    font-size: 0.8rem;
    font-weight: 600;
    width: fit-content;
}

.status-badge.active {
    background-color: #d1fae5;
    color: #065f46;
}

.status-badge.inactive {
    background-color: #fee2e2;
    color: #991b1b;
}

/* Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>