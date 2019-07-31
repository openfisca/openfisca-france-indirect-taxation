# -*- coding: utf-8 -*-


# Dans ce script on utilise des histogrammes pour comparer la distribution des variables dans les deux enquêtes.
# On peut ainsi juger si certaines d'entre elles doivent être ajustées de manière
# à les harmoniser entre les deux enquêtes.
# Cette décision se fait sur la base des résultats observés et ne dépend d'aucun critère précis.

from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_2_homogenize_variables import \
    homogenize_definitions
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes


data = homogenize_definitions()
data_erfs = data[0]
data_bdf = data[1]


def histogram_agepr():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['agepr'].quantile(i))
        list_values_erfs.append(data_erfs['agepr'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_agepr()


def histogram_cataeu():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [111, 112, 120, 211, 212, 221, 222, 300, 400]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.cataeu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs.cataeu == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_cataeu()


def histogram_nactifs():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf['nactifs'] == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs['nactifs'] == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_nactifs()


def histogram_ocde10():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [1, 1.3, 1.5, 1.6, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.ocde10 == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs.ocde10 == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_ocde10()


def histogram_rev_disponible():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['rev_disponible'].quantile(i))
        list_values_erfs.append(data_erfs['rev_disponible'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_rev_disponible()


def histogram_salaires():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['salaires'].quantile(i))
        list_values_erfs.append(data_erfs['salaires'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_salaires()


def histogram_retraites():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [.05, .2, .35, .5, 0.65, .8, 0.95]:
        list_values_bdf.append(data_bdf['retraites'].quantile(i))
        list_values_erfs.append(data_erfs['retraites'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_retraites()


def histogram_rev_etranger():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0.995, 0.996, 0.997, 0.998, 0.999, 0.9995]:
        list_values_bdf.append(data_bdf['rev_etranger'].quantile(i))
        list_values_erfs.append(data_erfs['rev_etranger'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_rev_etranger()


def histogram_rsa_act():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0.95, 0.98, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9995]:
        list_values_bdf.append(data_bdf['rsa_act'].quantile(i))
        list_values_erfs.append(data_erfs['rsa_act'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_rsa_act()


def histogram_prest_precarite_hand():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0.95, 0.98, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9995]:
        list_values_bdf.append(data_bdf['prest_precarite_hand'].quantile(i))
        list_values_erfs.append(data_erfs['prest_precarite_hand'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_prest_precarite_hand()


def histogram_prest_precarite_rsa():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0.95, 0.98, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9995]:
        list_values_bdf.append(data_bdf['prest_precarite_rsa'].quantile(i))
        list_values_erfs.append(data_erfs['prest_precarite_rsa'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_prest_precarite_rsa()


def histogram_prest_precarite_vieil():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0.95, 0.98, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999, 0.9995]:
        list_values_bdf.append(data_bdf['prest_precarite_vieil'].quantile(i))
        list_values_erfs.append(data_erfs['prest_precarite_vieil'].quantile(i))
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_prest_precarite_vieil()


def histogram_tau():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tau == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs.tau == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_tau()


def histogram_tuu():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5, 6, 7, 8]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.tuu == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs.tuu == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_tuu()


def histogram_typmen():
    list_values_bdf = []
    list_values_erfs = []
    list_keys = []
    for i in [0, 1, 2, 3, 4, 5]:
        data_bdf['pondmen_{}'.format(i)] = 0
        data_bdf['pondmen_{}'.format(i)].loc[data_bdf.typmen == i] = data_bdf['pondmen']
        part_bdf = data_bdf['pondmen_{}'.format(i)].sum() / data_bdf['pondmen'].sum()
        del data_bdf['pondmen_{}'.format(i)]

        data_erfs['pondmen_{}'.format(i)] = 0
        data_erfs['pondmen_{}'.format(i)].loc[data_erfs.typmen == i] = data_erfs['pondmen']
        part_erfs = data_erfs['pondmen_{}'.format(i)].sum() / data_erfs['pondmen'].sum()
        del data_erfs['pondmen_{}'.format(i)]

        list_values_bdf.append(part_bdf)
        list_values_erfs.append(part_erfs)
        list_keys.append('{}'.format(i))

    figure = histogrammes(list_keys, list_values_bdf, list_values_erfs, 'BdF', 'ERFS')

    return figure


histogram_typmen()
