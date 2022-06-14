import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# TVA sur different type de gazole:

class tva_sur_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de gazole B7"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b7_hors_tva = cout_gazole_b7_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_gazole_b7_ttc - Cout_gazole_b7_hors_tva
        return tva

class tva_sur_gazole_b10(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de gazole B10"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b10_hors_tva = cout_gazole_b10_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_gazole_b10_ttc - Cout_gazole_b10_hors_tva
        return tva

# TVA sur different type d'essence:

class tva_sur_essence_sp95_e10(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de l'essence sp95 e10"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_e10_hors_tva = cout_essence_sp95_e10_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_sp95_e10_ttc - Cout_essence_sp95_e10_hors_tva
        return tva