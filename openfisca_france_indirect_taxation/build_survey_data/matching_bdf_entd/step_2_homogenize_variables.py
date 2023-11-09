# -*- coding: utf-8 -*-

# Dans ce script les variables qui ont des différences de définition sont reconstruites
# sur le modèle de l'enquête BdF (ou entd dans certains cas où la nomenclature entd a plus de sens)
# de manière à avoir des définitions identiques.
# Les noms de variables sont aussi alignés.


from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_1_3_build_dataframes_indiv_teg import \
    merge_indiv_teg_menage


def homogenize_variables_definition_bdf_entd(year_data):
    data_entd, data_bdf = merge_indiv_teg_menage(year_data)

    # Aides au logement : séparation propriétaire/locataire dans BdF -> création d'une unique variable
    check = data_bdf.query('aidlog1 != 0')
    assert (check['aidlog2'] == 0).any()

    data_bdf['aba'] = data_bdf['aidlog1'] + data_bdf['aidlog2']
    del check, data_bdf['aidlog1'], data_bdf['aidlog2']

    # Distribution des ménages parisiens dans les catégories des grands pôles
    data_entd.loc[data_entd.numcom_au2010 == 113, 'numcom_au2010'] = 111
    data_entd.loc[data_entd.numcom_au2010 == 114, 'numcom_au2010'] = 112

    data_bdf.loc[data_bdf.stalog == 5, 'stalog'] = 4
    data_bdf.loc[data_bdf.stalog == 6, 'stalog'] = 5

    # Rename
    data_entd.rename(
        columns = {
            'nbuc': 'ocde10',
            'numcom_au2010': 'cataeu',
            'pondv1': 'pondmen',
            'rlog': 'aba',
            'tau99': 'tau',
            'tu99': 'tuu',
            'typmen5': 'typmen',
            'v1_logloymens': 'mloy_d',
            'v1_logocc': 'stalog',
            'v1_logpiec': 'nbphab',
            },
        inplace = True,
        )

    data_entd = data_entd.sort_index(axis = 1)
    data_bdf = data_bdf.sort_index(axis = 1)

    return data_entd, data_bdf


def create_new_variables(year_data):
    data_entd, data_bdf = homogenize_variables_definition_bdf_entd(year_data)

    def create_new_variables_(data, option = None):
        assert option in ['entd', 'bdf']

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

        data['aides_logement'] = 0
        data.loc[data['aba'] == 1, 'aides_logement'] = 1
        del data['aba']

        data['veh_tot'] = data['veh_tot'].fillna(0)
        data['mloy_d'] = data['mloy_d'].fillna(0)

        data['part_essence'] = (
            data.essence / (data.essence + data.diesel + data.autre_carbu)
            )
        data['part_diesel'] = (
            data.diesel / (data.essence + data.diesel + data.autre_carbu)
            )
        data['nb_essence'] = data.veh_tot * data.part_essence
        data['nb_diesel'] = data.veh_tot * data.part_diesel
        data[['nb_essence', 'nb_diesel']] = data[['nb_essence', 'nb_diesel']].fillna(0)

        data.drop(
            ['part_essence', 'part_diesel', 'essence', 'diesel', 'autre_carbu'],
            axis = 1,
            inplace = True
            )

        if option == 'entd':
            data['distance'] = data.distance_diesel + data.distance_essence + data.distance_autre_carbu

        return data

    return create_new_variables_(data_entd, option = 'entd'), create_new_variables_(data_bdf, option = 'bdf')


def create_niveau_vie_quantiles(year_data):
    data_entd, data_bdf = create_new_variables(year_data)

    def create_niveau_vie_quantiles_(data, option = None):
        assert option in ['entd', 'bdf']
        if option == 'entd':
            data['niveau_vie'] = data['revuc'].copy() * 12
            del data['revuc']
        else:
            data['niveau_vie'] = data.revtot / data.ocde10

        data = data.sort_values(by = ['niveau_vie'])
        data['sum_pondmen'] = data['pondmen'].cumsum()

        population_totale = data['sum_pondmen'].max()
        data['niveau_vie_decile'] = 0
        for j in range(1, 11):
            data.loc[data.sum_pondmen > population_totale * (float(j) / 10 - 0.1), 'niveau_vie_decile'] = j

        data['niveau_vie_quintile'] = 0
        for j in range(1, 6):
            data.loc[data.sum_pondmen > population_totale * (float(j) / 5 - 0.2), 'niveau_vie_decile'] = j

        data = data.sort_index()
        del data['sum_pondmen']

        return data.copy()

    return create_niveau_vie_quantiles_(data_entd, option = 'entd'), create_niveau_vie_quantiles_(data_bdf, option = 'bdf')


if __name__ == '__main__':
    data_entd, data_bdf = create_niveau_vie_quantiles()
