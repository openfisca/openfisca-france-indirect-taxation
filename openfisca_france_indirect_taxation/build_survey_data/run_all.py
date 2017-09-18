# -*- coding: utf-8 -*-


from __future__ import division


import logging
import os
import pandas
import numpy


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager.surveys import Survey
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import find_nearest_inferior

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

from openfisca_survey_manager.temporary import TemporaryStore

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype


log = logging.getLogger(__name__)


def run_all(year_calage = 2011, year_data_list = [1995, 2000, 2005, 2011]):

    temporary_store = TemporaryStore.create(file_name = "indirect_taxation_tmp")

    # Quelle base de données choisir pour le calage ?
    year_data = find_nearest_inferior(year_data_list, year_calage)

    # 4 étape parallèles d'homogénéisation des données sources :
    # Gestion des dépenses de consommation:
    build_depenses_homogenisees(year = year_data)
    build_imputation_loyers_proprietaires(year = year_data)

    depenses = temporary_store["depenses_bdf_{}".format(year_calage)]
    depenses.index = depenses.index.astype(ident_men_dtype)
    # depenses_by_grosposte = temporary_store["depenses_by_grosposte_{}".format(year_calage)]
    # depenses_by_grosposte.index = depenses_by_grosposte.index.astype(str)

    # Gestion des véhicules:
    build_homogeneisation_vehicules(year = year_data)
    if year_calage != 1995:
        vehicule = temporary_store['automobile_{}'.format(year_data)]
        vehicule.index = vehicule.index.astype(ident_men_dtype)
    else:
        vehicule = None

    # Gestion des variables socio démographiques:
    build_homogeneisation_caracteristiques_sociales(year = year_data)
    menage = temporary_store['donnes_socio_demog_{}'.format(year_data)]
    menage.index = menage.index.astype(ident_men_dtype)

    # Gestion des variables revenus:
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

    for name, preprocessed_data_frame in preprocessed_data_frame_by_name.iteritems():
        assert preprocessed_data_frame.index.name == 'ident_men', \
            'Index is labelled {} instead of ident_men in data frame {} for year {}'.format(
                preprocessed_data_frame.index.name, name, year_data)
        assert len(preprocessed_data_frame) != 0, 'Empty data frame {}'.format(name)
        assert preprocessed_data_frame.index.dtype == numpy.dtype('O'), "index for {} is {}".format(
            name, preprocessed_data_frame.index.dtype)

    data_frame = pandas.concat(
        preprocessed_data_frame_by_name.values(),
        axis = 1,
        )

    if year_data == 2005:
        for vehicule_variable in ['veh_tot', 'veh_essence', 'veh_diesel', 'pourcentage_vehicule_essence']:
            data_frame.loc[data_frame[vehicule_variable].isnull(), vehicule_variable] = 0
        for variable in ['age{}'.format(i) for i in range(3, 14)] + ['agecj', 'agfinetu', 'agfinetu_cj', 'nenfhors']:
            data_frame.loc[data_frame[variable].isnull(), variable] = 0
    if year_data == 2011:
        for vehicule_variable in ['veh_tot', 'veh_essence', 'veh_diesel', 'pourcentage_vehicule_essence',
        'rev_disp_loyerimput', 'rev_disponible', 'loyer_impute']:
            data_frame.loc[data_frame[vehicule_variable].isnull(), vehicule_variable] = 0
    # 'ratio_loyer_impute',  'ratio_revenus' To be added

    data_frame.index.name = "ident_men"
    # TODO: Homogénéiser: soit faire en sorte que ident_men existe pour toutes les années
    # soit qu'elle soit en index pour toutes

    # On ne garde que les ménages métropolitains
    if year_data == 2011:
        data_frame = data_frame.query('zeat != 0').copy()
        #pass

    try:
        data_frame.reset_index(inplace = True)
    except ValueError as e:
        log.info('ignoring reset_index because {}'.format(e))

    # Remove duplicated colums causing bug with HDFStore
    # according to https://github.com/pydata/pandas/issues/6240
    # using solution form stackoverflow
    # http://stackoverflow.com/questions/16938441/how-to-remove-duplicate-columns-from-a-dataframe-using-python-pandas
    data_frame = data_frame.T.groupby(level = 0).first().T

    log.info('Saving the openfisca indirect taxation input dataframe')
    try:
        openfisca_survey_collection = SurveyCollection.load(
            collection = 'openfisca_indirect_taxation', config_files_directory = config_files_directory)
    except:
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


def run(years_calage):
    import time
    year_data_list = [1995, 2000, 2005, 2011]
    for year_calage in years_calage:
        start = time.time()
        run_all(year_calage, year_data_list)
        log.info("Finished {}".format(time.time() - start))


if __name__ == '__main__':
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    years_calage = [2000, 2005, 2011]
    run(years_calage)
