# -*- coding: utf-8 -*-

# Import general modules


import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
# from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.almost_ideal_demand_system.elasticites_aidsills import get_elasticities_aidsills
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import brde, tee_10_3, precarite


def number_fuel_poors(year, data_year):
    dict_logement = dict()
    dict_transport = dict()
    dict_double = dict()
    dict_joint = dict()

    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    # elasticities = get_elasticities(data_year)
    elasticities = get_elasticities_aidsills(data_year, True)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'cheques_energie_ruraux_officielle_2018_in_2016',
        'cheques_energie_officielle_2018_in_2016',
        'cheques_energie_by_energy_officielle_2018_in_2016',
        'cheques_energie_ruraux_by_energy_officielle_2018_in_2016',
        'depenses_carburants_corrigees',
        'depenses_carburants_corrigees_officielle_2018_in_2016',
        'depenses_energies_logement',
        'depenses_energies_logement_officielle_2018_in_2016',
        'depenses_tot',
        'froid_4_criteres_3_deciles',
        'niveau_vie_decile',
        'pondmen',
        'ocde10',
        'reste_transferts_neutre_officielle_2018_in_2016',
        'rev_disponible',
        'surfhab_d',
        'tarifs_sociaux_electricite',
        'tarifs_sociaux_gaz'
        ]

    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    df_reforme = df_reforme.query('rev_disponible > 0')

   # Avant reforme
    df_reforme = brde(df_reforme, 'depenses_energies_logement', 'rev_disponible', 'logement')
    dict_logement['brde - avant reforme'] = (
        (df_reforme['brde_m2_logement_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_energies_logement', 'rev_disponible', 'logement')
    dict_logement['tee - avant reforme'] = (
        (df_reforme['tee_10_3_rev_disponible_logement'] * df_reforme['pondmen']).sum()
        )
    df_reforme = brde(df_reforme, 'depenses_carburants_corrigees', 'rev_disponible', 'transport')
    dict_transport['brde - avant reforme'] = (
        (df_reforme['brde_m2_transport_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_carburants_corrigees', 'rev_disponible', 'transport')
    dict_transport['tee - avant reforme'] = (
        (df_reforme['tee_10_3_rev_disponible_transport'] * df_reforme['pondmen']).sum()
        )

    df_reforme = precarite(df_reforme, 'brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement', 'logement')
    dict_logement['precarite - avant reforme'] = (
        (df_reforme['precarite_logement'] * df_reforme['pondmen']).sum()
        )
    df_reforme = precarite(df_reforme, 'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'transport')
    dict_transport['precarite - avant reforme'] = (
        (df_reforme['precarite_transport'] * df_reforme['pondmen']).sum()
        )

    df_reforme['double_precarite'] = (
        (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    df_reforme['precarite_joint'] = (
        df_reforme['precarite_logement'] + df_reforme['precarite_transport']
        - (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    dict_double['precarite - avant reforme'] = (
        (df_reforme['double_precarite'] * df_reforme['pondmen']).sum()
        )
    dict_joint['precarite - avant reforme'] = (
        (df_reforme['precarite_joint'] * df_reforme['pondmen']).sum()
        )

    df_reforme['precarite_logement_avant_ref'] = df_reforme['precarite_logement'].copy()
    df_reforme['precarite_transport_avant_ref'] = df_reforme['precarite_transport'].copy()
    df_reforme['precarite_double_avant_ref'] = df_reforme['double_precarite'].copy()
    df_reforme['precarite_joint_avant_ref'] = df_reforme['precarite_joint'].copy()

    # Avant redistribution
    df_reforme['depenses_energies_logement_officielle_avec_tarifs_sociaux'] = \
        df_reforme['depenses_energies_logement_officielle_2018_in_2016'] - df_reforme['tarifs_sociaux_electricite'] - df_reforme['tarifs_sociaux_gaz']
    df_reforme = brde(df_reforme, 'depenses_energies_logement_officielle_avec_tarifs_sociaux', 'rev_disponible', 'logement')
    dict_logement['brde - avant redistribution'] = (
        (df_reforme['brde_m2_logement_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_energies_logement_officielle_avec_tarifs_sociaux', 'rev_disponible', 'logement')
    dict_logement['tee - avant redistribution'] = (
        (df_reforme['tee_10_3_rev_disponible_logement'] * df_reforme['pondmen']).sum()
        )
    df_reforme = brde(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
    dict_transport['brde - avant redistribution'] = (
        (df_reforme['brde_m2_transport_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
    dict_transport['tee - avant redistribution'] = (
        (df_reforme['tee_10_3_rev_disponible_transport'] * df_reforme['pondmen']).sum()
        )

    df_reforme = precarite(df_reforme, 'brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement', 'logement')
    dict_logement['precarite - avant redistribution'] = (
        (df_reforme['precarite_logement'] * df_reforme['pondmen']).sum()
        )
    df_reforme = precarite(df_reforme, 'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'transport')
    dict_transport['precarite - avant redistribution'] = (
        (df_reforme['precarite_transport'] * df_reforme['pondmen']).sum()
        )

    df_reforme['double_precarite'] = (
        (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    df_reforme['precarite_joint'] = (
        df_reforme['precarite_logement'] + df_reforme['precarite_transport']
        - (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    dict_double['precarite - avant redistribution'] = (
        (df_reforme['double_precarite'] * df_reforme['pondmen']).sum()
        )
    dict_joint['precarite - avant redistribution'] = (
        (df_reforme['precarite_joint'] * df_reforme['pondmen']).sum()
        )

    # Après redistribution
    df_reforme['depenses_energies_logement_officielle_2018_in_2016'] = (
        df_reforme['depenses_energies_logement_officielle_2018_in_2016']
        - df_reforme['cheques_energie_officielle_2018_in_2016']
        )
    df_reforme['rev_disponible'] = (
        df_reforme['rev_disponible']
        + df_reforme['reste_transferts_neutre_officielle_2018_in_2016']
        )

    # logement
    df_reforme = brde(df_reforme, 'depenses_energies_logement_officielle_2018_in_2016', 'rev_disponible', 'logement')
    dict_logement['brde - apres redistribution'] = (
        (df_reforme['brde_m2_logement_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_energies_logement_officielle_2018_in_2016', 'rev_disponible', 'logement')
    dict_logement['tee apres redistribution'] = (
        (df_reforme['tee_10_3_rev_disponible_logement'] * df_reforme['pondmen']).sum()
        )
    df_reforme = precarite(df_reforme, 'brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement', 'logement')
    dict_logement['precarite - apres redistribution'] = (
        (df_reforme['precarite_logement'] * df_reforme['pondmen']).sum()
        )

    # carburants
    df_reforme = brde(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
    dict_transport['brde - apres redistribution'] = (
        (df_reforme['brde_m2_transport_rev_disponible'] * df_reforme['pondmen']).sum()
        )
    df_reforme = tee_10_3(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
    dict_transport['tee - apres redistribution'] = (
        (df_reforme['tee_10_3_rev_disponible_transport'] * df_reforme['pondmen']).sum()
        )

    df_reforme = precarite(df_reforme, 'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'transport')
    dict_transport['precarite - apres redistribution'] = (
        (df_reforme['precarite_transport'] * df_reforme['pondmen']).sum()
        )
    # double et joint
    df_reforme['double_precarite'] = (
        (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    df_reforme['precarite_joint'] = (
        df_reforme['precarite_logement'] + df_reforme['precarite_transport']
        - (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    dict_double['precarite - apres redistribution'] = (
        (df_reforme['double_precarite'] * df_reforme['pondmen']).sum()
        )
    dict_joint['precarite - apres redistribution'] = (
        (df_reforme['precarite_joint'] * df_reforme['pondmen']).sum()
        )

    # Entrants - sortants
    df_reforme['entrant_sortant_logement'] = (df_reforme['precarite_logement_avant_ref'] - df_reforme['precarite_logement'])
    dict_logement['precarite - entrants'] = (
        df_reforme.query('entrant_sortant_logement == -1')['pondmen'].sum()
        )
    dict_logement['precarite - sortants'] = (
        df_reforme.query('entrant_sortant_logement == 1')['pondmen'].sum()
        )

    df_reforme['entrant_sortant_transport'] = (df_reforme['precarite_transport_avant_ref'] - df_reforme['precarite_transport'])
    dict_transport['precarite - entrants'] = (
        df_reforme.query('entrant_sortant_transport == -1')['pondmen'].sum()
        )
    dict_transport['precarite - sortants'] = (
        df_reforme.query('entrant_sortant_transport == 1')['pondmen'].sum()
        )

    df_reforme['entrant_sortant_double'] = (df_reforme['precarite_double_avant_ref'] - df_reforme['double_precarite'])
    dict_double['precarite - entrants'] = (
        df_reforme.query('entrant_sortant_double == -1')['pondmen'].sum()
        )
    dict_double['precarite - sortants'] = (
        df_reforme.query('entrant_sortant_double == 1')['pondmen'].sum()
        )

    df_reforme['entrant_sortant_joint'] = (df_reforme['precarite_joint_avant_ref'] - df_reforme['precarite_joint'])
    dict_joint['precarite - entrants'] = (
        df_reforme.query('entrant_sortant_joint == -1')['pondmen'].sum()
        )
    dict_joint['precarite - sortants'] = (
        df_reforme.query('entrant_sortant_joint == 1')['pondmen'].sum()
        )

    return dict_logement, dict_transport, dict_double, dict_joint


if __name__ == '__main__':
    year = 2016
    data_year = 2011

    dict_reformes = dict()
    (dict_reformes['logement'], dict_reformes['transport'],
        dict_reformes['double'], dict_reformes['joint']) = \
        number_fuel_poors(year, data_year)
