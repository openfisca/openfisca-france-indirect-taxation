# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import brde, \
    cheque_energie_logement_transport, tee_10_3, precarite

    
def number_fuel_poors(year, data_year):
    dict_logement = dict()
    dict_transport = dict()
    dict_double = dict()
    dict_joint = dict()
    
    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    elasticities = get_elasticities(data_year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])
    
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = 'officielle_2018_in_2016',
        year = year,
        data_year = data_year
        )
    
    simulated_variables = [
        'cheques_energie_officielle_2018_in_2016',
        'cheques_energie_integral_inconditionnel_officielle_2018_in_2016',
        'depenses_carburants_corrigees',
        'depenses_carburants_corrigees_officielle_2018_in_2016',
        'depenses_energies_logement',
        'depenses_energies_logement_officielle_2018_in_2016',
        'depenses_tot',
        'froid_4_criteres_3_deciles',
        'niveau_vie_decile',
        'pondmen',
        'ocde10',
        'rev_disponible',
        'surfhab_d',
        ]
    
    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    
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
    dict_transport['brde - avant reforme'] = (
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
        df_reforme['precarite_logement'] + df_reforme['precarite_transport'] -
        (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
        )
    dict_double['precarite - avant reforme'] = (
        (df_reforme['double_precarite'] * df_reforme['pondmen']).sum()
        )
    dict_joint['precarite - avant reforme'] = (
        (df_reforme['precarite_joint'] * df_reforme['pondmen']).sum()
        )
    
    for cheque in ['cheques_energie_officielle_2018_in_2016', 'cheques_energie_integral_inconditionnel_officielle_2018_in_2016']:
    
        if cheque == 'cheques_energie_officielle_2018_in_2016':
            redistribution = 'officielle'
        else:
            redistribution = 'integrale'
    
        df_reforme = cheque_energie_logement_transport(
            df_reforme,
            'depenses_energies_logement_officielle_2018_in_2016',
            'depenses_carburants_corrigees_officielle_2018_in_2016',
            cheque
            )
        # logement
        df_reforme['depenses_energies_logement_officielle_2018_in_2016'] = (
            df_reforme['depenses_energies_logement_officielle_2018_in_2016'] -
            df_reforme['cheque_logement']
            )
        df_reforme = brde(df_reforme, 'depenses_energies_logement_officielle_2018_in_2016', 'rev_disponible', 'logement')
        dict_logement['brde - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['brde_m2_logement_rev_disponible'] * df_reforme['pondmen']).sum()
            )
        df_reforme = tee_10_3(df_reforme, 'depenses_energies_logement_officielle_2018_in_2016', 'rev_disponible', 'logement')
        dict_logement['tee - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['tee_10_3_rev_disponible_logement'] * df_reforme['pondmen']).sum()
            )
        df_reforme = precarite(df_reforme, 'brde_m2_logement_rev_disponible', 'tee_10_3_rev_disponible_logement', 'logement')
        dict_logement['precarite - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['precarite_logement'] * df_reforme['pondmen']).sum()
            )
    
        # carburants
        df_reforme['depenses_carburants_corrigees_officielle_2018_in_2016'] = (
            df_reforme['depenses_carburants_corrigees_officielle_2018_in_2016'] -
            df_reforme['cheque_transport']
            )
        df_reforme = brde(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
        dict_transport['brde - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['brde_m2_transport_rev_disponible'] * df_reforme['pondmen']).sum()
            )
        df_reforme = tee_10_3(df_reforme, 'depenses_carburants_corrigees_officielle_2018_in_2016', 'rev_disponible', 'transport')
        dict_transport['tee - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['tee_10_3_rev_disponible_transport'] * df_reforme['pondmen']).sum()
            )
        df_reforme = precarite(df_reforme, 'brde_m2_transport_rev_disponible', 'tee_10_3_rev_disponible_transport', 'transport')
        dict_transport['precarite - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['precarite_transport'] * df_reforme['pondmen']).sum()
            )
    
        # double et joint
        df_reforme['double_precarite'] = (
            (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
            )
        df_reforme['precarite_joint'] = (
            df_reforme['precarite_logement'] + df_reforme['precarite_transport'] -
            (df_reforme['precarite_logement'] * df_reforme['precarite_transport'])
            )
        dict_double['precarite - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['double_precarite'] * df_reforme['pondmen']).sum()
            )
        dict_joint['precarite - {0} - {1}'.format('officielle', redistribution)] = (
            (df_reforme['precarite_joint'] * df_reforme['pondmen']).sum()
            )

    return dict_logement, dict_transport, dict_double, dict_joint


if __name__ == '__main__':
    year = 2016
    data_year = 2011
    
    dict_reformes = dict()
    (dict_reformes['logement'], dict_reformes['transport'],
        dict_reformes['double'], dict_reformes['joint']) = \
        number_fuel_poors(year, data_year)
