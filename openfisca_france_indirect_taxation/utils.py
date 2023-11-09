import logging
import os
import pandas

try:
    from openfisca_survey_manager.survey_collections import SurveyCollection
except ImportError:
    SurveyCollection = None

from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location


log = logging.getLogger(__name__)

assets_directory = os.path.join(
    openfisca_france_indirect_taxation_location,
    'openfisca_france_indirect_taxation',
    'assets',
    )


def get_input_data_frame(year, use_entd = True):
    '''Retrieve budget des familles (BDF) survey data from disk with the opportunity to use variables from enquête nationale transports et déplacements (ENTD).

    :param year: survey year
    :type year: int
    :param use_entd: Use variables from ENTD, defaults to True
    :type use_entd: bool, optional
    :return: survey data
    :rtype: DataFrame
    '''
    openfisca_survey_collection = SurveyCollection.load(collection = 'openfisca_indirect_taxation')
    openfisca_survey = openfisca_survey_collection.get_survey('openfisca_indirect_taxation_data_{}'.format(year))
    input_data_frame = openfisca_survey.get_values(table = 'input')
    input_data_frame.reset_index(inplace = True)

    if use_entd and (year == 2011 or year == 2017):
        log.info('Using variables from ENTD')

        input_data_frame.rename(
            columns = {
                'depenses_carburants_corrigees_entd': 'depenses_carburants',
                'depenses_diesel_corrigees_entd': 'depenses_diesel',
                'depenses_essence_corrigees_entd': 'depenses_essence',
                },
            inplace = True,
            )

    return input_data_frame


def get_transfert_data_frames(year = None):
    assert year is not None
    matrice_passage_csv_file_path = os.path.join(
        assets_directory,
        'legislation',
        'Matrice passage {}-COICOP.csv'.format(year),
        )
    if os.path.exists(matrice_passage_csv_file_path):
        matrice_passage_data_frame = pandas.read_csv(matrice_passage_csv_file_path, index_col = False)
    else:
        matrice_passage_xls_file_path = os.path.join(
            assets_directory,
            'legislation',
            'Matrice passage {}-COICOP.xls'.format(year),
            )
        matrice_passage_data_frame = pandas.read_excel(matrice_passage_xls_file_path)
        # Do not write row names
        matrice_passage_data_frame.to_csv(matrice_passage_csv_file_path, encoding = 'utf-8', index = False)

    if year == 2005:
        matrice_passage_data_frame = matrice_passage_data_frame.query('poste2005 != 5316')
    if year >= 2011:
        matrice_passage_data_frame[f'poste{year}'] = \
            matrice_passage_data_frame[f'poste{year}'].apply(lambda x: int(x.replace('c', '').lstrip('0')))

    selected_parametres_fiscalite_data_frame = get_parametres_fiscalite_data_frame(year = year)
    return matrice_passage_data_frame, selected_parametres_fiscalite_data_frame


def get_parametres_fiscalite_data_frame(year = None):
    parametres_fiscalite_csv_file_path = os.path.join(
        assets_directory,
        'legislation',
        'Parametres fiscalite indirecte.csv',
        )
    if os.path.exists(parametres_fiscalite_csv_file_path):
        parametres_fiscalite_data_frame = pandas.read_csv(parametres_fiscalite_csv_file_path)
    else:
        parametres_fiscalite_xls_file_path = os.path.join(
            assets_directory,
            'legislation',
            'Parametres fiscalite indirecte.xls',
            )
        parametres_fiscalite_data_frame = pandas.read_excel(parametres_fiscalite_xls_file_path,
            sheet_name = 'categoriefiscale')
        parametres_fiscalite_data_frame.to_csv(parametres_fiscalite_csv_file_path, encoding = 'utf-8')

    if year:
        selected_parametres_fiscalite_data_frame = \
            parametres_fiscalite_data_frame[parametres_fiscalite_data_frame.annee == year].copy()
        return selected_parametres_fiscalite_data_frame
    else:
        return parametres_fiscalite_data_frame
