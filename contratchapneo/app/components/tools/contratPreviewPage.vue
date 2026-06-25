<template>
  <main class="preview-section">
        <div class="a4-document">
            <h1 class="doc-title">CONTRAT DE PRESTATION DE SERVICES</h1>
            
            <p class="doc-paragraph">Entre les soussignés :</p>
            
            <p class="doc-paragraph">
                La société <strong>Contratchap SAS</strong>, représentée par son gérant, d'une part,
            </p>
            
            <p class="doc-paragraph">
                Et M./Mme/La société <span class="dynamic-data">{{ contractData.nom_client || '[Nom du client]' }}</span>, 
                résidant à <span class="dynamic-data">{{ contractData.adresse || '[Adresse du client]' }}</span>, 
                ci-après dénommé(e) "Le Client", d'autre part.
            </p>

            <p class="doc-paragraph">
                Il a été convenu ce qui suit, à compter du <span class="dynamic-data">{{ formattedDate || '[Date de début]' }}</span> :
            </p>

            <h3 class="doc-subtitle">Article 1 : Objet</h3>
            <p class="doc-paragraph">
                Le présent contrat a pour objet la fourniture de services juridiques. 
                Le client s'engage à verser la somme de <span class="dynamic-data">{{ contractData.montant ? contractData.montant + ' FCFA' : '[Montant]' }}</span> 
                pour l'exécution de cette prestation.
            </p>

            <div class="signatures">
                <div class="sign-box">
                    <p>Pour le Prestataire</p>
                    <div class="sign-space"></div>
                </div>
                <div class="sign-box">
                    <p>Pour le Client</p>
                    <div class="sign-space"></div>
                </div>
            </div>
        </div>
    </main>
</template>

<script>
export default {

    name:'contractpreview',

    setup(){

        

    }

}
</script>

<style scoped>

/* =========================================
   FAUX DOCUMENT A4 (Droite/Bas)
   ========================================= */
.preview-section {
    flex: 2; /* Prend deux fois plus de place que le formulaire sur PC */
    display: flex;
    justify-content: center;
    overflow-x: auto; /* Permet de scroller horizontalement sur mobile si nécessaire */
}

.a4-document {
    background: #ffffff;
    width: 100%;
    max-width: 210mm; /* Largeur exacte d'un A4 */
    min-height: 297mm; /* Hauteur exacte d'un A4 */
    padding: 12% 10%; /* Marges intérieures typiques d'un Word */
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
    
    /* Typographie juridique */
    font-family: 'Times New Roman', Times, serif;
    color: #000000;
    line-height: 1.6;
}

/* Style des textes remplis dynamiquement */
.dynamic-data {
    color: #1a56db; /* Bleu pour montrer que c'est une variable */
    background-color: rgba(26, 86, 219, 0.05); /* Surlignage très léger */
    padding: 0 4px;
    border-radius: 2px;
}

.doc-title {
    text-align: center;
    font-size: 1.4rem;
    text-decoration: underline;
    margin-bottom: 3rem;
    text-transform: uppercase;
}

.doc-subtitle {
    margin-top: 2rem;
    margin-bottom: 1rem;
    font-size: 1.1rem;
    text-decoration: underline;
}

.doc-paragraph {
    margin-bottom: 1.2rem;
    text-align: justify;
}

.signatures {
    display: flex;
    justify-content: space-between;
    margin-top: 5rem;
}

.sign-box {
    width: 40%;
}

.sign-box p {
    font-weight: bold;
    margin-bottom: 0.5rem;
}

.sign-space {
    border-top: 1px dotted #000;
    height: 100px;
    margin-top: 3rem;
}

</style>