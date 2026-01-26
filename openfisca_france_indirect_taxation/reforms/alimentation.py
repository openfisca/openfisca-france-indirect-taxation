# -*- coding: utf-8 -*-


from openfisca_core.reforms import Reform

from openfisca_france_indirect_taxation.variables.consommation.categories_fiscales import generate_depenses_ht_categories_fiscales_variables


class reforme_alimentation(Reform):
    name = 'reforme_alimentation'

    def apply(self):
        from openfisca_france_indirect_taxation.variables.consommation.categories_fiscales import categories_fiscales_data_frame
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

        generate_depenses_ht_categories_fiscales_variables(
            tax_benefit_system = self,
            legislation_dataframe = categories_fiscales,
            reform_key = self.name,
            )
