# -*- coding: utf-8 -*-

# Import de modules généraux


import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette('Set2', 12))

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'tva_taux_plein',
        'tva_taux_intermediaire',
        'tva_taux_reduit',
        'tva_taux_super_reduit',
        'rev_disponible',
        ]
    for year in [2000, 2005, 2011]:
        survey_scenario = SurveyScenario.create(year = year)
        pivot_table = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'])
                ])
        taxes_indirectes = pivot_table.T

        taxes_indirectes['Part TVA taux super réduit'] = \
            taxes_indirectes['tva_taux_super_reduit'] / taxes_indirectes['rev_disponible']
        taxes_indirectes['Part TVA taux réduit'] = \
            taxes_indirectes['tva_taux_reduit'] / taxes_indirectes['rev_disponible']
        taxes_indirectes['Part TVA taux intermédiaire'] = \
            taxes_indirectes['tva_taux_intermediaire'] / taxes_indirectes['rev_disponible']
        taxes_indirectes['Part TVA taux plein'] = \
            taxes_indirectes['tva_taux_plein'] / taxes_indirectes['rev_disponible']

        df_to_graph = taxes_indirectes[['Part TVA taux plein', 'Part TVA taux intermédiaire',
            'Part TVA taux super réduit', 'Part TVA taux réduit']]

        # Graphe par décile de revenu par uc de la ventilation des taux de taxation
        graph_builder_bar(df_to_graph)
