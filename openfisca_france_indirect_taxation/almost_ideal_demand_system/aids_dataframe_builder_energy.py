# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 14:03:03 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
import numpy as np

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import \
    df_indice_prix_produit


# On importe la dataframe qui recense les indices de prix. Notre objectif est de construire une nouvelle dataframe avec
# le reste des informations, i.e. la consommation et autres variables pertinentes concernant les ménages.

# On commence par cinstruire une dataframe appelée data_conso rassemblant les informations sur les dépenses des ménages.
data_frame_for_reg = None
for year in [2000, 2005, 2011]:
    aggregates_data_frame = get_input_data_frame(year)
    aggregates_data_frame['somme_coicop'] = 0
    for i in range(1, 13):
        aggregates_data_frame['somme_coicop'] += aggregates_data_frame['coicop12_{}'.format(i)]

    # Pour estimer QAIDS, on se concentre sur les biens non-durables.
    # On élimine donc les biens durables de cette dataframe: 442 : redevance d'enlèvement des ordures, 711, 712, 713 :
    # achat de véhicules, 911, 912, 9122, 913, 9151 : technologies high-tech, 9211, 921, 923: gros équipements loisirs,
    # 941, 960 : voyages séjours et cadeaux, 10i0 : enseignement, 12.. : articles de soin et bijoux

    biens_durables = ['poste_coicop_442', 'poste_coicop_711', 'poste_coicop_712', 'poste_coicop_713',
        'poste_coicop_911', 'poste_coicop_912', 'poste_coicop_9122', 'poste_coicop_913', 'poste_coicop_9151',
        'poste_coicop_9211', 'poste_coicop_921', 'poste_coicop_922', 'poste_coicop_923', 'poste_coicop_960',
        'poste_coicop_941', 'poste_coicop_1010', 'poste_coicop_1015', 'poste_coicop_10152', 'poste_coicop_1020',
        'poste_coicop_1040', 'poste_coicop_1050', 'poste_coicop_1212', 'poste_coicop_1231', 'poste_coicop_1240',
        'poste_coicop_12411', 'poste_coicop_1270']

    for bien in biens_durables:
        try:
            aggregates_data_frame = aggregates_data_frame.drop(bien, axis = 1)
        except:
            aggregates_data_frame = aggregates_data_frame

    produits_alimentaire = ['poste_coicop_111', 'poste_coicop_112', 'poste_coicop_113', 'poste_coicop_114',
                            'poste_coicop_115', 'poste_coicop_1151', 'poste_coicop_116', 'poste_coicop_117',
                            'poste_coicop_118', 'poste_coicop_1181', 'poste_coicop_119', 'poste_coicop_121',
                            'poste_coicop_122']

    produits = [column for column in aggregates_data_frame.columns if column[:13] == 'poste_coicop_']
    del column

    aggregates_data_frame['depenses_alime'] = 0
    for element in produits_alimentaire:
        aggregates_data_frame['depenses_alime'] += aggregates_data_frame[element]

    aggregates_data_frame['depenses_carbu'] = aggregates_data_frame['poste_coicop_722']

    aggregates_data_frame['depenses_tot'] = 0
    for element in produits:
        if element[13:15] != '99' and element[13:15] != '13':
            aggregates_data_frame['depenses_tot'] += aggregates_data_frame[element]

    aggregates_data_frame['depenses_autre'] = (
        aggregates_data_frame['depenses_tot'] - aggregates_data_frame['depenses_alime'] -
        aggregates_data_frame['depenses_carbu'])

    data_conso = aggregates_data_frame[produits + ['vag'] + ['depenses_carbu'] + ['depenses_alime'] +
        ['depenses_autre']].copy()

    # On renverse la dataframe pour obtenir une ligne pour chaque article consommé par chaque personne
    data_conso.index.name = 'ident_men'
    data_conso.reset_index(inplace = True)
    df = pd.melt(data_conso, id_vars = ['vag', 'ident_men'], value_vars=produits,
        value_name = 'depense_bien', var_name = 'bien')

    df_indice_prix_produit = df_indice_prix_produit[['indice_prix_produit'] + ['prix'] + ['temps'] + ['mois']]

    df['vag'] = df['vag'].astype(str)
    df['indice_prix_produit'] = df['bien'] + '_' + df['vag']
