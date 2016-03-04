# -*- coding: utf-8 -*-

from __future__ import division


import itertools
import pandas


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory


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


def compute_kantar_elasticities():
    kantar_budget_share = pandas.DataFrame()
    for age, revenus, nomf in itertools.product(aliss.age.unique(), aliss.revenus.unique(), aliss.nomf.unique()):

        print '\n', age, revenus, nomf

        extract = aliss.query(
            'nomf == @nomf & age == @age & revenus == @revenus'
            )[
                ['age', 'revenus', 'nomk', 'dm_k', 'dm_f']
            ]

        assert len(extract.dm_f.unique()) == 1
        extract['budget_share_kf'] = extract.dm_k / extract.dm_f
        kantar_budget_share = kantar_budget_share.append(extract)

    for age, revenus in itertools.product(aliss.age.unique(), aliss.revenus.unique()):
        print age, revenus

    return kantar_budget_share


if __name__ == '__main__':
    aliss = build_clean_aliss_data_frame()
    kantar_elasticities = compute_kantar_elasticities()
