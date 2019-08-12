# -*- coding: utf-8 -*-


import os
import pkg_resources
import pandas as pd
import numpy as np

from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection


def add_area_dummy(dataframe):
    areas = ['rural', 'villes_petites', 'villes_moyennes', 'villes_grandes', 'agglo_paris']
    for area in areas:
        dataframe[area] = 0
    dataframe.loc[dataframe['strate'] == 0, 'rural'] = 1
    dataframe.loc[dataframe['strate'] == 1, 'villes_petites'] = 1
    dataframe.loc[dataframe['strate'] == 2, 'villes_moyennes'] = 1
    dataframe.loc[dataframe['strate'] == 3, 'villes_grandes'] = 1
    dataframe.loc[dataframe['strate'] == 4, 'agglo_paris'] = 1
    return dataframe


def add_niveau_vie_decile(dataframe):
    dataframe['niveau_de_vie'] = dataframe['rev_disponible'] / dataframe['ocde10']
    dataframe = dataframe.sort_values(by = ['niveau_de_vie'])
    dataframe['cum_pondmen'] = dataframe['pondmen'].cumsum()
    dataframe['rank'] = dataframe['cum_pondmen'] / dataframe['cum_pondmen'].max()
    dataframe['rank'] = dataframe['rank'].astype(float)
    dataframe['niveau_vie_decile'] = np.ceil(dataframe['rank'] * 10)
    dataframe.drop(['rank', 'cum_pondmen', 'niveau_de_vie'], axis = 1, inplace = True)
    return dataframe


def add_stalog_dummy(dataframe):
    stalog = ['proprietaire', 'accedant', 'locataire', 'sous_loc', 'loge_gratuit']
    for statut in stalog:
        dataframe[statut] = 0
    dataframe.loc[dataframe['stalog'] == 1, 'proprietaire'] = 1
    dataframe.loc[dataframe['stalog'] == 2, 'accedant'] = 1
    dataframe.loc[dataframe['stalog'] == 3, 'locataire'] = 1
    dataframe.loc[dataframe['stalog'] == 4, 'sous_loc'] = 1
    dataframe.loc[dataframe['stalog'] == 5, 'loge_gratuit'] = 1
    del dataframe['stalog']
    return dataframe


def add_vag_dummy(dataframe):
    first_vag = dataframe['vag'].min()
    last_vag = dataframe['vag'].max()
    for vag in range(first_vag, last_vag + 1):
        dataframe['vag_{}'.format(vag)] = 0
        dataframe.loc[dataframe['vag'] == vag, 'vag_{}'.format(vag)] = 1
    return dataframe


def electricite_only(dataframe):
    energie_logement_non_elec = ['poste_04_5_2_1_1', 'poste_04_5_2_2_1', 'poste_04_5_3_1_1', 'poste_04_5_4_1_1']

    dataframe['sum'] = 0
    for energie in energie_logement_non_elec:
        try:
            dataframe['sum'] += dataframe[energie]
        except Exception:
            pass
    dataframe['elect_only'] = 0
    dataframe.loc[dataframe['sum'] == 0, 'elect_only'] = 1
    del dataframe['sum']
    return dataframe


def indices_prix_carbus(year):
    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_carbu = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'prix',
            'prix_mensuel_carbu_match_to_vag.csv'
            ), sep =',', decimal = '.'
        )
    prix_carbu = prix_carbu[['diesel_ttc'] + ['super_95_ttc'] + ['vag']].astype(float)

    quantite_carbu_vp_france = pd.read_csv(os.path.join(default_config_files_directory,
            'openfisca_france_indirect_taxation', 'assets', 'quantites',
            'quantite_carbu_vp_france.csv'), sep = ',')
    quantite_carbu_vp_france.rename(columns = {'Unnamed: 0': 'annee'}, inplace = True)

    quantite_carbu_vp_france['part_conso_ess'] = \
        quantite_carbu_vp_france['essence'] / (quantite_carbu_vp_france['essence'] + quantite_carbu_vp_france['diesel'])
    quantite_carbu_vp_france = quantite_carbu_vp_france[quantite_carbu_vp_france['annee'] == year]
    part_conso_ess = quantite_carbu_vp_france['part_conso_ess'].min()

    prix_carbu['indice_ess'] = prix_carbu['super_95_ttc'] / (prix_carbu['super_95_ttc'] * part_conso_ess
+ prix_carbu['diesel_ttc'] * (1 - part_conso_ess))
    prix_carbu['indice_die'] = prix_carbu['indice_ess'] * (prix_carbu['diesel_ttc'] / prix_carbu['super_95_ttc'])

    return prix_carbu[['indice_ess'] + ['indice_die'] + ['vag']]


