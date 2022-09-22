from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR

# depense different type de gazole ttc:


class depense_gazole_b7_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gazole B7 ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        part_depenses_B7 = 1.0
        depense_gazole_total_ttc_entree = menage('depense_gazole_total_ttc_entree', period)
        depense_gazole_b7_ttc_entree = depense_gazole_total_ttc_entree * part_depenses_B7
        return depense_gazole_b7_ttc_entree


class depense_gazole_b10_ttc_entree(Variable):  # Il n'y a pour le moment pas assez d'usages de ce carburant (et donc de données)
    value_type = float
    entity = Menage
    label = 'depense du gazole B10 ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period):
        part_depenses_B10 = 0.0
        depense_gazole_total_ttc_entree = menage('depense_gazole_total_ttc_entree', period)
        depense_gazole_b10_ttc_entree = depense_gazole_total_ttc_entree * part_depenses_B10
        return depense_gazole_b10_ttc_entree


# depense different type d'essence ttc:


class depense_essence_sp95_e10_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp95 e10 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        depense_essence_total_ttc_entree = menage('depense_essence_total_ttc_entree', period)
        sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depense_essence_sp95_e10_ttc_entree = depense_essence_total_ttc_entree * sp_e10
        return depense_essence_sp95_e10_ttc_entree


class depense_essence_sp95_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp95 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        depense_essence_total_ttc_entree = menage('depense_essence_total_ttc_entree', period)
        sp_95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depense_essence_sp95_ttc_entree = depense_essence_total_ttc_entree * sp_95
        return depense_essence_sp95_ttc_entree


class depense_essence_sp98_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "Dépense en essence sp98 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        depense_essence_total_ttc_entree = menage('depense_essence_total_ttc_entree', period)
        sp_98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depense_essence_sp98_ttc_entree = depense_essence_total_ttc_entree * sp_98
        return depense_essence_sp98_ttc_entree


class depense_essence_super_plombe_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence super plombé ttc"
    definition_period = YEAR
    default_value = 0
    end = "2007-01-01"

    def formula(menage, period, parameters):
        depense_essence_total_ttc_entree = menage('depense_essence_total_ttc_entree', period)
        super_plombe = parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depense_essence_super_plombe_ttc_entree = depense_essence_total_ttc_entree * super_plombe
        return depense_essence_super_plombe_ttc_entree


class depense_essence_e85_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = "depense de l'essence e85 ttc"
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        depense_essence_total_ttc_entree = menage('depense_essence_total_ttc_entree', period)
        sp_e85 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e85
        depense_essence_e85_ttc_entree = depense_essence_total_ttc_entree * sp_e85
        return depense_essence_e85_ttc_entree


# depense total ttc:


class depenses_carburants_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Consommation de carburants'
    definition_period = YEAR
    default_value = 0


class depense_gazole_total_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Construction par pondération des dépenses spécifiques au diesel'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        conso_moyenne_vp_diesel = parameters(period.start).conso_vp_moyenne.voitures_particulieres_diesel
        conso_moyenne_vp_essence = parameters(period.start).conso_vp_moyenne.voitures_particulieres_essence
        conso_moyenne_vp_gpl = parameters(period.start).conso_vp_moyenne.voitures_particulieres_gpl

        parcours_moyenne_vp_diesel_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_diesel
        parcours_moyenne_vp_essense_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_essence
        parcours_moyenne_vp_gpl_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_gpl

        conso_moyenne_du_parcours_moyen_vp_diesel = parcours_moyenne_vp_diesel_en_km * conso_moyenne_vp_diesel / 100
        conso_moyenne_du_parcours_moyen_vp_essence = parcours_moyenne_vp_essense_en_km * conso_moyenne_vp_essence / 100
        conso_moyenne_du_parcours_moyen_vp_gpl = parcours_moyenne_vp_gpl_en_km * conso_moyenne_vp_gpl / 100

        nombre_vehicules_diesel = menage('veh_diesel', period)
        nombre_vehicules_essence = menage('veh_essence', period)
        nombre_vehicules_gpl = menage('veh_gpl', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence + nombre_vehicules_gpl

        depenses_carburants = menage('depenses_carburants_entree', period)

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_total != 0) * (nombre_vehicules_diesel * conso_moyenne_du_parcours_moyen_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_du_parcours_moyen_vp_essence) + (nombre_vehicules_gpl * conso_moyenne_du_parcours_moyen_vp_gpl)
            ) + (nombre_vehicules_total == 0) * 1

        part_conso_gazole = (nombre_vehicules_diesel * conso_moyenne_du_parcours_moyen_vp_diesel) / denominateur

        depenses_gazole = depenses_carburants * part_conso_gazole
        return depenses_gazole


