from django.db import models
import uuid

class SimulationDroits(models.Model):
    # --- ÉNUMÉRATIONS ---
    class TypeContrat(models.TextChoices):
        CDD = 'CDD', 'CDD'
        CDI = 'CDI', 'CDI'
        STAGE = 'Stage_Qualification', 'Stage de Qualification'

    class MotifRupture(models.TextChoices):
        DEMISSION = 'Demission', 'Démission'
        LIC_SANS_FAUTE = 'Licenciement_Sans_Faute', 'Licenciement Sans Faute'
        LIC_FAUTE_LOURDE = 'Licenciement_Faute_Lourde', 'Licenciement Faute Lourde'
        LIC_ECO = 'Licenciement_Eco', 'Licenciement Économique'
        FIN_CDD = 'Fin_CDD', 'Fin de CDD'
        COMMUN_ACCORD_CDD = 'Commun_Accord_CDD', "Rupture d'un commun accord"
        RUPTURE_ANTI_EMPLOYE = 'Rupture_Anticipee_Employe', "Rupture anticipée par l'employé"
        RUPTURE_ANTI_EMPLOYEUR = 'Rupture_Anticipee_Employeur', "Rupture anticipée abusive par l'employeur"
        FAUTE_LOURDE_CDD = 'Faute_Lourde_CDD', "Rupture pour faute lourde"
        RETRAITE = 'Retraite', 'Retraite'
        DECES = 'Deces', 'Décès'

    class CategoriePro(models.TextChoices):
        OUVRIER = 'Ouvrier_Manoeuvre', 'Ouvrier / Manœuvre'
        EMPLOYE = 'Employe_Qualifie', 'Employé Qualifié'
        AGENT = 'Agent_Maitrise', 'Agent de Maîtrise'
        CADRE = 'Cadre_Assimile', 'Cadre et Assimilé'

    # --- CHAMPS DE LA BASE DE DONNÉES ---
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # -- Email
    email = models.EmailField()

    type_contrat = models.CharField(max_length=50, choices=TypeContrat.choices)
    motif_rupture = models.CharField(max_length=50, choices=MotifRupture.choices)
    categorie_pro = models.CharField(max_length=50, choices=CategoriePro.choices)

    date_embauche = models.DateField(help_text="Date de début de contrat")
    date_rupture = models.DateField(help_text="Date de fin effective du contrat")

    salaire_base = models.DecimalField(max_digits=12, decimal_places=2, help_text="Salaire de base mensuel en FCFA")
    surtaux_accords = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # 💡 Astuce : On stocke le tableau des 12 mois dans un JSON
    salaires_12_mois = models.JSONField(default=list, help_text="Historique des 12 derniers salaires bruts perçus")

    preavis_effectue = models.BooleanField(default=False)
    jours_conges_acquis = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Simulation {self.type_contrat} - {self.motif_rupture}"
