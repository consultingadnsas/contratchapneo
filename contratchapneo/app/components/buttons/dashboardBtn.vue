<template>
    <div class="profile-wrapper" ref="wrapperRef">
          <button class="profile-button" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="icon-size">
              <path d="M12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12C22 17.5228 17.5228 22 12 22ZM12 6.5L7.5 11V13L12 17.5L16.5 13V11L12 6.5Z"></path>
            </svg>
            
            <span class="credits-text">{{ userCredits }} Crédits</span>
          </button>

          <Transition name="fade">
            <div v-if="isOpen" class="dropdown">
              <ul class="dropdown-menu">
                <span>Crédit contrats</span>
                <span>Statut</span>
                <span>Date Expiration</span>
              </ul>
            </div>
          </Transition>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// État local
const isOpen = ref(false)
const wrapperRef = ref(null)

// ⚡️ NOUVEAU : Variable pour stocker les crédits (à relier à ton store Pinia)
const userCredits = ref(15) 

// Fonctions
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

// Gestion du clic en dehors
const handleClickOutside = (event) => {
  if (wrapperRef.value && !wrapperRef.value.contains(event.target)) {
    closeDropdown()
  }
}

// Déconnexion (à remplacer par ta logique)
const logout = () => {
  console.log('Déconnexion')
  // Appel API, redirection, etc.
  closeDropdown()
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
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
  background-color: var(--primary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  gap: 0.5rem; /* Rapproché pour que l'icône et le texte soient liés */
  border: none;
  
  /* ⚡️ CORRECTION : On passe d'un cercle (50%) à un rectangle arrondi (8px ou 12px) */
  border-radius: 8px; 
  cursor: pointer;
  color: var(--background-white-color);
  
  /* ⚡️ CORRECTION : Padding asymétrique parfait pour un bouton rectangulaire */
  padding: 0.6rem 1.2rem; 
  transition: 0.4s;
}

.profile-button:hover {
  transform: translateY(-2px);
  transition: 0.2s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* Petit ajout d'ombre au survol */
}

/* ⚡️ NOUVEAU : Tailles gérées pour l'icône et le texte */
.icon-size {
  width: 22px;
  height: 22px;
}

.credits-text {
  font-size: 0.95rem;
  font-weight: 600;
  white-space: nowrap; /* Empêche le texte de passer à la ligne sur mobile */
}

.dropdown {
  position: absolute;
  top: calc(100% + 0.5rem);
  right: 0;
  min-width: 180px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1000;
  overflow: hidden;
}

.dropdown-menu {
  list-style: none;
  margin: 0;
  padding: 0;
}

.dropdown-menu li {
  padding: 0;
}

.dropdown-menu span,
.dropdown-menu button {
  display: block;
  width: 100%;
  padding: 10px 16px;
  text-decoration: none;
  color: #333;
  background: none;
  border: none;
  text-align: left;
  cursor: pointer;
  font-size: 0.9rem;
}

.dropdown-menu a:hover,
.dropdown-menu button:hover {
  background-color: #f5f5f5;
}

/* Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>