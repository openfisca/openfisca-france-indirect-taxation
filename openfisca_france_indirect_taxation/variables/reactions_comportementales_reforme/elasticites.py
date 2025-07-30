# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class elas_exp_1(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité dépense carburants'


class elas_exp_2(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité dépense énergie logement'


class elas_exp_3(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité dépense autres biens non durables'

class elas_ext(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Elasticité prix du carburants à la marge extensive"
    
    
class elas_price_1_1(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix carburants'


class elas_price_1_2(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée carburants - énergie logement'


class elas_price_1_3(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée carburants - autres biens non durables'


class elas_price_2_1(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée énergie logement - carburants'


class elas_price_2_2(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix énergie logement'


class elas_price_2_3(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée énergie logement - autres biens non durables'


class elas_price_3_1(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée autres biens non durables - carburants'


class elas_price_3_2(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix croisée autres biens non durables - énergie logement'


class elas_price_3_3(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Elasticité prix autres biens non durables'
