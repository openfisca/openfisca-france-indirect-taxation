# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore
import numpy



class depenses_carburants(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation de carburants"

    def formula(self, simulation, period):
        return simulation.calculate('poste_07_2_2_1_1', period)


class depenses_carburants_corrigees(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation en carburants corrigees après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    def formula_2011(self, simulation, period):
        depenses_carburants_corrigees = simulation.calculate('depenses_carburants_corrigees_entd', period)
        return depenses_carburants_corrigees
    
    def formula(self, simulation, period):
        depenses_carburants_corrigees = simulation.calculate('depenses_carburants', period)
        return depenses_carburants_corrigees


class depenses_carburants_corrigees_entd(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation de carburants corrigees après appariement ENTD"


class depenses_combustibles_liquides(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en combustibles liquides"

    def formula(self, simulation, period):
        depenses_combustibles_liquides = simulation.calculate('poste_04_5_3_1_1', period)

        return depenses_combustibles_liquides


class depenses_combustibles_solides(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en combustibles solides"

    def formula(self, simulation, period):
        depenses_combustibles_solides = simulation.calculate('poste_04_5_4_1_1', period)

        return depenses_combustibles_solides


class depenses_diesel(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au diesel"

    def formula(self, simulation, period):
        conso_totale_vp_diesel = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.diesel
        conso_totale_vp_essence = simulation.legislation_at(period.start).imposition_indirecte.quantite_carbu_vp.essence
        taille_parc_diesel = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.diesel
        taille_parc_essence = simulation.legislation_at(period.start).imposition_indirecte.parc_vp.essence

        conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
        conso_moyenne_vp_essence = conso_totale_vp_essence / taille_parc_essence

        nombre_vehicules_diesel = simulation.calculate('veh_diesel', period)
        nombre_vehicules_essence = simulation.calculate('veh_essence', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_diesel * conso_moyenne_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_vp_essence)
            ) * (nombre_vehicules_total != 0) + 1 * (nombre_vehicules_total == 0)

        part_conso_diesel = (nombre_vehicules_diesel * conso_moyenne_vp_diesel) / denominateur

        depenses_carburants = simulation.calculate('depenses_carburants', period)

        depenses_diesel = depenses_carburants * (
            (nombre_vehicules_total == 0) * (
                conso_totale_vp_diesel / (conso_totale_vp_diesel + conso_totale_vp_essence)
                ) +
            (nombre_vehicules_total != 0) * part_conso_diesel
            )

        return depenses_diesel


class depenses_diesel_corrigees(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation en diesel corrigees après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    def formula_2011(self, simulation, period):
        depenses_diesel_corrigees = simulation.calculate('depenses_diesel_corrigees_entd', period)
        return depenses_diesel_corrigees
    
    def formula(self, simulation, period):
        depenses_diesel_corrigees = simulation.calculate('depenses_diesel', period)
        return depenses_diesel_corrigees


class depenses_diesel_corrigees_entd(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation en diesel corrigees après appariement ENTD"


class depenses_diesel_htva(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en diesel htva (mais incluant toujours la TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel = simulation.calculate('depenses_diesel_corrigees', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)

        return depenses_diesel_htva


class depenses_diesel_ht(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en diesel ht (prix brut sans TVA ni TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_htva = simulation.calculate('depenses_diesel_htva', period)
        depenses_diesel_ht = \
            depenses_diesel_htva - tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return depenses_diesel_ht


class depenses_diesel_recalculees(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en diesel recalculées à partir du prix ht"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_diesel_ht = simulation.calculate('depenses_diesel_ht', period)

        try:
            majoration_ticpe_diesel = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except:
            accise_diesel_ticpe = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_gazole

        prix_diesel_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva)) /
            (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_recalculees = depenses_diesel_ht * (1 + taux_plein_tva) * (1 + taux_implicite_diesel)

        return depenses_diesel_recalculees


class depenses_electricite(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité totale après imputation factures jointes"

    def formula(self, simulation, period):
        depenses_electricite_seule = simulation.calculate('depenses_electricite_seule', period)
        depenses_electricite_factures_jointes = simulation.calculate('depenses_electricite_factures_jointes', period)
        depenses_electricite = depenses_electricite_seule + depenses_electricite_factures_jointes

        return depenses_electricite


class depenses_electricite_factures_jointes(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité estimées des factures jointes électricité et gaz"

    def formula(self, simulation, period):
        depenses_factures_jointes = simulation.calculate('poste_04_5_1_1_1_a', period)

        depenses_electricite_seule = simulation.calculate('depenses_electricite_seule', period)
        depenses_gaz_seul = simulation.calculate('depenses_gaz_seul', period)
        depenses_gaz_elec = (depenses_electricite_seule * depenses_gaz_seul) > 0      
        
        moyenne_elec = numpy.mean(depenses_electricite_seule * depenses_gaz_elec)
        moyenne_gaz = numpy.mean(depenses_gaz_seul * depenses_gaz_elec)
        part_elec = moyenne_elec / (moyenne_elec + moyenne_gaz)
        
        depenses_electricite_factures_jointes = depenses_factures_jointes * part_elec

        return depenses_electricite_factures_jointes


class depenses_electricite_percentile(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Classement par percentile des dépenses d'électricité"

    def formula(self, simulation, period):
        depenses_electricite = simulation.calculate('depenses_electricite', period)
        depenses_electricite_rank = depenses_electricite.argsort().argsort()
        depenses_electricite_percentile = depenses_electricite_rank / len(depenses_electricite_rank) * 100

        return depenses_electricite_percentile


class depenses_electricite_prix_unitaire(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Prix unitaire de l'électricité de chaque ménage, après affectation d'un compteur"

    def formula(self, simulation, period):
        depenses_electricite_percentile = simulation.calculate('depenses_electricite_percentile', period)

        # Note : les barèmes ne donnent que les prix unitaires pour 3 et 6 kva. Pour les puissances supérieures,
        # les valeurs sont assez proches de celles du compteur 6kva que nous utilisons comme proxy.
        prix_unitaire_3kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_3_kva
        prix_unitaire_6kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_base_edf_ttc.prix_du_kwh_6_kva

        prix_unitaire = (
            (depenses_electricite_percentile < 4) * prix_unitaire_3kva +
            (depenses_electricite_percentile > 4) * prix_unitaire_6kva
            )

        return prix_unitaire


class depenses_electricite_seule(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(self, simulation, period):
        depenses_electricite_seule = simulation.calculate('poste_04_5_1_1_1_b', period)

        return depenses_electricite_seule


class depenses_electricite_tarif_fixe(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité des ménages sur le coût fixe de l'abonnement, après affectation d'un compteur"

    def formula(self, simulation, period):
        depenses_electricite_percentile = simulation.calculate('depenses_electricite_percentile', period)

        tarif_fixe_3kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        tarif_fixe_6kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        tarif_fixe_9kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        tarif_fixe_12kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        tarif_fixe_15kva = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva

        tarif_fixe = (
            (depenses_electricite_percentile < 4) * tarif_fixe_3kva +
            (depenses_electricite_percentile > 4) * (depenses_electricite_percentile < 52) * tarif_fixe_6kva +
            (depenses_electricite_percentile > 52) * (depenses_electricite_percentile < 78) * tarif_fixe_9kva +
            (depenses_electricite_percentile > 78) * (depenses_electricite_percentile < 88) * tarif_fixe_12kva +
            (depenses_electricite_percentile > 88) * tarif_fixe_15kva
            )

        return tarif_fixe


class depenses_electricite_variables(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité des ménages, hors coût fixe de l'abonnement"

    def formula(self, simulation, period):
        depenses_electricite = simulation.calculate('depenses_electricite', period)
        depenses_electricite_tarif_fixe = simulation.calculate('depenses_electricite_tarif_fixe', period)
        depenses_electricite_variables = depenses_electricite - depenses_electricite_tarif_fixe
        depenses_electricite_variables = numpy.maximum(depenses_electricite_variables, 0)

        return depenses_electricite_variables


class depenses_energies_logement(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(self, simulation, period):
        depenses_electricite = simulation.calculate('depenses_electricite', period)
        depenses_gaz_ville = simulation.calculate('depenses_gaz_ville', period)
        depenses_gaz_liquefie = simulation.calculate('depenses_gaz_liquefie', period)
        depenses_combustibles_liquides = simulation.calculate('depenses_combustibles_liquides', period)
        depenses_combustibles_solides = simulation.calculate('depenses_combustibles_solides', period)
        depenses_energie_thermique = simulation.calculate('depenses_energie_thermique', period)
        depenses_energies_logement = (
            depenses_electricite + depenses_gaz_ville + depenses_gaz_liquefie + depenses_combustibles_liquides +
            depenses_combustibles_solides + depenses_energie_thermique
            )

        return depenses_energies_logement


class depenses_energie_thermique(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en énergie thermique"

    def formula(self, simulation, period):
        depenses_energie_thermique = simulation.calculate('poste_04_5_5_1_1', period)

        return depenses_energie_thermique


class depenses_energies_totales(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        depenses_carburants = simulation.calculate('depenses_carburants_corrigees', period)
        depenses_energies_totales = (
            depenses_energies_logement + depenses_carburants
            )

        return depenses_energies_totales


class depenses_essence(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par déduction des dépenses spécifiques à l'essence"

    def formula(self, simulation, period):
        depenses_carburants = simulation.calculate('depenses_carburants', period)
        depenses_diesel = simulation.calculate('depenses_diesel', period)
        depenses_essence = depenses_carburants - depenses_diesel

        return depenses_essence


class depenses_essence_corrigees(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation en essence corrigees après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    def formula_2011(self, simulation, period):
        depenses_essence_corrigees = simulation.calculate('depenses_essence_corrigees_entd', period)
        return depenses_essence_corrigees
    
    def formula(self, simulation, period):
        depenses_essence_corrigees = simulation.calculate('depenses_essence', period)
        return depenses_essence_corrigees


class depenses_essence_corrigees_entd(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Consommation en essence corrigees après appariement ENTD"


class depenses_essence_ht(Variable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence hors taxes (HT, i.e. sans TVA ni TICPE)"
    definition_period = YEAR

    def formula_2009(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_sp_e10_ht = simulation.calculate('depenses_sp_e10_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_sp_e10_ht)
        return depenses_essence_ht

    def formula_2007(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht)
        return depenses_essence_ht

    def formula_1990(self, simulation, period):
        depenses_sp_95_ht = simulation.calculate('depenses_sp_95_ht', period)
        depenses_sp_98_ht = simulation.calculate('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = simulation.calculate('depenses_super_plombe_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_super_plombe_ht)
        return depenses_essence_ht


class depenses_gaz_factures_jointes(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz estimées des factures jointes électricité et gaz"

    def formula(self, simulation, period):
        depenses_factures_jointes = simulation.calculate('poste_04_5_1_1_1_a', period)
        depenses_electricite_factures_jointes = simulation.calculate('depenses_electricite_factures_jointes', period)
        depenses_gaz_factures_jointes = depenses_factures_jointes - depenses_electricite_factures_jointes
 
        return depenses_gaz_factures_jointes


class depenses_gaz_liquefie(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz liquéfié"

    def formula(self, simulation, period):
        depenses_gaz_liquefie = simulation.calculate('poste_04_5_2_2_1', period)

        return depenses_gaz_liquefie


class depenses_gaz_prix_unitaire(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Prix unitaire du gaz rencontré par les ménages"

    def formula(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale = simulation.calculate('quantites_gaz_contrat_optimal', period)

        prix_unitaire_base = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        prix_unitaire_b0 = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        prix_unitaire_b1 = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        prix_unitaire_b2i = \
            simulation.legislation_at(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc

        prix_unitaire_optimal = (
            (quantite_base == quantite_optimale) * prix_unitaire_base +
            (quantite_b0 == quantite_optimale) * prix_unitaire_b0 +
            (quantite_b1 == quantite_optimale) * prix_unitaire_b1 +
            (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * prix_unitaire_b2i
            )

        return prix_unitaire_optimal


class depenses_gaz_seul(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz de ville"

    def formula(self, simulation, period):
        depenses_gaz_seul = simulation.calculate('poste_04_5_2_1_1', period)

        return depenses_gaz_seul


class depenses_gaz_tarif_fixe(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz des ménages sur le coût fixe de l'abonnement"

    def formula(self, simulation, period):
        quantite_base = simulation.calculate('quantites_gaz_contrat_base', period)
        quantite_b0 = simulation.calculate('quantites_gaz_contrat_b0', period)
        quantite_b1 = simulation.calculate('quantites_gaz_contrat_b1', period)
        quantite_b2i = simulation.calculate('quantites_gaz_contrat_b2i', period)
        quantite_optimale = simulation.calculate('quantites_gaz_contrat_optimal', period)

        tarif_fixe_base = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.base_0_1000
        tarif_fixe_b0 = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b0_1000_6000
        tarif_fixe_b1 = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b1_6_30000
        tarif_fixe_b2i = \
            simulation.legislation_at(period.start).tarification_energie_logement.tarif_fixe_gdf_ttc.b2i_30000

        tarif_fixe_optimal = (
            (quantite_base == quantite_optimale) * tarif_fixe_base +
            (quantite_b0 == quantite_optimale) * tarif_fixe_b0 +
            (quantite_b1 == quantite_optimale) * tarif_fixe_b1 +
            (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * tarif_fixe_b2i
            )

        return tarif_fixe_optimal


class depenses_gaz_variables(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz des ménages, hors coût fixe de l'abonnement"

    def formula(self, simulation, period):
        depenses_gaz = simulation.calculate('depenses_gaz_ville', period)
        tarif_fixe = simulation.calculate('depenses_gaz_tarif_fixe', period)

        depenses_gaz_variables = depenses_gaz - tarif_fixe
        depenses_gaz_variables = numpy.maximum(depenses_gaz_variables, 0)

        return depenses_gaz_variables


class depenses_gaz_ville(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en gaz estimées des factures jointes électricité et gaz"

    def formula(self, simulation, period):
        depenses_gaz_seul = simulation.calculate('depenses_gaz_seul', period)
        depenses_gaz_factures_jointes = simulation.calculate('depenses_gaz_factures_jointes', period)
        depenses_gaz_ville = depenses_gaz_seul + depenses_gaz_factures_jointes
 
        return depenses_gaz_ville


class depenses_sp_e10(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb e10"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10

        return depenses_sp_e10


class depenses_sp_e10_ht(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence sans plomb e10 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp_e10 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        depenses_sp_e10_htva = depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)

        try:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10
            majoration_ticpe_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except:
            accise_super_e10 = \
                simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super_e10

        super_95_e10_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva)) /
            (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_sp_e10_ht = \
            depenses_sp_e10_htva - tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return depenses_sp_e10_ht


class depenses_sp_95(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 95"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95

        return depenses_sp_95


class depenses_sp_95_ht(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence sans plomb 95 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super95 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except:
            accise_ticpe_super95 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_95_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva)) /
            (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp95 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        depenses_sp_95_ht = \
            depenses_sp_95_htva - tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return depenses_sp_95_ht


class depenses_sp_98(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au sans plomb 98"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98

        return depenses_sp_98


class depenses_sp_98_ht(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence sans plomb 98 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein

        try:
            accise_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598
            majoration_ticpe_super98 = \
                simulation.legislation_at(period.start).imposition_indirecte.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except:
            accise_ticpe_super98 = simulation.legislation_at(period.start).imposition_indirecte.ticpe.ticpe_super9598

        super_98_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_98_ttc
        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva)) /
            (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_sp98 = simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        depenses_sp_98_ht = \
            depenses_sp_98_htva - tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return depenses_sp_98_ht


class depenses_super_plombe(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Construction par pondération des dépenses spécifiques au super plombe"

    def formula(self, simulation, period):
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe

        return depenses_super_plombe


class depenses_super_plombe_ht(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"Dépenses en essence super plombée hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(self, simulation, period):
        taux_plein_tva = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        accise_super_plombe_ticpe = \
            simulation.legislation_at(period.start).imposition_indirecte.ticpe.super_plombe_ticpe
        super_plombe_ttc = simulation.legislation_at(period.start).imposition_indirecte.prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva)) /
            (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_essence = simulation.calculate('depenses_essence_corrigees', period)
        part_super_plombe = \
            simulation.legislation_at(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        depenses_super_plombe_ht = (depenses_super_plombe_htva -
            tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe))

        return depenses_super_plombe_ht

        
class combustibles_liquides(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"=1 si le menage consomme des combustibles liquides"

    def formula(self, simulation, period):
        depenses_combustibles_liquides = simulation.calculate('depenses_combustibles_liquides', period)
        combustibles_liquides = 1 * (depenses_combustibles_liquides > 0)
        
        return combustibles_liquides
    
        
class electricite(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"=1 si le menage consomme de l'électricité"

    def formula(self, simulation, period):
        depenses_electricite = simulation.calculate('depenses_electricite', period)
        electricite = 1 * (depenses_electricite > 0)
        
        return electricite
        
    
class gaz_ville(YearlyVariable):
    column = FloatCol
    entity = Menage
    label = u"=1 si le menage consomme du gaz"

    def formula(self, simulation, period):
        depenses_gaz_ville = simulation.calculate('depenses_gaz_ville', period)
        gaz_ville = 1 * (depenses_gaz_ville > 0)
        
        return gaz_ville
        
        