# -*- coding: utf-8 -*-

# Import general modules
from __future__ import division

import numpy as np

# Import modules specific to OpenFisca
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy

def cheque_vert(data_reference, data_reforme, reforme):
    unite_conso = (data_reforme['ocde10'] * data_reforme['pondmen']).sum()
    contribution = (
        (data_reforme['total_taxes_energies'] - data_reference['total_taxes_energies']) *
        data_reference['pondmen']
        ).sum()
    contribution_unite_conso = contribution / unite_conso

    if reforme != 'rattrapage_diesel':
        data_reforme['part_cheque_logement'] = (
            (data_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] - data_reforme['depenses_energies_logement']) /
            ((data_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] - data_reforme['depenses_energies_logement']) +
            (data_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] - data_reforme['depenses_carburants_corrigees']))
            )
        data_reforme['part_cheque_logement'] = data_reforme['part_cheque_logement'].fillna(1)
        data_reforme['part_cheque_logement'] = (
            (data_reforme['part_cheque_logement'] < 1) * data_reforme['part_cheque_logement'] +
            (data_reforme['part_cheque_logement'] > 1) * 1
            )
        data_reforme['part_cheque_logement'] = (data_reforme['part_cheque_logement'] > 0) * data_reforme['part_cheque_logement']
        data_reforme['cheque_vert_logement'] = data_reforme['part_cheque_logement'] * contribution_unite_conso * data_reforme['ocde10']
        data_reforme['cheque_vert_transport'] = (1 - data_reforme['part_cheque_logement']) * contribution_unite_conso * data_reforme['ocde10']
    else:
        data_reforme['cheque_vert_transport'] = contribution_unite_conso * data_reforme['ocde10']

    return data_reforme


def brde(data, depenses, revenu, logement):
    mediane_revenu_uc = np.median(
        data[revenu] / data['ocde10']
        )
    data['bas_revenu'] = (
        1 * (
        (data[revenu] / data['ocde10'])
        < (0.6 * mediane_revenu_uc))
        )
    if logement == 'logement':
        data['depenses_bis'] = data[depenses] / data['surfhab_d']
    else:
        data['depenses_bis'] = data[depenses].copy()
    mediane_depenses = np.median(data['depenses_bis'])
    data['depenses_elevees'] = 1 * (data['depenses_bis'] > mediane_depenses)
    data['brde_m2_{0}_{1}'.format(logement, revenu)] = (
        data['bas_revenu'] * data['depenses_elevees']
        )
    del data['depenses_bis']
    
    return data 


def tee_10_3(data, depenses, revenu, logement):
    data['tee_10_3_{0}_{1}'.format(revenu, logement)] = \
        1 * ((data[depenses] / data[revenu]) > 0.1) * (data['niveau_vie_decile'] < 4)

    return data


def precarite(data, brde, tee, logement):
    data['precarite_{}'.format(logement)] = data[brde] + data[tee] - (data[brde] * data[tee])
    
    return data

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2014
data_year = 2011
elasticities = get_elasticities(data_year)
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

