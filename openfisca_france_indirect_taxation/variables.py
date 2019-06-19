# -*- coding: utf-8 -*-


from openfisca_core.model_api import Variable
from openfisca_core.periods import YEAR


class YearlyVariable(Variable):
    def __init__(self, baseline_variable = None):
        self.__class__.definition_period = YEAR
        Variable.__init__(self, baseline_variable = None)

