import numpy as np

from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# cout different type de gazole ht:

class cout_gazole_b7_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout du gazole B7 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc', period)
        gazole_b7_ticpe = menage('gazole_b7_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b7_hors_tva = cout_gazole_b7_ttc * (1 / (1 + taux_plein_tva) )
        gazole_b7_ht = Cout_gazole_b7_hors_tva - gazole_b7_ticpe
        return gazole_b7_ht

class cout_gazole_b10_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout du gazole B10 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc', period)
        gazole_b10_ticpe = menage('gazole_b10_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gazole_b10_hors_tva = cout_gazole_b10_ttc * (1 / (1 + taux_plein_tva) )
        gazole_b10_ht = Cout_gazole_b10_hors_tva - gazole_b10_ticpe
        return gazole_b10_ht

# cout gazole total ht:
class cout_gazole_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout total du gazole ht"
    definition_period = YEAR
    default_value = 0

    def formula_2017(menage, period):
        cout_gazole_b7_ht = menage('cout_gazole_b7_ht', period)
        cout_gazole_b10_ht = menage('cout_gazole_b10_ht', period)
        cout_gazole_total_ht = (cout_gazole_b7_ht + cout_gazole_b10_ht)
        return cout_gazole_total_ht

    def formula(menage, period):
        cout_gazole_b7_ht = menage('cout_gazole_b7_ht', period)
        cout_gazole_total_ht = cout_gazole_b7_ht
        return cout_gazole_total_ht

# cout different type d'essence ht:

class cout_essence_sp95_e10_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence SP95 E10 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc', period)
        essence_sp95_e10_ticpe = menage('essence_sp95_e10_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_e10_hors_tva = cout_essence_sp95_e10_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_sp95_e10_ht = Cout_essence_sp95_e10_hors_tva - essence_sp95_e10_ticpe
        return cout_essence_sp95_e10_ht

class cout_essence_SP95_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence SP95 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc', period)
        essence_sp95_ticpe = menage('essence_sp95_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp95_hors_tva = cout_essence_sp95_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_sp95_ht = Cout_essence_sp95_hors_tva - essence_sp95_ticpe
        return cout_essence_sp95_ht

class cout_essence_SP98_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence SP98 ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc', period)
        essence_sp98_ticpe = menage('essence_sp98_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_sp98_hors_tva = cout_essence_sp98_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_sp98_ht = Cout_essence_sp98_hors_tva - essence_sp98_ticpe
        return cout_essence_sp98_ht

class cout_essence_super_plombe_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence super plombé ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc', period)
        essence_super_plombe_ticpe = menage('essence_super_plombe_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_super_plombe_hors_tva = cout_essence_super_plombe_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_super_plombe_ht = Cout_essence_super_plombe_hors_tva - essence_super_plombe_ticpe
        return cout_essence_super_plombe_ht

class cout_essence_essence_e85_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence e85 ht"
    definition_period = YEAR
    default_value = 0

    def formula_2007(menage, period, parameters):
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc', period)
        essence_e85_ticpe = menage('essence_e85_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_essence_e85_hors_tva = cout_essence_e85_ttc * (1 / (1 + taux_plein_tva) )
        cout_essence_e85_ht = Cout_essence_e85_hors_tva - essence_e85_ticpe
        return cout_essence_e85_ht

# cout essence total ht:

class cout_essence_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les types d'essences cumulés"
    definition_period = YEAR

    def formula_2009(menage, period):
        cout_essence_SP95_ht = menage('cout_essence_SP95_ht', period)
        cout_essence_SP98_ht = menage('cout_essence_SP98_ht', period)
        cout_essence_essence_e85_ht = menage('cout_essence_essence_e85_ht', period)
        cout_essence_sp95_e10_ht = menage('cout_essence_sp95_e10_ht', period)
        cout_essence_total_ht = (cout_essence_SP95_ht + cout_essence_SP98_ht + cout_essence_essence_e85_ht + cout_essence_sp95_e10_ht)
        return cout_essence_total_ht

    def formula_2007(menage, period):
        cout_essence_SP95_ht = menage('cout_essence_SP95_ht', period)
        cout_essence_SP98_ht = menage('cout_essence_SP98_ht', period)
        cout_essence_essence_e85_ht = menage('cout_essence_essence_e85_ht', period)
        cout_essence_total_ht = (cout_essence_SP95_ht + cout_essence_SP98_ht + cout_essence_essence_e85_ht)
        return cout_essence_total_ht

    def formula_1990(menage, period):
        cout_essence_SP95_ht = menage('cout_essence_SP95_ht', period)
        cout_essence_SP98_ht = menage('cout_essence_SP98_ht', period)
        cout_essence_super_plombe_ht = menage('cout_essence_super_plombe_ht', period)
        cout_essence_total_ht = (cout_essence_SP95_ht + cout_essence_SP98_ht + cout_essence_super_plombe_ht)
        return cout_essence_total_ht

# cout gaz de pétrole liquéfié carburant ht:

class cout_gpl_carburant_ht(Variable):
    value_type = float
    entity = Menage
    label = "cout du gaz de pétrole liquéfié - carburant ht"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        cout_gpl_carburant_ttc = menage('cout_gpl_carburant_ttc', period)
        gpl_carburant_ticpe = menage('gpl_carburant_ticpe', period)
        taux_plein_tva = parameters(period).imposition_indirecte.tva.taux_de_tva.taux_normal
        Cout_gpl_carburant_hors_tva = cout_gpl_carburant_ttc * (1 / (1 + taux_plein_tva) )
        cout_gpl_carburant_ht = Cout_gpl_carburant_hors_tva - gpl_carburant_ticpe
        return cout_gpl_carburant_ht

# cout carburant total:
class cout_carburant_total_ht(Variable):
    value_type = float
    entity = Menage
    label = "Calcul du montant de la TICPE sur tous les carburants cumulés"
    definition_period = YEAR

    def formula(menage, period):
        cout_essence_total_ht = menage('cout_essence_total_ht', period)
        cout_gazole_total_ht = menage('cout_gazole_total_ht', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ht', period)
        cout_carburant_total_ht = cout_gazole_total_ht + cout_essence_total_ht + cout_gpl_carburant_ht
        return cout_carburant_total_ht