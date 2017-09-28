# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class brde_m2_depenses_tot(YearlyVariable):
    column = StrCol
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
    column = StrCol
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
    column = StrCol
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
    column = StrCol
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


class froid(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver"


class froid_cout(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison du cout du chauffage"


class froid_impaye(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une coupure pour facture impayée"


class froid_installation(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une installation insuffisante"


class froid_isolation(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver en raison d'une mauvaise isolation"


class froid_4_criteres(YearlyVariable):
    column = StrCol
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
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement pendant l'hiver - 4 critères, 3 deciles"

    def formula(self, simulation, period):
        froid_4_criteres = simulation.calculate('froid_4_criteres', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        froid_4_criteres_3_deciles = froid_4_criteres * (nvd < 4)
        
        return froid_4_criteres_3_deciles


class froid_3_deciles(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Le ménage a éprouvé un sentiment de froid dans son logement - 3 premiers déciles"

    def formula(self, simulation, period):
        froid = simulation.calculate('froid', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        froid_3_deciles = froid * (nvd < 4)
        
        return froid_3_deciles


class precarite_energetique_depenses_tot(YearlyVariable):
    column = StrCol
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
    column = StrCol
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
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_transports_depenses_tot = simulation.calculate('brde_transports_depenses_tot', period)
        tee_transports_10_3_deciles_depenses_tot = simulation.calculate('tee_transports_10_3_deciles_depenses_tot', period)
        
        somme_3_indicateurs = brde_transports_depenses_tot + tee_transports_10_3_deciles_depenses_tot
        precarite_transports = 1 * (somme_3_indicateurs != 0)
        
        return precarite_transports


class precarite_transports_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_transports_rev_disponible = simulation.calculate('brde_transports_rev_disponible', period)
        tee_transports_10_3_deciles_rev_disponible = simulation.calculate('tee_transports_10_3_deciles_rev_disponible', period)
        
        somme_3_indicateurs = brde_transports_rev_disponible + tee_transports_10_3_deciles_rev_disponible
        precarite_transports = 1 * (somme_3_indicateurs != 0)
        
        return precarite_transports


class tee_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        depenses_tot = simulation.calculate('depenses_tot', period)
        
        tee = depenses_energies_logement / depenses_tot
        
        return tee


class tee_10_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_depenses_tot', period)
        tee_10 = (tee > 0.1) * 1
        
        return tee_10


class tee_10_3_deciles_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_depenses_tot', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1
        
        return tee_10_3_deciles


class tee_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        rev_disponible = simulation.calculate('rev_disponible', period)
        
        tee = depenses_energies_logement / rev_disponible
        
        return tee


class tee_10_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_rev_disponible', period)
        tee_10 = (tee > 0.1) * 1
        
        return tee_10


class tee_10_3_deciles_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_rev_disponible', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1
        
        return tee_10_3_deciles

								
class tee_transports_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_carburants = simulation.calculate('depenses_carburants_corrigees', period)
        depenses_tot = simulation.calculate('depenses_tot', period)
        
        tee = depenses_carburants / depenses_tot
        
        return tee


class tee_transports_10_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_depenses_tot', period)
        tee_10 = (tee > 0.1) * 1
        
        return tee_10


class tee_transports_10_3_deciles_depenses_tot(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_depenses_tot', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1
        
        return tee_10_3_deciles


class tee_transports_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_carburants_corrigees', period)
        rev_disponible = simulation.calculate('rev_disponible', period)
        
        tee = depenses_energies_logement / rev_disponible
        
        return tee


class tee_transports_10_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_rev_disponible', period)
        tee_10 = (tee > 0.1) * 1
        
        return tee_10


class tee_transports_10_3_deciles_rev_disponible(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee_transports_rev_disponible', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1
        
        return tee_10_3_deciles
