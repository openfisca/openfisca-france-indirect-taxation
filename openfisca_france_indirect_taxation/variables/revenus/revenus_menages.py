# -*- coding: utf-8 -*-


import numpy

from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class Deciles(Enum):
    __order__ = 'hors_champs decile_1 decile_2 decile_3 decile_4 decile_5 decile_6 decile_7 decile_8 decile_9 decile_10'  # Needed to keep the order in Python 2
    hors_champs = "Hors champ"
    decile_1 = "1er décile"
    decile_2 = "2nd décile"
    decile_3 = "3e décile"
    decile_4 = "4e décile"
    decile_5 = "5e décile"
    decile_6 = "6e décile"
    decile_7 = "7e décile"
    decile_8 = "8e décile"
    decile_9 = "9e décile"
    decile_10 = "10e décile"


class decuc(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Décile de niveau de vie (revenu/unité de consommation)"


class niveau_de_vie(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Revenus disponibles divisés par ocde10 soit le nombre d'unités de consommation du ménage"

    def formula(menage, period):
        rev_disponible = menage('rev_disponible', period)
        ocde10 = menage('ocde10', period)
        return rev_disponible / ocde10


class niveau_vie_decile(YearlyVariable):
    value_type = Enum
    default_value = Deciles.hors_champs
    possible_values = Deciles
    entity = Menage
    label = "Décile de niveau de vie"

    def formula(menage, period):
        niveau_de_vie = menage('niveau_de_vie', period)
        pondmen = menage('pondmen', period)
        labels = numpy.arange(1, 11)
        # Alternative method
        # method = 2
        # niveau_vie_decile, values = mark_weighted_percentiles(
        # niveau_de_vie, labels, pondmen, method, return_quantiles = True)
        niveau_vie_decile, values = weighted_quantiles(niveau_de_vie, labels, pondmen, return_quantiles = True)
        return niveau_vie_decile


class loyer_impute(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Loyer imputé du ménage"

class rev_apres_loyer(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Revenu disponible du ménage auquel on retranche le loyer (pas le loyer imputé)"

    def formula(menage, period):
        revenu_disponible = menage('rev_disponible', period)
        loyer = menage('poste_04_1_1_1_1', period)

        rev_apres_loyer = revenu_disponible - loyer

        return rev_apres_loyer


class rev_disp_yc_loyerimpute(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Revenu disponible du ménage auquel on ajoute le loyer imputé"


class rev_disponible(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Revenu disponible du ménage"


class revdecm(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Revenu déclaré du ménage (imputé à partir de l'ERFS)"


class revtot(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Revenu total du ménage"


class revtotuc(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Revenu total par unité de consommation du ménage"
