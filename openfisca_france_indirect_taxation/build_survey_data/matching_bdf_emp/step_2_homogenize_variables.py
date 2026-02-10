# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou emp dans certains cas où la nomenclature emp a plus de sens)
# de manière à avoir des définitions identiques. Les noms de variables sont aussi alignés.

import numpy as np
from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_emp.step_1_2_build_dataframes_vehicles import build_df_menages_vehicles


def homogenize_variables_definition_bdf_emp(year_data):
    data_bdf, data_emp = build_df_menages_vehicles(year_data)
    check = data_bdf.query('aidlog1 != 0')
    assert (check['aidlog2'] == 0).any()

    data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
    del check, data_bdf['aidlog1'], data_bdf['aidlog2']

    # Distribution des ménages parisiens dans les catégories des grands pôles
    # data_emp.loc[data_emp.numcom_au2010 == 113, 'numcom_au2010'] = 111
    # data_emp.loc[data_emp.numcom_au2010 == 114, 'numcom_au2010'] = 112

    data_bdf.loc[data_bdf.stalog == 5, 'stalog'] = 4
    data_bdf.loc[data_bdf.stalog == 6, 'stalog'] = 5

    # Rename
    data_emp.rename(
        columns = {
            'dipdetpr': 'dip14pr',
            'nivie10': 'niveau_vie_decile',         # emp 2008
            'decile_rev_uc': 'niveau_vie_decile',   # emp 2019
            'nbuc': 'ocde10',                       # emp 2008
            'coeffuc': 'ocde10',                    # emp 2019
            'jnbveh': 'veh_tot',                    # emp 2019
            # 'numcom_au2010': 'cataeu',
            'pondv1': 'pondmen',
            'pond_menc': 'pondmen',
            'rlog': 'aba',
            'tau99': 'tau',
            'tu99': 'tuu',                          # emp 2008
            'tuu2017_res': 'tuu',                   # emp 2019
            'typmen5': 'typmen',
            'v1_logloymens': 'mloy_d',
            'v1_logocc': 'stalog',
            'v1_logpiec': 'nbphab',
            },
        inplace = True,
        )
    data_emp = data_emp.sort_index(axis = 1)
    data_bdf = data_bdf.sort_index(axis = 1)

    return data_bdf, data_emp


def create_new_variables(year_data):
    data_bdf, data_emp = homogenize_variables_definition_bdf_emp(year_data)

    def create_new_variables_(data, option = None):
        assert option in ['emp', 'bdf']

        # Création de dummy variables pour la commune de résidence
        data['rural'] = 0
        data['petite_ville'] = 0
        data['moyenne_ville'] = 0
        data['grande_ville'] = 0
        data['paris'] = 0

        data.loc[data.tuu == 0, 'rural'] = 1
        data.loc[data.tuu == 1, 'petite_ville'] = 1
        data.loc[data.tuu == 2, 'petite_ville'] = 1
        data.loc[data.tuu == 3, 'petite_ville'] = 1
        data.loc[data.tuu == 4, 'moyenne_ville'] = 1
        data.loc[data.tuu == 5, 'moyenne_ville'] = 1
        data.loc[data.tuu == 6, 'moyenne_ville'] = 1
        data.loc[data.tuu == 7, 'grande_ville'] = 1
        data.loc[data.tuu == 8, 'paris'] = 1

        # data['aides_logement'] = 0
        # data.loc[data['aba'] == 1, 'aides_logement'] = 1
        # del data['aba']

        data['veh_tot'] = data['veh_tot'].fillna(0)
        data['essence'] = data['essence'].fillna(0)
        data['diesel'] = data['diesel'].fillna(0)
        data['autre_carbu'] = data['autre_carbu'].fillna(0)
        # Renommer les variables de nombre de véhicules par type de carburant
        data.rename(columns = {
            'diesel': 'nb_diesel',
            'essence': 'nb_essence',
            'autre_carbu': 'nb_autre_carbu'
            }, inplace = True
            )
        
        if option == 'emp':
            data['distance'] = data.distance_diesel + data.distance_essence + data.distance_autre_carbu

        return data

    return create_new_variables_(data_bdf, option = 'bdf'), create_new_variables_(data_emp, option = 'emp')


def create_niveau_vie_quantiles(year_data):
    data_bdf, data_emp = create_new_variables(year_data)

    def create_niveau_vie_quantiles_(data, option = None):
        assert option in ['emp', 'bdf']
        if option == 'bdf':
            data['niveau_vie'] = data.rev_disponible / data.ocde10

            data = data.sort_values(by = ['niveau_vie'])
            data['sum_pondmen'] = data['pondmen'].cumsum()

            population_totale = data['sum_pondmen'].max()
            data['niveau_vie_decile'] = 0

            for j in range(1, 11):
                data.loc[data.sum_pondmen > population_totale * (float(j) / 10 - 0.1), 'niveau_vie_decile'] = j

            data['niveau_vie_quintile'] = 0
            for j in range(1, 6):
                data.loc[data.sum_pondmen > population_totale * (float(j) / 5 - 0.2), 'niveau_vie_quintile'] = j

            del data['sum_pondmen']

        if option == 'emp':
            data['niveau_vie_quintile'] = data['niveau_vie_decile'].apply(lambda x: np.ceil(x / 2))
        data = data.sort_index()

        return data.copy()

    return create_niveau_vie_quantiles_(data_bdf, option = 'bdf'), create_niveau_vie_quantiles_(data_emp, option = 'emp')


if __name__ == '__main__':
    data_bdf, data_emp = create_niveau_vie_quantiles(2017)
