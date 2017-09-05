# -*- coding: utf-8 -*-


from __future__ import division


import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class age(YearlyVariable):
    column = AgeCol
    entity = Individu
    label = u"Age de l'individu"

    def formula(self, simulation, period):
        birth = simulation.calculate('birth', period)
        return (numpy.datetime64(period.date) - birth).astype('timedelta64[Y]')


class agepr(YearlyVariable):
    column = AgeCol
    entity = Individu
    label = u"Age personne de référence"


class age_group_pr(YearlyVariable):
    column = AgeCol
    entity = Menage
    label = u"Groupe d'âge personne de référence"

    def formula(self, simulation, period):
        age_group_pr = 0
        agepr = simulation.calculate('agepr', period)
        age_group_pr = (
            1 * (agepr < 30) +
            2 * (agepr < 40) * (agepr > 29) +
            3 * (agepr < 50) * (agepr > 39) +
            4 * (agepr < 60) * (agepr > 49) +
            5 * (agepr < 70) * (agepr > 59) +
            6 * (agepr > 69)
            )

        return age_group_pr


class birth(YearlyVariable):
    column = DateCol
    entity = Individu
    label = u"Date de naissance"


class nactifs(YearlyVariable):
    column = IntCol
    entity = Menage
    label = u"Nombre d'actifs dans le ménage"


class nadultes(YearlyVariable):
    column = IntCol
    entity = Individu
    label = u"Nombre d'adultes dans le ménage"


class nenfants(YearlyVariable):
    column = IntCol
    entity = Individu
    label = u"Nombre d'enfants dans le ménage"


class role_menage(YearlyVariable):
    column = IntCol
    entity = Individu
    label = u"Rôle dans le ménage"
