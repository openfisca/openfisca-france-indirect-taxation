# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, \
    save_dataframe_to_graph
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import dataframe_by_group

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])


for reforme in ['taxe_carbone']:#['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        #inflation_kwargs = inflation_kwargs,
        reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'depenses_carburants_corrigees',
        'depenses_energies_logement',
        'depenses_tot',
        'niveau_vie_decile',
        'pondmen',
        'ocde10',
        'rev_disponible',
        'surfhab_d',
        'total_taxes_energies',
        ]

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_reference = survey_scenario.create_data_frame_by_entity(simulated_variables,
        reference = True, period = year)

    menages_reforme = indiv_df_reform['menage']
    menages_reference = indiv_df_reference['menage']

    unite_conso = (menages_reforme['ocde10'] * menages_reforme['pondmen']).sum()
    contribution = (
        (menages_reforme['total_taxes_energies'] - menages_reference['total_taxes_energies']) *
        menages_reference['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    # Construire des indicateurs de précarité pour les deux df
    mediane_depenses_tot_uc = np.median(
        menages_reference['depenses_tot'] / menages_reference['ocde10']
        )
    menages_reference['bas_revenu'] = (
        1 * (
        (menages_reference['depenses_tot'] / menages_reference['ocde10'])
        < (0.6 * mediane_depenses_tot_uc))
        )

    mediane_depenses_surface = np.median(
        menages_reference['depenses_energies_logement'] / menages_reference['surfhab_d']
        )
    menages_reference['depenses_elevees'] = (
        1 * (
        (menages_reference['depenses_energies_logement'] / menages_reference['surfhab_d'])
        > mediane_depenses_surface)
        )
    menages_reference['brde_m2_depenses_tot'] = (
        menages_reference['bas_revenu'] * menages_reference['depenses_elevees']
        )


    # reforme        
    mediane_depenses_tot_uc = np.median(
        menages_reforme['depenses_tot'] / menages_reforme['ocde10']
        )
    menages_reforme['bas_revenu'] = (
        1 * (
        (menages_reforme['depenses_tot'] / menages_reforme['ocde10'])
        < (0.6 * mediane_depenses_tot_uc))
        )

    menages_reforme['depenses_energies_logement'] = (
        menages_reforme['depenses_energies_logement'] -
        (contribution_unite_conso * menages_reforme['ocde10'])
        )
    mediane_depenses_surface = np.median(
        menages_reforme['depenses_energies_logement'] / menages_reforme['surfhab_d']
        )
    menages_reforme['depenses_elevees'] = (
        1 * (
        (menages_reforme['depenses_energies_logement'] / menages_reforme['surfhab_d'])
        > mediane_depenses_surface)
        )
    menages_reforme['brde_m2_depenses_tot'] = (
        menages_reforme['bas_revenu'] * menages_reforme['depenses_elevees']
        )


    # A revoir : les dépenses apres reforme sont-elles les bonnes ? -> ajouter cela aux réformes
    # + bien prendre en compte que les contributions doivent aller aussi aux transports
    print menages_reforme['brde_m2_depenses_tot'].mean()
    print menages_reference['brde_m2_depenses_tot'].mean()
