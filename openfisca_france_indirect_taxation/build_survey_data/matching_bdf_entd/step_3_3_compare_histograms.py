# -*- coding: utf-8 -*-


# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_2_homogenize_variables import \
    create_niveau_vie_quantiles
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes


data_entd, data_bdf = create_niveau_vie_quantiles()


def histogram_agepr():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['agepr'].quantile(i))
        list_values_entd.append(data_entd['agepr'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_agepr()


def histogram_age_vehicule():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['age_vehicule'].quantile(i))
        list_values_entd.append(data_entd['age_vehicule'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_age_vehicule()


def histogram_age_carte_grise():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['age_carte_grise'].quantile(i))
        list_values_entd.append(data_entd['age_carte_grise'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_age_carte_grise()


def histogram_aides_logement():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.aides_logement == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.aides_logement == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_aides_logement()


def histogram_cataeu():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cataeu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.cataeu == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_cataeu()


def histogram_cs42pr():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['cs42pr'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['cs42pr'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_cs42pr()


def histogram_dip14pr():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 10, 12, 20, 30, 31, 33, 41, 42, 43, 44, 50, 60, 70, 71]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['dip14pr'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['dip14pr'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_dip14pr()


def histogram_mloy_d():  # comprendre ce qui ne va pas ici
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0.65, 0.7, 0.75, .8, 0.85, 0.9, 0.95]:
        list_values_bdf.append(data_bdf['mloy_d'].quantile(i))
        list_values_entd.append(data_entd['mloy_d'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_mloy_d()


def histogram_nactifs():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 7):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nactifs'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['nactifs'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_nactifs()


def histogram_nbphab():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 11):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nbphab == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.nbphab == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_nbphab()


def histogram_nb_diesel():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 9):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nb_diesel == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.nb_diesel == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_nb_diesel()


def histogram_nb_essence():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 11):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.nb_essence == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.nb_essence == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_nb_essence()


def histogram_nenfants():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 12):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nenfants'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['nenfants'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_nenfants()


def histogram_niveau_vie():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['niveau_vie'].quantile(i))
        list_values_entd.append(data_entd['niveau_vie'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_niveau_vie()


def histogram_npers():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 14):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['npers'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['npers'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_npers()


def histogram_ocde10():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ocde10 == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.ocde10 == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_ocde10()


def histogram_situapr():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(1, 8):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['situapr'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['situapr'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_situapr()


def histogram_stalog():  # This variable must be redefined
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(1, 6):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['stalog'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd['stalog'] == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_stalog()


def histogram_tau():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(1, 11):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tau == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.tau == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_tau()


def histogram_tuu():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 9):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tuu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.tuu == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_tuu()


def histogram_typmen():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(1, 6):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.typmen == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.typmen == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_typmen()


def histogram_veh_tot():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in range(0, 11):
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.veh_tot == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.veh_tot == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_veh_tot()


def histogram_vp_deplacements_pro():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.vp_deplacements_pro == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.vp_deplacements_pro == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_vp_deplacements_pro()


def histogram_vp_domicile_travail():
    list_values_bdf = []
    list_values_entd = []
    list_keys = []
    for i in [0, 1]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.vp_domicile_travail == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_entd['pondmen_{}'.format(i)] = 0
        data_entd['pondmen_{}'.format(i)].loc[data_entd.vp_domicile_travail == i] = data_entd['pondmen']
        part_entd = data_entd['pondmen_{}'.format(i)].sum() / data_entd['pondmen'].sum()
        del data_entd['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_entd.append(part_entd)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_entd, 'BdF', 'ENTD')

    return figure


histogram_vp_domicile_travail()
