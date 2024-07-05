from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
from openfisca_france_indirect_taxation.parameters.prix_carburants import get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre
from openfisca_france_indirect_taxation.parameters.prix_carburants import get_prix_carburant_par_annee_par_carburant_en_hectolitre

import numpy as np


class prix_gazole_b7_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 TTC par litre'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        code_region = menage('code_region', period)
        prix_gazole_b7_hectolitre_ttc = np.fromiter(
            (
                parameters(period.start).prix_carburants.diesel_ttc if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('Gazole', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gazole_b7_ttc = (prix_gazole_b7_hectolitre_ttc / 100)
        return prix_gazole_b7_ttc


class prix_gazole_b7_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B7 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b7_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b7_ttc = menage('prix_gazole_b7_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b7_hors_remise_ttc = prix_gazole_b7_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b7_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gazole_b7_ttc', period)


class prix_gazole_b10_ttc(Variable):  # ATTENTION: pas de prix disponible pour gazole B10, on utilise prix du gazole B7
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 TTC par litre'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        code_region = menage('code_region', period)
        prix_gazole_b10_hectolitre_ttc = np.fromiter(
            (
                parameters(period.start).prix_carburants.diesel_ttc if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('Gazole', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gazole_b10_ttc = (prix_gazole_b10_hectolitre_ttc / 100)
        return prix_gazole_b10_ttc


class prix_gazole_b10_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix du gazole B10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gazole_b10_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_gazole_b10_ttc = menage('prix_gazole_b10_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gazole_b10_hors_remise_ttc = prix_gazole_b10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_gazole_b10_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gazole_b10_ttc', period)


class prix_essence_sp95_e10_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period, parameters):
        code_region = menage('code_region', period)
        prix_essence_sp95_e10_hectolitre_ttc = np.fromiter(
            (
                parameters(period.start).prix_carburants.super_95_e10_ttc if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('E10', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp95_e10_ttc = (prix_essence_sp95_e10_hectolitre_ttc / 100)
        return prix_essence_sp95_e10_ttc


class prix_essence_sp95_e10_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 E10 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_e10_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_e10_ttc = menage('prix_essence_sp95_e10_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_e10_ttc = prix_essence_sp95_e10_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_e10_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_e10_ttc', period)


class prix_essence_sp95_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        code_region = menage('code_region', period)
        prix_essence_sp95_hectolitre_ttc = np.fromiter(
            (
                parameters(period.start).prix_carburants.super_95_ttc if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('SP95', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp95_ttc = (prix_essence_sp95_hectolitre_ttc / 100)
        return prix_essence_sp95_ttc


class prix_essence_sp95_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP95 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp95_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp95_ttc = menage('prix_essence_sp95_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp95_ttc = prix_essence_sp95_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp95_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp95_ttc', period)


class prix_essence_sp98_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        code_region = menage('code_region', period)
        prix_essence_sp98_hectolitre_ttc = np.fromiter(
            (
                parameters(period.start).prix_carburants.super_98_ttc if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('SP98', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp98_ttc = (prix_essence_sp98_hectolitre_ttc / 100)
        return prix_essence_sp98_ttc


class prix_essence_sp98_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence SP98 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_sp98_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_essence_sp98_ttc = menage('prix_essence_sp98_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_sp98_ttc = prix_essence_sp98_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_sp98_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_sp98_ttc', period)


class prix_essence_super_plombe_ttc(Variable):  # ATTENTION: pas prix par région disponible, on garde les prix TTC général de l'IPP. (INSEE)
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé TTC par litre"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"

    def formula(menage, period, parameters):
        prix_essence_essence_super_plombe_hectolitre_ttc = parameters(period).prix_carburants.super_plombe_ttc
        prix_essence_super_plombe_ttc = (prix_essence_essence_super_plombe_hectolitre_ttc / 100)
        return prix_essence_super_plombe_ttc


class prix_essence_e85_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        code_region = menage('code_region', period)
        prix_essence_e85_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_annee_par_carburant_en_hectolitre().get('E85', {}).get(f'{period}', 0) if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('E85', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_e85_ttc = (prix_essence_e85_hectolitre_ttc / 100)
        return prix_essence_e85_ttc


class prix_essence_e85_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'essence E85 TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_essence_e85_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_essence_e85_ttc = menage('prix_essence_e85_ttc', period)
        aide_exceptionnelle_gazole_essence_hl = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gazole_essence_hl
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_essence_e85_hors_remise_ttc = prix_essence_e85_ttc + (aide_exceptionnelle_gazole_essence_hl / 100) * (1 + taux_plein_tva)
        return prix_essence_e85_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_essence_e85_ttc', period)


class prix_gpl_carburant_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gaz de pétrole liquéfié - carburant TTC'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        code_region = menage('code_region', period)
        prix_gpl_carburant_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_annee_par_carburant_en_hectolitre().get('GPLc', {}).get(f'{period}', 0) if region_cell == "99" else get_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre().get(f'{region_cell}', {}).get('GPLc', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gpl_carburant_ttc = (prix_gpl_carburant_hectolitre_ttc / 100)
        return prix_gpl_carburant_ttc


class prix_gpl_carburant_hors_remise_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix du GPL TTC par litre si la remise n'avait pas eu lieu"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        return menage('prix_gpl_carburant_ttc', period)

    def formula_2022(menage, period, parameters):
        prix_gpl_carburant_ttc = menage('prix_gpl_carburant_ttc', period)
        aide_exceptionnelle_gpl_carburant_100kg = parameters(period.start).imposition_indirecte.produits_energetiques.aide_exceptionnelle_carburant.gpl_carburant_100kg
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        prix_gpl_carburant_hors_remise_ttc = prix_gpl_carburant_ttc + (aide_exceptionnelle_gpl_carburant_100kg / 100) * (1 + taux_plein_tva)
        return prix_gpl_carburant_hors_remise_ttc

    def formula_2023(menage, period):
        return menage('prix_gpl_carburant_ttc', period)
