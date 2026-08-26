# utils.py
from decimal import Decimal

def calculer_droits(simulation):
    """
    Calcule les droits de rupture en fonction des données de la simulation.
    Retourne un dictionnaire détaillé avec chaque indemnité.
    """
    resultats = {
        "salaire_moyen": Decimal('0.00'),
        "indemnite_licenciement": Decimal('0.00'),
        "indemnite_preavis": Decimal('0.00'),
        "indemnite_conges": Decimal('0.00'),
        "total_droits": Decimal('0.00')
    }

    # 1. Calcul du Salaire Moyen Mensuel (sur les 12 derniers mois)
    salaires = simulation.salaires_12_mois
    if salaires and len(salaires) > 0:
        salaire_moyen = sum(Decimal(str(s)) for s in salaires) / len(salaires)
    else:
        salaire_moyen = simulation.salaire_base + simulation.surtaux_accords
    
    resultats["salaire_moyen"] = round(salaire_moyen, 2)

    # 2. Indemnité compensatrice de Congés Payés
    # Base légale classique : (Salaire moyen / 30) * nombre de jours acquis
    if simulation.jours_conges_acquis > 0:
        indemnite_conges = (resultats["salaire_moyen"] / Decimal('30')) * Decimal(str(simulation.jours_conges_acquis))
        resultats["indemnite_conges"] = round(indemnite_conges, 2)

    # 3. Indemnité compensatrice de préavis (si applicable et non effectué)
    # Logique simplifiée : 1 mois pour les employés, 3 mois pour les cadres
    if not simulation.preavis_effectue and simulation.motif_rupture in ['Licenciement_Sans_Faute', 'Licenciement_Eco']:
        mois_preavis = Decimal('1.0') # Par défaut
        if simulation.categorie_pro in ['Agent_Maitrise', 'Cadre_Assimile']:
            mois_preavis = Decimal('3.0')
            
        resultats["indemnite_preavis"] = round(resultats["salaire_moyen"] * mois_preavis, 2)

    # 4. Indemnité de licenciement (si applicable)
    # Exemple : Nécessite au moins 1 an d'ancienneté. (Ex: 30% du salaire moyen par année d'ancienneté)
    if simulation.motif_rupture in ['Licenciement_Sans_Faute', 'Licenciement_Eco', 'Retraite', 'Deces']:
        jours_anciennete = (simulation.date_rupture - simulation.date_embauche).days
        annees_anciennete = Decimal(jours_anciennete) / Decimal('365.25')
        
        if annees_anciennete >= 1: 
            indemnite_licenciement = resultats["salaire_moyen"] * Decimal('0.30') * annees_anciennete
            resultats["indemnite_licenciement"] = round(indemnite_licenciement, 2)

    # 5. Calcul du Total
    resultats["total_droits"] = (
        resultats["indemnite_conges"] +
        resultats["indemnite_preavis"] +
        resultats["indemnite_licenciement"]
    )

    return resultats