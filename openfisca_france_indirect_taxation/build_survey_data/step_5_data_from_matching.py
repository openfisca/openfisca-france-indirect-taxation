# -*- coding: utf-8 -*-

from configparser import ConfigParser
import datetime
import os
import platform
import pandas
import subprocess

from openfisca_survey_manager.paths import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.utils import assets_directory
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_enl.step_4_1_clean_data import prepare_bdf_enl_matching_data
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_emp.step_4_1_save_data import prepare_bdf_emp_matching_data
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_emp.step_6_1_calage_depenses_carburants import cale_bdf_emp_matching_data
from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_4_1_clean_data import prepare_bdf_erfs_matching_data


def check_load_config_ini():
    """
    Ensure that config.ini has:
      - [openfisca_france_indirect_taxation] section with 'assets' option
      - [exe] section with paths to Rscript and r_libs_user (on Windows)
    If missing or invalid, backup the old file and update it.
    """
    config_parser = ConfigParser()
    config_ini = os.path.join(config_files_directory, 'config.ini')
    config_parser.read(config_ini)

    updated = False

    # ---- Ensure [openfisca_france_indirect_taxation] ----
    section_tax = 'openfisca_france_indirect_taxation'
    option_assets = 'assets'

    if not (config_parser.has_section(section_tax) and config_parser.has_option(section_tax, option_assets)):
        updated = True
        if not config_parser.has_section(section_tax):
            config_parser.add_section(section_tax)
        config_parser.set(section_tax, option_assets, assets_directory)

    # ---- Ensure [exe] ----
    section_exe = 'exe'
    if not config_parser.has_section(section_exe):
        updated = True
        config_parser.add_section(section_exe)

        if platform.system() == 'Windows':
            config_parser.set(section_exe, 'r_libs_user', os.path.expanduser("~\\R\\libs"))
            config_parser.set(section_exe, 'Rscript', "C:\\Program Files\\R\\R-4.0.0\\bin\\Rscript.exe")
        else:
            config_parser.set(section_exe, 'Rscript', "Rscript")

    # ---- Backup config if modified ----
    if updated:
        modified_time = os.path.getmtime(config_ini)
        timestamp = datetime.datetime.fromtimestamp(modified_time).strftime('%b-%d-%Y_%H.%M.%S')
        os.rename(config_ini, config_ini + '_' + timestamp)

        with open(config_ini, 'w') as configfile:
            config_parser.write(configfile)

    # ---- Extract validated paths ----
    if platform.system() == 'Windows':
        path_to_r_libs_user = os.path.normpath(config_parser.get(section_exe, 'r_libs_user'))
        rscript_path = os.path.normpath(config_parser.get(section_exe, 'Rscript'))
    else:
        path_to_r_libs_user = None
        rscript_path = config_parser.get(section_exe, 'Rscript')

    # ---- Validate Rscript path ----
    if not os.path.isfile(rscript_path):
        # fallback
        rscript_path = "Rscript"

    return path_to_r_libs_user, rscript_path


def main(year_data):
    path_to_r_libs_user, path_to_rscript_exe = check_load_config_ini()
    prepare_bdf_enl_matching_data(year_data)
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_enl', 'matching_rank_bdf_enl.R')
    if path_to_r_libs_user is not None:
        os.environ['R_LIBS_USER'] = path_to_r_libs_user
    process_call = [path_to_rscript_exe, '--vanilla', r_script_path]
    subprocess.call(process_call)

    data_matched_enl = pandas.read_csv(
        os.path.join(
            assets_directory,
            'matching',
            'matching_enl',
            'data_matched_rank.csv'
            ), sep =',', decimal = '.'
        )
    prepare_bdf_emp_matching_data(year_data)
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_emp', 'matching_rank_bdf_emp.R')
    process_call = [path_to_rscript_exe, '--vanilla', r_script_path]
    subprocess.call(process_call)
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_emp', 'matching_distance_bdf_emp.R')
    process_call = [path_to_rscript_exe, '--vanilla', r_script_path]
    subprocess.call(process_call)
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_emp', 'matching_random_bdf_emp.R')
    process_call = [path_to_rscript_exe, '--vanilla', r_script_path]
    subprocess.call(process_call)
    cale_bdf_emp_matching_data()
    data_matched_emp = pandas.read_csv(
        os.path.join(
            assets_directory,
            'matching',
            'matching_emp',
            'data_matched_final.csv'
            ), sep =',', decimal = '.'
        )
    prepare_bdf_erfs_matching_data(year_data)
    r_script_path = os.path.join(assets_directory, 'matching', 'matching_erfs', 'matching_rank_bdf_erfs.R')
    process_call = [path_to_rscript_exe, '--vanilla', r_script_path]
    subprocess.call(process_call)

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

    emp_variables = [
        'age_vehicule',
        'depenses_carburants_corrigees_emp',
        'depenses_diesel_corrigees_emp',
        'depenses_essence_corrigees_emp',
        'distance_diesel',
        'distance_essence',
        # 'distance_routiere_hebdomadaire_teg',         # not for EMP 2019
        'distance',
        # 'duree_moyenne_trajet_aller_retour_teg',      # not for EMP 2019
        'ident_men',
        # 'mode_principal_deplacement_teg',             # not for EMP 2019
        'vp_deplacements_pro',
        'vp_domicile_travail',
        ]
    data_matched_emp = data_matched_emp[emp_variables].copy()

    data_matched_erfs = data_matched_erfs[['revdecm', 'ident_men']].copy()

    data_frame = pandas.merge(data_matched_emp, data_matched_enl, on = 'ident_men', how = 'left')
    data_frame = pandas.merge(data_frame, data_matched_erfs, on = 'ident_men')
    data_frame['ident_men'] = data_frame['ident_men'].astype(str)
    data_frame = data_frame.fillna(0)

    data_frame.to_csv(
        os.path.join(assets_directory, 'matching', 'data_for_run_all_{}.csv'.format(year_data)),
        sep = ','
        )
    return data_frame


if __name__ == '__main__':
    import sys
    sys.exit(main())
