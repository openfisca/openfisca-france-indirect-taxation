# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 16:48:09 2015

@author: germainmarchand
"""

from __future__ import division

from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker #TODO: axes en pourcentage
import numpy as np

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


def simulate_df(var_to_be_simulated, year = 2000):
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

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Exemple: graphe par décile de revenu par uc de la ventilation de la consommation
    # selon les postes agrégés de la CN
    # Liste des coicop agrégées en 12 postes
    list_coicop12 = []
    for coicop12_index in range(1, 9):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))
    # Liste des variables que l'on veut simuler
    var_to_be_simulated = [
        'ident_men',
        'pondmen',
        'decuc',
        'age',
        'decile',
        'montant_tva_taux_plein',
        'montant_tva_taux_intermediaire',
        'montant_tva_taux_reduit',
        'montant_tva_taux_super_reduit',
        'montant_tva_total',
        'revtot',
        'somme_coicop12_conso',
        'ocde10',
        'niveau_de_vie',
        ]
    # Merge des deux listes
    var_to_be_simulated += list_coicop12

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate_df(var_to_be_simulated = var_to_be_simulated)
    var_to_concat = ['montant_tva_taux_plein', 'montant_tva_taux_intermediaire', 'montant_tva_taux_reduit', 'montant_tva_taux_super_reduit', 'montant_tva_total']
    Wconcat = df_weighted_average_grouped(dataframe = df, groupe = 'decuc', varlist = var_to_concat)

    list_part_TVA = []
    Wconcat['part_tva_taux_plein']=Wconcat['montant_tva_taux_plein']/Wconcat['montant_tva_total']
    list_part_TVA.append('part_tva_taux_plein')
    Wconcat['part_tva_taux_intermediaire']=Wconcat['montant_tva_taux_intermediaire']/Wconcat['montant_tva_total']
    list_part_TVA.append('part_tva_taux_intermediaire')
    Wconcat['part_tva_taux_reduit']=Wconcat['montant_tva_taux_reduit']/Wconcat['montant_tva_total']
    list_part_TVA.append('part_tva_taux_reduit')
    Wconcat['part_tva_taux_super_reduit']=Wconcat['montant_tva_taux_super_reduit']/Wconcat['montant_tva_total']
    list_part_TVA.append('part_tva_taux_super_reduit')


    df_to_graph = Wconcat[list_part_TVA].copy()
    print len(df_to_graph.columns)
    df_to_graph.columns = ['tva_taux_plein', 'tva_taux_intermediaire', 'tva_taux_reduit', 'tva_taux_super_reduit']

    axes = df_to_graph.plot(
        kind = 'bar',
        stacked = True,
        )
    plt.axhline(0, color = 'k')
    def percent_formatter(x, pos = 0):
        return '%1.0f%%' % (100 * x)
        # TODO utiliser format et corriger également ici
        # https://github.com/openfisca/openfisca-matplotlib/blob/master/openfisca_matplotlib/graphs.py#L123
    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))

    # Supprimer la légende du graphique
#    axes.legend(
#        bbox_to_anchor = (1.4, 1.0),
#        ) # TODO: supprimer la légende pour les lignes pointillées et continues
#    plt.show()
    # TODO: analyser, changer les déciles de revenus en déciles de consommation
    # faire un truc plus joli, mettres labels...
