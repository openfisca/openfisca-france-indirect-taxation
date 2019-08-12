# -*- coding: utf-8 -*-

import logging
import numpy


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


class depenses_carburants(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation de carburants"

    def formula(menage, period):
        return menage('poste_07_2_2_1_1', period)


class depenses_carburants_corrigees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation en carburants corrigees après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    def formula_2011(menage, period):
        depenses_carburants_corrigees = menage('depenses_carburants_corrigees_entd', period)
        return depenses_carburants_corrigees

    def formula(menage, period):
        depenses_carburants_corrigees = menage('depenses_carburants', period)
        return depenses_carburants_corrigees


class depenses_carburants_corrigees_entd(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation de carburants corrigees après appariement ENTD"


class depenses_combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en combustibles liquides"

    def formula(menage, period):
        depenses_combustibles_liquides = menage('poste_04_5_3_1_1', period)

        return depenses_combustibles_liquides


class depenses_combustibles_solides(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en combustibles solides"

    def formula(menage, period):
        depenses_combustibles_solides = menage('poste_04_5_4_1_1', period)

        return depenses_combustibles_solides


class depenses_diesel(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par pondération des dépenses spécifiques au diesel"

    def formula(menage, period, parameters):
        conso_totale_vp_diesel = parameters(period.start).quantite_carbu_vp.diesel
        conso_totale_vp_essence = parameters(period.start).quantite_carbu_vp.essence
        taille_parc_diesel = parameters(period.start).parc_vp.diesel
        taille_parc_essence = parameters(period.start).parc_vp.essence

        conso_moyenne_vp_diesel = conso_totale_vp_diesel / taille_parc_diesel
        conso_moyenne_vp_essence = conso_totale_vp_essence / taille_parc_essence

        nombre_vehicules_diesel = menage('veh_diesel', period)
        nombre_vehicules_essence = menage('veh_essence', period)
        nombre_vehicules_total = nombre_vehicules_diesel + nombre_vehicules_essence

        # to compute part_conso_diesel we need to avoid dividing by zero for those we do not have any vehicle
        # Thus, we choose arbitrarily to divide it by 1, but this choice won't affect the result as long as it is not 0
        denominateur = (
            (nombre_vehicules_diesel * conso_moyenne_vp_diesel) + (nombre_vehicules_essence * conso_moyenne_vp_essence)
            ) * (nombre_vehicules_total != 0) + 1 * (nombre_vehicules_total == 0)

        part_conso_diesel = (nombre_vehicules_diesel * conso_moyenne_vp_diesel) / denominateur

        depenses_carburants = menage('depenses_carburants', period)

        depenses_diesel = depenses_carburants * (
            (nombre_vehicules_total == 0) * (
                conso_totale_vp_diesel / (conso_totale_vp_diesel + conso_totale_vp_essence)
                )
            + (nombre_vehicules_total != 0) * part_conso_diesel
            )

        return depenses_diesel


class depenses_diesel_corrigees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation en diesel corrigees après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    def formula_2011(menage, period):
        depenses_diesel_corrigees = menage('depenses_diesel_corrigees_entd', period)
        return depenses_diesel_corrigees

    def formula(menage, period):
        depenses_diesel_corrigees = menage('depenses_diesel', period)
        return depenses_diesel_corrigees


class depenses_diesel_corrigees_entd(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation en diesel corrigees après appariement ENTD"


class depenses_diesel_htva(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en diesel htva (mais incluant toujours la TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_diesel = menage('depenses_diesel_corrigees', period)
        depenses_diesel_htva = depenses_diesel - tax_from_expense_including_tax(depenses_diesel, taux_plein_tva)

        return depenses_diesel_htva


class depenses_diesel_ht(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en diesel ht (prix brut sans TVA ni TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except Exception:
            accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

        prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva))
            / (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_htva = menage('depenses_diesel_htva', period)
        depenses_diesel_ht = \
            depenses_diesel_htva - tax_from_expense_including_tax(depenses_diesel_htva, taux_implicite_diesel)

        return depenses_diesel_ht


class depenses_diesel_recalculees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en diesel recalculées à partir du prix ht"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_diesel_ht = menage('depenses_diesel_ht', period)

        try:
            majoration_ticpe_diesel = \
                parameters(period.start).imposition_indirecte.major_regionale_ticpe_gazole.alsace
            accise_diesel = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole
            accise_diesel_ticpe = accise_diesel + majoration_ticpe_diesel
        except Exception:
            accise_diesel_ticpe = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.gazole

        prix_diesel_ttc = parameters(period.start).prix_carburants.diesel_ttc
        taux_implicite_diesel = (
            (accise_diesel_ticpe * (1 + taux_plein_tva))
            / (prix_diesel_ttc - accise_diesel_ticpe * (1 + taux_plein_tva))
            )

        depenses_diesel_recalculees = depenses_diesel_ht * (1 + taux_plein_tva) * (1 + taux_implicite_diesel)

        return depenses_diesel_recalculees


class depenses_electricite(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité totale après imputation factures jointes"

    def formula(menage, period):
        depenses_electricite_seule = menage('depenses_electricite_seule', period)
        depenses_electricite_factures_jointes = menage('depenses_electricite_factures_jointes', period)
        depenses_electricite = depenses_electricite_seule + depenses_electricite_factures_jointes

        return depenses_electricite


class depenses_electricite_factures_jointes(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité estimées des factures jointes électricité et gaz"

    def formula(menage, period):
        depenses_factures_jointes = menage('poste_04_5_1_1_1_a', period)

        depenses_electricite_seule = menage('depenses_electricite_seule', period)
        depenses_gaz_seul = menage('depenses_gaz_seul', period)
        depenses_gaz_elec = (depenses_electricite_seule * depenses_gaz_seul) > 0

        moyenne_elec = numpy.mean(depenses_electricite_seule * depenses_gaz_elec)
        moyenne_gaz = numpy.mean(depenses_gaz_seul * depenses_gaz_elec)
        part_elec = moyenne_elec / (moyenne_elec + moyenne_gaz)

        depenses_electricite_factures_jointes = depenses_factures_jointes * part_elec

        return depenses_electricite_factures_jointes


class depenses_electricite_percentile(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Classement par percentile des dépenses d'électricité"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_electricite_rank = depenses_electricite.argsort().argsort()
        depenses_electricite_percentile = depenses_electricite_rank / len(depenses_electricite_rank) * 100

        return depenses_electricite_percentile


class depenses_electricite_prix_unitaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Prix unitaire de l'électricité de chaque ménage, après affectation d'un compteur"

    def formula(menage, period, parameters):
        depenses_electricite_percentile = menage('depenses_electricite_percentile', period)

        # Note : les barèmes ne donnent que les prix unitaires pour 3 et 6 kva. Pour les puissances supérieures,
        # les valeurs sont assez proches de celles du compteur 6kva que nous utilisons comme proxy.
        prix_unitaire_3kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_3_kva
        prix_unitaire_6kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.prix_unitaire_base_edf_ttc.prix_kwh_6_kva

        prix_unitaire = (
            (depenses_electricite_percentile < 4) * prix_unitaire_3kva
            + (depenses_electricite_percentile > 4) * prix_unitaire_6kva
            )

        return prix_unitaire


class depenses_electricite_seule(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(menage, period):
        depenses_electricite_seule = menage('poste_04_5_1_1_1_b', period)

        return depenses_electricite_seule


class depenses_electricite_tarif_fixe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité des ménages sur le coût fixe de l'abonnement, après affectation d'un compteur"

    def formula(menage, period, parameters):
        depenses_electricite_percentile = menage('depenses_electricite_percentile', period)

        tarif_fixe_3kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_3_kva
        tarif_fixe_6kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_6_kva
        tarif_fixe_9kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_9_kva
        tarif_fixe_12kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_12_kva
        tarif_fixe_15kva = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_edf.tarif_fixe_base_edf_ttc.tarif_fixe_15_kva

        tarif_fixe = (
            (depenses_electricite_percentile < 4) * tarif_fixe_3kva
            + (depenses_electricite_percentile > 4) * (depenses_electricite_percentile < 52) * tarif_fixe_6kva
            + (depenses_electricite_percentile > 52) * (depenses_electricite_percentile < 78) * tarif_fixe_9kva
            + (depenses_electricite_percentile > 78) * (depenses_electricite_percentile < 88) * tarif_fixe_12kva
            + (depenses_electricite_percentile > 88) * tarif_fixe_15kva
            )

        return tarif_fixe


class depenses_electricite_variables(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité des ménages, hors coût fixe de l'abonnement"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_electricite_tarif_fixe = menage('depenses_electricite_tarif_fixe', period)
        depenses_electricite_variables = depenses_electricite - depenses_electricite_tarif_fixe
        depenses_electricite_variables = numpy.maximum(depenses_electricite_variables, 0)

        return depenses_electricite_variables


class depenses_energies_logement(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        depenses_gaz_ville = menage('depenses_gaz_ville', period)
        depenses_gaz_liquefie = menage('depenses_gaz_liquefie', period)
        depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
        depenses_combustibles_solides = menage('depenses_combustibles_solides', period)
        depenses_energie_thermique = menage('depenses_energie_thermique', period)
        depenses_energies_logement = (
            depenses_electricite + depenses_gaz_ville + depenses_gaz_liquefie + depenses_combustibles_liquides
            + depenses_combustibles_solides + depenses_energie_thermique
            )

        return depenses_energies_logement


class depenses_energie_thermique(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en énergie thermique"

    def formula(menage, period):
        depenses_energie_thermique = menage('poste_04_5_5_1_1', period)

        return depenses_energie_thermique


class depenses_energies_totales(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en électricité sans inclure dépenses jointes avec le gaz"

    def formula(menage, period):
        depenses_energies_logement = menage('depenses_energies_logement', period)
        depenses_carburants = menage('depenses_carburants_corrigees', period)
        depenses_energies_totales = (
            depenses_energies_logement + depenses_carburants
            )

        return depenses_energies_totales


class depenses_essence(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par déduction des dépenses spécifiques à l'essence"

    def formula(menage, period):
        depenses_carburants = menage('depenses_carburants', period)
        depenses_diesel = menage('depenses_diesel', period)
        depenses_essence = depenses_carburants - depenses_diesel

        return depenses_essence


class depenses_essence_corrigees(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation en essence corrigées après appariement ENTD pour 2011 seulement"
    definition_period = YEAR

    # def formula_2011(menage, period):
    #     depenses_essence_corrigees = menage('depenses_essence_corrigees_entd', period)
    #     return depenses_essence_corrigees

    def formula(menage, period):
        depenses_essence_corrigees = menage('depenses_essence', period)
        return depenses_essence_corrigees


class depenses_essence_corrigees_entd(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Consommation en essence corrigées après appariement ENTD"


class depenses_essence_ht(Variable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence hors taxes (HT, i.e. sans TVA ni TICPE)"
    definition_period = YEAR

    def formula_2009(menage, period):
        depenses_sp_95_ht = menage('depenses_sp_95_ht', period)
        depenses_sp_98_ht = menage('depenses_sp_98_ht', period)
        depenses_sp_e10_ht = menage('depenses_sp_e10_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_sp_e10_ht)
        return depenses_essence_ht

    def formula_2007(menage, period):
        depenses_sp_95_ht = menage('depenses_sp_95_ht', period)
        depenses_sp_98_ht = menage('depenses_sp_98_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht)
        return depenses_essence_ht

    def formula_1990(menage, period):
        depenses_sp_95_ht = menage('depenses_sp_95_ht', period)
        depenses_sp_98_ht = menage('depenses_sp_98_ht', period)
        depenses_super_plombe_ht = menage('depenses_super_plombe_ht', period)
        depenses_essence_ht = (depenses_sp_95_ht + depenses_sp_98_ht + depenses_super_plombe_ht)
        return depenses_essence_ht


class depenses_gaz_factures_jointes(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz estimées des factures jointes électricité et gaz"

    def formula(menage, period):
        depenses_factures_jointes = menage('poste_04_5_1_1_1_a', period)
        depenses_electricite_factures_jointes = menage('depenses_electricite_factures_jointes', period)
        depenses_gaz_factures_jointes = depenses_factures_jointes - depenses_electricite_factures_jointes

        return depenses_gaz_factures_jointes


class depenses_gaz_liquefie(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz liquéfié"

    def formula(menage, period):
        depenses_gaz_liquefie = menage('poste_04_5_2_2_1', period)

        return depenses_gaz_liquefie


class depenses_gaz_prix_unitaire(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Prix unitaire du gaz rencontré par les ménages"

    def formula(menage, period, parameters):
        quantite_base = menage('quantites_gaz_contrat_base', period)
        quantite_b0 = menage('quantites_gaz_contrat_b0', period)
        quantite_b1 = menage('quantites_gaz_contrat_b1', period)
        quantite_b2i = menage('quantites_gaz_contrat_b2i', period)
        quantite_optimale = menage('quantites_gaz_contrat_optimal', period)

        prix_unitaire_base = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        prix_unitaire_b0 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        prix_unitaire_b1 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc
        prix_unitaire_b2i = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.prix_unitaire_gdf_ttc.prix_kwh_b2i_ttc

        prix_unitaire_optimal = (
            (quantite_base == quantite_optimale) * prix_unitaire_base
            + (quantite_b0 == quantite_optimale) * prix_unitaire_b0
            + (quantite_b1 == quantite_optimale) * prix_unitaire_b1
            + (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * prix_unitaire_b2i
            )

        return prix_unitaire_optimal


class depenses_gaz_seul(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz de ville"

    def formula(menage, period):
        depenses_gaz_seul = menage('poste_04_5_2_1_1', period)

        return depenses_gaz_seul


class depenses_gaz_tarif_fixe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz des ménages sur le coût fixe de l'abonnement"

    def formula(menage, period, parameters):
        quantite_base = menage('quantites_gaz_contrat_base', period)
        quantite_b0 = menage('quantites_gaz_contrat_b0', period)
        quantite_b1 = menage('quantites_gaz_contrat_b1', period)
        quantite_b2i = menage('quantites_gaz_contrat_b2i', period)
        quantite_optimale = menage('quantites_gaz_contrat_optimal', period)

        tarif_fixe_base = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.base_0_1000
        tarif_fixe_b0 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b0_1000_6000
        tarif_fixe_b1 = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b1_6_30000
        tarif_fixe_b2i = \
            parameters(period.start).tarifs_energie.tarifs_reglementes_gdf.tarif_fixe_gdf_ttc.b2i_30000

        tarif_fixe_optimal = (
            (quantite_base == quantite_optimale) * tarif_fixe_base
            + (quantite_b0 == quantite_optimale) * tarif_fixe_b0
            + (quantite_b1 == quantite_optimale) * tarif_fixe_b1
            + (quantite_b2i == quantite_optimale) * (quantite_b1 != quantite_optimale) * tarif_fixe_b2i
            )

        return tarif_fixe_optimal


class depenses_gaz_variables(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz des ménages, hors coût fixe de l'abonnement"

    def formula(menage, period):
        depenses_gaz = menage('depenses_gaz_ville', period)
        tarif_fixe = menage('depenses_gaz_tarif_fixe', period)

        depenses_gaz_variables = depenses_gaz - tarif_fixe
        depenses_gaz_variables = numpy.maximum(depenses_gaz_variables, 0)

        return depenses_gaz_variables


class depenses_gaz_ville(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en gaz estimées des factures jointes électricité et gaz"

    def formula(menage, period):
        depenses_gaz_seul = menage('depenses_gaz_seul', period)
        depenses_gaz_factures_jointes = menage('depenses_gaz_factures_jointes', period)
        depenses_gaz_ville = depenses_gaz_seul + depenses_gaz_factures_jointes

        return depenses_gaz_ville


class depenses_sp_e10(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par pondération des dépenses spécifiques au sans plomb e10"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10

        return depenses_sp_e10


class depenses_sp_e10_ht(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence sans plomb e10 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp_e10 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_e10
        depenses_sp_e10 = depenses_essence * part_sp_e10
        depenses_sp_e10_htva = depenses_sp_e10 - tax_from_expense_including_tax(depenses_sp_e10, taux_plein_tva)
        try:
            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10
            majoration_ticpe_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super_e10 = accise_super_e10 + majoration_ticpe_super_e10
        except Exception:
            accise_super_e10 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_e10

        super_95_e10_ttc = parameters(period.start).prix_carburants.super_95_e10_ttc
        taux_implicite_sp_e10 = (
            (accise_ticpe_super_e10 * (1 + taux_plein_tva))
            / (super_95_e10_ttc - accise_ticpe_super_e10 * (1 + taux_plein_tva))
            )
        depenses_sp_e10_ht = \
            depenses_sp_e10_htva - tax_from_expense_including_tax(depenses_sp_e10_htva, taux_implicite_sp_e10)

        return depenses_sp_e10_ht


class depenses_sp_95(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par pondération des dépenses spécifiques au sans plomb 95"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95

        return depenses_sp_95


class depenses_sp_95_ht(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence sans plomb 95 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            accise_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super95 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super95 = accise_super95 + majoration_ticpe_super95
        except Exception as e:
            log.debug(e)
            accise_ticpe_super95 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        super_95_ttc = parameters(period.start).prix_carburants.super_95_ttc
        taux_implicite_sp95 = (
            (accise_ticpe_super95 * (1 + taux_plein_tva))
            / (super_95_ttc - accise_ticpe_super95 * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp95 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_95
        depenses_sp_95 = depenses_essence * part_sp95
        depenses_sp_95_htva = depenses_sp_95 - tax_from_expense_including_tax(depenses_sp_95, taux_plein_tva)
        depenses_sp_95_ht = \
            depenses_sp_95_htva - tax_from_expense_including_tax(depenses_sp_95_htva, taux_implicite_sp95)

        return depenses_sp_95_ht


class depenses_sp_98(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par pondération des dépenses spécifiques au sans plomb 98"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98

        return depenses_sp_98


class depenses_sp_98_ht(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence sans plomb 98 hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal

        try:
            accise_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98
            majoration_ticpe_super98 = \
                parameters(period.start).imposition_indirecte.produits_energetiques.major_regionale_ticpe_super.alsace
            accise_ticpe_super98 = accise_super98 + majoration_ticpe_super98
        except Exception:
            accise_ticpe_super98 = parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_95_98

        super_98_ttc = parameters(period.start).prix_carburants.super_98_ttc
        taux_implicite_sp98 = (
            (accise_ticpe_super98 * (1 + taux_plein_tva))
            / (super_98_ttc - accise_ticpe_super98 * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_sp98 = parameters(period.start).imposition_indirecte.part_type_supercarburants.sp_98
        depenses_sp_98 = depenses_essence * part_sp98
        depenses_sp_98_htva = depenses_sp_98 - tax_from_expense_including_tax(depenses_sp_98, taux_plein_tva)
        depenses_sp_98_ht = \
            depenses_sp_98_htva - tax_from_expense_including_tax(depenses_sp_98_htva, taux_implicite_sp98)

        return depenses_sp_98_ht


class depenses_super_plombe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Construction par pondération des dépenses spécifiques au super plombe"

    def formula(menage, period, parameters):
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_super_plombe = \
            parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe

        return depenses_super_plombe


class depenses_super_plombe_ht(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Dépenses en essence super plombée hors taxes (HT, i.e. sans TVA ni TICPE)"

    def formula(menage, period, parameters):
        taux_plein_tva = parameters(period.start).imposition_indirecte.tva.taux_de_tva.taux_normal
        accise_super_plombe_ticpe = \
            parameters(period.start).imposition_indirecte.produits_energetiques.ticpe.super_plombe
        super_plombe_ttc = parameters(period.start).prix_carburants.super_plombe_ttc
        taux_implicite_super_plombe = (
            (accise_super_plombe_ticpe * (1 + taux_plein_tva))
            / (super_plombe_ttc - accise_super_plombe_ticpe * (1 + taux_plein_tva))
            )
        depenses_essence = menage('depenses_essence_corrigees', period)
        part_super_plombe = \
            parameters(period.start).imposition_indirecte.part_type_supercarburants.super_plombe
        depenses_super_plombe = depenses_essence * part_super_plombe
        depenses_super_plombe_htva = \
            depenses_super_plombe - tax_from_expense_including_tax(depenses_super_plombe, taux_plein_tva)
        depenses_super_plombe_ht = (depenses_super_plombe_htva
- tax_from_expense_including_tax(depenses_super_plombe_htva, taux_implicite_super_plombe))

        return depenses_super_plombe_ht


class combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = "=1 si le menage consomme des combustibles liquides"

    def formula(menage, period):
        depenses_combustibles_liquides = menage('depenses_combustibles_liquides', period)
        combustibles_liquides = 1 * (depenses_combustibles_liquides > 0)

        return combustibles_liquides


class electricite(YearlyVariable):
    value_type = float
    entity = Menage
    label = "=1 si le menage consomme de l'électricité"

    def formula(menage, period):
        depenses_electricite = menage('depenses_electricite', period)
        electricite = 1 * (depenses_electricite > 0)

        return electricite


class gaz_ville(YearlyVariable):
    value_type = float
    entity = Menage
    label = "=1 si le menage consomme du gaz"

    def formula(menage, period):
        depenses_gaz_ville = menage('depenses_gaz_ville', period)
        gaz_ville = 1 * (depenses_gaz_ville > 0)

        return gaz_ville
