<template>
  <div class="features-cards">
    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-8">
      <path stroke-linecap="round" stroke-linejoin="round" d="M12 3v17.25m0 0c-1.472 0-2.882.265-4.185.75M12 20.25c1.472 0 2.882.265 4.185.75M18.75 4.97A48.416 48.416 0 0 0 12 4.5c-2.291 0-4.545.16-6.75.47m13.5 0c1.01.143 2.01.317 3 .52m-3-.52 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.988 5.988 0 0 1-2.031.352 5.988 5.988 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L18.75 4.971Zm-16.5.52c.99-.203 1.99-.377 3-.52m0 0 2.62 10.726c.122.499-.106 1.028-.589 1.202a5.989 5.989 0 0 1-2.031.352 5.989 5.989 0 0 1-2.031-.352c-.483-.174-.711-.703-.59-1.202L5.25 4.971Z" />
    </svg>
    <h4 class="features-title">
      {{ title }}
    </h4>
    <div class="btn-container">
      <button>
        <span>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-6">
            <path stroke-linecap="round" stroke-linejoin="round" d="m4.5 19.5 15-15m0 0H8.25m11.25 0v11.25" />
          </svg>
        </span>
      </button>
    </div>
  </div>
</template>

<script lang="ts">
export default {
  name: 'features-cards',
  props: {
    title: {
      type: String,
      default: 'Création et cession',
    },
  },
}
</script>

<style scoped>
/* Mobile first – forme inspirée de statCards, couleurs conservées */
.features-cards {
  z-index: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: start;
  gap: 1rem;
  width: 100%;
  min-height: 100px;
  height: auto;
  border-radius: 1.5rem;        /* arrondi homogène (plus de coin carré) */
  padding: 1rem 1.2rem;
  box-sizing: border-box;

  /* couleurs d'origine (pas de glassmorphism) */
  background: var(--secondary-dark-color);
}

.features-cards h4 {
  font-size: clamp(0.85rem, 2.5vw, 1.1rem);
  line-height: 1.3;
  font-weight: 600;
  color: var(--my-white);        /* couleur d'origine */
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  padding-right: 3rem;           /* évite chevauchement avec le bouton */
  margin: 0;
}

.btn-container {
  z-index: 2;
  position: absolute;
  bottom: -5px;
  right: -5px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border-top-left-radius: 2rem;
  border-bottom-right-radius: 1.5rem;
  width: 55px;
  height: 55px;
}

.features-cards button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: none;
  cursor: pointer;
  /* couleurs d'origine du bouton */
  color: var(--secondary-dark-color);
  background: var(--my-white);
  transition: transform 0.3s ease;
  flex-shrink: 0;
}

.features-cards button:hover {
  transform: scale(1.1) rotate(5deg);
}

.size-6 {
  width: 18px;
  height: 18px;
}

/* Tablette */
@media (min-width: 768px) {
  .features-cards {
    padding: 1.5rem;
    min-height: 140px;
  }

  .features-cards h4 {
    font-size: clamp(1.1rem, 2vw, 1.5rem);
  }

  .btn-container {
    width: 70px;
    height: 70px;
  }

  .features-cards button {
    width: 52px;
    height: 52px;
  }

  .size-6 {
    width: 22px;
    height: 22px;
  }
}

/* Desktop */
@media (min-width: 1200px) {
  .features-cards {
    padding: 2rem;
    min-height: 160px;
  }

  .features-cards h4 {
    font-size: clamp(1.2rem, 1.5vw, 1.8rem);
  }
}
</style>