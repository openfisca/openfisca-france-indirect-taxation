# -*- coding: utf-8 -*-


import os
import pkg_resources
import pandas


def main():
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)

    data_matched_enl = pandas.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'matching',
            'data_matched_rank.csv'
            ), sep =',', decimal = '.'
        )

    data_matched_entd = pandas.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'matching',
            'matching_entd',
            'data_matched_final.csv'
            ), sep =',', decimal = '.'
        )

    data_matched_erfs = pandas.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'matching',
            'matching_erfs',
            'data_matched_rank.csv'
            ), sep =',', decimal = '.'
        )

    enl_variables = [
        'aides_logement',
        'bat_49_74',
        'bat_ap_74',
        'bat_av_49',
        'froid_cout',
        'froid_impaye',
        'froid_installation',
        'froid_isolation',
        'froid',
        'ident_men',
        'isolation_fenetres',
        'isolation_murs',
        'isolation_toit',
        'log_indiv',
        'majorite_double_vitrage',
        'ouest_sud',
        'paris'
        'petite_ville',
        'rural',
        ]
    data_matched_enl = data_matched_enl[enl_variables]

    entd_variables = [
        'age_carte_grise',
        'age_vehicule',
        'depenses_carburants_corrigees_entd',
        'depenses_diesel_corrigees_entd',
        'depenses_essence_corrigees_entd',
        'distance_diesel',
        'distance_essence',
        'distance_routiere_hebdomadaire_teg',
        'distance',
        'duree_moyenne_trajet_aller_retour_teg',
        'ident_men',
        'mode_principal_deplacement_teg',
        'vp_deplacements_pro',
        'vp_domicile_travail',
        ]
    data_matched_entd = data_matched_entd[entd_variables]

    data_matched_erfs = data_matched_erfs[['revdecm', 'ident_men']]

    data_frame = pandas.merge(data_matched_entd, data_matched_enl, on = 'ident_men', how = 'left')
    data_frame = pandas.merge(data_frame, data_matched_erfs, on = 'ident_men')
    data_frame['ident_men'] = data_frame['ident_men'].astype(str)
    data_frame = data_frame.fillna(0)

    data_frame.to_csv(
        os.path.join(default_config_files_directory, 'openfisca_france_indirect_taxation', 'assets', 'matching', 'data_for_run_all.csv'),
        sep = ','
        )
    return


if __name__ == '__main__':
    import sys
    sys.exit(main())
