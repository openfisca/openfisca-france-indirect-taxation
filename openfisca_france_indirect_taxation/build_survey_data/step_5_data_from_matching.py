# -*- coding: utf-8 -*-


from configparser import ConfigParser
import datetime
import os
import pandas
import subprocess


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.utils import assets_directory


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_4_1_clean_data import prepare_bdf_enl_matching_data

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_4_1_save_data import prepare_bdf_entd_matching_data
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_6_1_calage_depenses_carburants import cale_bdf_entd_matching_data

from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_4_1_clean_data import prepare_bdf_erfs_matching_data


def check_config_ini():
    """
    Check that assets option of section openfisca_france_indirect_taxation is set in openfisca-survey-manager config.ini file
    since that file is used by R
    """
    config_parser = ConfigParser()
    config_ini = os.path.join(config_files_directory, 'config.ini')
    config_parser.read(config_ini)
    if config_parser.has_section('openfisca_france_indirect_taxation') and config_parser.has_option('openfisca_france_indirect_taxation', 'assets'):
        return
    else:
        modifiedTime = os.path.getmtime(config_ini)
        timestamp = datetime.datetime.fromtimestamp(modifiedTime).strftime("%b-%d-%Y_%H.%M.%S")
        os.rename(config_ini, config_ini + "_" + timestamp)
        try:
            config_parser.add_section("openfisca_france_indirect_taxation")

        finally:
            config_parser.set("openfisca_france_indirect_taxation", "assets", assets_directory)
            with open(config_ini, 'w') as configfile:
                config_parser.write(configfile)


def main():
    check_config_ini()
    prepare_bdf_enl_matching_data()
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_enl', 'matching_rank_bdf_enl.R')
    subprocess.call(['Rscript', '--vanilla', r_script_path])

    data_matched_enl = pandas.read_csv(
        os.path.join(
            assets_directory,
            'matching',
            'matching_enl',
            'data_matched_rank.csv'
            ), sep =',', decimal = '.'
        )
    prepare_bdf_entd_matching_data()
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_entd', 'matching_rank_bdf_entd.R')
    subprocess.call(['Rscript', '--vanilla', r_script_path])
    cale_bdf_entd_matching_data()
    data_matched_entd = pandas.read_csv(
        os.path.join(
            assets_directory,
            'matching',
            'matching_entd',
            'data_matched_final.csv'
            ), sep =',', decimal = '.'
        )
    prepare_bdf_erfs_matching_data()
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_erfs', 'matching_rank_bdf_erfs.R')
    subprocess.call(['Rscript', '--vanilla', r_script_path])

    data_matched_erfs = pandas.read_csv(
        os.path.join(
            assets_directory,
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
        'paris',
        'petite_ville',
        'rural',
        ]
    data_matched_enl = data_matched_enl[enl_variables].copy()

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
    data_matched_entd = data_matched_entd[entd_variables].copy()

    data_matched_erfs = data_matched_erfs[['revdecm', 'ident_men']].copy()

    data_frame = pandas.merge(data_matched_entd, data_matched_enl, on = 'ident_men', how = 'left')
    data_frame = pandas.merge(data_frame, data_matched_erfs, on = 'ident_men')
    data_frame['ident_men'] = data_frame['ident_men'].astype(str)
    data_frame = data_frame.fillna(0)

    data_frame.to_csv(
        os.path.join(assets_directory, 'matching', 'data_for_run_all.csv'),
        sep = ','
        )
    return data_frame


if __name__ == '__main__':
    import sys
    sys.exit(main())
