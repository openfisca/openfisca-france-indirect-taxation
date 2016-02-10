# -*- coding: utf-8 -*-


import os
import pandas
import pkg_resources


from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection

from openfisca_france_indirect_taxation.utils import get_parametres_fiscalite_data_frame
from openfisca_france_indirect_taxation.scripts.build_coicop_nomenclature import build_coicop_nomenclature

year = 2011
aliss_survey_collection = SurveyCollection.load(
    collection = 'aliss', config_files_directory = config_files_directory
    )
aliss_survey_collection
survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

df = survey.get_values(table = 'Base_ALISS_2011')
dirty_produits = df.souscode.unique()
code_coicop_by_dirty_produits = dict()

for dirty_produit in dirty_produits:
    code_coicop = '0' + '.'.join(dirty_produit[:4])
    code_coicop_by_dirty_produits[dirty_produit] = code_coicop

clean_dirty_produits_data_frame = pandas.DataFrame()
clean_dirty_produits_data_frame['dirty'] = code_coicop_by_dirty_produits.keys()
clean_dirty_produits_data_frame['code_coicop'] = code_coicop_by_dirty_produits.values()

print code_coicop_by_dirty_produits
data_frame = clean_dirty_produits_data_frame


def merge_with_coicop(data_frame):
    coicop_nomenclature = build_coicop_nomenclature()
    level = data_frame['code_coicop'].loc[0].count('.') + 1
    print level
    coicop_nomenclature['poste_coicop'] = coicop_nomenclature['code_coicop'].copy()
    coicop_nomenclature['code_coicop'] = coicop_nomenclature['code_coicop'].str[:2 * level]
    print coicop_nomenclature['code_coicop'][:5]
    df = data_frame.merge(coicop_nomenclature, on = 'code_coicop', how = 'outer')
    return df[[
        u'label_division', u'label_groupe', u'label_classe', u'label_sous_classe', u'label_poste',
        u'poste_coicop', u'code_coicop', u'dirty'
        ]].sort_values(by = u'poste_coicop')

df = merge_with_coicop(data_frame)
boum



liste_produits_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    'liste_produits.xlsx'
    )

liste_produits = pandas.read_excel(liste_produits_path)
liste_produits.columns
sous_codes = liste_produits.sous_code.dropna().tolist()
postes = list()
for sous_code in sous_codes:
    postes.append(sous_code[0:4])


taxe_by_categorie_fiscale_number = {
    1: 'tva_taux_super_reduit',
    2: 'tva_taux_reduit',
    3: 'tva_taux_plein',
    4: 'tva_taux_intermediaire',
    7: 'cigarettes',
    8: 'cigares',
    9: 'tabac_a_rouler',
    10: 'alcools_forts',
    11: 'tva_taux_plein',
    12: 'vin',
    13: 'biere',
    14: 'ticpe',
    15: 'assurance_transport',
    16: 'assurance_sante',
    17: 'autres_assurances'
    }

categories_fiscales_data_frame = get_parametres_fiscalite_data_frame()[
    ['posteCOICOP', 'annee', 'description', 'categoriefiscale']].copy()

categories_fiscales = categories_fiscales_data_frame.query('annee == @year')
produit_by_categorie_fiscale = categories_fiscales.loc[
    categories_fiscales.posteCOICOP.astype(str).str[:2].isin(['11', '21'])]

produit_by_taxe = produit_by_categorie_fiscale.replace({'categoriefiscale': taxe_by_categorie_fiscale_number})

# TODO check notamment problème avec sucre confiseries