from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
from openfisca_france_indirect_taxation.variables.prix_carburants_regions_years_AN import get_prix_carburant_par_region_par_carburant_par_an_hectolitre

import numpy as np

# cout different type de gazole ttc:
class cout_gazole_b7_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gazole B7 ttc'
    definition_period = YEAR
    default_value = 0

class cout_gazole_b10_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gazole B10 ttc'
    definition_period = YEAR
    default_value = 0

# cout different type d'essence ttc:

class cout_essence_sp95_e10_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp95 e10 ttc"
    definition_period = YEAR
    default_value = 0
class cout_essence_sp95_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp95 ttc"
    definition_period = YEAR
    default_value = 0

class cout_essence_sp98_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'escence sp98 ttc"
    definition_period = YEAR
    default_value = 0
class cout_essence_super_plombe_ttc_entree(Variable):  #ATTENTION: pas prix par région disponible, on garde les prix ttc général de l'IPP. (INSEE)
    value_type = float
    entity = Menage
    label = "cout de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"

class cout_essence_e85_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "cout de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0

# cout essence total ttc:

# cout gaz de pétrole liquéfié carburant ttc:

class cout_gpl_carburant_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'cout du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0
class cout_carburant_total_ttc_sans_distinction_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des couts sur tous les carburants cumulés ttc '
    definition_period = YEAR

    def formula_2017(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc_entree', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc_entree', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc_entree', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc_entree', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc_entree', period)
        cout_gazole_b10_ttc = menage('cout_gazole_b10_ttc_entree', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc_entree', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc +
         cout_essence_sp95_e10_ttc + cout_gazole_b7_ttc + cout_gazole_b10_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_2009(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc_entree', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc_entree', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc_entree', period)
        cout_essence_sp95_e10_ttc = menage('cout_essence_sp95_e10_ttc_entree', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc_entree', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc_entree', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc +
         cout_essence_sp95_e10_ttc + cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_2007(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc_entree', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc_entree', period)
        cout_essence_e85_ttc = menage('cout_essence_e85_ttc_entree', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc_entree', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc_entree', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_e85_ttc +
         cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc

    def formula_1990(menage, period):
        cout_essence_sp95_ttc = menage('cout_essence_sp95_ttc_entree', period)
        cout_essence_sp98_ttc = menage('cout_essence_sp98_ttc_entree', period)
        cout_essence_super_plombe_ttc = menage('cout_essence_super_plombe_ttc_entree', period)
        cout_gazole_b7_ttc = menage('cout_gazole_b7_ttc_entree', period)
        cout_gpl_carburant_ht = menage('cout_gpl_carburant_ttc_entree', period)
        cout_essence_total_ttc = (cout_essence_sp95_ttc + cout_essence_sp98_ttc + cout_essence_super_plombe_ttc +
         cout_gazole_b7_ttc + cout_gpl_carburant_ht)
        return cout_essence_total_ttc
