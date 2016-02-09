# -*- coding: utf-8 -*-


from __future__ import division

import numpy as np
import os
import pandas as pd
import pkg_resources


legislation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'legislation',
    )


sub_levels = ['divisions', 'groupes', 'classes', 'sous_classes', 'postes']
divisions = ['0{}'.format(i) for i in range(1, 10)] + ['11', '12']  # TODO: fix this
taxe_by_categorie_fiscale_number = {
    0: '',
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


def build_coicop_level_nomenclature(level):
    assert level in sub_levels
    data_frame = pd.read_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop_source_by_{}.csv'.format(level)),
        sep = ';',
        header = -1,
        )
    data_frame.reset_index(inplace = True)
    data_frame.rename(columns = {0: 'code_coicop', 1: 'label_{}'.format(level[:-1])}, inplace = True)
    data_frame = data_frame.ix[2:].copy()

    # Problème dû au fichier Excel, nous devons changer le contenu d'une case:
    if level == 'sous_classes':
        data_frame.loc[data_frame['code_coicop'] == "01.1.4.4", 'code_coicop'] = "'01.1.4.4"

    index, stop = 1, False
    for sub_level in sub_levels:
        if stop:
            continue
        if sub_level == 'divisions':
            data_frame[sub_level] = data_frame['code_coicop'].str[index:index + 2].astype(int)
            index = index + 3
        else:
            data_frame[sub_level] = data_frame['code_coicop'].str[index:index + 1].astype(int)
            index = index + 2

        if level == sub_level:
            stop = True

    if level == 'postes':
        data_frame['code_coicop'] = data_frame['code_coicop'].str[1:].copy()
    else:
        del data_frame['code_coicop']

    data_frame.reset_index(inplace = True, drop = True)
    data_frame.to_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop_by_{}.csv'.format(level)),
        sep = ';',
        )

    return data_frame


def build_coicop_nomenclature():
    for index in range(len(sub_levels) - 1):
        level = sub_levels[index]
        next_level = sub_levels[index + 1]
        on = sub_levels[:index + 1]
        if index == 0:
            coicop_nomenclature = pd.merge(
                build_coicop_level_nomenclature(level), build_coicop_level_nomenclature(next_level),
                on = on, left_index = False, right_index = False)
        else:
            coicop_nomenclature = pd.merge(coicop_nomenclature, build_coicop_level_nomenclature(next_level), on = on)

    coicop_nomenclature = coicop_nomenclature[
        ['code_coicop'] +
        ['label_{}'.format(sub_level[:-1]) for sub_level in sub_levels] +
        sub_levels
        ].copy()

    coicop_nomenclature['start'] = 0
    coicop_nomenclature['stop'] = 0
    coicop_nomenclature.to_csv(
        os.path.join(legislation_directory, 'nomenclature_coicop.csv'),
        sep = ';',
        )
    return coicop_nomenclature.copy()


def get_dominant_and_exceptions(division):
    assert division in divisions
    parametres_fiscalite_file_path = os.path.join(legislation_directory, 'coicop_to_categorie_fiscale.csv')
    parametres_fiscalite_data_frame = pd.read_csv(
        parametres_fiscalite_file_path,
        sep = ';',
        converters = {'posteCOICOP': unicode}
        )
    parametres_fiscalite_data_frame['division'] = parametres_fiscalite_data_frame['posteCOICOP'].str[:2].copy()

    division_dataframe = parametres_fiscalite_data_frame.query('division == @division')
    dominant_fiscal_category = division_dataframe.categoriefiscale.value_counts().argmax()
    exceptions = division_dataframe.query('categoriefiscale != @dominant_fiscal_category')

    return dominant_fiscal_category, exceptions


def format_exceptions(exceptions):
    grouped = exceptions.groupby(
        by = [exceptions.annee - np.arange(exceptions.shape[0]), 'posteCOICOP', 'categoriefiscale']
        )
    for k, g in grouped:
        # print g
        print g.posteCOICOP.unique(), g.description.unique(), g.annee.min(), g.annee.max(), \
            taxe_by_categorie_fiscale_number[int(g.categoriefiscale.unique())]


for coicop_division in divisions:
    dominant, exceptions = get_dominant_and_exceptions(coicop_division)
    print coicop_division
    print dominant
    format_exceptions(exceptions)
    print "  "


