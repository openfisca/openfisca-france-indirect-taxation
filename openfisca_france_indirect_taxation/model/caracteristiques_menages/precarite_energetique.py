# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class cmu(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage touche la couverture maladie universelle complémentaire "


class brde_m2_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"bas revenu (depenses tot )dépenses élevées (énergies logement)"

    def formula(self, simulation, period):
        depenses_tot = simulation.calculate('depenses_tot', period)
        uc = simulation.calculate('ocde10', period)
        depenses_tot_uc = depenses_tot / uc
        mediane_depenses_tot_uc = np.median(depenses_tot_uc)
        bas_revenu = 1 * (depenses_tot_uc < 0.6 * mediane_depenses_tot_uc)

        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        surface = simulation.calculate('surfhab_d', period)
        depenses_surface = depenses_energies_logement / surface
        mediane_depenses_surface = np.median(depenses_surface)
        depenses_elevees = 1 * (depenses_surface > mediane_depenses_surface)

        brde = bas_revenu * depenses_elevees

        return brde


class brde_m2_rev_disponible(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"bas revenu (revenu disponible) dépenses élevées (énergies logement)"

    def formula(self, simulation, period):
        revenu = simulation.calculate('rev_disponible', period)
        uc = simulation.calculate('ocde10', period)
        revenu_uc = revenu / uc
        mediane_revenu_uc = np.median(revenu_uc)
        bas_revenu = 1 * (revenu_uc < 0.6 * mediane_revenu_uc)

        depenses_energies_logement = simulation.calculate('depenses_carburants_corrigees', period)
        surface = simulation.calculate('surfhab_d', period)
        depenses_surface = depenses_energies_logement / surface
        mediane_depenses_surface = np.median(depenses_surface)
        depenses_elevees = 1 * (depenses_surface > mediane_depenses_surface)

        brde = bas_revenu * depenses_elevees

        return brde


class brde_transports_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"bas revenu (depenses tot) dépenses élevées (en carburants)"

    def formula(self, simulation, period):
        depenses_tot = simulation.calculate('depenses_tot', period)
        uc = simulation.calculate('ocde10', period)
        depenses_tot_uc = depenses_tot / uc
        mediane_depenses_tot_uc = np.median(depenses_tot_uc)
        bas_revenu = 1 * (depenses_tot_uc < 0.6 * mediane_depenses_tot_uc)

        # Médiane ou médiane parmi ceux conduisant ?
        depenses_carburants = simulation.calculate('depenses_carburants_corrigees', period)
        mediane_depenses_carburants = np.median(depenses_carburants)
        depenses_elevees = 1 * (depenses_carburants > mediane_depenses_carburants)

        brde = bas_revenu * depenses_elevees

        return brde


class brde_transports_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"bas revenu (revenu disponible) dépenses élevées (en carburants)"

    def formula(self, simulation, period):
        revenu = simulation.calculate('rev_disponible', period)
        uc = simulation.calculate('ocde10', period)
        revenu_uc = revenu / uc
        mediane_revenu_uc = np.median(revenu_uc)
        bas_revenu = 1 * (revenu_uc < 0.6 * mediane_revenu_uc)

        # Médiane ou médiane parmi ceux conduisant ?
        depenses_carburants = simulation.calculate('depenses_carburants_corrigees', period)
        mediane_depenses_carburants = np.median(depenses_carburants)
        depenses_elevees = 1 * (depenses_carburants > mediane_depenses_carburants)

        brde = bas_revenu * depenses_elevees

        return brde


# critère basé sur les barèmes d'éligibilité à la CMU-C en utilisant le revenu fiscal.
# Le revenu pris en compte est normalement différent mais le nombre de ménages bénéficiaires est le même.
class eligibilite_tarifs_sociaux_energies(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage est éligible aux tarifs sociaux de l'énergie"

    def formula(self, simulation, period):
        revenu = simulation.calculate('revdecm', period)
        npers = simulation.calculate('npers', period)

        eligible = (
            1 * (revenu < 8653) * (npers == 1) +
            1 * (revenu < 12980) * (npers == 2) +
            1 * (revenu < 15576) * (npers == 3) +
            1 * (revenu < 18172 + ((npers - 4) * 3461.26)) * ((npers == 4) + (npers > 4))
            )

        return eligible


class froid(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver"


class froid_cout(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison du cout du chauffage"


class froid_impaye(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une coupure pour facture impayée"


class froid_installation(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une installation insuffisante"


class froid_isolation(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une mauvaise isolation"


class froid_4_criteres(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver - 4 critères"

    def formula(self, simulation, period):
        froid_cout = simulation.calculate('froid_cout', period)
        froid_impaye = simulation.calculate('froid_impaye', period)
        froid_installation = simulation.calculate('froid_installation', period)
        froid_isolation = simulation.calculate('froid_isolation', period)

        somme_4_criteres = froid_cout + froid_impaye + froid_installation + froid_isolation
        froid_4_criteres = 1 * (somme_4_criteres != 0)

        return froid_4_criteres


class froid_4_criteres_3_deciles(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver - 4 critères, 3 deciles"

    def formula(self, simulation, period):
        froid_4_criteres = simulation.calculate('froid_4_criteres', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        froid_4_criteres_3_deciles = froid_4_criteres * (nvd < 4)

        return froid_4_criteres_3_deciles


class froid_3_deciles(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement - 3 premiers déciles"

    def formula(self, simulation, period):
        froid = simulation.calculate('froid', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        froid_3_deciles = froid * (nvd < 4)

        return froid_3_deciles


class precarite_energetique_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_m2 = simulation.calculate('brde_m2_depenses_tot', period)
        froid_4_criteres_3_deciles = simulation.calculate('froid_4_criteres_3_deciles', period)
        tee_10_3_deciles = simulation.calculate('tee_10_3_deciles_depenses_tot', period)

        somme_3_indicateurs = brde_m2 + froid_4_criteres_3_deciles + tee_10_3_deciles
        precarite_energetique_3_indicateurs = 1 * (somme_3_indicateurs != 0)

        return precarite_energetique_3_indicateurs


class precarite_energetique_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_m2 = simulation.calculate('brde_m2_rev_disponible', period)
        froid_4_criteres_3_deciles = simulation.calculate('froid_4_criteres_3_deciles', period)
        tee_10_3_deciles = simulation.calculate('tee_10_3_deciles_rev_disponible', period)

        somme_3_indicateurs = brde_m2 + froid_4_criteres_3_deciles + tee_10_3_deciles
        precarite_energetique_3_indicateurs = 1 * (somme_3_indicateurs != 0)

        return precarite_energetique_3_indicateurs


class precarite_transports_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_transports_depenses_tot = simulation.calculate('brde_transports_depenses_tot', period)
        tee_transports_10_3_deciles_depenses_tot = simulation.calculate('tee_transports_10_3_deciles_depenses_tot', period)

        somme_3_indicateurs = brde_transports_depenses_tot + tee_transports_10_3_deciles_depenses_tot
        precarite_transports = 1 * (somme_3_indicateurs != 0)

        return precarite_transports


class precarite_transports_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_transports_rev_disponible = simulation.calculate('brde_transports_rev_disponible', period)
        tee_transports_10_3_deciles_rev_disponible = simulation.calculate('tee_transports_10_3_deciles_rev_disponible', period)

        somme_3_indicateurs = brde_transports_rev_disponible + tee_transports_10_3_deciles_rev_disponible
        precarite_transports = 1 * (somme_3_indicateurs != 0)

        return precarite_transports


class tarifs_sociaux_electricite(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Montant perçus en tarifs sociaux sur l'électricité (TPN)"

    def formula(self, simulation, period):
        depenses_electricite_percentile = simulation.calculate('depenses_electricite_percentile', period)
        eligible = simulation.calculate('eligibilite_tarifs_sociaux_energies', period)
        uc = simulation.calculate('ocde10', period)
        uc_1 = 1 * (uc == 1)
        uc_1_2 = 1 * (uc > 1) * (uc < 2)
        uc_2 = 1 * ((uc == 2) + (uc > 2))
        kva_3 = 1 * (depenses_electricite_percentile < 4)
        kva_6 = 1 * (depenses_electricite_percentile > 4) * (depenses_electricite_percentile < 52)
        kva_9 = 1 * (depenses_electricite_percentile > 52)
        tarifs_sociaux = eligible * (
            kva_3 * (uc_1 * 71 + uc_1_2 * 88 + uc_2 * 106) +
            kva_6 * (uc_1 * 87 + uc_1_2 * 109 + uc_2 * 131) +
            kva_9 * (uc_1 * 94 + uc_1_2 * 117 + uc_2 * 140)
            )

        depenses_electricite = simulation.calculate('depenses_electricite', period)
        tarifs_sociaux = (
            tarifs_sociaux * (tarifs_sociaux < depenses_electricite) +
            depenses_electricite * (tarifs_sociaux > depenses_electricite)
            ) * eligible

        return tarifs_sociaux


class tarifs_sociaux_gaz(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Montant perçus en tarifs sociaux sur l'électricité (TSS)"

    def formula(self, simulation, period):
        depenses_gaz_prix_unitaire = simulation.calculate('depenses_gaz_prix_unitaire', period)
        prix_unitaire_base = \
            parameters(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_base_ttc
        prix_unitaire_b0 = \
            parameters(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b0_ttc
        prix_unitaire_b1 = \
            parameters(period.start).tarification_energie_logement.prix_unitaire_gdf_ttc.prix_kwh_b1_ttc

        eligible = simulation.calculate('eligibilite_tarifs_sociaux_energies', period)
        uc = simulation.calculate('ocde10', period)
        uc_1 = 1 * (uc == 1)
        uc_1_2 = 1 * (uc > 1) * (uc < 2)
        uc_2 = 1 * ((uc == 2) + (uc > 2))
        base = 1 * (depenses_gaz_prix_unitaire == prix_unitaire_base)
        b0 = 1 * (depenses_gaz_prix_unitaire == prix_unitaire_b0)
        b1 = 1 * (depenses_gaz_prix_unitaire == prix_unitaire_b1)
        tarifs_sociaux = eligible * (
            base * (uc_1 * 23 + uc_1_2 * 30 + uc_2 * 38) +
            b0 * (uc_1 * 72 + uc_1_2 * 95 + uc_2 * 117) +
            b1 * (uc_1 * 123 + uc_1_2 * 153 + uc_2 * 185)
            )

        depenses_gaz_ville = simulation.calculate('depenses_gaz_ville', period)
        tarifs_sociaux = (
            tarifs_sociaux * (tarifs_sociaux < depenses_gaz_ville) +
            depenses_gaz_ville * (tarifs_sociaux > depenses_gaz_ville)
            ) * eligible

        return tarifs_sociaux


class tee_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        depenses_tot = simulation.calculate('depenses_tot', period)

        tee = depenses_energies_logement / depenses_tot

        return tee


class tee_10_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_depenses_tot', period)
        tee_10 = (tee > 0.1) * 1

        return tee_10


class tee_10_3_deciles_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_depenses_tot', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1

        return tee_10_3_deciles


class tee_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        rev_disponible = simulation.calculate('rev_disponible', period)

        tee = depenses_energies_logement / rev_disponible

        return tee


class tee_10_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_rev_disponible', period)
        tee_10 = (tee > 0.1) * 1

        return tee_10


class tee_10_3_deciles_rev_disponible(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_rev_disponible', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1

        return tee_10_3_deciles


class tee_transports_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_carburants = simulation.calculate('depenses_carburants_corrigees', period)
        depenses_tot = simulation.calculate('depenses_tot', period)

        tee = depenses_carburants / depenses_tot

        return tee


class tee_transports_10_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_depenses_tot', period)
        tee_10 = (tee > 0.1) * 1

        return tee_10


class tee_transports_10_3_deciles_depenses_tot(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_depenses_tot', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1

        return tee_10_3_deciles


class tee_transports_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_carburants_corrigees', period)
        rev_disponible = simulation.calculate('rev_disponible', period)

        tee = depenses_energies_logement / rev_disponible

        return tee


class tee_transports_10_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_rev_disponible', period)
        tee_10 = (tee > 0.1) * 1

        return tee_10


class tee_transports_10_3_deciles_rev_disponible(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_rev_disponible', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1

        return tee_10_3_deciles
