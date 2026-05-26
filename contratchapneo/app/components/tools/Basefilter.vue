<template>
<div class="filter-wrapper">
<div class="mobile-filter">
    <select v-model="selectedCategory" @change="emitFilter">
        <option value="">Toutes les catégories</option>
        <option v-for="cat in categories" :key="cat" :value="cat">
            {{ cat }}
        </option>
    </select>
</div>

<div class="desktop-filter">
    <button 
    :class="{ active: selectedCategory === '' }" 
    @click="selectCategory('')"
    >
    Tout
    </button>
    <button 
    v-for="cat in categories" 
    :key="cat"
    :class="{ active: selectedCategory === cat }"
    @click="selectCategory(cat)"
    >
    {{ cat }}
    </button>
</div>
</div>
</template>

<script lang="ts">
import { ref } from 'vue';

export default {
name: 'CategoryFilter',
emits: ['filter-change'],
setup(props, { emit }) {
// Liste de tes catégories (à adapter selon tes besoins ou à passer en props)
const categories = ref(['Tech', 'Design', 'Marketing', 'Légal', 'Finance']);
const selectedCategory = ref('');

const selectCategory = (cat: string) => {
    selectedCategory.value = cat;
    emitFilter();
};

const emitFilter = () => {
    emit('filter-change', selectedCategory.value);
};

return {
    categories,
    selectedCategory,
    selectCategory,
    emitFilter
};
}
};
</script>

<style scoped>
.filter-wrapper {
width: 100%;
margin: 1rem 0;
}

/* ==========================================
STYLE MOBILE (Par défaut)
========================================== */
.desktop-filter {
display: none; /* Caché sur mobile */
}

.mobile-filter select {
width: 100%;
padding: 0.75rem 1rem;
font-size: 1rem;
border: 1px solid #e2e8f0;
border-radius: 8px;
background-color: #ffffff;
color: #1a1a1a;
cursor: pointer;
outline: none;
}

/* ==========================================
STYLE TABLETTE & DESKTOP (Écrans >= 768px)
========================================== */
@media (min-width: 768px) {
.mobile-filter {
display: none; /* Caché sur tablette/ordinateur */
}

.desktop-filter {
display: flex; /* Devient visible et en ligne */
gap: 0.5rem;
flex-wrap: wrap; /* Permet de passer à la ligne si trop de catégories */
}

.desktop-filter button {
padding: 0.5rem 1.2rem;
font-size: 0.95rem;
font-weight: 500;
border: 1px solid #e2e8f0;
border-radius: 999px; /* Style "pill" en forme de capsule */
background-color: #ffffff;
color: #4a5568;
cursor: pointer;
transition: all 0.2s ease;
}

.desktop-filter button:hover {
background-color: #f7fafc;
border-color: #cbd5e0;
}

/* Style du bouton de la catégorie actuellement sélectionnée */
.desktop-filter button.active {
background-color: #1a1a1a; /* Devient noir (ou ta couleur principale) */
color: #ffffff;
border-color: #1a1a1a;
}
}
</style>