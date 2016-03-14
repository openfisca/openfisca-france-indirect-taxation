# -*- coding: utf-8 -*-

from __future__ import division


import itertools
import os
import pandas
import pkg_resources


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory


elasticities_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    )


def build_clean_aliss_data_frame():
    year = 2011
    aliss_survey_collection = SurveyCollection.load(
        collection = 'aliss', config_files_directory = config_files_directory
        )
    survey = aliss_survey_collection.get_survey('aliss_{}'.format(year))

    aliss = survey.get_values(table = 'Base_ALISS_2011')
    aliss['age'] = 99
    aliss['revenus'] = 99

    triplets = [
        ('1 : Jeune/Ais', 0, 3),
        ('2 : Jeune/MoyenSup', 0, 2),
        ('3 : Jeune/MoyenInf', 0, 1),
        ('4 : Jeune/Modeste', 0, 0),
        ('5 : Age Moyen/Ais', 1, 3),
        ('6 : Age Moyen/MoyenSup', 1, 2),
        ('7 : Age Moyen/MoyenInf', 1, 1),
        ('8 : Age Moyen/Modeste', 1, 0),
        ('9 : Age Sup/Ais', 2, 3),
        ('10 : Age Sup/MoyenSup', 2, 2),
        ('11 : Age Sup/MoyenInf', 2, 1),
        ('12 : Age Sup/Modeste', 2, 0),
        ('13 : Vieux/Ais', 3, 3),
        ('14 : Vieux/MoyenSup', 3, 2),
        ('15 : Vieux/MoyenInf', 3, 1),
        ('16 : Vieux/Modeste', 3, 0),
        ]

    for household_type, age, revenus in triplets:
        print household_type, age, revenus
        selection = aliss.type.str.startswith(household_type)
        aliss.loc[selection, 'age'] = age
        aliss.loc[selection, 'revenus'] = revenus

    assert aliss.age.isin(range(4)).all()
    assert aliss.revenus.isin(range(4)).all()
    del aliss['type']
    return aliss


def compute_correction_coefficient():
    # Calculer les cales
    pass


def compute_kantar_elasticities(aliss):

    nomf_by_dirty_nomf = {
        '1 : Juices': 'Juic',
        '2 : Alcohol': 'Alc',
        '3 : Soft drinks': 'SD',
        '4 : Bottled water': 'Wat',
        '5 : Coffee and tea': 'Cof',
        '6 : Fresh fruits and vegetables': 'FFV',
        '7 : Spices': 'Spices',
        '8 : Plant-based foods high in fats': 'PBF',
        '9 : Plant-based dishes': 'PBD',
        '10 : Plant-based foods high in sugar': 'PBS',
        '11 : Starchy foods': 'Starch',
        '12 : Processed fruits and vegetables': 'PFV',
        '13 : Beef': 'Beef',
        '14 : Other meats': 'OM',
        '15 : Cooked meats': 'CM',
        '16 : Animal-based foods high in fats': 'ABF',
        '17 : Cheese': 'Cheese',
        '18 : Fish and seafoods': 'Fish',
        '19 : Dairy products': 'Dairy',
        '20 : Prepared mixed meals': 'PrepM',
        '21 : Prepared desserts': 'PrepD',
        }

    nomf_nomk = aliss.query('age == 0 & revenus == 0')[['nomf', 'nomk']]
    (nomf_nomk.nomk.value_counts() == 1).all()
    nomf_by_nomk = nomf_nomk.set_index('nomk').to_dict()['nomf']
    nomks_by_nomf = dict(
        (nomf_by_dirty_nomf.get(nomf), nomf_nomk.query('nomf == @nomf')['nomk'].unique())
        for nomf in nomf_nomk.nomf.unique()
        )

    # budget shares
    budget_share_path = os.path.join(elasticities_path, 'budget_share.csv')
    if os.path.exists(budget_share_path):
        kantar_budget_share = pandas.read_csv(budget_share_path)
    else:
        kantar_budget_share = pandas.DataFrame()
        for age, revenus, nomf in itertools.product(aliss.age.unique(), aliss.revenus.unique(), aliss.nomf.unique()):

            extract = aliss.query(
                'nomf == @nomf & age == @age & revenus == @revenus'
                )[
                    ['age', 'revenus', 'nomk', 'dm_k', 'dm_f']
                ]

            assert len(extract.dm_f.unique()) == 1

            extract['budget_share_kf'] = extract.dm_k / extract.dm_f
            extract['nomf'] = nomf_by_dirty_nomf.get(nomf)
            kantar_budget_share = kantar_budget_share.append(extract)

        kantar_budget_share.fillna(0, inplace = True)
        kantar_budget_share.to_csv(budget_share_path)

    csv_path_name = os.path.join(
        elasticities_path,
        'cross_price_elasticities.csv',
        )
    nomf_cross_price_elasticities = pandas.read_csv(csv_path_name)

    nomks = aliss.nomk.unique()

    nomk_cross_price_elasticity = pandas.DataFrame(
        index = nomks,
        columns = list(nomks) + ['age', 'revenus'],
        )

    for age, revenus in itertools.product(aliss.age.unique(), aliss.revenus.unique()):

        nomf_cross_price_elasticity = nomf_cross_price_elasticities.query(
            'age == @age & revenus == @revenus').set_index('product')
        nomf_cross_price_elasticity.drop(['age', 'revenus'], axis = 1, inplace = True)
        nomfs = nomf_cross_price_elasticity.index.unique()

        for f, fprime in itertools.product(nomfs, nomfs):
            elasticity_ffprime = nomf_cross_price_elasticity.loc[f, fprime]
            elasticity_kkprime = pandas.DataFrame(
                index = nomks_by_nomf[f],
                columns = nomks_by_nomf[fprime],
                )
            nomks_for_fprime = nomks_by_nomf[fprime]
            budget_share = kantar_budget_share.query(
                'age == @age & revenus == @revenus & nomk in @nomks_for_fprime & nomf == @fprime'
                )[['nomk', 'budget_share_kf']].set_index(('nomk'))
            transposed_elasticity_kkprime = elasticity_kkprime.T
            transposed_elasticity_kkprime.loc[nomks_for_fprime] = budget_share * elasticity_ffprime
            elasticity_kkprime = transposed_elasticity_kkprime.T
            elasticity_kkprime['age'] = age
            elasticity_kkprime['revenus'] = revenus
            nomk_cross_price_elasticity = nomk_cross_price_elasticity.combine_first(elasticity_kkprime)

    return nomk_cross_price_elasticity


if __name__ == '__main__':
    aliss = build_clean_aliss_data_frame()
    kantar_elasticities = compute_kantar_elasticities(aliss)
