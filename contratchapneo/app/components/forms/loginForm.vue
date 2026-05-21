<template>
    <form action="">
        <h3>Connexion</h3>
        <BaseInputVue label="Email" name="email" type="email" placeholder="Entrez votre email" />
        <BaseInputVue label="Mot de passe" name="password" type="password" placeholder="Entrez votre mot de passe" />
        <formButtonVue label="Connexion" />
    </form>
</template>

<script>
import formButtonVue from '../buttons/formButton.vue'
import BaseInputVue from '../input/BaseInput.vue'


export default {
    components:{
        BaseInputVue,
        formButtonVue
    }
}
</script>

<style scoped>


</style>