# On veut construire des indices de prix plus précis pour les carburants, en prenant en compte le type de voitures
# dont disposent les ménages. On pondère donc en utilisant un indice de prix qui dépend de la part de véhicules essences
# de chaque ménage. On estime que si 1/2 véhicule est essence, on affecte pour 1/2 l'indice du prix de l'essence,
# et sur 1/2 celui du diesel. On ne prend donc pas en compte les distances parcourus avec chaque véhicule.
def price_carbu_pond(dataframe):
    dataframe['veh_tot'] = dataframe['veh_essence'] + dataframe['veh_diesel']
    dataframe['part_veh_essence'] = 0.5
    dispose_de_vehicule = dataframe['veh_tot'] != 0
    dataframe.loc[dispose_de_vehicule, 'part_veh_essence'] = \
        dataframe.loc[dispose_de_vehicule, 'veh_essence'] / dataframe.loc[dispose_de_vehicule, 'veh_tot']
    dataframe['prix_carbu'] = dataframe['prix_carbu'] * (dataframe['part_veh_essence'] * dataframe['indice_ess']
+ (1 - dataframe['part_veh_essence']) * dataframe['indice_die'])
    del dataframe['indice_ess'], dataframe['indice_die']
    return dataframe


def price_carbu_from_quantities(dataframe, year):
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory
        )
    survey = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year))

    carnets = survey.get_values(table = 'CARNETS')
    carnets_carbu = carnets[carnets['nomen5'] == 7221].copy()
    carnets_carbu[['quantite', 'montant']] = carnets_carbu[['quantite', 'montant']].astype(float)

    carnets_carbu = carnets_carbu.rename(columns = {'ident_me': 'ident_men'})
    grouped = carnets_carbu.groupby(['ident_men']).sum()

    grouped['prix_carbu_consommateur'] = grouped['montant'] / grouped['quantite']
    carnets_carbu_select = grouped[grouped['prix_carbu_consommateur'] < 2].copy()
    carnets_carbu_select = carnets_carbu_select[carnets_carbu_select['prix_carbu_consommateur'] > .8].copy()
    carnets_carbu_select = carnets_carbu_select.reset_index()
    carnets_carbu_select['ident_men'] = carnets_carbu_select['ident_men'].astype(str)

    indice_prix_moyen = dataframe['prix_carbu'].mean()
    prix_consommateur_moyen = carnets_carbu_select['prix_carbu_consommateur'].mean()
    dataframe2 = pd.merge(
        dataframe, carnets_carbu_select[['ident_men', 'prix_carbu_consommateur']],
        on = 'ident_men', how = 'left'
        )
    dataframe2.loc[dataframe2['prix_carbu_consommateur'] < 2, 'prix_carbu'] = \
        dataframe2['prix_carbu_consommateur'] * indice_prix_moyen / prix_consommateur_moyen

    return dataframe2


def price_energy_from_contracts(dataframe, year):
    assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
        )
    prix_contrats = pd.DataFrame.read_csv(os.path.join(assets_directory,
        'openfisca_france_indirect_taxation', 'assets', 'prix',
        'prix_unitaire_gaz_electricite_par_menage_{}.csv'.format(year)))
    prix_contrats['identifiant_menage'] = prix_contrats['identifiant_menage'].astype(str)
    moyenne_prix_gaz = \
        prix_contrats.query('depenses_gaz_prix_unitaire > 0').depenses_gaz_prix_unitaire.mean()
    moyenne_prix_electricite = \
        prix_contrats.query('depenses_electricite_prix_unitaire > 0').depenses_electricite_prix_unitaire.mean()
    prix_contrats.loc[prix_contrats['depenses_gaz_prix_unitaire'] == 0, 'depenses_gaz_prix_unitaire'] = moyenne_prix_gaz
    prix_contrats.loc[prix_contrats['depenses_electricite_prix_unitaire'] == 0, 'depenses_electricite_prix_unitaire'] = \
        moyenne_prix_electricite
    dataframe = pd.merge(dataframe, prix_contrats, on = 'identifiant_menage')
    dataframe.loc[dataframe['bien'] == 'poste_04_5_2_1_1', 'prix'] = (
        dataframe['prix'] * dataframe['depenses_gaz_prix_unitaire'] / moyenne_prix_gaz
        )
    dataframe.loc[dataframe['bien'] == 'poste_04_5_1_1_1_b', 'prix'] = (
        dataframe['prix'] * dataframe['depenses_electricite_prix_unitaire'] / moyenne_prix_electricite
        )

    return dataframe
