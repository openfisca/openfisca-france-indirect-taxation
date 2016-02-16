# -*- coding: utf-8 -*-


import pandas


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_indirect_taxation.scripts.build_coicop_nomenclature import build_coicop_nomenclature
from openfisca_france_indirect_taxation.scripts.build_coicop_legislation import get_categorie_fiscale


def coicop_from_aliss(year = 2011):
    assert year == 2011
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

    aliss = survey.get_values(table = 'Base_ALISS_2011')
    dirty_produits = aliss.souscode.unique()
    entries = list()

    for dirty_produit in dirty_produits:
        entries.append(dict(
            code_coicop = '0' + '.'.join(dirty_produit[:4]),
            label = dirty_produit[6:],
            code_aliss = dirty_produit[:6],
            ))

    result = pandas.DataFrame(entries)

    assert not result.code_coicop.duplicated().any()

    return result


def coicop_from_bdf(year = 2011):
    assert year == 2011
    from openfisca_france_indirect_taxation.utils import get_transfert_data_frames
    matrice_passage_data_frame, _ = get_transfert_data_frames(year)
    matrice_passage_data_frame.rename(
        columns = {
            'poste{}'.format(year): 'poste_bdf',
            'label{}'.format(year): 'label',
            },
        inplace = True
        )
    dirty_produits = matrice_passage_data_frame['poste_bdf'].unique()
    entries = list()

    for dirty_produit in dirty_produits:
        dirty_produit_str = str(dirty_produit)
        selection = matrice_passage_data_frame.poste_bdf == dirty_produit
        code_coicop = '0' + '.'.join(dirty_produit_str) \
            if len(dirty_produit_str) <= 4 \
            else dirty_produit_str[:2] + '.' + '.'.join(dirty_produit_str[2:])
        entries.append(dict(
            code_coicop = code_coicop,
            label = matrice_passage_data_frame.loc[selection, 'label'].unique()[0],
            code_bdf = dirty_produit_str,
            ))

    result = pandas.DataFrame(entries)
    assert not result.code_coicop.duplicated().any()
    return result


def merge_with_coicop(data_frame):
    coicop_nomenclature = build_coicop_nomenclature()
    level = data_frame['code_coicop'].loc[0].count('.') + 1
    coicop_nomenclature['poste_coicop'] = coicop_nomenclature['code_coicop'].copy()
    coicop_nomenclature['code_coicop'] = coicop_nomenclature['code_coicop'].str[:2 * level]
    df = data_frame.merge(coicop_nomenclature, on = 'code_coicop', how = 'outer')
    return df[[
        u'label_division', u'label_groupe', u'label_classe', u'label_sous_classe', u'label_poste',
        u'poste_coicop', u'code_coicop', u'label'
        ]].sort_values(by = u'poste_coicop')


def test_coicop_to_legislation(data_frame, adjust_coicop, year):
    errors = list()
    for code_coicop in data_frame.code_coicop.unique():
        selection = data_frame.loc[data_frame.code_coicop == code_coicop].copy()
        products = selection.label.unique()
        try:
            print code_coicop, products
            print get_categorie_fiscale(
                adjust_coicop.get(code_coicop, code_coicop), year = year)
        except AssertionError:
            print 'error'
            error = dict(
                code_coicop = code_coicop,
                products = products,
                categorie_fiscale = get_categorie_fiscale(
                    adjust_coicop.get(code_coicop, code_coicop),
                    year = year,
                    assertion_error = False)
                )
            errors.append(error)
    return errors


