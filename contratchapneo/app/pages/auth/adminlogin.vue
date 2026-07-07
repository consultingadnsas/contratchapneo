<template>
  <div class="main-wrapper h-screen w-screen overflow-hidden">
    <div class="login-section">
      
      <div class="form-container">
        <adminLoginForm class="w-full max-w-md p-4" /> 
        </div>
      
      <div class="pic-section">
        <div class="image-container">
          <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" alt="Bienvenue">
          <div class="overlay"></div>
          <div class="image-text">
            <h2>Bienvenue sur notre plateforme</h2>
            <p>Connectez-vous pour accéder à vos packs de contrats</p>
          </div>
        </div>
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
    display: grid;
    grid-template-columns: 1fr 1fr; /* 50% formulaire, 50% image */
    height: 100vh;
  }

  .form-container {
    width: 100%;
    height: 100vh; /* Re-déclare la hauteur stricte pour la grille */
  }

  .pic-section {
    display: block;
    width: 100%;
    height: 100vh;
    position: relative;
    overflow: hidden;
  }

  .image-container {
    width: 100%;
    height: 100%;
    position: relative;
  }

  /* Remplissage absolu pour empêcher l'image de pousser les murs de la grille */
  .image-container img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover; 
    object-position: center;
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

  .image-text {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    color: white;
    text-align: center;
    z-index: 2;
    width: 80%;
  }

  .image-text h2 {
    font-size: 1.8rem;
    margin-bottom: 0.5rem;
  }

  .image-text p {
    font-size: 1rem;
    opacity: 0.9;
  }
}
</style>