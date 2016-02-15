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
    dirty_produits = input_data_frame.souscode.unique()
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
    errors = list()
    for code_coicop in data_frame.code_coicop.unique():
        selection = data_frame.loc[data_frame.code_coicop == code_coicop].copy()

        try:
            print code_coicop, selection.dirty.unique()
            print get_categorie_fiscale(
                adjust_coicop.get(code_coicop, code_coicop), year = 2010)
        except AssertionError:
            print 'error'
            error = dict(
                code_coicop = code_coicop,
                products = selection.dirty.unique(),
                categorie_fiscale = get_categorie_fiscale(
                    adjust_coicop.get(code_coicop, code_coicop),
                    year = 2010,
                    assertion_error = False)
                )
            errors.append(error)
    return errors


def aliss():
    adjust_coicop = {
        '01.1.5.2': '01.1.5.2.2',
        '01.1.8.1': '01.1.8.1.1',
        # '01.1.1.5'  [ Autres c�r�ales et produits � base de c�r�ales]
        # '01.1.2.7'  [ Autres viandes comestibles fra�ches ou surge...
        '01.1.3.0': '01.1.3.1.1',  # '01.1.3.0' [ Poissons frais]
        '01.1.3.3': '01.1.3.2.1',  # '01.1.3.3'  [ Poissons et fruits de mer sal�s, fum�s, s�ch�s]
        '01.1.3.4': '01.1.3.2.2',  # '01.1.3.4'  [ Conserves et plats pr�par�s � base de produi...
        # '01.1.4.5'                          [ Fromage et lait caill�]
        # '01.1.4.6'  [ Autres produits laitiers (dessert � base de ...
        '01.1.4.7': '01.1.4.4.1',  # '01.1.4.7' [ Oeufs]
        # '01.1.5.3'                     [ Huiles alimentaires d'olive]
        # '01.1.5.4'  [ Huiles alimentaires d'arachide, de tournesol...
        # '01.1.5.5'   [ saindoux et autres graisses d'origine animale]
        '01.1.6.3': '01.1.6.1',  # '01.1.6.3'  [ pommes] # TODO: affiner
        '01.1.6.4': '01.1.6.1',  # '01.1.6.4' [ poires]  # TODO: affiner
        # '01.1.6.5'             [ fruits � noyaux (frais ou congel�s)]
        # '01.1.6.6'                   [ baies (fra�ches ou congel�es)]
        # '01.1.6.7'  [ autres fruits, fruits tropicaux (frais ou co...
        # '01.1.6.8'                                   [ fruits s�ch�s]
        # '01.1.6.9'              [ fruits au sirop et fruits surgel�s]
        # '01.1.7.3'        [ l�gumes frais cultiv�s pour leurs fruits]
        # '01.1.7.4'  [ racines alimentaires fraiches et champignons...
        # '01.1.7.5'                                    [ l�gumes secs]
        # '01.1.7.6'                 [ l�gumes surgel�s (non cuisin�s)]
        # '01.1.7.7'  [ l�gumes et plats � base de l�gume, en conser...
        # '01.1.7.8'  [ l�gumes pr�par�s et plats � base de l�gumes,...
        # '01.1.7.9'  [ pomme de terre, autres tubercules, produits ...
        # '01.1.8.4'        [ sucreries, bonbons et autres confiseries]
        # '01.1.8.5'       [ cr�mes glac�es, sorbets, entremets glac�s]
        # '01.1.8.6'                 [ autres produits � base de sucre]
        # '01.1.9.4'                    [ autres produits alimentaires]
        # '01.2.2.3'  [ jus de fruits et de l�gumes, sirops, boisson...
        # '01.2.2.4'                                  [ jus de l�gumes]
        # '11.1.1.2'  cafés, bar pb boisson alcoolisées ou pas [nan] tva_taux_reduit, tva_taux_plein
        # '12.4.1.1'  assurances-vie                                             [nan] tva_taux_plein, tva_taux_reduit
        # '12.4.1.2'                                              [nan] tva_taux_reduit, tva_taux_plein
        # '12.4.1.3'                                              [nan] tva_taux_reduit, tva_taux_plein
        }

    aliss_coicop = coicop_from_aliss()
    data_frame = merge_with_coicop(aliss_coicop)
    return test_coicop_to_legislation(data_frame, adjust_coicop)


def bdf():
    bdf_coicop = coicop_from_bdf()
    data_frame = merge_with_coicop(bdf_coicop)


# TODO check notamment problème avec sucre confiseries
if __name__ == '__main__':
    result = coicop_from_aliss()
    errors = aliss()
    len(errors)
    df = pandas.DataFrame.from_records(errors).sort_values(by = 'code_coicop')
    print df[['code_coicop', 'products', 'categorie_fiscale']]
