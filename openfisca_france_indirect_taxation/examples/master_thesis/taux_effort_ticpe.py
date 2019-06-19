# -*- coding: utf-8 -*-

# Import de modules généraux
from __future__ import division

import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar_percent, save_dataframe_to_graph, \
    dataframe_by_group
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


def plot_taux_effort_ticpe():
    simulated_variables = [
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe',
        'rev_disp_loyerimput',
        'depenses_tot'
        ]

    year = 2016
    data_year = 2011
    survey_scenario = SurveyScenario.create(year = year, data_year = data_year)

    for category in ['niveau_vie_decile']:
        taxe_indirectes = dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =True)

        for revenu in ['rev_disp_loyerimput', 'depenses_tot']:
            list_part_taxes = []
            for taxe in ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe']:
                taxe_indirectes['part_' + taxe] = (
                    taxe_indirectes[taxe] / taxe_indirectes[revenu]
                    )
                'list_part_taxes_{}'.format(taxe)
                list_part_taxes.append('part_' + taxe)

            df_to_graph = taxe_indirectes[list_part_taxes]

            print '''Contributions aux différentes taxes indirectes en part de {0},
                par décile de revenu en {1}'''.format(revenu, year)
            graph_builder_bar_percent(df_to_graph)
            save_dataframe_to_graph(df_to_graph, 'Monetary/effort_rate_ticpe_over_{}.csv'.format(revenu))


if __name__ == '__main__':
    plot_taux_effort_ticpe()
