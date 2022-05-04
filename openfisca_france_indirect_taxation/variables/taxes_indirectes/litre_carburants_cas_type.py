from openfisca_france_indirect_taxation.variables.base import Menage
from openfisca_france_indirect_taxation.yearly_variable import YearlyVariable

## caracteristiques menages

class region(YearlyVariable):
    value_type = str
    entity = Menage
    label = "region du menage"


## nombre litres diesel

class nombre_litres_diesel(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de diesel consommés par le menage"
    default_value = 0

## nombre litres essence

class nombre_litres_sp_e10(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super e10 consommés par le menage"
    default_value = 0

class nombre_litres_sp_95(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super 95 consommés par le menage"
    default_value = 0

class nombre_litres_sp_98(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super 98 consommés par le menage"
    default_value = 0

class nombre_litres_super_plombe(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de super plombé consommés par le menage"
    default_value = 0

## nombre litres combustibles liquides

class nombre_litres_combustibles_liquides(YearlyVariable):
    value_type = float
    entity = Menage
    label = "nombre de litres de combustibles liquides consommés par le menage"
    default_value = 0
