<template>
    <div class="features-cards">

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

export default{

    name:'features-cards',
    props:{
        title:{
            type:String,
            default:"Création et cession"
        }
    }

}

</script>

<style scoped>

/* Mobile first */

.features-cards{
    z-index: 1;
    position: relative;
    display: flex;
    align-items: center;
    height: 180px;
    width: 180px;
    background: var(--secondary-dark-color);
    border-radius: 1rem;
    border-bottom-right-radius: 0;
    padding: 0.5rem;
}

.features-cards h4{
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--my-white);
}

.btn-container{
    z-index: 2;
    position: absolute;
    bottom: 0;
    right: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--secondary-color); 
    border-top-left-radius: 2rem;
    width: 65px;
    height: 65px;
    padding: 0.5rem;
}

.features-cards button{
    position: absolute;
    bottom: 1;
    right: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    font-size: 1rem;
    color: var(--secondary-dark-color);
    background: var(--my-white);
}

@media(min-width: 768px){
    .features-cards{
        width: 300px;
        height:300px;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    .features-cards h4{
        font-size: 1.6rem;
        font-weight: 500;
        color: var(--my-white);
    }
}

</style>