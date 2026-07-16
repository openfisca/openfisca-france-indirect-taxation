from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore

class impot_revenu(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'impôt sur le revenu'