import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

class prix_litre_diesel_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du diesel ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        region = menage('region', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_diesel = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazole
        major_ticpe_diesel = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_gazole
        # major_regionale_ticpe_diesel_region = major_regionale_ticpe_diesel[region]  ##non utilisé à cause du fait que toutes les régions n'existent pas en majoration
        major_regionale_ticpe_diesel = np.fromiter(
            (
                getattr(major_ticpe_diesel, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        majoration_ticpe_diesel_hectolitre = accise_diesel + major_regionale_ticpe_diesel
        diesel_ttc_hectolitre = parameters(period).prix_carburants.diesel_ttc
        diesel_ht = ((diesel_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_diesel_hectolitre / 100)
        return diesel_ht

class prix_litre_super_95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super e10 ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        region = menage('region', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_sp_e10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_e10
        major_ticpe_super = parameters(period).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super
        major_regionale_ticpe_super = np.fromiter(
            (
                getattr(major_ticpe_super, region_cell, 0)
                for region_cell in region
            ),
            dtype=np.float32
        )
        majoration_ticpe_super_hectolitre = accise_sp_e10 + major_regionale_ticpe_super
        super_95_e10_ttc_hectolitre = parameters(period).prix_carburants.super_95_e10_ttc
        sp_e10_ht = ((super_95_e10_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_super_hectolitre / 100)
        return sp_e10_ht

class prix_litre_super_95_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super 95 ht"
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
        super_95_ttc_hectolitre = parameters(period).prix_carburants.super_95_ttc
        super_95_ht = ((super_95_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_super_hectolitre / 100)
        return super_95_ht

class prix_litre_super_98_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super 98 ht"
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
        super_98_ttc_hectolitre = parameters(period).prix_carburants.super_98_ttc
        super_98_ht = ((super_98_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (majoration_ticpe_super_hectolitre / 100)
        return super_98_ht

class prix_litre_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombe ht"
    definition_period = YEAR
    end = "2006-12-31"
    default_value = 0
    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        ticpe_super_plombe_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        super_plombe_ttc_hectolitre = parameters(period).prix_carburants.super_plombe_ttc
        print('taux_plein_tva',taux_plein_tva)
        print('ticpe_super_plombe_hectolitre',ticpe_super_plombe_hectolitre)
        print('super_plombe_ttc_hectolitre',super_plombe_ttc_hectolitre)
        super_plombe_ht = ((super_plombe_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (ticpe_super_plombe_hectolitre / 100)
        return super_plombe_ht

class prix_litre_gplc_ht(Variable):
    value_type = float
    entity = Menage
    label = "prix du gplc ht"
    definition_period = YEAR
    default_value = 0
    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        ticpe_gplc_hectolitre = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre
        gplc_ttc_hectolitre = parameters(period).prix_carburants.gplc_ttc
        print('taux_plein_tva',taux_plein_tva)
        print('ticpe_gplc_hectolitre',ticpe_gplc_hectolitre)
        print('gplc_ttc_hectolitre',gplc_ttc_hectolitre)
        super_plombe_ht = ((gplc_ttc_hectolitre /100) / (1 + taux_plein_tva) ) - (ticpe_gplc_hectolitre / 100)
        return super_plombe_ht