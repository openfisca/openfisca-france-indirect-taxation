# -*- coding: utf-8 -*-

# Import de modules généraux


import pandas
import seaborn

# Import de modules spécifiques à Openfisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, save_dataframe_to_graph, \
    dataframe_by_group
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
        'assurance_transport_taxe',
        'assurance_sante_taxe',
        'autres_assurances_taxe',
        'rev_disp_loyerimput',
        'taxes_indirectes_total'
        ]
    year = 2000
    data_year = 2000
    survey_scenario = SurveyScenario.create(year = year, data_year = data_year)

    for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
        taxe_indirectes = \
            dataframe_by_group(survey_scenario, category, simulated_variables, use_baseline =True)

        taxe_indirectes['TVA'] = taxe_indirectes['tva_total']
        taxe_indirectes['TICPE'] = taxe_indirectes['ticpe_totale']
        taxe_indirectes['Taxes alcools'] = (
            taxe_indirectes['vin_droit_d_accise']
            + taxe_indirectes['biere_droit_d_accise']
            + taxe_indirectes['alcools_forts_droit_d_accise']
            ).copy()
        taxe_indirectes['Taxes assurances'] = (
            taxe_indirectes['assurance_sante_taxe']
            + taxe_indirectes['assurance_transport_taxe']
            + taxe_indirectes['autres_assurances_taxe']
            ).copy()
        taxe_indirectes['Taxes tabacs'] = (
            taxe_indirectes['cigarette_droit_d_accise']
            + taxe_indirectes['cigares_droit_d_accise']
            + taxe_indirectes['tabac_a_rouler_droit_d_accise']
            ).copy()

        taxe_indirectes = taxe_indirectes.rename(columns = {
            'rev_disp_loyerimput': 'revenu disponible',
            'taxes_indirectes_total': 'toutes les taxes indirectes'})
        for revenu in ['revenu disponible']:  # [u'revenu disponible', u'depenses totales', u'toutes les taxes indirectes']
            list_part_taxes = []
            for taxe in ['TVA', 'TICPE', 'Taxes alcools', 'Taxes assurances', 'Taxes tabacs']:
                taxe_indirectes['part ' + taxe] = (
                    taxe_indirectes[taxe] / taxe_indirectes[revenu]
                    )
                'list_part_taxes_{}'.format(taxe)
                list_part_taxes.append('part ' + taxe)

            df_to_graph = taxe_indirectes[list_part_taxes]

            print(('''Contributions aux différentes taxes indirectes en part de {0},
                par décile de revenu en {1}'''.format(revenu, year)))
            graph_builder_bar(df_to_graph)
            # save_dataframe_to_graph(
            #    df_to_graph, 'Taxes_indirectes/effort_rate_indirect_taxation_on_{0}_by_{1}.csv'.format(revenu, category)
            #    )
