# -*- coding: utf-8 -*-
"""
Created on Wed Nov 04 14:03:03 2015

@author: thomas.douenne
"""

from __future__ import division

import pandas as pd
import numpy as np
from pandas import concat

from openfisca_france_indirect_taxation.example.utils_example import get_input_data_frame
from openfisca_france_indirect_taxation.almost_ideal_demand_system.aids_price_index_builder import \
    df_indice_prix_produit


# Now that we have our price indexes, we construct a dataframe with the rest of the information

data_frame_for_reg = None
for year in [2000]:
    aggregates_data_frame = get_input_data_frame(year)
    aggregates_data_frame['depenses_tot'] = 0
    for i in range(1, 13):
        aggregates_data_frame['depenses_tot'] += aggregates_data_frame['coicop12_{}'.format(i)]
        aggregates_data_frame['depenses_non_energie'] = (
            aggregates_data_frame['depenses_tot'] - aggregates_data_frame['poste_coicop_722'])

    produits = [column for column in aggregates_data_frame.columns if column[:13] == 'poste_coicop_']

    data = aggregates_data_frame[produits + ['vag'] + ['depenses_non_energie']].copy()

    # data recense les dépenses de chaque ménage dans chacun des biens reportés dans les enquêtes. Pour estimer QAIDS,
    # on se concentre sur les biens non-durables. On élimine donc les biens durables de cette dataframe.

    # On renverse la dataframe pour obtenir une ligne pour chaque article consommé par chaque personne
    data.index.name = 'ident_men'
    data.reset_index(inplace = True)
    df = pd.melt(data, id_vars = ['vag', 'ident_men'], value_vars=produits,
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

    # df2 contient les dépenses de consommation et les prix associés à ces dépenses.
    # Il faut maintenant construire les catégories de biens que l'on souhaite comparer.
    df_depenses_prix['energie'] = 0
    df_depenses_prix.loc[df_depenses_prix['bien'] == 'poste_coicop_722', 'energie'] = 1

    # Construire les indices de prix pondérés pour les deux catégories
    df_depenses_prix[['energie'] + ['ident_men']] = df_depenses_prix[['energie'] + ['ident_men']].astype(str)
    df_depenses_prix['id'] = df_depenses_prix['energie'] + '_' + df_depenses_prix['ident_men']

    data['ident_men'] = data['ident_men'].astype(str)
    df_depenses_prix = pd.merge(df_depenses_prix, data[['depenses_non_energie'] + ['ident_men']], on = 'ident_men')
    df_depenses_prix[['depense_bien'] + ['depenses_non_energie'] + ['prix']] = \
        df_depenses_prix[['depense_bien'] + ['depenses_non_energie'] + ['prix']].astype(float)
    df_depenses_prix['part_bien_categorie'] = (
        df_depenses_prix['depense_bien'] / df_depenses_prix['depenses_non_energie'])
    df_depenses_prix.fillna(0, inplace=True)
    df_depenses_prix['indice_prix_pondere'] = 0
    df_depenses_prix['indice_prix_pondere'] = df_depenses_prix['part_bien_categorie'] * df_depenses_prix['prix']
    df_depenses_prix.loc[df_depenses_prix['energie'] == '1', 'indice_prix_pondere'] = df_depenses_prix['prix']

    # grouped donne l'indice de prix pondéré pour chacune des deux catégories pour chaque individu
    # On met cette dataframe en forme pour avoir pour chaque individu l'indice de prix pour chaque catégorie
    # Cela donne df_prix_to_merge
    df_depenses_prix.sort(['id'])
    grouped = df_depenses_prix['indice_prix_pondere'].groupby(df_depenses_prix['id'])
    grouped = grouped.aggregate(np.sum)
    grouped.index.name = 'id'
    grouped = grouped.reset_index()

    grouped['prix_energie'] = 0
    grouped['prix_non_energie'] = 0
    grouped['categorie'] = grouped['id'].str[:1]
    grouped.loc[grouped['categorie'] == '1', 'prix_energie'] = grouped['indice_prix_pondere']
    grouped.loc[grouped['categorie'] == '0', 'prix_non_energie'] = grouped['indice_prix_pondere']

    grouped_energie = grouped[grouped['categorie'] == '1']
    grouped_energie['ident_men'] = grouped_energie['id'].str[2:]
    grouped_non_energie = grouped[grouped['categorie'] == '0']
    grouped_non_energie['ident_men'] = grouped_non_energie['id'].str[2:]
    df_prix_to_merge = pd.merge(grouped_energie[['ident_men'] + ['prix_energie']], grouped_non_energie[['ident_men'] +
        ['prix_non_energie']], on = 'ident_men')

    # On récupère les informations importantes sur les ménages
    df_info_menage = aggregates_data_frame[['ocde10'] + ['depenses_tot'] + ['depenses_non_energie'] + ['vag'] +
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
    df_info_menage['part_non_energie'] = df_info_menage['depenses_non_energie'] / df_info_menage['depenses_tot']
    df_info_menage['part_energie'] = 1 - df_info_menage['part_non_energie']

    # On merge les informations sur les caractéristiques du ménage et leurs consommations avec les indices de prix
    # pondérés pour les deux catégories
    dataframe = pd.merge(df_info_menage, df_prix_to_merge, on = 'ident_men')
    dataframe['depenses_par_uc'] = dataframe['depenses_tot'] / dataframe['ocde10']
    dataframe = dataframe[['ident_men'] + ['part_non_energie'] + ['part_energie'] + ['prix_non_energie'] +
        ['prix_energie'] + ['depenses_par_uc'] + ['typmen'] + ['fumeur']]

data_frame_for_reg = dataframe.rename(columns = {'part_non_energie': 'w1', 'part_energie':'w2',
    'prix_non_energie': 'p1', 'prix_energie': 'p2'})
data_frame_for_reg.to_csv('data_frame_energy.csv', sep = ',')

# Must add another categorie -> at least 3 expenditure shares to compute AIDS on Stata.
# -> it could be other energetic goods, or other kind of transports
# Must get rid of durable goods
# Must look at the sample, if I keep all of it or if I delete outliers
