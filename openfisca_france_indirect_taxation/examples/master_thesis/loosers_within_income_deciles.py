# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

# Simulate contribution to fuel tax reform by categories
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
del inflation_kwargs['inflator_by_variable']['somme_coicop12']

for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = [
        'total_taxes_energies',
        'depenses_energies',
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        ]

    survey_scenario = SurveyScenario.create(
        #elasticities = elasticities,
        #inflation_kwargs = inflation_kwargs,
        #reform_key = '{}'.format(reforme),
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_reference = survey_scenario.create_data_frame_by_entityl(simulated_variables,
        reference = True, period = year)

    menages_reform = indiv_df_reform['menage']
    menages_reference = indiv_df_reference['menage']

    unite_conso = (menages_reform['ocde10'] * menages_reform['pondmen']).sum()
    contribution = (
        (menages_reform['total_taxes_energies'] - menages_reference['total_taxes_energies']) *
        menages_reform['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    # for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
    menages_reform[u'Cost_after_green_cheques'] = (
        contribution_unite_conso * menages_reform['ocde10'] -
        (menages_reform['total_taxes_energies'] - menages_reference['total_taxes_energies'])
        )

    print reforme
    for i in range(1, 11):
        menages_decile = menages_reform.loc[menages_reform['niveau_vie_decile'] == i]
        len_decile = float(len(menages_decile))

        menages_decile_loosers = menages_decile.query(u'Cost_after_green_cheques < 0')
        len_loosers = float(len(menages_decile_loosers))
        share = len_loosers / len_decile

        mean_loosers = menages_decile_loosers['Cost_after_green_cheques'].mean()
        mean_loosers_income = menages_decile_loosers['rev_disp_loyerimput'].mean()

        print i, share * 100, mean_loosers, mean_loosers_income
