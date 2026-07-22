<template>
    <div class="profile-wrapper" ref="wrapperRef">
          <button class="profile-button" @click="toggleDropdown">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
              <path stroke-linecap="round" stroke-linejoin="round" d="M12 18v-5.25m0 0a6.01 6.01 0 0 0 1.5-.189m-1.5.189a6.01 6.01 0 0 1-1.5-.189m3.75 7.478a12.06 12.06 0 0 1-4.5 0m3.75 2.383a14.406 14.406 0 0 1-3 0M14.25 18v-.192c0-.983.658-1.823 1.508-2.316a7.5 7.5 0 1 0-7.517 0c.85.493 1.509 1.333 1.509 2.316V18" />
            </svg>
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
/* (les mêmes styles que précédemment) */
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
  gap: 1rem;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  color: var(--background-white-color);
  font-size: 0.9rem;
  font-weight: 600;
  padding: 0.9rem;
  transition: 0.4s;
}

.profile-button:hover {
  transform: translateY(-2px);
  transition: 0.2s;
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