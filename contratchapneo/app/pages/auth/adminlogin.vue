<template>
  <div class="main-wrapper h-screen w-screen overflow-hidden">
    <div class="login-section">
      
      <div class="form-container">
        <adminLoginForm class="w-full max-w-md p-4" /> 
        </div>

    </div>
  </div>
</template>

<script>
import adminLoginForm from '../../components/forms/adminLoginForm.vue'
export default {
  components: {
    adminLoginForm
  }
}
</script>

<style scoped>
/* --- CONFIGURATION GLOBALE --- */
.main-wrapper {
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.login-section {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  overflow: hidden;
}

/* Par défaut (Mobile / Tablette) : le formulaire prend tout l'écran, l'image est cachée */
.form-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pic-section {
  display: none;
}

/* --- GRANDS ÉCRANS (PC) --- */
@media (min-width: 1024px) {
  .login-section {
    display: flex;
    grid-template-columns: 1fr 1fr; /* 50% formulaire, 50% image */
    height: 100vh;
  }

  .form-container {
    width: 100%;
    height: 100vh; /* Re-déclare la hauteur stricte pour la grille */
  }

  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    z-index: 1;
  }

}
</style>