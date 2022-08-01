from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

import numpy as np


# TICPE carburant


# TICPE gazole:


class gazole_b7_ticpe(Variable):
    value_type = float
    entity = Menage
    label = 'Accise (ex-TICPE) prélevée sur le diesel (gazole B7)'
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
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
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        montant_gazole_b7_ticpe = nombre_litres_gazole_b7 * (accise_gazole_b7_total / 100)
        return montant_gazole_b7_ticpe

    def formula(menage, period, parameters):
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
        nombre_litres_gazole_b7 = menage('nombre_litres_gazole_b7', period)
        montant_gazole_b7_ticpe = nombre_litres_gazole_b7 * (accise_gazole_b7_total / 100)
        return montant_gazole_b7_ticpe


class gazole_b10_ticpe(Variable):
    value_type = float
    entity = Menage
    label = 'Accise (ex-TICPE) prélevée sur le diesel (gazole B10)'
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
        accise_gazole_b10 = parameters(period).imposition_indirecte.produits_energetiques.ticpe.gazol_b_10_hectolitre
        nombre_litres_gazole_b10 = menage('nombre_litres_gazole_b10', period)
        montant_gazole_b10_ticpe = nombre_litres_gazole_b10 * (accise_gazole_b10 / 100)
        return montant_gazole_b10_ticpe


# TICPE gazole total:


class gazole_ticpe_total(Variable):
    value_type = float
    entity = Menage
    label = 'Accise (ex-TICPE) prélevée sur les différents diesels'
    definition_period = YEAR

    def formula_2017(menage, period):
        gazole_B7_ticpe = menage('gazole_b7_ticpe', period)
        gazole_B10_ticpe = menage('gazole_b10_ticpe', period)
        gazole_ticpe = (gazole_B7_ticpe + gazole_B10_ticpe)
        return gazole_ticpe

    def formula(menage, period):
        gazole_B7_ticpe = menage('gazole_b7_ticpe', period)
        gazole_ticpe = gazole_B7_ticpe
        return gazole_ticpe


# TICPE essence:


class essence_sp95_e10_ticpe(Variable):  # paru au Journal Officiel le 31 janvier 2009, a autorisé sa distribution sur le marché français depuis le 1er avril 2009.
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur l'essence sans plomb 95 E10 en station service"
    definition_period = YEAR

    def formula_2019(menage, period, parameters):
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
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        montant_sp_e10_ticpe = nombre_litres_essence_sp95_e10 * (accise_sp_e10_ticpe / 100)
        return montant_sp_e10_ticpe

    def formula_2017(menage, period, parameters):
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
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        montant_sp_e10_ticpe = nombre_litres_essence_sp95_e10 * (accise_sp_e10_ticpe / 100)
        return montant_sp_e10_ticpe

    def formula_2009(menage, period, parameters):
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
        nombre_litres_essence_sp95_e10 = menage('nombre_litres_essence_sp95_e10', period)
        montant_sp_e10_ticpe = nombre_litres_essence_sp95_e10 * (accise_sp_e10_ticpe / 100)
        return montant_sp_e10_ticpe


class essence_sp95_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur l'essence sans plomb 95 en station service"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
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
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        montant_sp95_ticpe = nombre_litres_essence_sp95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe

    def formula_2002(menage, period, parameters):
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
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        montant_sp95_ticpe = nombre_litres_essence_sp95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe

    def formula(menage, period, parameters):
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
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        montant_sp95_ticpe = nombre_litres_essence_sp95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe


class essence_sp98_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur l'essence sans plomb 98 en station service"
    definition_period = YEAR

    def formula_2017(menage, period, parameters):
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
        nombre_litres_essence_sp98 = menage('nombre_litres_essence_sp98', period)
        montant_sp98_ticpe = nombre_litres_essence_sp98 * (accise_sp_98_ticpe / 100)
        return montant_sp98_ticpe

    def formula_2002(menage, period, parameters):
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
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        montant_sp95_ticpe = nombre_litres_essence_sp95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe

    def formula(menage, period, parameters):
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
        nombre_litres_essence_sp95 = menage('nombre_litres_essence_sp95', period)
        montant_sp95_ticpe = nombre_litres_essence_sp95 * (accise_sp_95_ticpe / 100)
        return montant_sp95_ticpe


