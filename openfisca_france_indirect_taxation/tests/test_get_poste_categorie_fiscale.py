import pytest


from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import get_poste_categorie_fiscale


confiserie = dict(
    value = ['01.1.8.1.3', '01.1.8.2.1'],
    categorie_fiscale = 'tva_taux_plein'
    )
# 02 Boissons alcoolisées et tabac
# alccols forts
alcools = dict(
    value = '02.1.1.1.1',
    categorie_fiscale = 'alcools_forts',
    )
# vins et boissons fermentées
vin = dict(
    value = '02.1.2.1.1',
    categorie_fiscale = 'vin',
    )
# bière
biere = dict(
    value = '02.1.3.1.1',
    categorie_fiscale = 'biere',
    )

@pytest.mark.parametrize("categorie", [confiserie, alcools, vin, biere])
def test_categorie_fiscale(categorie):
    postes_coicop = categorie['value']
    categorie_fiscale = categorie['categorie_fiscale']
    if isinstance(postes_coicop, str):
        assert_categorie_fiscale(postes_coicop, [categorie_fiscale])
    else:
        for poste_coicop in postes_coicop:
            assert_categorie_fiscale(poste_coicop, [categorie_fiscale])


def assert_categorie_fiscale(poste_coicop, categorie_fiscale):
    got = get_poste_categorie_fiscale(poste_coicop)
    assert categorie_fiscale == got, \
        "For poste coicop {} we have wrong categorie fiscale: \n got {} but should be {}".format(
            poste_coicop, got, categorie_fiscale)
