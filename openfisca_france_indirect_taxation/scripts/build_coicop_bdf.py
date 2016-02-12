# -*- coding: utf-8 -*-


import pandas


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_indirect_taxation.scripts.build_coicop_nomenclature import build_coicop_nomenclature
from openfisca_france_indirect_taxation.scripts.build_coicop_legislation import get_categorie_fiscale


def coicop_from_aliss():
    year = 2011
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

    aliss = survey.get_values(table = 'Base_ALISS_2011')
    dirty_produits = aliss.souscode.unique()
    code_coicop_by_dirty_produits = dict()

    for dirty_produit in dirty_produits:
        code_coicop = '0' + '.'.join(dirty_produit[:4])
        code_coicop_by_dirty_produits[dirty_produit[6:]] = code_coicop

    result = pandas.DataFrame(dict(
        dirty = code_coicop_by_dirty_produits.keys(),
        code_coicop = code_coicop_by_dirty_produits.values()
        ))
    assert not result.code_coicop.duplicated().any()

    return result


def coicop_from_bdf():
    year = 2011
    openfisca_survey_collection = SurveyCollection.load(collection = "openfisca_indirect_taxation")
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)

    postes_coicop = [col for col in input_data_frame.columns if col.startswith('post')]
    postes_coicop
    dirty_produits = df.souscode.unique()
    code_coicop_by_dirty_produits = dict()

    for dirty_produit in dirty_produits:
        code_coicop = '0' + '.'.join(dirty_produit[:4])
        code_coicop_by_dirty_produits[dirty_produit[6:]] = code_coicop

    result = pandas.DataFrame(dict(
        dirty = code_coicop_by_dirty_produits.keys(),
        code_coicop = code_coicop_by_dirty_produits.values()
        ))
    return result


def merge_with_coicop(data_frame):
    coicop_nomenclature = build_coicop_nomenclature()
    level = data_frame['code_coicop'].loc[0].count('.') + 1
    coicop_nomenclature['poste_coicop'] = coicop_nomenclature['code_coicop'].copy()
    coicop_nomenclature['code_coicop'] = coicop_nomenclature['code_coicop'].str[:2 * level]
    df = data_frame.merge(coicop_nomenclature, on = 'code_coicop', how = 'outer')
    return df[[
        u'label_division', u'label_groupe', u'label_classe', u'label_sous_classe', u'label_poste',
        u'poste_coicop', u'code_coicop', u'dirty'
        ]].sort_values(by = u'poste_coicop')


def test_coicop_to_legislation(data_frame, adjust_coicop):
    for code_coicop in data_frame.code_coicop.unique():
        selection = data_frame.loc[data_frame.code_coicop == code_coicop].copy()
        try:
            print code_coicop, selection.dirty.unique()
            print get_categorie_fiscale(
                adjust_coicop.get(code_coicop, code_coicop), year = 2010)
        except:
            print selection
            raise()

def aliss():
    adjust_coicop = {
        '01.1.5.2': '01.1.5.2.2',
        '01.1.8.1': '01.1.8.1.1',
        }
    aliss_coicop = coicop_from_aliss()
    data_frame = merge_with_coicop(aliss_coicop)
    test_coicop_to_legislation(data_frame, adjust_coicop)


def bdf():
    bdf_coicop = coicop_from_bdf()
    data_frame = merge_with_coicop(aliss_coicop)


# TODO check notamment problème avec sucre confiseries
