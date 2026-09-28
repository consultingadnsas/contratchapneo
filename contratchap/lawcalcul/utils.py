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
        "indemnite_fin_cdd": Decimal('0.00'),
        "dommages_interets": Decimal('0.00'),
        "total_droits": Decimal('0.00')
    }

    # Helper function for préavis
    def get_preavis_months(categorie, years_of_seniority):
        if categorie == 'Ouvrier_Manoeuvre':
            if years_of_seniority < 1: return Decimal(8)/Decimal(30)
            if years_of_seniority <= 5: return Decimal('1')
            if years_of_seniority <= 10: return Decimal('2')
            return Decimal('3')
        elif categorie == 'Employe_Qualifie':
            if years_of_seniority < 1: return Decimal('1')
            if years_of_seniority <= 5: return Decimal('2')
            if years_of_seniority <= 10: return Decimal('3')
            return Decimal('4')
        elif categorie == 'Agent_Maitrise':
            if years_of_seniority < 1: return Decimal('2')
            if years_of_seniority <= 5: return Decimal('3')
            if years_of_seniority <= 10: return Decimal('4')
            return Decimal('5')
        else: # Cadre_Assimile
            if years_of_seniority < 1: return Decimal('3')
            if years_of_seniority <= 5: return Decimal('4')
            if years_of_seniority <= 10: return Decimal('5')
            return Decimal('6')

    # Ancienneté
    jours_anciennete = (simulation.date_rupture - simulation.date_embauche).days
    annees_anciennete = Decimal(jours_anciennete) / Decimal('365.25')

    # 1. Calcul du Salaire Moyen Mensuel (sur les 12 derniers mois)
    salaires = simulation.salaires_12_mois
    if salaires and len(salaires) > 0:
        salaire_moyen = sum(Decimal(str(s)) for s in salaires) / len(salaires)
    else:
        salaire_moyen = simulation.salaire_base + simulation.surtaux_accords
    
    resultats["salaire_moyen"] = round(salaire_moyen, 2)

    # 2. Indemnité compensatrice de Congés Payés
    if simulation.jours_conges_acquis > 0:
        if simulation.type_contrat == 'CDD':
            # For CDD, the frontend uses totalGrossSalary for ICCP approxMonthly / 26
            approx_monthly = simulation.salaire_base / max(Decimal('1.0'), Decimal(jours_anciennete) / Decimal('30.416'))
            indemnite_conges = (approx_monthly / Decimal('26')) * Decimal(str(simulation.jours_conges_acquis))
        else:
            indemnite_conges = (resultats["salaire_moyen"] / Decimal('26')) * Decimal(str(simulation.jours_conges_acquis))
        resultats["indemnite_conges"] = round(indemnite_conges, 2)

    if simulation.is_trial_period:
        resultats["total_droits"] = resultats["indemnite_conges"]
        return resultats

    if simulation.type_contrat == 'CDI':
        # Préavis
        if simulation.motif_rupture in ['Demission']:
            if not simulation.preavis_effectue:
                mois_preavis = get_preavis_months(simulation.categorie_pro, annees_anciennete)
                resultats["indemnite_preavis"] = -round(resultats["salaire_moyen"] * mois_preavis, 2)
        elif not simulation.preavis_effectue and simulation.motif_rupture in ['Licenciement_Sans_Faute', 'Licenciement_Eco', 'Licenciement_Abusif', 'Maladie_Longue_Duree', 'Retraite']:
            mois_preavis = get_preavis_months(simulation.categorie_pro, annees_anciennete)
            resultats["indemnite_preavis"] = round(resultats["salaire_moyen"] * mois_preavis, 2)

        # Indemnité de licenciement
        if simulation.motif_rupture in ['Licenciement_Sans_Faute', 'Licenciement_Eco', 'Retraite', 'Deces', 'Commun_Accord_CDI', 'Maladie_Longue_Duree']:
            if annees_anciennete >= 1:
                tranche1 = min(annees_anciennete, Decimal('5')) * Decimal('0.30') * resultats["salaire_moyen"]
                tranche2 = min(annees_anciennete - Decimal('5'), Decimal('5')) * Decimal('0.35') * resultats["salaire_moyen"] if annees_anciennete > 5 else Decimal('0')
                tranche3 = (annees_anciennete - Decimal('10')) * Decimal('0.40') * resultats["salaire_moyen"] if annees_anciennete > 10 else Decimal('0')
                
                resultats["indemnite_licenciement"] = round(tranche1 + tranche2 + tranche3, 2)

        # Dommages et intérêts
        if simulation.motif_rupture == 'Licenciement_Abusif':
            di_months = max(Decimal('3'), min(Decimal('20'), annees_anciennete))
            resultats["dommages_interets"] = round(resultats["salaire_moyen"] * di_months, 2)

    elif simulation.type_contrat == 'CDD':
        # Prime de précarité
        if simulation.motif_rupture in ['Fin_CDD', 'Commun_Accord_CDD']:
            if not simulation.cdd_transforms_to_cdi:
                resultats["indemnite_fin_cdd"] = round(simulation.salaire_base * Decimal('0.03'), 2)
        elif simulation.motif_rupture == 'Rupture_Anticipee_Employeur':
            # approximately monthly salary calculated from totalGross (salaire_base for CDD)
            approx_monthly = simulation.salaire_base / max(Decimal('1.0'), Decimal(jours_anciennete) / Decimal('30.416'))
            resultats["dommages_interets"] = round(approx_monthly * simulation.remaining_months, 2)
        elif simulation.motif_rupture == 'Rupture_Anticipee_Employe':
            if simulation.employer_damages > 0:
                resultats["dommages_interets"] = -round(simulation.employer_damages, 2)

    # 5. Calcul du Total
    resultats["total_droits"] = (
        resultats["indemnite_conges"] +
        resultats["indemnite_preavis"] +
        resultats["indemnite_licenciement"] +
        resultats["indemnite_fin_cdd"] +
        resultats["dommages_interets"]
    )

    return resultats