# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import division

from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

import openfisca_france_indirect_taxation
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_data import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.surveys import SurveyScenario


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca_indirect_taxation", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def simulate_df(var_to_be_simulated, year = 2005):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()

    tax_benefit_system = TaxBenefitSystem()
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    simulation = survey_scenario.new_simulation()
    return DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in var_to_be_simulated

            ])
        )


def wavg(groupe, var):
    '''
    Fonction qui calcule la moyenne pondérée par groupe d'une variable
    '''
    d = groupe[var]
    w = groupe['pondmen']
    return (d * w).sum() / w.sum()


def collapse(dataframe, groupe, var):
    '''
    Pour une variable, fonction qui calcule la moyenne pondérée au sein de chaque groupe.
    '''
    grouped = dataframe.groupby([groupe])
    var_weighted_grouped = grouped.apply(lambda x: wavg(groupe = x, var = var))
    return var_weighted_grouped


def df_weighted_average_grouped(dataframe, groupe, varlist):
    '''
    Agrège les résultats de weighted_average_grouped() en une unique dataframe pour la liste de variable 'varlist'.
    '''
    return DataFrame(
        dict([
            (var, collapse(dataframe, groupe, var)) for var in varlist
            ])
        )


# On va dans ce fichier créer les graphiques permettant de voir les taux d'effort selon trois définition du revenu:
# - revenu total
# - revenu disponible
# - revenu disponible et loyer imputé

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)


    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'decile',
        'revtot',
        'somme_coicop12_conso',
        'ocde10',
        'niveau_de_vie',
        'revtot' ,
        'rev_disponible',
        'rev_disp_loyerimput',
        'montant_tva_total',
        'montant_droit_d_accise_alcool',
        'montant_droit_d_accise_tabac',
        'montant_taxe_assurance',
        'montant_tipp'
        ]



# Taux d'effort par rapport au revenu disponible des ménages en 2005, par taxe indirecte
# et par décile de revenu disponible

     # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2005)

    if year == 2011:
        df.decile[df.decuc == 10 ] = 10

    varlist = ['rev_disponible','montant_tva_total', 'montant_droit_d_accise_alcool', 'montant_droit_d_accise_tabac', 'montant_taxe_assurance', 'montant_tipp']
    Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'decile', varlist = varlist)

    # Example
    list_taux_d_effort = []
    Wconcat['taux_d_effort_tva'] = Wconcat['montant_tva_total'] / Wconcat['rev_disponible']
    list_taux_d_effort.append('taux_d_effort_tva')

    Wconcat['taux_d_effort_alcool'] = Wconcat['montant_droit_d_accise_alcool'] / Wconcat['rev_disponible']
    list_taux_d_effort.append('taux_d_effort_alcool')

    Wconcat['taux_d_effort_tabac'] = Wconcat['montant_droit_d_accise_tabac'] / Wconcat['rev_disponible']
    list_taux_d_effort.append('taux_d_effort_tabac')

    Wconcat['taux_d_effort_assurance'] = Wconcat['montant_taxe_assurance'] / Wconcat['rev_disponible']
    list_taux_d_effort.append('taux_d_effort_assurance')

    Wconcat['taux_d_effort_tipp'] = Wconcat['montant_tipp'] / Wconcat['rev_disponible']
    list_taux_d_effort.append('taux_d_effort_tipp')

    df_to_graph = Wconcat[list_taux_d_effort].copy()
    df_to_graph.columns = ['taux_d_effort_tva', 'taux_d_effort_alcool', 'taux_d_effort_tabac', 'taux_d_effort_assurance', 'taux_d_effort_tipp']

    axes = df_to_graph.plot(
        kind = 'bar',
        stacked = True,
        )
    plt.axhline(0, color = 'k')


