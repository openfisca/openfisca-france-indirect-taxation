# -*- coding: utf-8 -*-


from ..scripts.build_coicop_legislation import get_categorie_fiscale


def test():
    margarine = dict(
        value = '01.1.5.2.2',
        categorie_fiscale = 'tva_taux_plein',
        )
    # et les confiseries et le chocolat
    confiserie = dict(
        value = ['01.1.8.1.3', '01.1.8.2.1', '01.1.8.2.2'],
        categorie_fiscale = 'tva_taux_plein'
        )
    # 02 Boissons alcoolisées et tabac
    # alccols forts
    alcools = dict(
        value = '02.1.1',
        categorie_fiscale = 'alcools_forts',
        )
    # vins et boissons fermentées
    vin = dict(
        value = '02.1.2',
        categorie_fiscale = 'vin',
        )

    for member in [margarine, confiserie, alcools, vin]:
        assert get_categorie_fiscale(member['value']) == member['categorie_fiscale']


def test_education():
    for value in [10, '10']:
        assert get_categorie_fiscale(value) == ''