def apply_modification(coicop_nomenclature = None, value = None, categorie_fiscale = None, start = 1994, stop = 2014):
    assert coicop_nomenclature is not None

    categorie_fiscale in taxe_by_categorie_fiscale_number.values()

    if isinstance(value, int):
        selection = coicop_nomenclature.divisions == value
    elif isinstance(value, str):
        selection = coicop_nomenclature.code_coicop.str[:len(value)] == value
    elif isinstance(value, list):
        selection = coicop_nomenclature.code_coicop.isin(value)

    coicop_nomenclature.loc[selection, 'categorie_fiscale'] = categorie_fiscale
    filled_start_stop = (
        coicop_nomenclature.loc[selection, 'start'].unique() != 0 or
        coicop_nomenclature.loc[selection, 'stop'].unique() != 0
        )
    if filled_start_stop and (start != 1994 or stop != 2014):
        coicop_copy = coicop_nomenclature.loc[selection].copy()
        coicop_copy['start'] = start
        coicop_copy['stop'] = stop
        print coicop_copy
        coicop_nomenclature = coicop_nomenclature.append(coicop_copy, ignore_index = True)
        coicop_nomenclature.reset_index(inplace = True, drop = True)
        coicop_nomenclature.sort_values(by = 'code_coicop', inplace = True)
    else:
        coicop_nomenclature.loc[selection, 'start'] = 1994
        coicop_nomenclature.loc[selection, 'stop'] = 2014

    print coicop_nomenclature.categorie_fiscale.value_counts()
    return coicop_nomenclature


coicop_nomenclature = build_coicop_nomenclature()

# 01 Produits alimentaires et boissons non alcoolisées
# ils sont tous à taux réduit
alimentation = dict(
    value = 1,
    categorie_fiscale = 'tva_taux_reduit'
    )
# sauf la margarine à taux plein
margarine = dict(
    value = '01.1.5.2.2',
    categorie_fiscale = 'tva_taux_plein',
    )
# et les confiseries et le chocolat  # TODO check
confiserie = dict(
    value = ['01.1.8.1.3', '01.1.8.2.1', '01.1.8.2.2'],
    categorie_fiscale = 'tva_taux_plein'
    )
# 02 Boissons alcoolisées et tabac
# alccols forts
alcools = dict(
    value = '02.1.1',
    categorie_fiscale = 'alcools_forts',
    )
# vins et boissons fermentées
vin = dict(
    value = '02.1.2',
    categorie_fiscale = 'vin',
    )
# bière
biere = dict(
    value = '02.1.3',
    categorie_fiscale = 'biere',
    )
# TODO: tabac
# u'02202'] ['Cigares et cigarillos'] 1994 2014 cigares
# [u'02201'] ['Cigarettes'] 1994 2014 cigarettes
# TODO: Rajouter Stupéfiants sans taxe
#
# 03 Habillement et chaussures
habillement = dict(
    value = 3,
    categorie_fiscale = 'tva_taux_plein'
    )

# 04 Logement, eau, gaz, électricité et autres combustibles
logement = dict(
    value = 4,
    categorie_fiscale = 'tva_taux_plein',
    )
# sauf distribution d'eau, enlèvement des ordures ménagères, assainissement, autres services liés au logement n.d.a.
# qui sont au taux réduit de 1994 à 2011
eau_ordures_assainissement = dict(
    value = ['04.4.1.1.1', '04.4.1.2.1', '04.4.1.3.1'],
    categorie_fiscale = 'tva_taux_reduit',
    stop = '2011',
    )
# avant de passer au taux intermédiaire
eau_ordures_assainissement_reforme_2012 = dict(
    value = ['04.4.1.1.1', '04.4.1.2.1', '04.4.1.3.1'],
    categorie_fiscale = 'tva_taux_intermediaire',
    start = '2012',
    )
# et pas de taxation des loyers
loyers = dict(
    value = ['04.1.1.1.1', '04.1.1.2.1'],
    categorie_fiscale = '',
    )
# TODO ajouter loyers fictifs
# 05 Ameublement, équipement ménager et entretien courant de la maison
ameublement = dict(
    value= 5,
    categorie_fiscale = 'tva_taux_plein',
    )
# sauf Services domestiques et autres services pour l'habitation
services_domestiques = dict(
    value = '05.6.2',
    categorie_fiscale = 'tva_taux_reduit',
    )

for member in [
    alimentation, margarine, confiserie,
    alcools, vin, biere,
    habillement,
    logement, eau_ordures_assainissement, eau_ordures_assainissement_reforme_2012, loyers,
    ameublement, services_domestiques,
    ]:
    coicop_nomenclature = apply_modification(coicop_nomenclature, **member)

boum
