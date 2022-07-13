from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

import numpy as np


class prix_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 ht par litre'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc', period)
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
        prix_gazole_b7_hors_tva = prix_gazole_b7_ttc * (1 / (1 + taux_plein_tva))
        prix_gazole_b7_ht = prix_gazole_b7_hors_tva - (accise_gazole_b7_total / 100)
        return prix_gazole_b7_ht


class prix_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 ht par litre'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc', period)
        accise_gazole_b10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazol_b_10_hectolitre
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_tva = prix_gazole_b10_ttc * (1 / (1 + taux_plein_tva))
        prix_gazole_b10_ht = prix_gazole_b10_hors_tva - (accise_gazole_b10 / 100)
        return prix_gazole_b10_ht


class prix_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 ht par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc', period)
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
        refraction_corse_tipce_sp95_E10 = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_sp95_E10
        accise_sp_e10_ticpe = accise_super_e10 + majoration_ticpe_super - (maximum_value_affectation - affectation_regionale_ticpe_sp95_e10) + ((code_region == '11') * major_mobilites_tipce_sp95_e10) - ((code_region == '94') * refraction_corse_tipce_sp95_E10)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_hors_tva = prix_essence_sp95_e10_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp95_e10_ht = prix_essence_sp95_e10_hors_tva - (accise_sp_e10_ticpe / 100)
        return prix_essence_sp95_e10_ht


class prix_essence_sp95_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 ht par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc', period)
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
        prix_essence_sp95_hors_tva = prix_essence_sp95_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp95_ht = prix_essence_sp95_hors_tva - (accise_sp_95_ticpe / 100)
        return prix_essence_sp95_ht


class prix_essence_sp98_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 ht par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc', period)
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

        prix_essence_sp98_hors_tva = prix_essence_sp98_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_sp98_ht = prix_essence_sp98_hors_tva - (accise_sp_98_ticpe / 100)
        return prix_essence_sp98_ht


class prix_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé ht par litre"
    definition_period = YEAR
    default_value = 0
    end = "2017-01-01"

    def formula(menage, period, parameters):
        prix_essence_super_plombe_ttc = menage('prix_essence_super_plombe_ttc', period)
        code_region = menage('code_region', period)
        accise_super_plombe_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        refraction_corse_tipce_super_plombe = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_super_plombe
        super_plombe_ticpe = (accise_super_plombe_ticpe / 100) - ((code_region == '94') * refraction_corse_tipce_super_plombe)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_super_plombe_hors_tva = prix_essence_super_plombe_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_super_plombe_ht = prix_essence_super_plombe_hors_tva - (super_plombe_ticpe / 100)
        return prix_essence_super_plombe_ht


class prix_essence_e85_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence e85 ht par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc', period)
        accise_e85 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e_85_utilise_comme_carburant_hectolitre
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal

        prix_essence_e85_hors_tva = prix_essence_e85_ttc * (1 / (1 + taux_plein_tva))
        prix_essence_e85_ht = prix_essence_e85_hors_tva - (accise_e85 / 100)
        return prix_essence_e85_ht


class prix_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant ht par litre'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc', period)
        accise_combustibles_liquides = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kg
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_tva = prix_gpl_carburant_ttc * (1 / (1 + taux_plein_tva))
        prix_gpl_carburant_ht = prix_gpl_carburant_hors_tva - (accise_combustibles_liquides / 100)
        return prix_gpl_carburant_ht
