# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills

from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy


year = 2016
data_year = 2011
inflators_by_year = get_inflators_by_year_energy(rebuild = False)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
elasticities = get_elasticities_aidsills(data_year, True)

reforme = 'officielle_2018_in_2016'

survey_scenario = SurveyScenario.create(
    elasticities = elasticities,
    inflation_kwargs = inflation_kwargs,
    reform_key = reforme,
    year = year,
    data_year = data_year
    )

simulated_variables = [
    'niveau_vie_decile',
    'pondmen',
    'depenses_energies_logement',
    'depenses_energies_logement_officielle_2018_in_2016',
    'depenses_energies_totales',
    'depenses_carburants_corrigees',
    'combustibles_liquides',
    'gaz_ville',
    'rev_disp_loyerimput',
    'depenses_tot',
    'cheques_energie_officielle_2018_in_2016',
    'reste_transferts_neutre_officielle_2018_in_2016',
    'revenu_reforme_officielle_2018_in_2016',
    'precarite_transports_rev_disponible',
    'precarite_energetique_rev_disponible',
    'tarifs_sociaux_electricite',
    'tarifs_sociaux_gaz',
    'depenses_gaz_ville_officielle_2018_in_2016',
    'depenses_gaz_ville',
    'depenses_combustibles_liquides_officielle_2018_in_2016',
    'depenses_combustibles_liquides',
    ]

df = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']

keep = df[
    ['depenses_energies_logement_officielle_2018_in_2016']
    + ['depenses_energies_logement']
    + ['tarifs_sociaux_electricite']
    + ['tarifs_sociaux_gaz']
    + ['depenses_combustibles_liquides_officielle_2018_in_2016']
    + ['depenses_combustibles_liquides']
    + ['depenses_gaz_ville_officielle_2018_in_2016']
    + ['depenses_gaz_ville']
    ]

keep['net_logement'] = keep['depenses_energies_logement_officielle_2018_in_2016'] - keep['depenses_energies_logement']
weird = keep.query('net < 0')

keep['net_gaz'] = keep['depenses_gaz_ville_officielle_2018_in_2016'] - keep['depenses_gaz_ville']
keep['net_fioul'] = keep['depenses_combustibles_liquides_officielle_2018_in_2016'] - keep['depenses_combustibles_liquides']

weird_fioul = keep.query('net_fioul < 0')
weird_gaz = keep.query('net_gaz < 0')
weird_gaz_keep = weird_gaz[['depenses_gaz_ville_officielle_2018_in_2016'] + ['depenses_gaz_ville']]

precaires_log = (df['precarite_energetique_rev_disponible'] * df['pondmen']).sum()
precaires_tra = (df['precarite_transports_rev_disponible'] * df['pondmen']).sum()
df['preca_joint'] = 1 * ((df['precarite_energetique_rev_disponible'] + df['precarite_transports_rev_disponible']) > 0)
df['preca_both'] = 1 * ((df['precarite_energetique_rev_disponible'] + df['precarite_transports_rev_disponible']) > 1)

preca_joint = (df['preca_joint'] * df['pondmen']).sum()
preca_both = (df['preca_both'] * df['pondmen']).sum()


weird.net.min()