class depense_essence_total_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Construction par pondération des dépenses spécifiques au diesel'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        conso_moyenne_vp_diesel = parameters(period.start).conso_vp_moyenne.voitures_particulieres_diesel
        conso_moyenne_vp_essence = parameters(period.start).conso_vp_moyenne.voitures_particulieres_essence
        conso_moyenne_vp_gpl = parameters(period.start).conso_vp_moyenne.voitures_particulieres_gpl

        parcours_moyenne_vp_diesel_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_diesel
        parcours_moyenne_vp_essense_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_essence
        parcours_moyenne_vp_gpl_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_gpl

        conso_moyenne_du_parcours_moyen_vp_diesel = parcours_moyenne_vp_diesel_en_km * conso_moyenne_vp_diesel / 100
        conso_moyenne_du_parcours_moyen_vp_essence = parcours_moyenne_vp_essense_en_km * conso_moyenne_vp_essence / 100
        conso_moyenne_du_parcours_moyen_vp_gpl = parcours_moyenne_vp_gpl_en_km * conso_moyenne_vp_gpl / 100

        nombre_vehicules_diesel = menage('veh_diesel', period)
        nombre_vehicules_essence = menage('veh_essence', period)
        nombre_vehicules_gpl = menage('veh_gpl', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence + nombre_vehicules_gpl

        depenses_carburants = menage('depenses_carburants_entree', period)

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_total != 0) * (nombre_vehicules_diesel * conso_moyenne_du_parcours_moyen_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_du_parcours_moyen_vp_essence) + (nombre_vehicules_gpl * conso_moyenne_du_parcours_moyen_vp_gpl)
            ) + (nombre_vehicules_total == 0) * 1

        part_conso_essence = (nombre_vehicules_essence * conso_moyenne_du_parcours_moyen_vp_essence) / denominateur

        depenses_essence = depenses_carburants * part_conso_essence
        return depenses_essence

# depense gaz de pétrole liquéfié carburant ttc:


class depense_gpl_carburant_ttc_entree(Variable):
    value_type = float
    entity = Menage
    label = 'depense du gaz de pétrole liquéfié - carburant ttc'
    definition_period = YEAR
    default_value = 0

    def formula(menage, period, parameters):
        conso_moyenne_vp_diesel = parameters(period.start).conso_vp_moyenne.voitures_particulieres_diesel
        conso_moyenne_vp_essence = parameters(period.start).conso_vp_moyenne.voitures_particulieres_essence
        conso_moyenne_vp_gpl = parameters(period.start).conso_vp_moyenne.voitures_particulieres_gpl

        parcours_moyenne_vp_diesel_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_diesel
        parcours_moyenne_vp_essense_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_essence
        parcours_moyenne_vp_gpl_en_km = parameters(period.start).taille_parcours_moyen.voitures_particulieres_gpl

        conso_moyenne_du_parcours_moyen_vp_diesel = parcours_moyenne_vp_diesel_en_km * conso_moyenne_vp_diesel / 100
        conso_moyenne_du_parcours_moyen_vp_essence = parcours_moyenne_vp_essense_en_km * conso_moyenne_vp_essence / 100
        conso_moyenne_du_parcours_moyen_vp_gpl = parcours_moyenne_vp_gpl_en_km * conso_moyenne_vp_gpl / 100

        nombre_vehicules_diesel = menage('veh_diesel', period)
        nombre_vehicules_essence = menage('veh_essence', period)
        nombre_vehicules_gpl = menage('veh_gpl', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence + nombre_vehicules_gpl

        depenses_carburants = menage('depenses_carburants_entree', period)

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_total != 0) * (nombre_vehicules_diesel * conso_moyenne_du_parcours_moyen_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_du_parcours_moyen_vp_essence) + (nombre_vehicules_gpl * conso_moyenne_du_parcours_moyen_vp_gpl)
            ) + (nombre_vehicules_total == 0) * 1

        part_conso_gpl = (nombre_vehicules_gpl * conso_moyenne_du_parcours_moyen_vp_gpl) / denominateur

        depenses_gpl = depenses_carburants * part_conso_gpl
        return depenses_gpl


class depense_carburant_total_ttc_sans_distinction_entree(Variable):
    value_type = float
    entity = Menage
    label = 'Calcul du montant des depenses sur tous les carburants cumulés ttc '
    definition_period = YEAR

    def formula_2017(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gazole_b10_ttc = menage('depense_gazole_b10_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gazole_b10_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2009(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_essence_sp95_e10_ttc = menage('depense_essence_sp95_e10_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_essence_sp95_e10_ttc + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_2007(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_e85_ttc = menage('depense_essence_e85_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_e85_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc

    def formula_1990(menage, period):
        depense_essence_sp95_ttc = menage('depense_essence_sp95_ttc_entree', period)
        depense_essence_sp98_ttc = menage('depense_essence_sp98_ttc_entree', period)
        depense_essence_super_plombe_ttc = menage('depense_essence_super_plombe_ttc_entree', period)
        depense_gazole_b7_ttc = menage('depense_gazole_b7_ttc_entree', period)
        depense_gpl_carburant_ht = menage('depense_gpl_carburant_ttc_entree', period)
        depense_essence_total_ttc = (depense_essence_sp95_ttc + depense_essence_sp98_ttc + depense_essence_super_plombe_ttc
        + depense_gazole_b7_ttc + depense_gpl_carburant_ht)
        return depense_essence_total_ttc
