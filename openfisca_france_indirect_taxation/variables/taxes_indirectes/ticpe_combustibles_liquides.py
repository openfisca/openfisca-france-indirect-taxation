# -*- coding: utf-8 -*-
from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class combustibles_liquides_ticpe(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant de TICPE sur les combustibles liquides'

    def formula(menage, period, parameters):
        quantites_combustibles_liquides = menage('quantites_combustibles_liquides', period)
        accise_combustibles_liquides = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole_fioul_domestique_hectolitre
        combustibles_liquides_ticpe = quantites_combustibles_liquides * accise_combustibles_liquides / 100

        return combustibles_liquides_ticpe
