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

    def formula_2017(menage, period, parameters):
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

    def formula_2009(menage, period, parameters):
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_e10_hors_tva = cout_essence_sp95_e10_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_sp95_e10_ttc - Cout_essence_sp95_e10_hors_tva
        return tva

class tva_sur_essence_sp95(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de l'essence sp95"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_hors_tva = cout_essence_sp95_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_sp95_ttc - Cout_essence_sp95_hors_tva
        return tva

class tva_sur_essence_sp98(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de l'essence sp98"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp98_hors_tva = cout_essence_sp98_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_sp98_ttc - Cout_essence_sp98_hors_tva
        return tva

class tva_sur_essence_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de l'essence super plombé"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_super_plombe_hors_tva = cout_essence_super_plombe_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_super_plombe_ttc - Cout_essence_super_plombe_hors_tva
        return tva

class tva_sur_essence_e85(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de l'essence e85"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_essence_e85_hors_tva = cout_essence_e85_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_essence_e85_ttc - Cout_essence_essence_e85_hors_tva
        return tva

# TVA sur le gaz de pétrole liquéfié carburant:

class tva_sur_gpl_carburant(Variable):
    value_type = float
    entity = Menage
    label = "TVA sur la consommation de gaz de pétrole liquéfié carburant"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gpl_carburant_ttc = menage('cout_gpl_carburant_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gpl_carburant_hors_tva = cout_gpl_carburant_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_gpl_carburant_ttc - Cout_gpl_carburant_hors_tva
        return tva