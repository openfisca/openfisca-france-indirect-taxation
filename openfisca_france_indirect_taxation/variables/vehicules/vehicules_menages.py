# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class pourcentage_vehicule_essence(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Pourcentage de véhicules essence dans le ménage"


class veh_diesel(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Nombre de véhicules diesel dans le ménage"


class veh_essence(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Nombre de véhicules essence dans le ménage"


class veh_tot(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Nombre de véhicules total dans le ménage"
