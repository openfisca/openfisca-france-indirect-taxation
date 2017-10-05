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

share_loosers = dict()
for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    simulated_variables = [
        'total_taxes_energies',
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile',
        'precarite_energetique_rev_disponible',
        'precarite_transports_rev_disponible',
        ]

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        #inflation_kwargs = inflation_kwargs,
        reform_key = reforme,
        year = year,
        data_year = data_year
        )

    menages_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    menages_reference = survey_scenario.create_data_frame_by_entity(simulated_variables,
        reference = True, period = year)['menage']

    unite_conso = (menages_reforme['ocde10'] * menages_reforme['pondmen']).sum()
    contribution = (
        (menages_reforme['total_taxes_energies'] - menages_reference['total_taxes_energies']) *
        menages_reforme['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    # for category in ['niveau_vie_decile', 'age_group_pr', 'strate']:
    menages_reforme[u'Cost_after_green_cheques_{}'.format(reforme)] = (
        contribution_unite_conso * menages_reforme['ocde10'] -
        (menages_reforme['total_taxes_energies'] - menages_reference['total_taxes_energies'])
        )

    menages_reforme['precaire_energetique'] = (
        menages_reforme['precarite_energetique_rev_disponible'] + menages_reforme['precarite_transports_rev_disponible'] -
        (menages_reforme['precarite_energetique_rev_disponible'] * menages_reforme['precarite_transports_rev_disponible'])
        )
    menages_reforme = menages_reforme.query('precaire_energetique == 1')

    len_tot = float(len(menages_reforme))

    menages_loosers = menages_reforme.query(u'Cost_after_green_cheques_{} < 0'.format(reforme))
    len_loosers = float(len(menages_loosers))
    share = len_loosers / len_tot

    mean_loosers = menages_loosers[u'Cost_after_green_cheques_{}'.format(reforme)].mean()

    share_loosers[reforme] = [share * 100, mean_loosers]
