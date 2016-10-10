# -*- coding: utf-8 -*-

# Les variables qui ont des différences de définition doivent être reconstruites
# sur le modèle de l'enquête ENL (ou BdF) de manière à avoir des définitions identiques
# Les noms de variables doivent aussi être alignés.

import numpy as np

from openfisca_france_indirect_taxation.build_survey_data.homogeneisation_bdf_enl.step_1_build_dataframes import \
    menage_enl_keep, conso_bdf_keep


data_bdf = conso_bdf_keep.copy()
data_enl = menage_enl_keep.copy()
del conso_bdf_keep, menage_enl_keep

# Differences in definition

# Aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
check = data_bdf.query('aidlog1 != 0')
assert (check['aidlog2'] == 0).any()

data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
del check

# Montant des aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
for i in [1, 2]:
    data_bdf['mall{}'.format(i)] = data_bdf['mall{}'.format(i)].fillna(0)
    check = data_bdf.query('aidlog{} != 1'.format(i))
    assert (check['mall{}'.format(i)] == 0).any()

data_bdf['amr'] = data_bdf['mall1'] + data_bdf['mall2']
del data_bdf['aidlog1'], data_bdf['aidlog2'], data_bdf['mall1'], data_bdf['mall2'], check

# Les définitions du ménage dans BdF et ENL sont différentes : 
# on vérifie que la variable HTL est définie de la même manière
for i in [4, 6]:
    check = data_bdf.query('htl == {}'.format(i))
    assert len(check) == 0
    del check

# Changement nomenclature variable année de construction du batiment :
data_enl['ancons'] = 0
data_enl.ancons.loc[data_enl.iaat < 4] = 1
data_enl.ancons.loc[data_enl.iaat == 4] = 2
data_enl.ancons.loc[data_enl.iaat == 5] = 3
data_enl.ancons.loc[data_enl.iaat == 6] = 4
data_enl.ancons.loc[data_enl.iaat == 7] = 5
data_enl.ancons.loc[data_enl.iaat == 8] = 6
data_enl.ancons.loc[data_enl.iaat == 9] = 7
# Pour après 1998 on affecte aléatoirement 8 ou 9 (99-03 ou 03-et après)
data_enl.ancons.loc[data_enl.iaat == 10] = np.random.choice(np.array([8, 9]))

# Voir problème diplôme


# Situapr et Situacj vs Msitua


# Typmen vs Mtyad


# OCDE10 vs MUC1


# Rename
data_enl.rename(
    columns = {
        'cataeu2010': 'cataeu',
        'cceml': 'mfac_eau1_d',
        'coml11': 'poste_coicop_451',
        'coml12': 'poste_coicop_452',
        'coml2': 'poste_coicop_453',
        'enfhod': 'nbh1',
        'fchauf': 'mchof_d',
        'hnph1': 'nbphab',
        'hsh1': 'surfhab_d',
        'lmlm': 'mloy_d',
        'mag': 'agepr',
        'mcs': 'cs42pr',
        'mcsc': 'cs42cj',
        'mne1': 'nenfants',
        'mpa': 'nactifs',
        'mrtota2': 'revtot',
        'qex': 'pondmen',
        'tau2010': 'tau',
        'tu2010': 'tuu',
               },

    inplace = True,
    )
