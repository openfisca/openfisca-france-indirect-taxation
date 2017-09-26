# -*- coding: utf-8 -*-

from __future__ import division

import numpy as np

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class brde_m2(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"bas revenu dépenses élevées"

    def formula(self, simulation, period):
        revenu = simulation.calculate('rev_apres_loyer', period)
        uc = simulation.calculate('ocde10', period)
        revenu_uc = revenu / uc
        mediane_revenu_uc = np.median(revenu_uc)
        bas_revenu = 1 * (revenu_uc < 0.6 * mediane_revenu_uc)
        
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        surface = simulation.calculate('surfhab_d', period)
        depenses_surface = depenses_energies_logement / surface
        mediane_depenses_surface = np.median(depenses_surface)
        depenses_elevees = 1 * (depenses_surface > mediane_depenses_surface)
        
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


class precarite_energetique_3_indicateurs(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        brde_m2 = simulation.calculate('brde_m2', period)
        froid_4_criteres_3_deciles = simulation.calculate('froid_4_criteres_3_deciles', period)
        tee_10_3_deciles = simulation.calculate('tee_10_3_deciles', period)
        
        somme_3_indicateurs = brde_m2 + froid_4_criteres_3_deciles + tee_10_3_deciles
        precarite_energetique_3_indicateurs = 1 * (somme_3_indicateurs != 0)
        
        return precarite_energetique_3_indicateurs


# Revenu ou revenu par uc ? Loyer imputé ou non ? revtot ou rev disp ? Ou les dépenses ?
class tee(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Taux d'effort énergétique du ménage pour le logement, en fonction du revenu disponible"

    def formula(self, simulation, period):
        depenses_energies_logement = simulation.calculate('depenses_energies_logement', period)
        revenu_disponible = simulation.calculate('depenses_tot', period)
        
        tee = depenses_energies_logement / revenu_disponible
        
        return tee


class tee_10(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10%"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee', period)
        tee_10 = (tee > 0.1) * 1
        
        return tee_10


class tee_10_3_deciles(YearlyVariable):
    column = StrCol
    entity = Menage
    label = u"Indicateur, taux d'effort énergétique supérieur à 10% et 3 premiers déciles"

    def formula(self, simulation, period):
        tee = simulation.calculate('tee', period)
        nvd = simulation.calculate('niveau_vie_decile', period)
        tee_10_3_deciles = (tee > 0.1) * (nvd < 4) * 1
        
        return tee_10_3_deciles
