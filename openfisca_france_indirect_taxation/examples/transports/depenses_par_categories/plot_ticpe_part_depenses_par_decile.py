# -*- coding: utf-8 -*-

# L'objectif est d'exprimer pour chaque décile de revenu la part que représente les dépenses en TICPE sur l'ensemble
# du revenu. Ce revenu prend trois définitions : le revenu total, le revenu disponible, ou l'ensemble des dépenses du
# ménage. Ces calculs sont réalisés pour 2000, 2005 et 2011, et les parts spécifiques à l'essence et au diesel sont
# spécifiées.

# Import de modules généraux


import pandas
import seaborn
from pandas import concat

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_line
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    simulated_variables = [
        'revtot',
        'somme_coicop12_conso',
        'rev_disp_loyerimput',
        'ticpe_totale',
        'diesel_ticpe',
        'essence_ticpe'
        ]

    # Formation des bases de données, dépenses moyennes en TICPE par décile de revenu, que l'on divise ensuite par le
    # revenu. On réalise une boucle dans une boucle, i.e. toutes les années pour chaque type de carburant.
    for element in ['ticpe_totale', 'diesel_ticpe', 'essence_ticpe']:
        revtot = None
        rev_disp_loyerimput = None
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

            part_revtot = pandas.DataFrame()
            part_revtot['part ' + element.replace('_', ' ') + ' revtot {}'.format(year)] = \
                df[element] / df['revtot']

            part_rev_loyerimput = pandas.DataFrame()
            part_rev_loyerimput['part ' + element.replace('_', ' ') + ' rev disp loyerimput {}'.format(year)] = \
                df[element] / df['rev_disp_loyerimput']

            part_depenses = pandas.DataFrame()
            part_depenses['part ' + element.replace('_', ' ') + ' depenses {}'.format(year)] = \
                df[element] / df['somme_coicop12_conso']

            if revtot is not None:
                revtot = concat([revtot, part_revtot], axis = 1)
            else:
                revtot = part_revtot

            if rev_disp_loyerimput is not None:
                rev_disp_loyerimput = concat([rev_disp_loyerimput, part_rev_loyerimput], axis = 1)
            else:
                rev_disp_loyerimput = part_rev_loyerimput

            if depenses is not None:
                depenses = concat([depenses, part_depenses], axis = 1)
            else:
                depenses = part_depenses

        graph_builder_line(revtot)
        graph_builder_line(rev_disp_loyerimput)
        graph_builder_line(depenses)
