# -*- coding: utf-8 -*-

# Import de modules généraux
from __future__ import division

import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar
from openfisca_france_indirect_taxation.surveys import SurveyScenario

# Import d'une nouvelle palette de couleurs
seaborn.set_palette(seaborn.color_palette("Set2", 12))


if __name__ == '__main__':

    simulated_variables = [
        'tva_total',
        'ticpe_totale',
        'vin_droit_d_accise',
        'biere_droit_d_accise',
        'alcools_forts_droit_d_accise',
        'cigarette_droit_d_accise',
        'cigares_droit_d_accise',
        'tabac_a_rouler_droit_d_accise',
        #'assurance_transport_taxe',
        #'assurance_sante_taxe',
        #'autres_assurances_taxe',
        'revtot',
        'rev_disponible',
        #'somme_coicop12',
        #'taxes_indirectes_total'
        ]
    for year in [2011]: #[2000, 2005, 2011]
        survey_scenario = SurveyScenario.create(year = year)
        pivot_table = pandas.DataFrame()
        for values in simulated_variables:
            pivot_table = pandas.concat([
                pivot_table,
                survey_scenario.compute_pivot_table(values = [values], columns = ['niveau_vie_decile'], period = year)
                ])
        taxe_indirectes = pivot_table.T

        taxe_indirectes['TVA'] = taxe_indirectes['tva_total']
        taxe_indirectes['TICPE'] = taxe_indirectes['ticpe_totale']
        taxe_indirectes[u'Taxes alcools'] = (
            taxe_indirectes['vin_droit_d_accise'] +
            taxe_indirectes['biere_droit_d_accise'] +
            taxe_indirectes['alcools_forts_droit_d_accise']
            ).copy()
        #taxe_indirectes[u'Taxes assurances'] = (
        #    taxe_indirectes['assurance_sante_taxe'] +
        #    taxe_indirectes['assurance_transport_taxe'] +
        #    taxe_indirectes['autres_assurances_taxe']
        #    ).copy()
        taxe_indirectes[u'Taxes tabacs'] = (
            taxe_indirectes['cigarette_droit_d_accise'] +
            taxe_indirectes['cigares_droit_d_accise'] +
            taxe_indirectes['tabac_a_rouler_droit_d_accise']
            ).copy()

        taxe_indirectes = taxe_indirectes.rename(columns = {'revtot': u'revenu total',
            'rev_disponible': u'revenu disponible'}) #, 'taxes_indirectes_total': u'toutes les taxes indirectes'
        for revenu in [u'revenu total']: #[u'revenu total', u'revenu disponible', u'depenses totales', u'toutes les taxes indirectes']
            list_part_taxes = []
            for taxe in ['TVA', 'TICPE', u'Taxes alcools', u'Taxes tabacs']: #u'Taxes assurances',
                taxe_indirectes[u'part ' + taxe] = (
                    taxe_indirectes[taxe] / taxe_indirectes[revenu]
                    )
                'list_part_taxes_{}'.format(taxe)
                list_part_taxes.append(u'part ' + taxe)

            df_to_graph = taxe_indirectes[list_part_taxes]

            print(''')Contributions aux différentes taxes indirectes en part de {0},
                par décile de revenu en {1}'''.format(revenu, year)
            graph_builder_bar(df_to_graph)
