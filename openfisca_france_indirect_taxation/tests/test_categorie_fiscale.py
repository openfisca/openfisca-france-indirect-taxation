import pytest


from ..scripts.build_coicop_legislation import get_categorie_fiscale


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
restauration_sur_place = dict(
    value = '11.1.1.1.1',
    categorie_fiscale = 'tva_taux_plein',
    year = 2009,
    )
restauration_sur_place_reforme_2010 = dict(
    value = '11.1.1.1.1',
    categorie_fiscale = 'tva_taux_reduit',
    year = 2010,
    )


@pytest.mark.parametrize('member', [margarine, confiserie, alcools, vin, restauration_sur_place, restauration_sur_place_reforme_2010])
def check_categorie_fiscale(member):
    computed_categorie_fiscale = get_categorie_fiscale(member['value'], year = member.get('year'))
    assert computed_categorie_fiscale == member['categorie_fiscale'], \
        '\nError with coicop = {}, year = {}: \ncomputed categorie_fiscale {} != {}'.format(
        member['value'],
        member.get('year'),
        computed_categorie_fiscale,
        member['categorie_fiscale']
        )
