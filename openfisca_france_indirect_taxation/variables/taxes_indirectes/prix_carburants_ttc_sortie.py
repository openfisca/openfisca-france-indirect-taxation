from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

import numpy as np


class prix_gazole_b7_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 TTC par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        code_region = menage('code_region', period)
        taux_conversion_gazoles = parameters(period).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_gazoles

        #  On récupère l'accise en euro/mwh et on le converti en euro/hectolitre
        accise_gazole_b7_mwh = parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.gazoles
        accise_gazole_b7_hectolitre = accise_gazole_b7_mwh * taux_conversion_gazoles

        # On récupère la majoration régionale de l'accise en euro/mwh pour toutes les régions,
        # Pour chaque cellules du vecteur, on récupère la valeur regionale de la majoration et on la converti en euro/hectolitre
        majoration_ticpe_gazole_b7_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_gazole
        majoration_regionale_ticpe_gazole_b7_hectolitre = np.fromiter(
            (
                getattr(majoration_ticpe_gazole_b7_mwh, region_cell, 0) * taux_conversion_gazoles
                for region_cell in code_region),
            dtype=np.float32)

        # On récupère la valeur maximale de la part de l'accise de base qui revient à la région, qui est déjà en euro/hectolitre
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole.maximum_value_affectation
        # Pour chaque cellules du vecteur, on récupère la valeur regionale de l'affectation
        affectation_ticpe_gazole_b7_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole
        affectation_regionale_ticpe_gazole_b7_hectolitre = np.fromiter(
            (
                getattr(affectation_ticpe_gazole_b7_hectolitre, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)

        #  On récupère la majoration specifique mobilité de l'Île-de-France en euro/mwh et on le converti en euro/hectolitre
        major_mobilites_tipce_gazole_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_gazole
        major_mobilites_tipce_gazole_hectolitre = major_mobilites_tipce_gazole_mwh * taux_conversion_gazoles

        accise_gazole_b7_total = accise_gazole_b7_hectolitre + majoration_regionale_ticpe_gazole_b7_hectolitre - (maximum_value_affectation - affectation_regionale_ticpe_gazole_b7_hectolitre) + ((code_region == '11') * major_mobilites_tipce_gazole_hectolitre)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_gazole_b7_hors_tva = prix_gazole_b7_ht + (accise_gazole_b7_total / 100)
        prix_gazole_b7_ttc = prix_gazole_b7_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b7_ttc

    def formula_2017(menage, period, parameters):
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        code_region = menage('code_region', period)
        accise_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazole
        majoration_ticpe_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_gazole
        majoration_regionale_ticpe_gazole_b7 = np.fromiter(
            (
                getattr(majoration_ticpe_gazole_b7, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole.maximum_value_affectation
        affectation_ticpe_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole
        affectation_regionale_ticpe_gazole_b7 = np.fromiter(
            (
                getattr(affectation_ticpe_gazole_b7, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        major_mobilites_tipce_gazole = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_gazole
        accise_gazole_b7_total = accise_gazole_b7 + majoration_regionale_ticpe_gazole_b7 - (maximum_value_affectation - affectation_regionale_ticpe_gazole_b7) + ((code_region == '11') * major_mobilites_tipce_gazole)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_gazole_b7_hors_tva = prix_gazole_b7_ht + (accise_gazole_b7_total / 100)
        prix_gazole_b7_ttc = prix_gazole_b7_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b7_ttc

    def formula(menage, period, parameters):
        prix_gazole_b7_ht = menage('prix_gazole_b7_ht', period)
        code_region = menage('code_region', period)
        accise_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazole
        majoration_ticpe_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_gazole
        majoration_regionale_ticpe_gazole_b7 = np.fromiter(
            (
                getattr(majoration_ticpe_gazole_b7, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole.maximum_value_affectation
        affectation_ticpe_gazole_b7 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_gazole
        affectation_regionale_ticpe_gazole_b7 = np.fromiter(
            (
                getattr(affectation_ticpe_gazole_b7, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        accise_gazole_b7_total = accise_gazole_b7 + majoration_regionale_ticpe_gazole_b7 - (maximum_value_affectation - affectation_regionale_ticpe_gazole_b7)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_gazole_b7_hors_tva = prix_gazole_b7_ht + (accise_gazole_b7_total / 100)
        prix_gazole_b7_ttc = prix_gazole_b7_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b7_ttc


class prix_gazole_b7_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B7 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b7_hors_remise_ttc = prix_gazole_b7_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b7_hors_remise_ttc
    
    def formula_2023(menage, period):
        return menage('prix_gazole_b7_ttc_sortie', period)


class prix_gazole_b10_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 TTC par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        taux_conversion_gazoles = parameters(period).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_gazoles
        accise_gazole_b10_mwh = parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.gazoles
        accise_gazole_b10_hectolitre = accise_gazole_b10_mwh * taux_conversion_gazoles
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_tva = prix_gazole_b10_ht + (accise_gazole_b10_hectolitre / 100)
        prix_gazole_b10_ttc_sortie = prix_gazole_b10_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b10_ttc_sortie

    def formula_2017(menage, period, parameters):
        prix_gazole_b10_ht = menage('prix_gazole_b10_ht', period)
        accise_gazole_b10_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazol_b_10_hectolitre
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_tva = prix_gazole_b10_ht + (accise_gazole_b10_hectolitre / 100)
        prix_gazole_b10_ttc_sortie = prix_gazole_b10_hors_tva * (1 + taux_plein_tva)
        return prix_gazole_b10_ttc_sortie


class prix_gazole_b10_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_remise_ttc = prix_gazole_b10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b10_hors_remise_ttc
        
    def formula_2023(menage, period):
        return menage('prix_gazole_b10_ttc_sortie', period)


class prix_essence_sp95_e10_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        code_region = menage('code_region', period)
        taux_conversion_essence_sp95_e10 = parameters(period).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_essence_sp95_e10

        accise_super_e10_mwh = parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.essence_sp95_e10
        accise_super_e10_hectolitre = accise_super_e10_mwh * taux_conversion_essence_sp95_e10

        major_regionale_ticpe_super_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super_hectolitre = np.fromiter(
            (
                getattr(major_regionale_ticpe_super_mwh, region_cell, 0) * taux_conversion_essence_sp95_e10
                for region_cell in code_region),
            dtype=np.float32)

        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10.maximum_value_affectation
        affectation_ticpe_sp_95_e10_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10
        affectation_regionale_ticpe_sp95_e10_hectolitre = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_e10_hectolitre, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)

        major_mobilites_tipce_sp95_e10_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_e10
        major_mobilites_tipce_sp95_e10_hectolitre = major_mobilites_tipce_sp95_e10_mwh * taux_conversion_essence_sp95_e10

        refraction_corse_tipce_sp95_e10_mwh = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_e10
        refraction_corse_tipce_sp95_e10_hectolitre = refraction_corse_tipce_sp95_e10_mwh * taux_conversion_essence_sp95_e10

        accise_sp_e10_ticpe = accise_super_e10_hectolitre + majoration_ticpe_super_hectolitre - (maximum_value_affectation - affectation_regionale_ticpe_sp95_e10_hectolitre) + ((code_region == '11') * major_mobilites_tipce_sp95_e10_hectolitre) - ((code_region == '94') * refraction_corse_tipce_sp95_e10_hectolitre)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ht + (accise_sp_e10_ticpe / 100)
        prix_essence_sp95_e10_ttc_sortie = prix_essence_sp95_e10_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc_sortie

    def formula_2019(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        code_region = menage('code_region', period)
        accise_super_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e10
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10.maximum_value_affectation
        affectation_ticpe_sp_95_e10 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10
        affectation_regionale_ticpe_sp95_e10 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_e10, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        major_mobilites_tipce_sp95_e10 = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_e10
        refraction_corse_tipce_sp95_E10 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_e10
        accise_sp_e10_ticpe = accise_super_e10 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_e10) + ((code_region == '11') * major_mobilites_tipce_sp95_e10) - ((code_region == '94') * refraction_corse_tipce_sp95_E10)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ht + (accise_sp_e10_ticpe / 100)
        prix_essence_sp95_e10_ttc_sortie = prix_essence_sp95_e10_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc_sortie

    def formula_2017(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        code_region = menage('code_region', period)
        accise_super_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e10
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10.maximum_value_affectation
        affectation_ticpe_sp_95_e10 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10
        affectation_regionale_ticpe_sp95_e10 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_e10, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        major_mobilites_tipce_sp95_e10 = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_e10
        accise_sp_e10_ticpe = accise_super_e10 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_e10) + ((code_region == '11') * major_mobilites_tipce_sp95_e10)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ht + (accise_sp_e10_ticpe / 100)
        prix_essence_sp95_e10_ttc_sortie = prix_essence_sp95_e10_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc_sortie

    def formula_2009(menage, period, parameters):
        prix_essence_sp95_e10_ht = menage('prix_essence_sp95_e10_ht', period)
        code_region = menage('code_region', period)
        accise_super_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e10
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10.maximum_value_affectation
        affectation_ticpe_sp_95_e10 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_e10
        affectation_regionale_ticpe_sp95_e10 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_e10, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        accise_sp_e10_ticpe = accise_super_e10 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_e10)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ht + (accise_sp_e10_ticpe / 100)
        prix_essence_sp95_e10_ttc_sortie = prix_essence_sp95_e10_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc_sortie


class prix_essence_sp95_e10_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_ttc = prix_essence_sp95_e10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc
    
    def formula_2023(menage, period):
        return menage('prix_essence_sp95_e10_ttc_sortie', period)


class prix_essence_sp95_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        code_region = menage('code_region', period)
        taux_conversion_essences = parameters(period).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_essences

        accise_essences_mwh = parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.essences
        accise_essences_hectolitre = accise_essences_mwh * taux_conversion_essences

        major_regionale_ticpe_super_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super_hectolitre = np.fromiter(
            (
                getattr(major_regionale_ticpe_super_mwh, region_cell, 0) * taux_conversion_essences
                for region_cell in code_region),
            dtype=np.float32)

        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp95_sp98_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98_hectolitre = np.fromiter(
            (
                getattr(affectation_ticpe_sp95_sp98_hectolitre, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)

        major_mobilites_tipce_sp95_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_sp98
        major_mobilites_tipce_sp95_hectolitre = major_mobilites_tipce_sp95_mwh * taux_conversion_essences

        refraction_corse_tipce_sp95_mwh = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        refraction_corse_tipce_sp95_hectolitre = refraction_corse_tipce_sp95_mwh * taux_conversion_essences

        accise_sp_95_ticpe = accise_essences_hectolitre + majoration_ticpe_super_hectolitre - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98_hectolitre) + ((code_region == '11') * major_mobilites_tipce_sp95_hectolitre) - ((code_region == '94') * refraction_corse_tipce_sp95_hectolitre)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_ht + (accise_sp_95_ticpe / 100)
        prix_essence_sp95_ttc_sortie = prix_essence_sp95_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc_sortie

    def formula_2017(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        code_region = menage('code_region', period)
        accise_super95 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        major_mobilites_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_sp98
        refraction_corse_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        accise_sp_95_ticpe = accise_super95 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98) + ((code_region == '11') * major_mobilites_tipce_sp95_sp98) - ((code_region == '94') * refraction_corse_tipce_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_ht + (accise_sp_95_ticpe / 100)
        prix_essence_sp95_ttc_sortie = prix_essence_sp95_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc_sortie

    def formula_2002(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        code_region = menage('code_region', period)
        accise_super95 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        refraction_corse_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        accise_sp_95_ticpe = accise_super95 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98) - ((code_region == '94') * refraction_corse_tipce_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_ht + (accise_sp_95_ticpe / 100)
        prix_essence_sp95_ttc_sortie = prix_essence_sp95_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc_sortie

    def formula(menage, period, parameters):
        prix_essence_sp95_ht = menage('prix_essence_sp95_ht', period)
        code_region = menage('code_region', period)
        accise_super95 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        accise_sp_95_ticpe = accise_super95 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_hors_tva = prix_essence_sp95_ht + (accise_sp_95_ticpe / 100)
        prix_essence_sp95_ttc_sortie = prix_essence_sp95_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc_sortie


class prix_essence_sp95_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_ttc = prix_essence_sp95_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc
        
    def formula_2023(menage, period):
        return menage('prix_essence_sp95_ttc_sortie', period)


class prix_essence_sp98_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        code_region = menage('code_region', period)
        taux_conversion_essences = parameters(period).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_essences

        accise_essences_mwh = parameters(period).imposition_indirecte.produits_energetiques.accise_energie_metropole.essences
        accise_essences_hectolitre = accise_essences_mwh * taux_conversion_essences

        major_regionale_ticpe_super_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super_hectolitre = np.fromiter(
            (
                getattr(major_regionale_ticpe_super_mwh, region_cell, 0) * taux_conversion_essences
                for region_cell in code_region),
            dtype=np.float32)

        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp95_sp98_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98_hectolitre = np.fromiter(
            (
                getattr(affectation_ticpe_sp95_sp98_hectolitre, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)

        major_mobilites_tipce_sp98_mwh = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_sp98
        major_mobilites_tipce_sp98_hectolitre = major_mobilites_tipce_sp98_mwh * taux_conversion_essences

        refraction_corse_tipce_sp98_mwh = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        refraction_corse_tipce_sp98_hectolitre = refraction_corse_tipce_sp98_mwh * taux_conversion_essences

        accise_sp_98_ticpe = accise_essences_hectolitre + majoration_ticpe_super_hectolitre - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98_hectolitre) + ((code_region == '11') * major_mobilites_tipce_sp98_hectolitre) - ((code_region == '94') * refraction_corse_tipce_sp98_hectolitre)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_ht + (accise_sp_98_ticpe / 100)
        prix_essence_sp98_ttc_sortie = prix_essence_sp98_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc_sortie

    def formula_2017(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        code_region = menage('code_region', period)
        accise_super98 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        major_mobilites_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.majoration_ile_de_france_mobilites_ticpe.major_mobilites_tipce_sp95_sp98
        refraction_corse_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        accise_sp_98_ticpe = accise_super98 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98) + ((code_region == '11') * major_mobilites_tipce_sp95_sp98) - ((code_region == '94') * refraction_corse_tipce_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_ht + (accise_sp_98_ticpe / 100)
        prix_essence_sp98_ttc_sortie = prix_essence_sp98_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc_sortie

    def formula_2002(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        code_region = menage('code_region', period)
        accise_super98 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        refraction_corse_tipce_sp95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_sp98
        accise_sp_98_ticpe = accise_super98 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98) - ((code_region == '94') * refraction_corse_tipce_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_ht + (accise_sp_98_ticpe / 100)
        prix_essence_sp98_ttc_sortie = prix_essence_sp98_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc_sortie

    def formula(menage, period, parameters):
        prix_essence_sp98_ht = menage('prix_essence_sp98_ht', period)
        code_region = menage('code_region', period)
        accise_super98 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_regionale_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.majoration_regionale_ticpe_sp95_sp98_sp95_e10
        majoration_ticpe_super = np.fromiter(
            (
                getattr(major_regionale_ticpe_super, region_cell, 0)
                for region_cell in code_region),
            dtype=np.float32)
        maximum_value_affectation = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98.maximum_value_affectation
        affectation_ticpe_sp_95_sp98 = parameters(period).imposition_indirecte.produits_energetiques.affectation_regionale_ticpe_sp95_sp98
        affectation_regionale_ticpe_sp95_sp98 = np.fromiter(
            (
                getattr(affectation_ticpe_sp_95_sp98, region_cell, maximum_value_affectation)
                for region_cell in code_region),
            dtype=np.float32)
        accise_sp_98_ticpe = accise_super98 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_sp98)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_hors_tva = prix_essence_sp98_ht + (accise_sp_98_ticpe / 100)
        prix_essence_sp98_ttc_sortie = prix_essence_sp98_hors_tva * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc_sortie


class prix_essence_sp98_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_ttc = prix_essence_sp98_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc
        
    def formula_2023(menage, period):
        return menage('prix_essence_sp98_ttc_sortie', period)


class prix_essence_super_plombe_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period, parameters):
        prix_essence_super_plombe_ht = menage('prix_essence_super_plombe_ht', period)
        code_region = menage('code_region', period)
        accise_super_plombe_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        refraction_corse_tipce_super_plombe = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_super_plombe
        super_plombe_ticpe = (accise_super_plombe_ticpe / 100) - ((code_region == '94') * refraction_corse_tipce_super_plombe)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_super_plombe_hors_tva = prix_essence_super_plombe_ht + (super_plombe_ticpe / 100)
        prix_essence_super_plombe_ttc_sortie = prix_essence_super_plombe_hors_tva * (1 + taux_plein_tva)
        return prix_essence_super_plombe_ttc_sortie


class prix_essence_e85_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre à la pompe"
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        accise_e85_mwh = parameters(period.start).imposition_indirecte.produits_energetiques.accise_energie_metropole.superethanol_e85
        taux_conversion_superethanol_e85 = parameters(period.start).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_superethanol_e85
        accise_e85_hectolitre = accise_e85_mwh * taux_conversion_superethanol_e85
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_e85_hors_tva = prix_essence_e85_ht + (accise_e85_hectolitre / 100)
        prix_essence_e85_ttc_sortie = prix_essence_e85_hors_tva * (1 + taux_plein_tva)
        return prix_essence_e85_ttc_sortie

    def formula_2007(menage, period, parameters):
        prix_essence_e85_ht = menage('prix_essence_e85_ht', period)
        accise_e85_hectolitre = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e_85_utilise_comme_carburant_hectolitre
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_essence_e85_hors_tva = prix_essence_e85_ht + (accise_e85_hectolitre / 100)
        prix_essence_e85_ttc_sortie = prix_essence_e85_hors_tva * (1 + taux_plein_tva)
        return prix_essence_e85_ttc_sortie


class prix_essence_e85_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc_sortie', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_e85_hors_remise_ttc = prix_essence_e85_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_e85_hors_remise_ttc
        
    def formula_2023(menage, period):
        return menage('prix_essence_e85_ttc_sortie', period)


class prix_gpl_carburant_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant  par litre à la pompe'
    definition_period = YEAR
    default_value = 0

    def formula_2022(menage, period, parameters):
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        accise_gpl_carburant_mwh = parameters(period.start).imposition_indirecte.produits_energetiques.accise_energie_metropole.gpl_carburant
        taux_conversion_gpl_carburant = parameters(period.start).imposition_indirecte.produits_energetiques.taux_conversion_euro_par_mwh_a_euro_par_hectolitre.taux_conversion_gpl_carburant
        accise_gpl_carburant_hectolitre = accise_gpl_carburant_mwh * taux_conversion_gpl_carburant
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_tva = prix_gpl_carburant_ht + (accise_gpl_carburant_hectolitre / 100)
        prix_gpl_carburant_ttc_sortie = prix_gpl_carburant_hors_tva * (1 + taux_plein_tva)
        return prix_gpl_carburant_ttc_sortie

    def formula(menage, period, parameters):
        prix_gpl_carburant_ht = menage('prix_gpl_carburant_ht', period)
        accise_gpl_carburant_hectolitre = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kg
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_tva = prix_gpl_carburant_ht + (accise_gpl_carburant_hectolitre / 100)
        prix_gpl_carburant_ttc_sortie = prix_gpl_carburant_hors_tva * (1 + taux_plein_tva)
        return prix_gpl_carburant_ttc_sortie


class prix_gpl_carburant_hors_remise_ttc_sortie(Variable):
    value_type = float
    entity = Menage
    label = "prix du GPL TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc_sortie', period)
        aide_exceptionnelle_gpl_carburant_100kg = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gpl_carburant_100kg
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_remise_ttc = prix_gpl_carburant_ttc + (aide_exceptionnelle_gpl_carburant_100kg / 100) * (1 + taux_plein_tva)
        return prix_gpl_carburant_hors_remise_ttc
