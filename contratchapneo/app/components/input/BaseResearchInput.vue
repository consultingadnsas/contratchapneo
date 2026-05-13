<template>
  <div class="input-group" :class="{ 'has-error': !!errorMessage, 'is-disabled': disabled }">
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>

    <div class="input-wrapper">
      <span class="input-icon input-icon-left">
        <slot name="prepend">
          <svg class="search-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </slot>
      </span>

      <input
        :id="inputId"
        ref="inputRef"
        class="form-input search-padding"
        :class="{ 'pr-icon': $slots.append }"
        :value="modelValue"
        :disabled="disabled"
        v-bind="$attrs"
        @input="handleInput"
        @blur="$emit('blur', $event)"
        :placeholder="placeholder"
      />

      <span v-if="$slots.append" class="input-icon input-icon-right">
        <slot name="append"></slot>
      </span>
    </div>

    <p v-if="errorMessage" :id="`${inputId}-error`" class="message error-message">
       {{ errorMessage }}
    </p>
  </div>
</template>

<script>
import {useId} from 'vue'

export default {
  name: 'SearchInput',
  inheritAttrs: false,
  props: {
    modelValue: { type: [String, Number], default: '' },
    label: { type: String, default: '' },
    errorMessage: { type: String, default: '' },
    hint: { type: String, default: '' },
    id: { type: String, default: null },
    disabled: { type: Boolean, default: false },
    required: { type: Boolean, default: false },
    placeholder: { type: String, default: 'Trouver un contrat...' }
  },
  emits: ['update:modelValue', 'blur'],
  setup(){
    const generatedId = useId()
    return{
      generatedId
    }
  },
  computed:{
    inputId(){
      return this.id || `search-${this.generatedId}`
    }
  }
};
</script>

<style scoped>
.input-group {
  --glass-bg: rgba(255, 255, 255, 0.1);
  --glass-border: rgba(255, 255, 255, 0.2);
  --primary-color: #60a5fa; 
  --text-color: #ffffff;
  
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 1rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-label{
    text-align: start;
}

.form-input {
  width: 100%;
  padding: 1rem 1.5rem;
  /* On laisse de la place à gauche pour l'icône */
  padding-left: 3.5rem; 
  font-size: 1.1rem;
  color: var(--text-color);
  background: var(--glass-bg);
  backdrop-filter: blur(15px);
  -webkit-backdrop-filter: blur(15px);
  border: 1px solid var(--glass-border);
  border-radius: 999px; /* Forme pilule parfaite */
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  padding-left: 3.8rem !important;
  z-index: 1;
}

.form-input:focus {
  outline: none;
  background: rgba(255, 255, 255, 0.18);
  border-color: var(--primary-color);
  box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
  transform: scale(1.01); /* Petit effet de zoom au focus */
}

.input-icon {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  pointer-events: none;
  z-index: 2;
}

.input-icon-left {
    left: 8px; /* On le rapproche un peu du bord gauche */
    background: var(--secondary-light-color); /* Le fond du rond */
    width: 40px;  /* Taille du rond */
    height: 40px; /* Taille du rond */
    border-radius: 50%; /* Rend le fond parfaitement rond */
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s ease;
}

/* On ajuste l'icône à l'intérieur du rond */
.input-icon-left :deep(svg), 
.input-icon-left svg {
    width: 20px;
    height: 20px;
    color: white !important; /* L'icône devient blanche pour trancher sur le bleu */
}

/* Style de la loupe */
.search-icon {
  width: 20px;
  height: 20px;
  /* Ici on applique la couleur primaire à l'icône */
  color: var(--primary-color);
  filter: drop-shadow(0 0 5px rgba(96, 165, 250, 0.4));
}

.form-input::placeholder {
  color: rgba(255, 255, 255, 0.5);
  font-weight: 300;
}

.error-message {
  color: #f87171;
  font-size: 0.85rem;
  margin: 0.5rem 0 0 1.5rem;
}
</style>