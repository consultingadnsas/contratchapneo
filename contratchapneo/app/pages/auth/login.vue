<template>
  <div class="main-wrapper">
    <div class="login-section">
      <div class=" w-full flex justify-center items-center">
        <loginFormVue />
      </div>
      <div class="pic-section">
        <div class="image-container">
          <img src="../../assets/pictures/ContratChap/pexels-kampus-8475168.jpg" alt="">
          <div class="overlay"></div>
          <div class="image-text">
            <h2>Bienvenue sur notre plateforme</h2>
            <p>Connectez-vous pour accéder à vos contrats</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import loginFormVue from '../../components/forms/loginForm.vue'

export default {
  components: {
    loginFormVue
  }
}
</script>

<style scoped>
.login-section {
  width: 100%;
  height: 100vh;
  display: flex;
  overflow: hidden;
}

.pic-section {
  display: none;
}

@media (min-width: 1024px) {
  .login-section {
    display: grid;
    grid-template-columns: 1fr 1fr;
  }

  .pic-section {
    display: block;
  }

  .image-container {
    position: relative;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .image-container img {
    width: 100%;
    height: 100%;
    max-width: 600px;
    max-height: 950px;
    object-fit: cover;
    display: block;
  }

  .overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5); /* Ajuste l'opacité pour plus ou moins sombre */
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