#    df = df[['ident_men'] + ['coicop_12_numero'] + ['indice_prix_produit'] + ['depense_bien'] + ['vag']]

    # On merge les prix des biens avec les dépenses déjà présentes dans df. Le merge se fait sur 'indice_prix_produit'
    # Indice prix produit correspond à poste_coicop_xyz_vag
    df_depenses_prix = pd.merge(df, df_indice_prix_produit, on = 'indice_prix_produit')

    # La taille de df est réduite après le merge, ce qui signifie que certains biens de consommation ne sont matchés
    # avec aucun prix. Common nous indique quels sont ces biens. On peut vérifier que se sont des biens qui commencent
    # par 99. Leur présence est inutile pour l'estimation du QAIDS.
    check = df['indice_prix_produit'].drop_duplicates('indice_prix_produit')
    check2 = df_depenses_prix['indice_prix_produit'].drop_duplicates('indice_prix_produit')
    common_check = [x for x in check]
    common_check2 = [x for x in check2]
    common = [x for x in common_check if x not in common_check2]
    del check, check2, common_check, common_check2
    for element in common:
        short_name = element[13:15]
        assert short_name == '99' or short_name == '13'
    del common, df, short_name, x

    # df2 contient les dépenses de consommation et les prix associés à ces dépenses.
    # Il faut maintenant construire les catégories de biens que l'on souhaite comparer.
    df_depenses_prix['type_bien'] = 'autre'
    df_depenses_prix.loc[df_depenses_prix['bien'] == 'poste_coicop_722', 'type_bien'] = 'carbu'
    for element in produits_alimentaire:
        df_depenses_prix.loc[df_depenses_prix['bien'] == element, 'type_bien'] = 'alime'
    del element

    # Construire les indices de prix pondérés pour les deux catégories
    df_depenses_prix[['type_bien'] + ['ident_men']] = df_depenses_prix[['type_bien'] + ['ident_men']].astype(str)
    df_depenses_prix['id'] = df_depenses_prix['type_bien'] + '_' + df_depenses_prix['ident_men']

    data_conso['ident_men'] = data_conso['ident_men'].astype(str)
    df_depenses_prix = pd.merge(
        df_depenses_prix, data_conso[['depenses_carbu'] + ['depenses_alime'] + ['depenses_autre'] +
        ['ident_men']], on = 'ident_men'
        )
    del data_conso
    df_depenses_prix[['depense_bien'] + ['depenses_alime'] + ['depenses_carbu'] +
        ['depenses_autre'] + ['prix']] = df_depenses_prix[['depense_bien'] + ['depenses_alime'] +
        ['depenses_carbu'] + ['depenses_autre'] + ['prix']].astype(float)

    df_depenses_prix['part_bien_categorie'] = 0
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'autre', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_autre']
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'alime', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_alime']
    df_depenses_prix.loc[df_depenses_prix['type_bien'] == 'carbu', 'part_bien_categorie'] = \
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_carbu']

    df_depenses_prix.fillna(0, inplace=True)

    # On peut réaliser quelques vérifications pour s'assurer que les parts que représentent chaque bien dans leur
    # catégorie donne 1 dans chacune de ces catégories lorsqu'on les somme.
    for i in range(0, 100):
        df_ident_men_0 = df_depenses_prix[df_depenses_prix['ident_men'] == '{}'.format(i)]
        df_ident_men_0_autre = df_ident_men_0[df_ident_men_0['type_bien'] == 'autre']
        assert 0.999 < df_ident_men_0_autre['part_bien_categorie'].sum() < 1.001 or \
            -0.001 < df_ident_men_0_autre['part_bien_categorie'].sum() < 0.001

        df_ident_men_0_alime = df_ident_men_0[df_ident_men_0['type_bien'] == 'alime']
        assert 0.999 < df_ident_men_0_alime['part_bien_categorie'].sum() < 1.001 or \
            -0.001 < df_ident_men_0_alime['part_bien_categorie'].sum() < 0.001

        df_ident_men_0_carbu = df_ident_men_0[df_ident_men_0['type_bien'] == 'carbu']
        assert 0.999 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 1.001 or \
            -0.001 < df_ident_men_0_carbu['part_bien_categorie'].sum() < 0.001

    del df_ident_men_0, df_ident_men_0_autre, df_ident_men_0_alime, df_ident_men_0_carbu, i

    # Les parts des biens dans leur catégorie permettent de construire des indices de prix pondérés (Cf. Lewbel)
    df_depenses_prix['indice_prix_pondere'] = 0
    df_depenses_prix['indice_prix_pondere'] = df_depenses_prix['part_bien_categorie'] * df_depenses_prix['prix']

    # grouped donne l'indice de prix pondéré pour chacune des deux catégories pour chaque individu
    # On met cette dataframe en forme pour avoir pour chaque individu l'indice de prix pour chaque catégorie
    # Cela donne df_prix_to_merge
    df_depenses_prix.sort(['id'])
    grouped = df_depenses_prix['indice_prix_pondere'].groupby(df_depenses_prix['id'])
    del df_depenses_prix
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    grouped['prix_carbu'] = 0
    grouped['prix_alime'] = 0
    grouped['prix_autre'] = 0
    grouped['categorie'] = grouped['id'].str[:5]
    grouped.loc[grouped['categorie'] == 'carbu', 'prix_carbu'] = grouped['indice_prix_pondere']
    grouped.loc[grouped['categorie'] == 'alime', 'prix_alime'] = grouped['indice_prix_pondere']
    grouped.loc[grouped['categorie'] == 'autre', 'prix_autre'] = grouped['indice_prix_pondere']

    grouped_carbu = grouped[grouped['categorie'] == 'carbu']
    grouped_carbu['ident_men'] = grouped_carbu['id'].str[6:]
    grouped_alime = grouped[grouped['categorie'] == 'alime']
    grouped_alime['ident_men'] = grouped_alime['id'].str[6:]
    grouped_autre = grouped[grouped['categorie'] == 'autre']
    grouped_autre['ident_men'] = grouped_autre['id'].str[6:]

    df_prix_to_merge = pd.merge(grouped_carbu[['ident_men'] + ['prix_carbu']], grouped_alime[['ident_men'] +
        ['prix_alime']], on = 'ident_men')
    df_prix_to_merge = pd.merge(df_prix_to_merge, grouped_autre[['ident_men'] + ['prix_autre']], on = 'ident_men')
    del grouped, grouped_alime, grouped_autre, grouped_carbu

    # Problème: ceux qui ne consomment pas de carbu ou d'alimentaire se voient affecter un indice de prix égal à 0.

    # On récupère les informations importantes sur les ménages
    df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['depenses_carbu'] +
        ['depenses_alime'] + ['depenses_autre'] + ['vag'] +
        ['typmen'] + ['revtot'] + ['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']]
    df_info_menage['fumeur'] = 0
    df_info_menage[['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']] = \
        df_info_menage[['poste_coicop_2201'] + ['poste_coicop_2202'] + ['poste_coicop_2203']].astype(float)
    df_info_menage['consommation_tabac'] = (
        df_info_menage['poste_coicop_2201'] + df_info_menage['poste_coicop_2202'] + df_info_menage['poste_coicop_2203']
        )
    df_info_menage['fumeur'] = 1 * (df_info_menage['consommation_tabac'] > 0)
    df_info_menage.drop(['consommation_tabac', 'poste_coicop_2201', 'poste_coicop_2202', 'poste_coicop_2203'],
        inplace = True, axis = 1)
    df_info_menage.index.name = 'ident_men'
    df_info_menage.reset_index(inplace = True)
    df_info_menage['ident_men'] = df_info_menage['ident_men'].astype(str)
    df_info_menage['part_carbu'] = df_info_menage['depenses_carbu'] / df_info_menage['depenses_tot']
    df_info_menage['part_alime'] = df_info_menage['depenses_alime'] / df_info_menage['depenses_tot']
    df_info_menage['part_autre'] = df_info_menage['depenses_autre'] / df_info_menage['depenses_tot']

    # On merge les informations sur les caractéristiques du ménage et leurs consommations avec les indices de prix
    # pondérés pour les deux catégories
    dataframe = pd.merge(df_info_menage, df_prix_to_merge, on = 'ident_men')
    del df_info_menage, df_prix_to_merge

    price_carbu = df_indice_prix_produit[df_indice_prix_produit['indice_prix_produit'].str[13:16] == '722']
    price_carbu['vag'] = price_carbu['indice_prix_produit'].str[17:].astype(int)
    price_carbu = price_carbu[['vag'] + ['prix']]
    price_carbu['prix'] = price_carbu['prix'].astype(float)
    dataframe = pd.merge(dataframe, price_carbu, on = 'vag')
    del price_carbu
    dataframe.loc[dataframe['prix_carbu'] == 0, 'prix_carbu'] = dataframe['prix']

    dataframe['depenses_par_uc'] = dataframe['depenses_tot'] / dataframe['ocde10']

    dataframe = dataframe[['ident_men'] + ['part_carbu'] + ['part_alime'] + ['part_autre'] + ['prix_carbu'] +
        ['prix_alime'] + ['prix_autre'] + ['depenses_par_uc'] + ['depenses_tot'] + ['typmen'] + ['fumeur']]

    # On supprime de la base de données les individus pour lesquels on ne dispose d'aucune consommation alimentaire.
    # Leur présence est susceptible de biaiser l'analyse puisque de toute évidence s'ils ne dépensent rien pour la
    # nourriture ce n'est pas qu'ils n'en consomment pas, mais qu'ils n'en ont pas acheté sur la période (réserves, etc)
    dataframe = dataframe[dataframe['prix_alime'] != 0]

    data_frame_for_reg = dataframe.rename(columns = {'part_carbu': 'w1', 'part_alime': 'w2', 'part_autre': 'w3',
        'prix_carbu': 'p1', 'prix_alime': 'p2', 'prix_autre': 'p3'})
    data_frame_for_reg.to_csv('data_frame_energy_{}.csv'.format(year), sep = ',')


# Must get rid of durable goods
# Must look at the sample, if I keep all of it or if I delete outliers
# Must find a way to compute confidence intervals for elasticities
