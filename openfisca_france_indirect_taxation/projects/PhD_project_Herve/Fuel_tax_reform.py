from openfisca_core.reforms import Reform

DIESEL_KG_CO2_PAR_HL = 264.5
ESSENCE_KG_CO2_PAR_HL = 228.4
ETHANOL_KG_CO2_PAR_HL = 171.6


class reform_ticpe_2019_in_2018(Reform):
    name = u'Augmentation de la TICPE programmée pour 2019'

    def apply(self):
        def reform_modify_parameters(parameters):
            reform_parameters = parameters
            reform_parameters.imposition_indirecte.produits_energetiques.ticpe.gazole.update(
                start="2018-01-01",
                value=59.4 + 2.6 + (55.0 - 44.6) / 1e3 * DIESEL_KG_CO2_PAR_HL
            )
            reform_parameters.imposition_indirecte.produits_energetiques.ticpe.super_95_98.update(
                start="2018-01-01",
                value=68.29 + (55.0 - 44.6) / 1e3 * ESSENCE_KG_CO2_PAR_HL
            )
            reform_parameters.imposition_indirecte.produits_energetiques.ticpe.super_e10.update(
                start="2018-01-01",
                value=66.29 + (55.0 - 44.6) / 1e3 * ESSENCE_KG_CO2_PAR_HL
            )
            reform_parameters.imposition_indirecte.produits_energetiques.ticpe.super_plombe.update(
                start="2018-01-01",
                value=71.56 + (55.0 - 44.6) / 1e3 * ESSENCE_KG_CO2_PAR_HL
            )
            reform_parameters.imposition_indirecte.produits_energetiques.ticpe.super_e_85_utilise_comme_carburant_hectolitre.update(
                start="2018-01-01",
                value=11.83 + (55.0 - 44.6) / 1e3 * ESSENCE_KG_CO2_PAR_HL
            )
            reform_parameters.imposition_indirecte.emissions_CO2.carburants.CO2_diesel.update(
                start="2018-01-01",
                value=DIESEL_KG_CO2_PAR_HL / 100
            )
            reform_parameters.imposition_indirecte.emissions_CO2.carburants.CO2_essence.update(
                start="2018-01-01",   
                value=ESSENCE_KG_CO2_PAR_HL / 100
            )
            return parameters

        self.modify_parameters(modifier_function=reform_modify_parameters)