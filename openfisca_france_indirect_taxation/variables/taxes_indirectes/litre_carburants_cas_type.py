from openfisca_france_indirect_taxation.variables.base import Menage, Variable, YEAR
#from openfisca_france_indirect_taxation.yearly_variable import YearlyVariable

## caracteristiques menages

class region(Variable):
    value_type = str
    entity = Menage
    label = "region du menage"
    definition_period = YEAR


## nombre litres diesel

class nombre_litres_diesel(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de diesel consommés par le menage"
    definition_period = YEAR
    default_value = 0

## nombre litres essence

class nombre_litres_sp_e10(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super e10 consommés par le menage"
    definition_period = YEAR
    default_value = 0

class nombre_litres_sp_95(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super 95 consommés par le menage"
    definition_period = YEAR
    default_value = 0

class nombre_litres_sp_98(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super 98 consommés par le menage"
    definition_period = YEAR
    default_value = 0

class nombre_litres_super_plombe(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super plombé consommés par le menage"
    definition_period = YEAR
    default_value = 0

## nombre litres combustibles liquides

class nombre_litres_combustibles_liquides(Variable):
    value_type = float
    entity = Menage
    label = "nombre de litres de combustibles liquides consommés par le menage"
    definition_period = YEAR
    default_value = 0
