# -*- coding: utf-8 -*-


import logging
import os
import pandas
import numpy


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager.surveys import Survey
from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.temporary import temporary_store_decorator

from openfisca_france_indirect_taxation.build_survey_data.utils import find_nearest_inferior

from openfisca_france_indirect_taxation.build_survey_data.step_1_1_homogeneisation_donnees_depenses \
    import build_depenses_homogenisees

from openfisca_france_indirect_taxation.build_survey_data.step_1_2_imputations_loyers_proprietaires \
    import build_imputation_loyers_proprietaires

from openfisca_france_indirect_taxation.build_survey_data.step_2_homogeneisation_vehicules \
    import build_homogeneisation_vehicules

from openfisca_france_indirect_taxation.build_survey_data.step_3_homogeneisation_caracteristiques_menages \
    import build_homogeneisation_caracteristiques_sociales
from openfisca_france_indirect_taxation.build_survey_data.step_4_homogeneisation_revenus_menages \
    import build_homogeneisation_revenus_menages


from openfisca_france_indirect_taxation.build_survey_data.utils import ident_men_dtype
from openfisca_france_indirect_taxation.utils import assets_directory


log = logging.getLogger(__name__)


YEAR_DATA_LIST = (1995, 2000, 2005, 2011, 2017)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def run_all_steps(temporary_store = None, year_calage = 2017, skip_matching = False):

    assert temporary_store is not None

    # Quelle base de données choisir pour le calage ?
    year_data = find_nearest_inferior(YEAR_DATA_LIST, year_calage)

    # 4 étape parallèles d'homogénéisation des données sources :
    # 1. Gestion des dépenses de consommation:
    build_depenses_homogenisees(year = year_data)
    build_imputation_loyers_proprietaires(year = year_data)

    depenses = temporary_store["depenses_bdf_{}".format(year_calage)]
    depenses.index = depenses.index.astype(ident_men_dtype)

    # 2. Gestion des véhicules:
    build_homogeneisation_vehicules(year = year_data)
    if year_calage != 1995:
        vehicule = temporary_store['automobile_{}'.format(year_data)]
        vehicule.index = vehicule.index.astype(ident_men_dtype)
    else:
        vehicule = None

    # 3. Gestion des variables socio démographiques:
    build_homogeneisation_caracteristiques_sociales(year = year_data)
    menage = temporary_store['donnes_socio_demog_{}'.format(year_data)]
    menage.index = menage.index.astype(ident_men_dtype)

    # 4. Gestion des variables revenus:
    build_homogeneisation_revenus_menages(year = year_data)
    revenus = temporary_store["revenus_{}".format(year_calage)]
    revenus.index = revenus.index.astype(ident_men_dtype)

    temporary_store.close()

    # Concaténation des résultas de ces 4 étapes
    preprocessed_data_frame_by_name = dict(
        revenus = revenus,
        vehicule = vehicule,
        menage = menage,
        depenses = depenses,
        )
    for name, preprocessed_data_frame in list(preprocessed_data_frame_by_name.items()):
        assert preprocessed_data_frame.index.name == 'ident_men', \
            'Index is labelled {} instead of ident_men in data frame {} for year {}'.format(
                preprocessed_data_frame.index.name, name, year_data)
        assert len(preprocessed_data_frame) != 0, 'Empty data frame {}'.format(name)
        assert preprocessed_data_frame.index.dtype == numpy.dtype('O'), "index for {} is {}".format(
            name, preprocessed_data_frame.index.dtype)

    data_frame = pandas.concat(
        list(preprocessed_data_frame_by_name.values()),
        axis = 1,
        sort = True
        )
    if year_data == 2005:
        nullified_variables = (
            ['veh_tot', 'veh_essence', 'veh_diesel', 'pourcentage_vehicule_essence']
            + ['age{}'.format(i) for i in range(3, 14)] + ['agecj', 'agfinetu', 'agfinetu_cj', 'nenfhors']
            )
        data_frame[nullified_variables] = data_frame[nullified_variables].fillna(0)

    if year_data == 2011:
        nullified_variables = ['veh_tot', 'veh_essence', 'veh_diesel', 'pourcentage_vehicule_essence',
            'rev_disp_loyerimput', 'rev_disponible', 'loyer_impute']
        data_frame[nullified_variables] = data_frame[nullified_variables].fillna(0)
    
    if year_data == 2017:
        nullified_variables = ['veh_tot', 'veh_essence', 'veh_diesel', 'pourcentage_vehicule_essence',
            'rev_disp_loyerimput', 'rev_disponible', 'loyer_impute']
        data_frame[nullified_variables] = data_frame[nullified_variables].fillna(0)

    if year_data == 2005:
        data_frame['ident_men'] = list(range(0, len(data_frame)))
        data_frame['ident_men'] = data_frame['ident_men'] + 200500000
        data_frame = data_frame.set_index('ident_men')

    data_frame.index.name = "ident_men"

    # TODO: Homogénéiser: soit faire en sorte que ident_men existe pour toutes les années soit qu'elle soit en index pour toutes

    try:
        data_frame.reset_index(inplace = True)
    except ValueError as e:
        log.info('ignoring reset_index because {}'.format(e))

    # On ne garde que les ménages métropolitains
    if year_data in [2011, 2017]:
        data_frame = data_frame.query('zeat != 0').copy()

    if year_data in [2011, 2017] and not skip_matching:
        # Save file needed by step_5_data_from_matching
        save(data_frame, year_data, year_calage)
        try:
            # On apparie ajoute les données appariées de l'ENL et l'ENTD
            data_matched = pandas.read_csv(
                os.path.join(
                    assets_directory,
                    'matching',
                    'data_for_run_all.csv'
                    ), sep =',', decimal = '.'
                )
        except FileNotFoundError as e:
            log.debug("Matching data with ENL and ENTD are not present")
            log.debug(e)
            log.debug("Skipping this step")
            from openfisca_france_indirect_taxation.build_survey_data import step_5_data_from_matching
            data_matched = step_5_data_from_matching.main()

        data_matched['ident_men'] = data_matched['ident_men'].astype(str).copy()
        data_frame = pandas.merge(data_frame, data_matched, on = 'ident_men')

    save(data_frame, year_data, year_calage)


