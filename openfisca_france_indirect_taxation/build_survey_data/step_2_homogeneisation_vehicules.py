

import logging


from openfisca_survey_manager.survey_collections import SurveyCollection


from openfisca_survey_manager.temporary import temporary_store_decorator
from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype


log = logging.getLogger(__name__)


# Etape 0-2 : Homogénéïsation des données sur les véhicules
#
# Données sur les types de carburants


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def build_homogeneisation_vehicules(temporary_store = None, year = None):
    '''Compute vehicule numbers by type'''
    assert temporary_store is not None
    temporary_store.open()
    assert year is not None
    # Load data
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory)
    survey = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year))

    if year == 1995:
        vehicule = None

    # L'enquête BdF 1995 ne contient pas d'information sur le type de carburant utilisé par les véhicules.

    if year == 2000:
        vehicule = survey.get_values(table = 'depmen')
        kept_variables = ['ident', 'carbu01', 'carbu02']
        vehicule = vehicule[kept_variables].copy()
        vehicule.rename(columns = {'ident': 'ident_men'}, inplace = True)
        vehicule.rename(columns = {'carbu01': 'carbu1'}, inplace = True)
        vehicule.rename(columns = {'carbu02': 'carbu2'}, inplace = True)
        vehicule['veh_tot'] = 1
        vehicule['veh_essence'] = 1 * (vehicule['carbu1'] == 1) + 1 * (vehicule['carbu2'] == 1)
        vehicule['veh_diesel'] = 1 * (vehicule['carbu1'] == 2) + 1 * (vehicule['carbu2'] == 2)
        vehicule.index = vehicule.index.astype(ident_men_dtype)

    if year in [2005, 2011, 2017]:
        vehicule = survey.get_values(table = 'automobile', ignorecase = True)

        if year == 2005:
            vehicule = vehicule[
                ['ident_men', 'carbu']
                ].copy()
            vehicule['veh_tot'] = 1
            vehicule['veh_essence'] = vehicule['carbu'] == 1
            vehicule['veh_diesel'] = vehicule['carbu'] == 2

        if year == 2011:
            kept_variables = ['ident_men', 'carbu']
            vehicule = vehicule.rename(
                columns = {'ident_me': 'ident_men'},
                )[kept_variables].copy()
            vehicule['veh_tot'] = 1
            vehicule['veh_essence'] = vehicule['carbu'] == 1
            vehicule['veh_diesel'] = vehicule['carbu'] == 2

        if year == 2017:
            vehicule['veh_tot'] = 1
            vehicule['veh_essence'] = vehicule['carbu1'] == 1
            vehicule['veh_diesel'] = vehicule['carbu2'] == 1
            vehicule['veh_gpl'] = vehicule['carbu3'] == 1
            vehicule['veh_electrique'] = vehicule['carbu4'] == 1
            vehicule['veh_autre'] = vehicule['carbu5'] == 1

        # Compute the number of cars by category and save
        # Ignore GPL, electric and others than essence and diesel
        vehicule = vehicule.groupby(by = 'ident_men')[['veh_tot', 'veh_essence', 'veh_diesel']].sum()
        vehicule['pourcentage_vehicule_essence'] = 0
        vehicule.loc[vehicule.veh_tot != 0, 'pourcentage_vehicule_essence'] = vehicule.veh_essence / vehicule.veh_tot
        # Save in temporary store
        vehicule.index = vehicule.index.astype(ident_men_dtype)
        temporary_store['automobile_{}'.format(year)] = vehicule
        temporary_store.close()


if __name__ == '__main__':
    import sys
    import time
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    deb = time.process_time()()
    year = 2005
    build_homogeneisation_vehicules(year = year)
    log.info('step 0_2_homogeneisation_vehicules duration is {}'.format(time.process_time()() - deb))
