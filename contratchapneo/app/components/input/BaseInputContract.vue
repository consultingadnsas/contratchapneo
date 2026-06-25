<template>
  <div
    class="input-group"
    :class="{
      'has-error': !!errorMessage,
      'is-disabled': disabled
    }"
  >
    <label v-if="label" :for="inputId" class="input-label">
      {{ label }}
      <span v-if="required" class="required-mark">*</span>
    </label>

    <div class="input-wrapper">
      <span v-if="$slots.prepend" class="input-icon input-icon-left">
        <slot name="prepend"></slot>
      </span>

      <input
        :id="inputId"
        ref="inputRef"
        class="form-input"
        :class="{
          'pl-icon': $slots.prepend,
          'pr-icon': $slots.append
        }"
        :value="modelValue"
        :disabled="disabled"
        :aria-invalid="!!errorMessage"
        :aria-describedby="
          errorMessage
            ? `${inputId}-error`
            : hint
              ? `${inputId}-hint`
              : undefined
        "
        v-bind="$attrs"
        @input="handleInput"
        @blur="$emit('blur', $event)"
        :placeholder="placeholder"
      />

      <span v-if="$slots.append" class="input-icon input-icon-right">
        <slot name="append"></slot>
      </span>
    </div>

    <p
      v-if="errorMessage"
      :id="`${inputId}-error`"
      class="message error-message"
    >
      <svg
        xmlns="http://www.w3.org/2000/svg"
        viewBox="0 0 20 20"
        fill="currentColor"
        class="msg-icon"
      >
        <path
          fill-rule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
          clip-rule="evenodd"
        />
      </svg>
      {{ errorMessage }}
    </p>

    <p
      v-else-if="hint"
      :id="`${inputId}-hint`"
      class="message hint-message"
    >
      {{ hint }}
    </p>
  </div>
</template>

<script>
import { useId, computed } from 'vue';

export default {
  name: 'BaseInputContract',
  inheritAttrs: false,
  props: {
    modelValue: {
      type: [String, Number],
      default: ''
    },
    label: {
      type: String,
      default: ''
    },
    errorMessage: {
      type: String,
      default: ''
    },
    hint: {
      type: String,
      default: ''
    },
    id: {
      type: String,
      default: null
    },
    disabled: {
      type: Boolean,
      default: false
    },
    required: {
      type: Boolean,
      default: false
    },
    placeholder: {
      type: String,
      default: 'Entrer votre nom'
    }
  },
  emits: ['update:modelValue', 'blur'],
  setup(props, { emit }) {
    const generatedId = useId();

    const inputId = computed(() => props.id || `input-${generatedId}`);

    const handleInput = (event) => {
      emit('update:modelValue', event.target.value);
    };

    return {
      inputId,
      handleInput
    };
  }
};
</script>

<style scoped>
/* Variables CSS pour faciliter la personnalisation */
.input-group {
  --primary-color: #3b82f6;
  --error-color: #ef4444;
  --text-color: #1f2937;
  --label-color: #374151;
  --border-color: #d1d5db;
  --bg-disabled: #f3f4f6;

  display: flex;
  flex-direction: column;
  margin-bottom: 0.5rem;
  font-family: sans-serif;
  width: 100%;
}

.input-label {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--label-color);
  margin-bottom: 0.5rem;
  display: block;
}

.required-mark {
  color: var(--error-color);
  margin-left: 2px;
}

/* Wrapper utilisé pour positionner les lignes animées et les icônes */
.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

/* Ligne grise par défaut (inactive) */
.input-wrapper::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: var(--border-color);
  transition: background-color 0.2s ease;
}

/* Ligne colorée animée qui se remplit au focus */
.input-wrapper::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background-color: var(--primary-color);
  transition: width 0.3s ease;
}

/* Au focus (ou quand un enfant est focus), la bordure se remplit */
.input-wrapper:focus-within::after {
  width: 100%;
}

/* État d'erreur : remplacer la couleur de l'animation et de la ligne par la couleur d'erreur */
.has-error .input-wrapper::before {
  background-color: var(--error-color);
}
.has-error .input-wrapper::after {
  background-color: var(--error-color);
}
.has-error .input-wrapper:focus-within::after {
  background-color: var(--error-color);
}

/* État désactivé : rendre la ligne plus discrète */
.is-disabled .input-wrapper::before {
  background-color: #e5e7eb;
}
.is-disabled .input-wrapper::after {
  background-color: transparent; /* pas d'animation quand désactivé */
}

/* Le champ en lui-même : plus de bordure visible, pas d'outline */
.form-input {
  width: 100%;
  padding: 0.7rem;
  font-size: 1rem;
  line-height: 1.5;
  color: var(--text-color);
  background-color: transparent;
  border: none;
  outline: none;
  box-shadow: none;
}

/* Gestion des icônes */
.input-icon {
  position: absolute;
  top: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2.5rem;
  color: #9ca3af;
  pointer-events: none; /* L'icône ne bloque pas le clic */
}

.input-icon-left {
  left: 0;
}
.input-icon-right {
  right: 0;
}

.pl-icon {
  padding-left: 2.5rem;
}
.pr-icon {
  padding-right: 2.5rem;
}

/* État d'erreur sur le label */
.has-error .input-label {
  color: var(--error-color);
}

.has-error .input-icon {
  color: var(--error-color);
}

/* Messages (Erreur et Hint) */
.message {
  font-size: 0.8rem;
  margin-top: 0.375rem;
  display: flex;
  align-items: center;
  gap: 4px;
}

.error-message {
  color: var(--error-color);
}

.hint-message {
  color: #6b7280;
}

.msg-icon {
  width: 14px;
  height: 14px;
}

/* État désactivé */
.is-disabled .form-input {
  background-color: var(--bg-disabled);
  cursor: not-allowed;
  opacity: 1;
}
</style>