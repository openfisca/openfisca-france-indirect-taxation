import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# montant TVA sur different type de gazole:

class tva_sur_gazole_b7(Variable):
    value_type = float
    entity = Menage
    label = 'TVA sur la consommation de gazole B7'
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
    label = 'TVA sur la consommation de gazole B10'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period, parameters):
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b10_hors_tva = cout_gazole_b10_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_gazole_b10_ttc - Cout_gazole_b10_hors_tva
        return tva

# montant TVA sur gazole total:

class tva_sur_gazole_total(Variable):
    value_type = float
    entity = Menage
    label = 'TVA total sur le gazole'
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        tva_sur_gazole_b7 = menage('tva_sur_gazole_b7', period)
        tva_sur_gazole_b10 = menage('tva_sur_gazole_b10', period)
        tva_sur_gazole_total = (tva_sur_gazole_b7 + tva_sur_gazole_b10)
        return tva_sur_gazole_total

    def formula(menage, period):
        tva_sur_gazole_b7 = menage('tva_sur_gazole_b7', period)
        tva_sur_gazole_total = tva_sur_gazole_b7
        return tva_sur_gazole_total

# montant TVA sur different type d'essence:

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

# montant TVA total sur l'essence
class tva_sur_essence_total(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TVA sur tous les types d'essences cumulés"
    definition_period = YEAR

    def formula_2009(menage, period):
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        tva_sur_essence_e85 = menage('tva_sur_essence_e85', period)
        tva_sur_essence_sp95_e10 = menage('tva_sur_essence_sp95_e10', period)
        tva_sur_essence_total = (tva_sur_essence_sp95 + tva_sur_essence_sp98 + tva_sur_essence_e85 + tva_sur_essence_sp95_e10)
        return tva_sur_essence_total

    def formula_2007(menage, period):
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        tva_sur_essence_e85 = menage('tva_sur_essence_e85', period)
        tva_sur_essence_total = (tva_sur_essence_sp95 + tva_sur_essence_sp98 + tva_sur_essence_e85)
        return tva_sur_essence_total

    def formula_1990(menage, period):
        tva_sur_essence_sp95 = menage('tva_sur_essence_sp95', period)
        tva_sur_essence_sp98 = menage('tva_sur_essence_sp98', period)
        tva_sur_essence_super_plombe = menage('tva_sur_essence_super_plombe', period)
        tva_sur_essence_total = (tva_sur_essence_sp95 + tva_sur_essence_sp98 + tva_sur_essence_super_plombe)
        return tva_sur_essence_total

# montant TVA sur le gaz de pétrole liquéfié carburant:

class tva_sur_gpl_carburant(Variable):
    value_type = float
    entity = Menage
    label = 'TVA sur la consommation de gaz de pétrole liquéfié carburant'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gpl_carburant_ttc = menage('cout_gpl_carburant_ttc', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gpl_carburant_hors_tva = cout_gpl_carburant_ttc * (1 / (1 + taux_plein_tva) )
        tva = cout_gpl_carburant_ttc - Cout_gpl_carburant_hors_tva
        return tva

# montant carburant total:
class tva_sur_carburant_total(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant de la TVA sur tous les carburants cumulés'
    definition_period = YEAR

    def formula(menage, period):
        tva_sur_essence_total = menage('tva_sur_essence_total', period)
        tva_sur_gazole_total = menage('tva_sur_gazole_total', period)
        tva_sur_gpl_carburant = menage('tva_sur_gpl_carburant', period)
        tva_sur_carburant_total = tva_sur_gazole_total + tva_sur_essence_total + tva_sur_gpl_carburant
        return tva_sur_carburant_total