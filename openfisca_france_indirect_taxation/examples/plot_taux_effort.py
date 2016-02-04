# -*- coding: utf-8 -*-


from __future__ import division

import pandas
import seaborn

from openfisca_france_indirect_taxation.examples.utils_example import (
    create_survey_scenario,
    simulate,
    graph_builder_line_percent,
    save_dataframe_to_graph
    )
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))

if __name__ == '__main__':
    #  Création des graphiques des taux d'effort selon trois définition du revenu:
    # - revenu total
    # - revenu disponible
    # - revenu disponible et loyer imputé

    # Liste des variables que l'on veut simuler
    variables = [
        'revtot',
        'somme_coicop12_conso',
        'rev_disponible',
        'rev_disp_loyerimput',
        'total_taxes_indirectes'
        ]

    # 1 calcul taux d'effort sur le revenu total
    # Constition d'une base de données agrégée par décile

    for revenu in ['revtot', 'rev_disponible', 'rev_disp_loyerimput']:
        taux_d_effort = pandas.DataFrame()
        for year in [2000, 2005, 2011]:
            survey_scenario = create_survey_scenario(year)
            simulation = survey_scenario.new_simulation()
            pivot_table = pandas.DataFrame()
            for values in ['revtot', 'total_taxes_indirectes', 'rev_disponible', 'rev_disp_loyerimput']:
                pivot_table = pandas.concat([
                    pivot_table,
                    survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'])
                    ])
            df = pivot_table.T

            df.rev_disponible = df.rev_disponible * 1.33

            taux_d_effort['taux_d_effort_{}_{}'.format(revenu, year)] = \
                df['total_taxes_indirectes'] / df[revenu]

        graph_builder_line_percent(taux_d_effort, 1, 1)

        # save_dataframe_to_graph(
        #    taux_d_effort['taux_d_effort_{}_{}'.format(revenu, year)],
        #    'taux_d_effort_{}_{}.csv'.format(revenu, year)
        #    )
