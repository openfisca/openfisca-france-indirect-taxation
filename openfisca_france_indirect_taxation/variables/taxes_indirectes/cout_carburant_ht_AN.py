import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# prix litre gazole:

class cout_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout total du gazole B7 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        gazole_b7_ticpe = menage('gazole_b7_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b7_hors_tva = cout_gazole_b7_ttc * (1 / (1 + taux_plein_tva) )
        gazole_b7_ht = Cout_gazole_b7_hors_tva - gazole_b7_ticpe
        return gazole_b7_ht

class cout_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout total du gazole B10 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        gazole_b10_ticpe = menage('gazole_b10_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b10_hors_tva = cout_gazole_b10_ttc * (1 / (1 + taux_plein_tva) )
        gazole_b10_ht = Cout_gazole_b10_hors_tva - gazole_b10_ticpe
        return gazole_b10_ht

# prix litre essence:

class cout_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout total de l'essence SP95 E10 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        essence_sp95_e10_ticpe = menage('essence_sp95_e10_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_e10_hors_tva = cout_essence_sp95_e10_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_sp95_e10_ht = Cout_essence_sp95_e10_hors_tva - essence_sp95_e10_ticpe
        return cout_essence_sp95_e10_ht

class prix_litre_essence_SP95_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        region = menage('region', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_sp_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        major_regionale_ticpe_super = np.fromiter(
            (
                getattr(major_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        majoration_ticpe_super_hectolitre = accise_sp_e10 + major_regionale_ticpe_super
        super_95_ttc_hectolitre = parameters(period).prix_carburants.super_95_ttc   ### à modifier avec le nouveau CSV
        essence_SP95_ht = ((super_95_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_super_hectolitre / 100)
        return essence_SP95_ht

class prix_litre_essence_SP98_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        region = menage('region', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_sp_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_95_98
        major_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        major_regionale_ticpe_super = np.fromiter(
            (
                getattr(major_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        majoration_ticpe_super_hectolitre = accise_sp_e10 + major_regionale_ticpe_super
        super_98_ttc_hectolitre = parameters(period).prix_carburants.super_98_ttc   ### à modifier avec le nouveau CSV
        essence_SP98 = ((super_98_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_super_hectolitre / 100)
        return essence_SP98

class prix_litre_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombe ht"
    definition_period = YEAR
    end = "2006-12-31"
    default_value = 0
    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        ticpe_super_plombe_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        super_plombe_ttc_hectolitre = parameters(period).prix_carburants.super_plombe_ttc   ### à modifier avec le nouveau CSV
        essence_super_plombe_ht = ((super_plombe_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (ticpe_super_plombe_hectolitre / 100)
        return essence_super_plombe_ht

class prix_litre_essence_E85_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        ticpe_essence_E85_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e_85_utilise_comme_carburant_hectolitre
        essence_E85_hectolitre_ttc = parameters(period).prix_carburants.super_95_ttc    ### à modifier avec le nouveau CSV (pas le bon)
        essence_E85_ht = ((essence_E85_hectolitre_ttc /100) / (1 + taux_plein_tva) ) - (ticpe_essence_E85_hectolitre / 100)
        return essence_E85_ht

# prix combustibles liquides

class prix_litre_gplc_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gplc ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        ticpe_gplc_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kgazole_fioul_domestique_hectolitre
        gplc_ttc_hectolitre = parameters(period).prix_carburants.gplc_ttc   ### à modifier avec le nouveau CSV
        print('taux_plein_tva',taux_plein_tva)
        gplc_ht = ((gplc_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (ticpe_gplc_hectolitre / 100)
        return gplc_ht