class essence_super_plombe_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur l'essence super plombé en station service"
    definition_period = YEAR
    end = '2006-12-31'

    def formula_2002(menage, period, parameters):
        code_region = menage('code_region', period)
        accise_super_plombe_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        refraction_corse_tipce_super_plombe = parameters(period).imposition_indirecte.produits_energetiques.refraction_corse_ticpe.refraction_corse_tipce_super_plombe
        nombre_litres_essence_super_plombe = menage('nombre_litres_essence_super_plombe', period)
        montant_super_plombe_ticpe = nombre_litres_essence_super_plombe * (accise_super_plombe_ticpe / 100) - ((code_region == '94') * refraction_corse_tipce_super_plombe)
        return montant_super_plombe_ticpe

    def formula(menage, period, parameters):
        accise_super_plombe_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        nombre_litres_essence_super_plombe = menage('nombre_litres_essence_super_plombe', period)
        montant_super_plombe_ticpe = nombre_litres_essence_super_plombe * (accise_super_plombe_ticpe / 100)
        return montant_super_plombe_ticpe


class essence_e85_ticpe(Variable):  # Il a été introduit en 2007 sur le marché français.
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur l'essence super ethanol 85 en station service"
    definition_period = YEAR

    def formula_2007(menage, period, parameters):
        accise_e85 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e_85_utilise_comme_carburant_hectolitre
        nombre_litres_essence_e85 = menage('nombre_litres_essence_e85', period)
        montant_e85_ticpe = nombre_litres_essence_e85 * (accise_e85 / 100)
        return montant_e85_ticpe


# TICPE essence total:


class essence_ticpe_total(Variable):
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur les différents essenses"
    definition_period = YEAR

    def formula_2009(menage, period):
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        essence_sp95_E10_ticpe = menage('essence_sp95_e10_ticpe', period)
        essence_ticpe = (essence_sp95_ticpe + essence_sp98_ticpe + essence_e85_ticpe + essence_sp95_E10_ticpe)
        return essence_ticpe

    def formula_2007(menage, period):
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        essence_ticpe = (essence_sp95_ticpe + essence_sp98_ticpe + essence_e85_ticpe)
        return essence_ticpe

    def formula_1990(menage, period):
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        super_plombe_ticpe = menage('essence_super_plombe_ticpe', period)
        essence_ticpe = (essence_sp95_ticpe + essence_sp98_ticpe + super_plombe_ticpe)
        return essence_ticpe


# TICPE combustibles liquides:


class gpl_carburant_ticpe(Variable):
    value_type = float
    entity = Menage
    label = "Accise (ex-TICPE) prélevée sur le GPL carburant en station service"
    definition_period = YEAR

    def formula(menage, period, parameters):
        nombre_litres_gpl_carburant = menage('nombre_litres_gpl_carburant', period)
        accise_combustibles_liquides = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.autres_gaz_petrole_liquefies_utilises_comme_carburants_autres_100kg
        combustibles_liquides_ticpe = nombre_litres_gpl_carburant * (accise_combustibles_liquides / 100)

        return combustibles_liquides_ticpe


# total taxes energies (ticpe diesel + ticpe essence + ticpe GPL-c)


class ticpe_carburant_total(Variable):
    value_type = float
    entity = Menage
    label = 'Accise (ex-TICPE) prélevée sur les carburants en station service'
    definition_period = YEAR

    def formula(menage, period):
        essence_ticpe_total = menage('essence_ticpe_total', period)
        gazole_ticpe_total = menage('gazole_ticpe_total', period)
        gpl_carburant_ticpe = menage('gpl_carburant_ticpe', period)
        ticpe_total_carburant = gazole_ticpe_total + essence_ticpe_total + gpl_carburant_ticpe
        return ticpe_total_carburant
