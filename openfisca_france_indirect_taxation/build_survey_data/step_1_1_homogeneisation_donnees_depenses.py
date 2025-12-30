#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from openfisca_survey_manager.temporary import temporary_store_decorator
from openfisca_survey_manager.paths import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_france_indirect_taxation.scripts.build_bdf_nomenclature import build_complete_bdf_nomenclature

log = logging.getLogger(__name__)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def build_depenses_homogenisees(temporary_store = None, year = None):
    '''Build menage consumption by categorie fiscale dataframe.'''
    log.debug(f'Entering build_depenses_homogenisees for year={year}')
    assert temporary_store is not None
    temporary_store.open()
    assert year is not None
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory
        )
    survey = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year))

    # Homogénéisation des bases de données de dépenses
    if year == 1995:
        socioscm = survey.get_values(table = 'socioscm')
        poids = socioscm[['mena', 'ponderrd', 'exdep', 'exrev']]
        # cette étape de ne garder que les données dont on est sûr de la qualité et de la véracité
        # exdep = 1 si les données sont bien remplies pour les dépenses du ménage
        # exrev = 1 si les données sont bien remplies pour les revenus du ménage
        poids = poids[(poids.exdep == 1) & (poids.exrev == 1)]
        del poids['exdep'], poids['exrev']
        poids.rename(
            columns = {
                'mena': 'ident_men',
                'ponderrd': 'pondmen',
                },
            inplace = True
            )
        poids.set_index('ident_men', inplace = True)

        conso = survey.get_values(table = 'depnom')
        conso = conso[['valeur', 'montant', 'mena', 'nomen5']]
        conso = conso.groupby(['mena', 'nomen5']).sum()
        conso = conso.reset_index()
        conso.rename(
            columns = {
                'mena': 'ident_men',
                'nomen5': 'poste{}'.format(year),
                'valeur': 'depense',
                'montant': 'depense_avt_imput',
                },
            inplace = True
            )

        # Passage à l'euro
        conso.depense = conso.depense / 6.55957
        conso.depense_avt_imput = conso.depense_avt_imput / 6.55957
        conso_small = conso[['ident_men', 'poste1995', 'depense']]

        conso_unstacked = conso_small.set_index(['ident_men', 'poste1995']).unstack('poste1995')
        conso_unstacked = conso_unstacked.fillna(0)

        levels = conso_unstacked.columns.levels[1]
        labels = conso_unstacked.columns.labels[1]
        conso_unstacked.columns = levels[labels]
        conso_unstacked.rename(index = {0: 'ident_men'}, inplace = True)
        conso = conso_unstacked.merge(poids, left_index = True, right_index = True)
        conso = conso.reset_index()

    if year == 2000:
        conso = survey.get_values(table = 'consomen')
        conso.rename(
            columns = {
                'ident': 'ident_men',
                },
            inplace = True,
            )
        for variable in ['ctotale', 'c99', 'c99999'] + \
                        ['c0{}'.format(i) for i in range(1, 10)] + \
                        ['c{}'.format(i) for i in range(10, 14)]:
            del conso[variable]

    if year == 2005:
        conso = survey.get_values(table = 'c05d')

    if year == 2011 or year == 2017:
        conso = survey.get_values(table = 'c05', ignorecase = True)
        conso.rename(
            columns = {
                'ident_me': 'ident_men',
                },
            inplace = True,
            )

    if 'ctot' in conso.columns:
        del conso['ctot']

    # Grouping by coicop
    poids = conso[['ident_men', 'pondmen']].copy()
    poids.set_index('ident_men', inplace = True)
    conso.drop('pondmen', axis = 1, inplace = True)
    conso.set_index('ident_men', inplace = True)

    # Renomme les colonnes (c01111 - > poste_01_1_1_1) et utilie une nomenclautre BDF ajustée sur la comptabilité nationale.
    bdf_nomenclature = build_complete_bdf_nomenclature(year = 2017, to_csv= False)
    bdf_nomenclature.loc[:, 'adjusted_bdf'] = bdf_nomenclature.loc[:, 'adjusted_bdf'].apply(lambda x: 'poste_' + x.replace('.', '_'))
    bdf_nomenclature.loc[:, 'Code_sous_classe'] = bdf_nomenclature.loc[:, 'Code_sous_classe'].apply(lambda x: 'c' + x)
    bdf_nomenclature.rename({'Code_sous_classe': 'code_bdf'}, axis = 1, inplace = True)

    assert not set(conso.columns).difference(set(bdf_nomenclature.code_bdf))
    dict_codes = bdf_nomenclature.dropna().set_index('code_bdf').to_dict()['adjusted_bdf']
    coicop_data_frame = conso.rename(columns = dict_codes)
    depenses = coicop_data_frame.merge(poids, left_index = True, right_index = True)
    
    # On ventile les dépenses gaz et elec (factures jointes) dans les postes facture gaz et facture elec
    depenses['depenses_gaz_et_elec'] = (depenses['poste_04_5_2_1'] * depenses['poste_04_5_1_1']) > 0
    depenses_elec_seul_bdf = (depenses['poste_04_5_1_1'] * depenses['pondmen'] * depenses['depenses_gaz_et_elec']).sum()
    depenses_gaz_seul_bdf = (depenses['poste_04_5_2_1'] * depenses['pondmen'] * depenses['depenses_gaz_et_elec']).sum()
    part_gaz_seul_bdf = depenses_gaz_seul_bdf / (depenses_elec_seul_bdf + depenses_gaz_seul_bdf)
    part_elec_seul_bdf = 1 - part_gaz_seul_bdf
    depenses['poste_04_5_1_1'] = depenses['poste_04_5_1_1'] + part_elec_seul_bdf * depenses['poste_04_5_0_0']
    depenses['poste_04_5_2_1'] = depenses['poste_04_5_2_1'] + part_gaz_seul_bdf * depenses['poste_04_5_0_0']
    depenses['poste_04_5_0_0'] = 0
    depenses.drop('depenses_gaz_et_elec', axis = 1, inplace = True)
    
    temporary_store['depenses_{}'.format(year)] = depenses
    temporary_store.close()


if __name__ == '__main__':
    import sys
    import time
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    deb = time.process_time()()
    year = 2017
    build_depenses_homogenisees(year = year)
    log.info('duration is {}'.format(time.process_time()() - deb))
