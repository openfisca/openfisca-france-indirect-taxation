# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_core import reforms

from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import generate_variables


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'test_reforme_alimentation',
        name = u"Réforme de l'imposition indirecte des biens alimentaires",
        reference = tax_benefit_system,
        )
    from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import categories_fiscales_data_frame
    categories_fiscales = categories_fiscales_data_frame.copy()
    categories_fiscales.loc[
        (categories_fiscales.categorie_fiscale == 'tva_taux_super_reduit') & (
            categories_fiscales.code_bdf.str.startswith('c06111')),
        'categorie_fiscale'
        ] = ''
    categories_fiscales.loc[
        categories_fiscales.categorie_fiscale == 'vin',
        'categorie_fiscale'
        ] = ''

    generate_variables(
        categories_fiscales = categories_fiscales,
        Reform = Reform,
        tax_benefit_system = tax_benefit_system,
        )

    reform = Reform()
    # reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform


