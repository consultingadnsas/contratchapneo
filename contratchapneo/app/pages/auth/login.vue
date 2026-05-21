<template>
    <div class="main-wrapper">
        <div class="login-section ">
            <loginFormVue/>
        </div>
    </div>
</template>

<script>
import loginFormVue from '../../components/forms/loginForm.vue'

export default {
    components:{
        loginFormVue
    }
}
</script>

<style scoped>

.login-section{
    display: flex;
}

</style>