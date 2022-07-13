from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
from openfisca_france_indirect_taxation.variables.taxes_indirectes.prix_carburants_par_region import get_prix_carburant_par_region_par_carburant_par_an_hectolitre

import numpy as np


class prix_gazole_b7_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'prix du gazole B7 ttc par litre'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        code_region = menage('code_region', period)
        prix_gazole_b7_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('Gazole', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gazole_b7_ttc = (prix_gazole_b7_hectolitre_ttc / 100)
        return prix_gazole_b7_ttc


class prix_gazole_b10_ttc(Variable):  # ATTENTION: pas de prix disponible pour gazole B10, on utilise prix du gazole B7
    value_type = float
    entity = Menage
    label = 'prix du gazole B10 ttc par litre'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        code_region = menage('code_region', period)
        prix_gazole_b10_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('Gazole', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gazole_b10_ttc = (prix_gazole_b10_hectolitre_ttc / 100)
        return prix_gazole_b10_ttc


class prix_essence_sp95_e10_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'escence sp95 e10 ttc âr litre"
    definition_period = YEAR
    default_value = 0

    def formula_2009(menage, period):
        code_region = menage('code_region', period)
        prix_essence_sp95_e10_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('E10', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp95_e10_ttc = (prix_essence_sp95_e10_hectolitre_ttc / 100)
        return prix_essence_sp95_e10_ttc


class prix_essence_sp95_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'escence sp95 ttc par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        code_region = menage('code_region', period)
        prix_essence_sp95_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('SP95', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp95_ttc = (prix_essence_sp95_hectolitre_ttc / 100)
        return prix_essence_sp95_ttc


class prix_essence_sp98_ttc(Variable):
    value_type = float
    entity = Menage
    label = "prix de l'escence sp98 ttc par litre"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        code_region = menage('code_region', period)
        prix_essence_sp98_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('SP98', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_sp98_ttc = (prix_essence_sp98_hectolitre_ttc / 100)
        return prix_essence_sp98_ttc


class prix_essence_super_plombe_ttc(Variable):  # ATTENTION: pas prix par région disponible, on garde les prix ttc général de l'IPP. (INSEE)
    value_type = float
    entity = Menage
    label = "prix de l'essence super plombé ttc par litre"
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
    label = "prix de l'essence e85 ttc par litre"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period):
        code_region = menage('code_region', period)
        prix_essence_e85_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('E85', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_essence_e85_ttc = (prix_essence_e85_hectolitre_ttc / 100)
        return prix_essence_e85_ttc


class prix_gpl_carburant_ttc(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        code_region = menage('code_region', period)
        prix_gpl_carburant_hectolitre_ttc = np.fromiter(
            (
                get_prix_carburant_par_region_par_carburant_par_an_hectolitre().get(f'{region_cell}', {}).get('GPLc', {}).get(f'{period}', 0)
                for region_cell in code_region),
            dtype=np.float32)
        prix_gpl_carburant_ttc = (prix_gpl_carburant_hectolitre_ttc / 100)
        return prix_gpl_carburant_ttc
