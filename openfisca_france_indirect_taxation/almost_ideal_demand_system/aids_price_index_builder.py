# -*- coding: utf-8 -*-


import datetime as dt
import os
import pandas as pd
import pkg_resources


from openfisca_france_indirect_taxation.utils import get_input_data_frame


def date_to_vag(date):
    args = date.split('_') + ['1']
    args = [int(arg) for arg in args]
    datetime = dt.datetime(*args)

    for vague in vagues:
        if vague['start'] <= datetime <= vague['end']:
            return vague['number']

    return None


default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
indice_prix_mensuel_98_2015 = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'prix',
        'indice_prix_mensuel_98_2015.csv'
        ), sep =';', decimal = ','
    )

indice_prix_mensuel_98_2015 = indice_prix_mensuel_98_2015.astype(str)

# On veut que les biens prennent les mêmes noms que ceux du modèle, i.e. poste_x_y_z
# On doit donc changer le nom de tous les biens renseignés dans cette base de donnée
# On sépare les biens des coicop 1 à 9 des autres de manière à enlever les 0 à la fin des noms sans faire d'erreurs

coicop_un_neuf = indice_prix_mensuel_98_2015.ix[:, :'_9600']

produits_rename = [column for column in coicop_un_neuf.columns if len(column) == 5 and column[4:] == '0']
change_name = coicop_un_neuf[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:4]}, inplace = True)

autres_produits_list = [column for column in coicop_un_neuf.columns if len(column) != 5 or column[4:] != '0']
autres_produits = coicop_un_neuf[autres_produits_list]

coicop_un_neuf_new = pd.concat([change_name, autres_produits], axis = 1)

for col in coicop_un_neuf_new.columns.tolist():
    if col[:1] == '_':
        if len(col) == 4:
            coicop_un_neuf_new.rename(columns={col: 'poste_0{0}_{1}_{2}'.format(col[1], col[2], col[3])}, inplace = True)
        else:
            coicop_un_neuf_new.rename(columns={col: 'poste_0{0}_{1}_{2}_{3}'.format(col[1], col[2], col[3], col[4])}, inplace = True)

coicop_dix_douze = indice_prix_mensuel_98_2015.ix[:, '_10000':]
produits_rename = [column for column in coicop_dix_douze.columns if len(column) == 6 and column[5:] == '0']
change_name = coicop_dix_douze[produits_rename]
for element in change_name.columns:
    change_name.rename(columns={element: element[:5]}, inplace = True)

autres_produits_list = [column for column in coicop_dix_douze.columns if len(column) != 6 or column[5:] != '0']
autres_produits = coicop_dix_douze[autres_produits_list]

coicop_dix_douze_new = pd.concat([change_name, autres_produits], axis = 1)

for col in coicop_dix_douze_new.columns.tolist():
    if col[:1] == '_':
        if len(col) == 5:
            coicop_dix_douze_new.rename(columns={col: 'poste_{0}_{1}_{2}'.format(col[1:3], col[3], col[4])}, inplace = True)
        else:
            coicop_dix_douze_new.rename(columns={col: 'poste_{0}_{1}_{2}_{3}'.format(col[1:3], col[3], col[4], col[5])}, inplace = True)

indice_prix_mensuel_98_2015 = pd.concat([coicop_un_neuf_new, coicop_dix_douze_new], axis = 1)

colonnes_prix = indice_prix_mensuel_98_2015.columns.tolist()


unpriced = []
for year in [2000, 2005, 2011]:
    bdf = get_input_data_frame(year)
    postes_bdf = [column for column in bdf.columns if column[:6] == 'poste_' and int(column[6:8]) < 13]
    for poste_bdf in postes_bdf:
        if (poste_bdf[:12] in colonnes_prix) is True:
            indice_prix_mensuel_98_2015[poste_bdf] = indice_prix_mensuel_98_2015[poste_bdf[:12]]
        elif (poste_bdf[:14] in colonnes_prix) is True:
            indice_prix_mensuel_98_2015[poste_bdf] = indice_prix_mensuel_98_2015[poste_bdf[:14]]
        else:
            if poste_bdf not in unpriced:
                unpriced.append(poste_bdf)