def save(data_frame, year_data, year_calage):
    # Remove duplicated colums causing bug with HDFStore
    # according to https://github.com/pydata/pandas/issues/6240
    # using solution form stackoverflow
    # http://stackoverflow.com/questions/16938441/how-to-remove-duplicate-columns-from-a-dataframe-using-python-pandas
    data_frame = data_frame.T.groupby(level = 0).first().T
    # Créer un nouvel identifiant pour les ménages
    data_frame['identifiant_menage'] = list(range(0, len(data_frame)))
    data_frame['identifiant_menage'] = data_frame['identifiant_menage'] + (year_data * 100000)

    log.debug('Saving the openfisca indirect taxation input dataframe')
    try:
        openfisca_survey_collection = SurveyCollection.load(
            collection = 'openfisca_indirect_taxation', config_files_directory = config_files_directory)
    except Exception:
        openfisca_survey_collection = SurveyCollection(
            name = 'openfisca_indirect_taxation', config_files_directory = config_files_directory)

    output_data_directory = openfisca_survey_collection.config.get('data', 'output_directory')
    survey_name = "openfisca_indirect_taxation_data_{}".format(year_calage)
    table = "input"
    hdf5_file_path = os.path.join(output_data_directory, "{}.h5".format(survey_name))
    survey = Survey(
        name = survey_name,
        hdf5_file_path = hdf5_file_path,
        )
    survey.insert_table(name = table, data_frame = data_frame)
    openfisca_survey_collection.surveys.append(survey)
    openfisca_survey_collection.dump()


def run(years_calage, skip_matching = False):
    import time
    for year_calage in years_calage:
        start = time.time()
        log.info(f"Starting year = {year_calage}")
        run_all_steps(year_calage = year_calage, skip_matching = skip_matching)
        log.info(f"Finished in {(time.time() - start)} for year = {year_calage}")


if __name__ == '__main__':
    import sys
    log = logging.getLogger(__name__)
    logging.basicConfig(level = logging.DEBUG, stream = sys.stdout)
    run([2011], skip_matching = False)
