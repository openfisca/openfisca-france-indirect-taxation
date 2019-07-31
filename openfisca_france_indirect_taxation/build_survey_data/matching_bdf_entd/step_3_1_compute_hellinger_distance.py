# -*- coding: utf-8 -*-

"""
Computing the Hellinger distance between two discrete
probability distributions
"""

# To be completed : add missing variables

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    hellinger

data = create_niveau_vie_quantiles()
data_entd = data[0]
data_bdf = data[1]


def hellinger_agepr(data_bdf, data_entd):
    data_bdf['agepr'] = data_bdf['agepr'].astype(float)
    data_entd['agepr'] = data_entd['agepr'].astype(float)
    age_max = int(max(data_bdf['agepr'].max(), data_entd['agepr'].max()))

    distribution_bdf = dict()
    for i in range(0, age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, age_max):
        distribution_entd['{}'.format(i)] = (data_entd.query('agepr == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_agepr = hellinger_agepr(data_bdf, data_entd)


def hellinger_age_carte_grise(data_bdf, data_entd):
    data_bdf['age_carte_grise'] = data_bdf['age_carte_grise'].astype(float)
    data_entd['age_carte_grise'] = data_entd['age_carte_grise'].astype(float)
    age_max = int(max(data_bdf['age_carte_grise'].max(), data_entd['age_carte_grise'].max()))

    distribution_bdf = dict()
    for i in range(0, age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('age_carte_grise == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, age_max):
        distribution_entd['{}'.format(i)] = (data_entd.query('age_carte_grise == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_age_carte_grise = hellinger_age_carte_grise(data_bdf, data_entd)


def hellinger_age_vehicule(data_bdf, data_entd):
    data_bdf['age_vehicule'] = data_bdf['age_vehicule'].astype(float)
    data_entd['age_vehicule'] = data_entd['age_vehicule'].astype(float)
    age_max = int(max(data_bdf['age_vehicule'].max(), data_entd['age_vehicule'].max()))

    distribution_bdf = dict()
    for i in range(0, age_max):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('age_vehicule == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, age_max):
        distribution_entd['{}'.format(i)] = (data_entd.query('age_vehicule == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_age_vehicule = hellinger_age_vehicule(data_bdf, data_entd)


def hellinger_aides_logement(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [0, 1]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('aides_logement == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [0, 1]:
        distribution_entd['{}'.format(i)] = (data_entd.query('aides_logement == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_aides_logement = hellinger_aides_logement(data_bdf, data_entd)


def hellinger_cataeu(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('cataeu == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        distribution_entd['{}'.format(i)] = (data_entd.query('cataeu == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_cataeu = hellinger_cataeu(data_bdf, data_entd)


def hellinger_cs42pr(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(11, 87):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('cs42pr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(11, 87):
        distribution_entd['{}'.format(i)] = (data_entd.query('cs42pr == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_cs42pr = hellinger_cs42pr(data_bdf, data_entd)


# By construction, the distance should be extremely close to 0
def hellinger_deciles(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 11):
        distribution_entd['{}'.format(i)] = (data_entd.query('niveau_vie_decile == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_deciles = hellinger_deciles(data_bdf, data_entd)


def hellinger_dip14pr(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('dip14pr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        distribution_entd['{}'.format(i)] = (data_entd.query('dip14pr == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_dip14pr = hellinger_dip14pr(data_bdf, data_entd)


def hellinger_mloy_d(data_bdf, data_entd):  # comprendre ce qui ne va pas ici
    data_bdf['mloy_d'] = data_bdf['mloy_d'].astype(float)
    data_bdf['mloy_d_racine'] = (data_bdf['mloy_d']) ** (0.5)
    mloy_d_racine_max_bdf = data_bdf['mloy_d_racine'].max()

    data_entd['mloy_d'] = data_entd['mloy_d'].astype(float)
    data_entd['mloy_d_racine'] = (data_entd['mloy_d']) ** (0.5)
    mloy_d_racine_max_entd = data_entd['mloy_d_racine'].max()

    mloy_d_racine_max = max(mloy_d_racine_max_bdf, mloy_d_racine_max_entd)
    data_bdf['mloy_d_groupe'] = (data_bdf['mloy_d_racine'] / mloy_d_racine_max).round(decimals = 2)
    data_entd['mloy_d_groupe'] = (data_entd['mloy_d_racine'] / mloy_d_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('mloy_d_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_entd['{}'.format(j)] = (data_entd.query('mloy_d_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_mloy_d = hellinger_mloy_d(data_bdf, data_entd)


def hellinger_nactifs(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 7):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nactifs == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 7):
        distribution_entd['{}'.format(i)] = (data_entd.query('nactifs == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_nactifs = hellinger_nactifs(data_bdf, data_entd)


def hellinger_nb_diesel(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 9):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nb_diesel == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 9):
        distribution_entd['{}'.format(i)] = (data_entd.query('nb_diesel == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_nb_diesel = hellinger_nb_diesel(data_bdf, data_entd)


def hellinger_nb_essence(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nb_essence == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 11):
        distribution_entd['{}'.format(i)] = (data_entd.query('nb_essence == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_nb_essence = hellinger_nb_essence(data_bdf, data_entd)


def hellinger_nbphab(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 11):
        distribution_entd['{}'.format(i)] = (data_entd.query('nbphab == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_nbphab = hellinger_nbphab(data_bdf, data_entd)


def hellinger_nenfants(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 12):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('nenfants == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 12):
        distribution_entd['{}'.format(i)] = (data_entd.query('nenfants == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_nenfants = hellinger_nenfants(data_bdf, data_entd)


def hellinger_niveau_vie(data_bdf, data_entd):
    data_bdf['niveau_vie'] = data_bdf['niveau_vie'].astype(float)
    data_bdf['niveau_vie_racine'] = (data_bdf['niveau_vie']) ** (0.5)
    niveau_vie_racine_max_bdf = data_bdf['niveau_vie_racine'].max()

    data_entd['niveau_vie'] = data_entd['niveau_vie'].astype(float)
    data_entd['niveau_vie_racine'] = (data_entd['niveau_vie']) ** (0.5)
    niveau_vie_racine_max_entd = data_entd['niveau_vie_racine'].max()

    niveau_vie_racine_max = max(niveau_vie_racine_max_bdf, niveau_vie_racine_max_entd)
    data_bdf['niveau_vie_groupe'] = (data_bdf['niveau_vie_racine'] / niveau_vie_racine_max).round(decimals = 2)
    data_entd['niveau_vie_groupe'] = (data_entd['niveau_vie_racine'] / niveau_vie_racine_max).round(decimals = 2)

    distribution_bdf = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_bdf['{}'.format(j)] = (data_bdf.query('niveau_vie_groupe == {}'.format(j))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 101):
        j = float(i) / 100
        distribution_entd['{}'.format(j)] = (data_entd.query('niveau_vie_groupe == {}'.format(j))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_niveau_vie = hellinger_niveau_vie(data_bdf, data_entd)


def hellinger_npers(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 14):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('npers == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 14):
        distribution_entd['{}'.format(i)] = (data_entd.query('npers == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_npers = hellinger_npers(data_bdf, data_entd)


def hellinger_ocde10(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        distribution_entd['{}'.format(i)] = (data_entd.query('ocde10 == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_ocde10 = hellinger_ocde10(data_bdf, data_entd)


# By construction, the distance should be extremely close to 0
def hellinger_quintiles(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 10):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 10):
        distribution_entd['{}'.format(i)] = (data_entd.query('niveau_vie_quintile == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_quintiles = hellinger_quintiles(data_bdf, data_entd)


def hellinger_situapr(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 8):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('situapr == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 8):
        distribution_entd['{}'.format(i)] = (data_entd.query('situapr == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_situapr = hellinger_situapr(data_bdf, data_entd)


def hellinger_stalog(data_bdf, data_entd):  # This variable must be redefined
    distribution_bdf = dict()
    for i in range(1, 6):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('stalog == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 6):
        distribution_entd['{}'.format(i)] = (data_entd.query('stalog == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_stalog = hellinger_stalog(data_bdf, data_entd)


def hellinger_tau(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 11):
        distribution_entd['{}'.format(i)] = (data_entd.query('tau == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_tau = hellinger_tau(data_bdf, data_entd)


# Test if two opposite distributions have hellinger distance = 1
def hellinger_test(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 51):
        distribution_bdf['{}'.format(i)] = 0.02
    for i in range(51, 101):
        distribution_bdf['{}'.format(i)] = 0

    distribution_entd = dict()
    for i in range(1, 51):
        distribution_entd['{}'.format(i)] = 0
    for i in range(51, 101):
        distribution_entd['{}'.format(i)] = 0.02

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_test = hellinger_test(data_bdf, data_entd)


def hellinger_tuu(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 9):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 9):
        distribution_entd['{}'.format(i)] = (data_entd.query('tuu == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_tuu = hellinger_tuu(data_bdf, data_entd)


def hellinger_typmen(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(1, 6):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('typmen == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(1, 6):
        distribution_entd['{}'.format(i)] = (data_entd.query('typmen == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_typmen = hellinger_typmen(data_bdf, data_entd)


def hellinger_veh_tot(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in range(0, 11):
        distribution_bdf['{}'.format(i)] = (data_bdf.query('veh_tot == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in range(0, 11):
        distribution_entd['{}'.format(i)] = (data_entd.query('veh_tot == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_veh_tot = hellinger_veh_tot(data_bdf, data_entd)


def hellinger_vp_deplacements_pro(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [0, 1]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('vp_deplacements_pro == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [0, 1]:
        distribution_entd['{}'.format(i)] = (data_entd.query('vp_deplacements_pro == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_vp_deplacements_pro = hellinger_vp_deplacements_pro(data_bdf, data_entd)


def hellinger_vp_domicile_travail(data_bdf, data_entd):
    distribution_bdf = dict()
    for i in [0, 1]:
        distribution_bdf['{}'.format(i)] = (data_bdf.query('vp_domicile_travail == {}'.format(i))['pondmen'].sum() /
                 data_bdf['pondmen'].sum())

    distribution_entd = dict()
    for i in [0, 1]:
        distribution_entd['{}'.format(i)] = (data_entd.query('vp_domicile_travail == {}'.format(i))['pondmen'].sum() /
                 data_entd['pondmen'].sum())

    hellinger_distance = hellinger(list(distribution_bdf.values()), list(distribution_entd.values()))

    return hellinger_distance


hellinger_vp_domicile_travail = hellinger_vp_domicile_travail(data_bdf, data_entd)