# Pour les variables de BdF n'ayant pas de prix correspondant, en imputer un manuellement
c = 'poste_'
indice_prix_mensuel_98_2015[c + '01_10_1'] = indice_prix_mensuel_98_2015[c + '01_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '01_10_2'] = indice_prix_mensuel_98_2015[c + '01_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '02_2_2'] = indice_prix_mensuel_98_2015[c + '02_2_0']  # tabacs autres
indice_prix_mensuel_98_2015[c + '02_2_3'] = indice_prix_mensuel_98_2015[c + '02_2_0']  # tabacs autres
indice_prix_mensuel_98_2015[c + '02_3'] = indice_prix_mensuel_98_2015[c + '02_2_0']  # stupéfiants
indice_prix_mensuel_98_2015[c + '02_4'] = indice_prix_mensuel_98_2015[c + '02_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '03_3_1'] = indice_prix_mensuel_98_2015[c + '03_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '03_3_2'] = indice_prix_mensuel_98_2015[c + '03_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '03_4_1_1'] = indice_prix_mensuel_98_2015[c + '03_0_0']
indice_prix_mensuel_98_2015[c + '04_2_1'] = indice_prix_mensuel_98_2015[c + '04_1_1']  # loyer imputé
indice_prix_mensuel_98_2015[c + '04_6'] = indice_prix_mensuel_98_2015[c + '04_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '05_1_4_1'] = indice_prix_mensuel_98_2015[c + '05_0_0']
indice_prix_mensuel_98_2015[c + '05_2_1_1_3'] = indice_prix_mensuel_98_2015[c + '05_2_0']  # articles literie
indice_prix_mensuel_98_2015[c + '05_2_1_2_1'] = indice_prix_mensuel_98_2015[c + '05_2_0']  # articles literie
indice_prix_mensuel_98_2015[c + '05_5_2_3'] = indice_prix_mensuel_98_2015[c + '05_2_0']  # articles literie
indice_prix_mensuel_98_2015[c + '05_7_1'] = indice_prix_mensuel_98_2015[c + '05_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '05_7_2'] = indice_prix_mensuel_98_2015[c + '05_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '06_3'] = indice_prix_mensuel_98_2015[c + '06_0_0']  # services hospitaliers
indice_prix_mensuel_98_2015[c + '06_4_1'] = indice_prix_mensuel_98_2015[c + '06_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '06_4_2'] = indice_prix_mensuel_98_2015[c + '06_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '07_1_3'] = indice_prix_mensuel_98_2015[c + '07_1_1']  # achats autres véhicules
indice_prix_mensuel_98_2015[c + '07_3_0_0'] = indice_prix_mensuel_98_2015[c + '07_3_1']
indice_prix_mensuel_98_2015[c + '07_4_1'] = indice_prix_mensuel_98_2015[c + '07_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '07_4_2'] = indice_prix_mensuel_98_2015[c + '07_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '08_1_1_1_1'] = indice_prix_mensuel_98_2015[c + '08_1_0']  # services postaux
indice_prix_mensuel_98_2015[c + '08_2'] = indice_prix_mensuel_98_2015[c + '08_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '09_2_2_2'] = indice_prix_mensuel_98_2015[c + '09_2_1']  # gros équipements loisirs
indice_prix_mensuel_98_2015[c + '09_2_3_1'] = indice_prix_mensuel_98_2015[c + '09_2_1']  # réparation équipements loisirs
indice_prix_mensuel_98_2015[c + '09_4_3'] = indice_prix_mensuel_98_2015[c + '09_4_2']  # jeux de hasard
indice_prix_mensuel_98_2015[c + '09_6_1_1_1'] = indice_prix_mensuel_98_2015[c + '09_6_0']  # voyages à forfait
indice_prix_mensuel_98_2015[c + '09_7_1'] = indice_prix_mensuel_98_2015[c + '09_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '09_7_2'] = indice_prix_mensuel_98_2015[c + '09_0_0']  # cadeaux
indice_prix_mensuel_98_2015[c + '10_1'] = indice_prix_mensuel_98_2015[c + '10_1_0']
indice_prix_mensuel_98_2015[c + '10_2'] = indice_prix_mensuel_98_2015[c + '10_0_0']
indice_prix_mensuel_98_2015[c + '10_3'] = indice_prix_mensuel_98_2015[c + '10_0_0']
indice_prix_mensuel_98_2015[c + '10_4'] = indice_prix_mensuel_98_2015[c + '10_0_0']
indice_prix_mensuel_98_2015[c + '10_5_1'] = indice_prix_mensuel_98_2015[c + '10_0_0']
indice_prix_mensuel_98_2015[c + '10_5_2'] = indice_prix_mensuel_98_2015[c + '10_0_0']
indice_prix_mensuel_98_2015[c + '11_1_1_1_1'] = indice_prix_mensuel_98_2015[c + '11_0_0']
indice_prix_mensuel_98_2015[c + '11_1_1_1_2'] = indice_prix_mensuel_98_2015[c + '11_0_0']
indice_prix_mensuel_98_2015[c + '11_1_3_1'] = indice_prix_mensuel_98_2015[c + '11_0_0']
indice_prix_mensuel_98_2015[c + '11_1_3_2'] = indice_prix_mensuel_98_2015[c + '11_0_0']
indice_prix_mensuel_98_2015[c + '11_2_1_1_1'] = indice_prix_mensuel_98_2015[c + '11_2_0']
indice_prix_mensuel_98_2015[c + '12_2_1_1'] = indice_prix_mensuel_98_2015[c + '12_3_1']
indice_prix_mensuel_98_2015[c + '12_2_2_1'] = indice_prix_mensuel_98_2015[c + '12_0_0']
indice_prix_mensuel_98_2015[c + '12_2_2_2'] = indice_prix_mensuel_98_2015[c + '12_0_0']
indice_prix_mensuel_98_2015[c + '12_3_3_1_1'] = indice_prix_mensuel_98_2015[c + '12_0_0']
indice_prix_mensuel_98_2015[c + '12_4_2_1'] = indice_prix_mensuel_98_2015[c + '12_4_0']
indice_prix_mensuel_98_2015[c + '12_4_3_1'] = indice_prix_mensuel_98_2015[c + '12_4_0']
indice_prix_mensuel_98_2015[c + '12_4_4_1'] = indice_prix_mensuel_98_2015[c + '12_4_0']
indice_prix_mensuel_98_2015[c + '12_4_5_1'] = indice_prix_mensuel_98_2015[c + '12_4_0']
indice_prix_mensuel_98_2015[c + '12_5_1_1_1'] = indice_prix_mensuel_98_2015[c + '12_5_0']
indice_prix_mensuel_98_2015[c + '12_5_5_1_1'] = indice_prix_mensuel_98_2015[c + '12_5_0']
indice_prix_mensuel_98_2015[c + '12_7_1_1_1'] = indice_prix_mensuel_98_2015[c + '12_7_0']
indice_prix_mensuel_98_2015[c + '12_7_1_2_1'] = indice_prix_mensuel_98_2015[c + '12_7_0']
indice_prix_mensuel_98_2015[c + '12_8_1'] = indice_prix_mensuel_98_2015[c + '12_0_0']
indice_prix_mensuel_98_2015[c + '12_9_1_1'] = indice_prix_mensuel_98_2015[c + '12_0_0']

indice_prix_mensuel_98_2015['date'] = indice_prix_mensuel_98_2015['Annee'] + '_' + indice_prix_mensuel_98_2015['Mois']
indice_prix_mensuel_98_2015[['Annee', 'Mois']] = indice_prix_mensuel_98_2015[['Annee', 'Mois']].astype(float)
indice_prix_mensuel_98_2015['temps'] = \
    ((indice_prix_mensuel_98_2015['Annee'] - 1998) * 12) + indice_prix_mensuel_98_2015['Mois']
del indice_prix_mensuel_98_2015['Annee']
indice_prix_mensuel_98_2015['mois'] = indice_prix_mensuel_98_2015['Mois'].copy()
del indice_prix_mensuel_98_2015['Mois']

produits = list(column for column in indice_prix_mensuel_98_2015.columns if column[:6] == 'poste_')

df_indice_prix_produit = pd.melt(indice_prix_mensuel_98_2015, id_vars = ['date', 'temps', 'mois'], value_vars=produits,
    value_name = 'prix', var_name = 'bien')
# df_indice_prix_produit.bien = df_indice_prix_produit.bien.str.split('_').str[1]

vagues = [
    dict(
        number = 9,
        start = dt.datetime(2000, 5, 9),
        end = dt.datetime(2000, 6, 18),
        ),
    dict(
        number = 10,
        start = dt.datetime(2000, 6, 19),
        end = dt.datetime(2000, 7, 30),
        ),
    dict(
        number = 11,
        start = dt.datetime(2000, 8, 14),
        end = dt.datetime(2000, 9, 24),
        ),
    dict(
        number = 12,
        start = dt.datetime(2000, 9, 25),
        end = dt.datetime(2000, 11, 5),
        ),
    dict(
        number = 13,
        start = dt.datetime(2000, 11, 6),
        end = dt.datetime(2000, 12, 17),
        ),
    dict(
        number = 14,
        start = dt.datetime(2001, 1, 2),
        end = dt.datetime(2001, 2, 11),
        ),
    dict(
        number = 15,
        start = dt.datetime(2001, 2, 12),
        end = dt.datetime(2001, 3, 25),
        ),
    dict(
        number = 16,
        start = dt.datetime(2001, 3, 26),
        end = dt.datetime(2001, 5, 6),
        ),
    dict(
        number = 17,
        start = dt.datetime(2005, 3, 1),
        end = dt.datetime(2005, 4, 24),
        ),
    dict(
        number = 18,
        start = dt.datetime(2005, 4, 25),
        end = dt.datetime(2005, 6, 19),
        ),
    dict(
        number = 19,
        start = dt.datetime(2005, 6, 20),
        end = dt.datetime(2005, 8, 28),
        ),
    dict(
        number = 20,
        start = dt.datetime(2005, 8, 29),
        end = dt.datetime(2005, 10, 23),
        ),
    dict(
        number = 21,
        start = dt.datetime(2005, 10, 24),
        end = dt.datetime(2005, 12, 18),
        ),
    dict(
        number = 22,
        start = dt.datetime(2006, 1, 2),
        end = dt.datetime(2006, 2, 27),
        ),
    dict(
        number = 23,
        start = dt.datetime(2010, 10, 4),
        end = dt.datetime(2010, 11, 27),
        ),
    dict(
        number = 24,
        start = dt.datetime(2010, 11, 29),
        end = dt.datetime(2011, 1, 29),
        ),
    dict(
        number = 25,
        start = dt.datetime(2011, 1, 31),
        end = dt.datetime(2011, 3, 26),
        ),
    dict(
        number = 26,
        start = dt.datetime(2011, 3, 28),
        end = dt.datetime(2011, 5, 21),
        ),
    dict(
        number = 27,
        start = dt.datetime(2011, 5, 23),
        end = dt.datetime(2011, 7, 23),
        ),
    dict(
        number = 28,
        start = dt.datetime(2011, 8, 1),
        end = dt.datetime(2011, 10, 1),
        ),
    ]

df_indice_prix_produit['vag'] = df_indice_prix_produit['date'].map(date_to_vag)
df_indice_prix_produit = df_indice_prix_produit.dropna()
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(int)  # delete the .0 after each number
df_indice_prix_produit['vag'] = df_indice_prix_produit['vag'].astype(str)
df_indice_prix_produit['indice_prix_produit'] = df_indice_prix_produit['bien'] + '_' + df_indice_prix_produit['vag']
df_indice_prix_produit = df_indice_prix_produit.drop_duplicates(
    subset = ['indice_prix_produit'], keep = 'last')

df_indice_prix_produit.to_csv(os.path.join(default_config_files_directory,
    'openfisca_france_indirect_taxation', 'assets',
    'prix', 'df_indice_prix_produit.csv'), sep = ';')
