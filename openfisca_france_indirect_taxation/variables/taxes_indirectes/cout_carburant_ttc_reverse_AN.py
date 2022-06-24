from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
from openfisca_france_indirect_taxation.variables.prix_carburants_regions_years_AN import get_prix_carburant_par_region_par_carburant_par_an_hectolitre

class cout_gazole_total_ttc_reverse(Variable):
    value_type = float
    entity = Menage
    label = 'cout total du gazole ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gazole_total_ht = menage('cout_gazole_total_ht', period)
        gazole_ticpe_total = menage('gazole_ticpe_total', period)
        tva_sur_gazole_total = menage('tva_sur_gazole_total', period)
        cout_gazole_total_ttc_reverse = cout_gazole_total_ht + gazole_ticpe_total + tva_sur_gazole_total
        return cout_gazole_total_ttc_reverse

class cout_essence_total_ttc_reverse(Variable):
    value_type = float
    entity = Menage
    label = 'cout total du gpl ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_essence_total_ht = menage('tva_sur_gazole_total', period)
        essence_ticpe_total = menage('essence_ticpe_total', period)
        tva_sur_essence_total = menage('tva_sur_essence_total', period)
        cout_essence_total_ttc_reverse = cout_essence_total_ht + essence_ticpe_total + tva_sur_essence_total
        return cout_essence_total_ttc_reverse

class cout_gpl_carburant_ttc_reverse(Variable):
    value_type = float
    entity = Menage
    label = 'cout total du gpl ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        cout_gpl_carburant_ht = menage('gpl_carburant_ticpe', period)
        essence_ticpe_total = menage('essence_ticpe_total', period)
        tva_sur_gpl_carburant = menage('tva_sur_gpl_carburant', period)
        cout_essence_total_ttc_reverse = cout_gpl_carburant_ht + essence_ticpe_total + tva_sur_gpl_carburant
        return cout_essence_total_ttc_reverse

class cout_carburant_ttc_reverse(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des couts sur tous les carburants cumulés ttc'
    definition_period = YEAR

    def formula(menage, period):
        cout_gazole_total_ttc_reverse = menage('cout_gazole_total_ttc_reverse', period)
        cout_essence_total_ttc_reverse = menage('cout_essence_total_ttc_reverse', period)
        cout_gpl_carburant_ttc_reverse = menage('cout_gpl_carburant_ttc_reverse', period)
        cout_carburant_ttc_reverse = cout_gazole_total_ttc_reverse + cout_essence_total_ttc_reverse + cout_gpl_carburant_ttc_reverse
        return cout_carburant_ttc_reverse