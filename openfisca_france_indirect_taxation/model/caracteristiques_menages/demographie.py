# -*- coding: utf-8 -*-


from __future__ import division


import numpy

from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class age(YearlyVariable):
    value_type = int
    entity = Individu
    label = u"Age de l'individu"

    def formula(individu, period):
        birth = individu('birth', period)
        return (numpy.datetime64(period.date) - birth).astype('timedelta64[Y]')


class agepr(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Age personne de référence"


class age_group_pr(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Groupe d'âge personne de référence"

    def formula(menage, period):
        age_group_pr = 0
        agepr = menage('agepr', period)
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
    value_type = date
    entity = Individu
    label = u"Date de naissance"


class nactifs(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Nombre d'actifs dans le ménage"


class nadultes(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Nombre d'adultes dans le ménage"


class nenfants(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Nombre d'enfants dans le ménage"


class npers(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Nombre de personnes dans le ménage"


class role_menage(YearlyVariable):
    value_type = int
    entity = Individu
    label = u"Rôle dans le ménage"
