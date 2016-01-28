# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 11:09:50 2016

@author: thomas.douenne
"""


# Ce script a pour objectif de décrire pour chaque décile de revenu la consommation annuelle moyenne de carburants,
# ainsi que les dépenses moyennes pour la TICPE

# Import de modules généraux
from __future__ import division

import pandas
import seaborn
from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.example.utils_example import graph_builder_line
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    # Sélection des variables que l'on veut simuler
    simulated_variables = [
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe',
        'consommation_ticpe',
        'diesel_depenses',
        'essence_depenses'
        ]

    # Le but est de construire un graphique représentant les 3 années pour chaque variable. On fait donc une boucle
    # dans une boucle.
    to_graph = ['ticpe totale ', 'ticpe diesel ', 'ticpe essence ', 'depenses carburants ', 'depenses diesel ',
                'depenses essence ']
    for element in to_graph:
        depenses = None
        for year in [2000, 2005, 2011]:
            survey_scenario = SurveyScenario.create(year = year)
            pivot_table = pandas.DataFrame()
            for values in simulated_variables:
                pivot_table = pandas.concat([
                    pivot_table,
                    survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'])
                    ])
            df = pivot_table.T
            df.rename(columns = {'ticpe_totale': 'ticpe totale {}'.format(year),
                'diesel_ticpe': 'ticpe diesel {}'.format(year),
                'essence_ticpe': 'ticpe essence {}'.format(year),
                'consommation_ticpe': 'depenses carburants {}'.format(year),
                'diesel_depenses': 'depenses diesel {}'.format(year),
                'essence_depenses': 'depenses essence {}'.format(year)},
                inplace = True)

            if depenses is not None:
                depenses = concat(
                    [depenses, df[element + '{}'.format(year)]], axis = 1)
            else:
                depenses = df[element + '{}'.format(year)]
        graph_builder_line(depenses)