adjust_coicop = {
    '01.1.1.5': '01.1.1.4.1',  # Autres céréales et produits à base de céréales]
    '01.1.2.7': '01.1.2.6.1',  # Autres viandes comestibles fraîches ou surge...
    '01.1.3.0': '01.1.3.1.1',  # Poissons frais
    '01.1.3.3': '01.1.3.2.1',  # Poissons et fruits de mer salés, fumés, séchés]
    '01.1.3.4': '01.1.3.2.2',  # Conserves et plats préparés à base de produi...
    '01.1.4.5': '01.1.4.3.1',  # Fromage et lait caillé]
    '01.1.4.6': '01.1.4.2.2',  # Autres produits laitiers (dessert à base de ...
    '01.1.4.7': '01.1.4.4.1',  # Oeufs
    '01.1.5.2': '01.1.5.2.2',  # Margarine
    '01.1.5.3': '01.1.5.2.1',  # Huiles alimentaires d'olive]
    '01.1.5.4': '01.1.5.2.1',  # Huiles alimentaires d'arachide, de tournesol...
    # On a rassemblé les deux les huiles alimentaires # TODO: peut-être faut-il séparer les huiles végétales
    # '01.1.5.5'  [ saindoux et autres graisses d'origine animale]
    '01.1.6.2': '01.1.6.1.1',  # bananes fraiches
    '01.1.6.3': '01.1.6.1.1',  # pommes
    '01.1.6.4': '01.1.6.1.1',  # poires
    # TODO: affiner 01.1.6.1.1 ou pas ?
    '01.1.6.5': '01.1.6.2.1',  # fruits à noyaux (frais ou congelés)]
    '01.1.6.6': '01.1.6.2.1',  # baies (fraîches ou congelées)]
    '01.1.6.7': '01.1.6.2.1',  # autres fruits, fruits tropicaux (frais ou co...
    '01.1.6.8': '01.1.6.2.1',  # fruits séchés]
    '01.1.6.9': '01.1.6.2.1',  # fruits au sirop et fruits surgelés]
    # TODO: affiner 01.1.6.2.1 ou pas ?
    '01.1.7.2': '01.1.7.1.1',  # choux (frais)
    '01.1.7.3': '01.1.7.1.1',  # légumes frais cultivés pour leurs fruits]
    '01.1.7.4': '01.1.7.1.1',  # racines alimentaires fraiches et champignons...
    '01.1.7.5': '01.1.7.2.1',  # légumes secs]
    '01.1.7.6': '01.1.7.2.1',  # légumes surgelés (non cuisinés)]
    '01.1.7.7': '01.1.7.2.1',  # légumes et plats à base de légume, en conser...
    '01.1.7.9': '01.1.7.2.2',  # pomme de terre, autres tubercules, produits ...
    '01.1.7.8': '01.1.7.2.3',  # légumes préparés et plats à base de légumes,...
    '01.1.8.1': '01.1.8.1.1',  # sucre
    '01.1.8.2': '01.1.8.1.2',  # confitures, marmelade, compote, gelées, purées et pâtes de fruits, miel
    '01.1.8.3': '01.1.8.2.1',  # chocolat
    '01.1.8.4': '01.1.8.1.3',  # sucreries, bonbons et autres confiseries
    '01.1.8.5': '01.1.8.3.1',  # crèmes glacées, sorbets, entremets glacés]
    '01.1.8.6': '01.1.8.1.1',  # autres produits à base de sucre (fruits confits, pâtes à tartiner)
    # TODO: créer une nouvelle section ? pour 01.1.8.6
    '01.1.9.4': '01.1.8.1.1',  # autres produits alimentaires (aliments enfants, produits diététiques)
    '01.2.1.1': '01.2.1.2',    # café
    '01.2.1.2': '01.2.1.3.1',  # thé et plantes à infusion
    '01.2.1.3': '01.2.1.1.1',  # cacao et chocolat en poudre
    '01.2.2.1': '01.2.2.1.1',  # eaux minérales
    '01.2.2.2': '01.2.2.2.2',  # boissons gazeuses
    '01.2.2.3': '01.2.2.2',    # jus de fruits et de légumes, sirops, boisson...
    '01.2.2.4': '01.2.2.2.1',  # jus de légumes
    '11.1.1.2': '11.1.1.1.2',  # Repas dans cafés, bar
    }


def aliss(year = 2011):
    aliss_coicop = coicop_from_aliss(year = year)
    data_frame = merge_with_coicop(aliss_coicop)
    return test_coicop_to_legislation(data_frame, adjust_coicop, year = year)


def bdf(year = 2011):
    bdf_coicop = coicop_from_bdf(year = year)
    data_frame = merge_with_coicop(bdf_coicop)
    return test_coicop_to_legislation(data_frame, adjust_coicop, year = year)


# TODO check notamment problème avec sucre confiseries
if __name__ == '__main__':
    # result = coicop_from_bdf(year = 2011)
    errors = bdf()
    len(errors)
    df = pandas.DataFrame.from_records(errors).sort_values(by = 'code_coicop')
    print df[['code_coicop', 'products', 'categorie_fiscale']]
