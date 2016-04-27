# -*- coding: utf-8 -*-

# Import de modules généraux
from __future__ import division

import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


if __name__ == '__main__':

    simulated_variables = [
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe',
        'rev_disp_loyerimput',
        'somme_coicop12',
        ]
    year = 2014
    data_year = 2011
    survey_scenario = SurveyScenario.create(year = year, data_year = data_year)
    for category in ['niveau_vie_decile', 'age_group_pr', 'strate_agrege']:
        pivot_table = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = ['{}'.format(category)])
                ])
        taxe_indirectes = pivot_table.T

        for revenu in ['rev_disp_loyerimput', 'somme_coicop12']:
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
            graph_builder_bar(df_to_graph)
            save_dataframe_to_graph(
                df_to_graph, 'Taxes_indirectes/effort_rate_ticpe_on_{0}_by_{1}.csv'.format(revenu, category)
                )