effets_reforme_transport = dict()
effets_reforme_logement = dict()
for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        reform_key = reforme,
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'depenses_carburants_corrigees',
        'depenses_carburants_corrigees_ajustees_{}'.format(reforme),
        'depenses_energies_logement',
        'depenses_energies_logement_ajustees_{}'.format(reforme),
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

    for redistribution in ['before', 'after']:
        if redistribution == 'after':
        # Compute value of green cheques and their allocation between housing and transports
            if reforme != 'rattrapage_diesel':
                menages_reforme = cheque_vert(menages_reference, menages_reforme, reforme)
                menages_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] = (
                    menages_reforme['depenses_energies_logement_ajustees_{}'.format(reforme)] - menages_reforme['cheque_vert_logement']
                    )
                menages_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] = (
                    menages_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] - menages_reforme['cheque_vert_transport']
                    )
            if reforme == 'rattrapage_diesel':
                menages_reforme = cheque_vert(menages_reference, menages_reforme, reforme)
                menages_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] = (
                    menages_reforme['depenses_carburants_corrigees_ajustees_{}'.format(reforme)] - menages_reforme['cheque_vert_transport']
                    )
          
        # Compute BRDE
        if reforme != 'rattrapage_diesel':
            menages_reference = brde(menages_reference, 'depenses_energies_logement', 'depenses_tot',  'logement')
            menages_reforme = brde(menages_reforme, 'depenses_energies_logement_ajustees_{}'.format(reforme), 'depenses_tot', 'logement')
    
            effets_reforme_logement['brde - {0} - {1}'.format(reforme, redistribution)] = float(
                (menages_reforme['brde_m2_logement_depenses_tot'] * menages_reforme['pondmen']).sum() -
                (menages_reference['brde_m2_logement_depenses_tot'] * menages_reference['pondmen']).sum()
                ) / menages_reference['pondmen'].sum() * 100
    
        menages_reference = brde(menages_reference, 'depenses_carburants_corrigees', 'depenses_tot',  'transport')
        menages_reforme = brde(menages_reforme, 'depenses_carburants_corrigees_ajustees_{}'.format(reforme), 'depenses_tot', 'transport')
    
        effets_reforme_transport['brde - {0} - {1}'.format(reforme, redistribution)] = float(
            (menages_reforme['brde_m2_transport_depenses_tot'] * menages_reforme['pondmen']).sum() -
            (menages_reference['brde_m2_transport_depenses_tot'] * menages_reference['pondmen']).sum()
            ) / menages_reference['pondmen'].sum() * 100
    
        # Compute TEE
        if reforme != 'rattrapage_diesel':
            menages_reference = tee_10_3(menages_reference, 'depenses_energies_logement', 'depenses_tot', 'logement')
            menages_reforme = tee_10_3(menages_reforme, 'depenses_energies_logement_ajustees_{}'.format(reforme), 'depenses_tot', 'logement')
            effets_reforme_logement['tee - {0} - {1}'.format(reforme, redistribution)] = float(
                (menages_reforme['tee_10_3_depenses_tot_logement'] * menages_reforme['pondmen']).sum() -
                (menages_reference['tee_10_3_depenses_tot_logement'] * menages_reference['pondmen']).sum()
                ) / menages_reference['pondmen'].sum() * 100  
    
        menages_reference = tee_10_3(menages_reference, 'depenses_carburants_corrigees', 'depenses_tot', 'transport')
        menages_reforme = tee_10_3(menages_reforme, 'depenses_carburants_corrigees_ajustees_{}'.format(reforme), 'depenses_tot', 'transport')
    
        effets_reforme_transport['tee - {0} - {1}'.format(reforme, redistribution)] = float(
            (menages_reforme['tee_10_3_depenses_tot_transport'] * menages_reforme['pondmen']).sum() -
            (menages_reference['tee_10_3_depenses_tot_transport'] * menages_reference['pondmen']).sum()
            ) / menages_reference['pondmen'].sum() * 100
    
    
        # Compute precarite
        if reforme != 'rattrapage_diesel':
            menages_reference = precarite(menages_reference, 'brde_m2_logement_depenses_tot', 'tee_10_3_depenses_tot_logement', 'logement')
            menages_reforme = precarite(menages_reforme, 'brde_m2_logement_depenses_tot', 'tee_10_3_depenses_tot_logement', 'logement')
        
            effets_reforme_logement['precarite - {0} - {1}'.format(reforme, redistribution)] = float(
                (menages_reforme['precarite_logement'] * menages_reforme['pondmen']).sum() -
                (menages_reference['precarite_logement'] * menages_reference['pondmen']).sum()
                ) / menages_reference['pondmen'].sum() * 100  

        menages_reference = precarite(menages_reference, 'brde_m2_transport_depenses_tot', 'tee_10_3_depenses_tot_transport', 'transport')
        menages_reforme = precarite(menages_reforme, 'brde_m2_transport_depenses_tot', 'tee_10_3_depenses_tot_transport', 'transport')

        effets_reforme_transport['precarite - {0} - {1}'.format(reforme, redistribution)] = float(
            (menages_reforme['precarite_transport'] * menages_reforme['pondmen']).sum() -
            (menages_reference['precarite_transport'] * menages_reference['pondmen']).sum()
            ) / menages_reference['pondmen'].sum() * 100
