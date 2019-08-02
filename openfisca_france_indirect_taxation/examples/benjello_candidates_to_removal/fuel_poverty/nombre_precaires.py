# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_estimation_from_stata import get_elasticities
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import brde, cheque_vert, tee_10_3, precarite


def nombre_precaires_reformes(reforme, year, data_year):
    dict_logement = dict()
    dict_transport = dict()
    dict_double = dict()
    dict_joint = dict()

    inflators_by_year = get_inflators_by_year_energy(rebuild = False)
    elasticities = get_elasticities(data_year)
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        # inflation_kwargs = inflation_kwargs,
        reform = reforme,
        year = year,
        data_year = data_year
        )

    simulated_variables = [
        'depenses_carburants_corrigees',
        'depenses_carburants_corrigees_ajustees_{}'.format(reforme),
        'depenses_energies_logement',
        'depenses_energies_logement_ajustees_{}'.format(reforme),
        'depenses_tot',
        'froid_4_criteres_3_deciles',
        'niveau_vie_decile',
        'pondmen',
        'ocde10',
        'rev_disponible',
        'surfhab_d',
        'total_taxes_energies',
        ]

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    indiv_df_reference = survey_scenario.create_data_frame_by_entity(simulated_variables,
        use_baseline =True, period = year)

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
            menages_reference = brde(menages_reference, 'depenses_energies_logement', 'depenses_tot', 'logement')
            menages_reforme = brde(menages_reforme, 'depenses_energies_logement_ajustees_{}'.format(reforme), 'depenses_tot', 'logement')

            dict_logement['brde - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['brde_m2_logement_depenses_tot'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_logement['brde - {0} - reference'.format(reforme)] = (
                float((menages_reference['brde_m2_logement_depenses_tot'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )

        menages_reference = brde(menages_reference, 'depenses_carburants_corrigees', 'depenses_tot', 'transport')
        menages_reforme = brde(menages_reforme, 'depenses_carburants_corrigees_ajustees_{}'.format(reforme), 'depenses_tot', 'transport')

        dict_transport['brde - {0} - {1}'.format(reforme, redistribution)] = (
            float((menages_reforme['brde_m2_transport_depenses_tot'] * menages_reforme['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )
        dict_transport['brde - {0} - reference'.format(reforme)] = (
            float((menages_reference['brde_m2_transport_depenses_tot'] * menages_reference['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )

        # Compute TEE
        if reforme != 'rattrapage_diesel':
            menages_reference = tee_10_3(menages_reference, 'depenses_energies_logement', 'depenses_tot', 'logement')
            menages_reforme = tee_10_3(menages_reforme, 'depenses_energies_logement_ajustees_{}'.format(reforme), 'depenses_tot', 'logement')
            dict_logement['tee - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['tee_10_3_depenses_tot_logement'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_logement['tee - {0} - reference'.format(reforme)] = (
                float((menages_reference['tee_10_3_depenses_tot_logement'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )

        menages_reference = tee_10_3(menages_reference, 'depenses_carburants_corrigees', 'depenses_tot', 'transport')
        menages_reforme = tee_10_3(menages_reforme, 'depenses_carburants_corrigees_ajustees_{}'.format(reforme), 'depenses_tot', 'transport')

        dict_transport['tee - {0} - {1}'.format(reforme, redistribution)] = (
            float((menages_reforme['tee_10_3_depenses_tot_transport'] * menages_reforme['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )
        dict_transport['tee - {0} - reference'.format(reforme)] = (
            float((menages_reference['tee_10_3_depenses_tot_transport'] * menages_reference['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )

        # Compute froid
        if reforme != 'rattrapage_diesel':
            dict_logement['froid - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['froid_4_criteres_3_deciles'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_logement['froid - {0} - reference'.format(reforme)] = (
                float((menages_reference['froid_4_criteres_3_deciles'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )

        # Compute precarite
        if reforme != 'rattrapage_diesel':
            menages_reference = precarite(menages_reference, 'brde_m2_logement_depenses_tot', 'tee_10_3_depenses_tot_logement', 'logement')
            menages_reforme = precarite(menages_reforme, 'brde_m2_logement_depenses_tot', 'tee_10_3_depenses_tot_logement', 'logement')

            dict_logement['precarite - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['precarite_logement'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_logement['precarite - {0} - reference'.format(reforme)] = (
                float((menages_reference['precarite_logement'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )

        menages_reference = precarite(menages_reference, 'brde_m2_transport_depenses_tot', 'tee_10_3_depenses_tot_transport', 'transport')
        menages_reforme = precarite(menages_reforme, 'brde_m2_transport_depenses_tot', 'tee_10_3_depenses_tot_transport', 'transport')

        if reforme != 'rattrapage_diesel':
            menages_reference['double_precaire'] = (
                (menages_reference['precarite_logement'] * menages_reference['precarite_transport'])
                )
            menages_reforme['double_precaire'] = (
                (menages_reforme['precarite_logement'] * menages_reforme['precarite_transport'])
                )
            menages_reference['precarite_joint'] = (
                menages_reference['precarite_logement'] + menages_reference['precarite_transport']
                - (menages_reference['precarite_logement'] * menages_reference['precarite_transport'])
                )
            menages_reforme['precarite_joint'] = (
                menages_reforme['precarite_logement'] + menages_reforme['precarite_transport']
                - (menages_reforme['precarite_logement'] * menages_reforme['precarite_transport'])
                )
            dict_double['precarite - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['double_precaire'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_double['precarite - {0} - reference'.format(reforme)] = (
                float((menages_reference['double_precaire'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_joint['precarite - {0} - {1}'.format(reforme, redistribution)] = (
                float((menages_reforme['precarite_joint'] * menages_reforme['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )
            dict_joint['precarite - {0} - reference'.format(reforme)] = (
                float((menages_reference['precarite_joint'] * menages_reference['pondmen']).sum())
                / menages_reference['pondmen'].sum()
                )

        dict_transport['precarite - {0} - {1}'.format(reforme, redistribution)] = (
            float((menages_reforme['precarite_transport'] * menages_reforme['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )
        dict_transport['precarite - {0} - reference'.format(reforme)] = (
            float((menages_reference['precarite_transport'] * menages_reference['pondmen']).sum())
            / menages_reference['pondmen'].sum()
            )

    return dict_logement, dict_transport, dict_double, dict_joint


if __name__ == '__main__':
    year = 2014
    data_year = 2011

    dict_reformes = dict()
    for reforme in ['rattrapage_diesel', 'taxe_carbone', 'cce_2015_in_2014', 'cce_2016_in_2014']:
        (dict_reformes['logement - {}'.format(reforme)], dict_reformes['transport - {}'.format(reforme)],
            dict_reformes['double - {}'.format(reforme)], dict_reformes['joint - {}'.format(reforme)]) = \
            nombre_precaires_reformes(reforme, year, data_year)
