# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform

from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import generate_variables


class reforme_alimentation(Reform):
    name = 'Allocations familiales imposables'

    def apply(self):
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
            reform_key = self.name,
            tax_benefit_system = self,
            )
