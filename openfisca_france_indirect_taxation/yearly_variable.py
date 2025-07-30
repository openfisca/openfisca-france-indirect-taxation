# -*- coding: utf-8 -*-


from openfisca_core.model_api import Variable
from openfisca_core.periods import YEAR


class YearlyVariable(Variable):
    def __init__(self, baseline_variable = None):
        self.__class__.definition_period = YEAR
        try:
            delattr(self.__class__, 'baseline_variable')
        except AttributeError:
            pass
        else:
            print(('deleting class baseline_variable for {}'.format(self.__class__.__name__)))

        try:
            delattr(self, 'baseline_variable')
        except AttributeError:
            pass
        else:
            print(('deleting instance baseline_variable for {}'.format(self.__class__.__name__)))

        Variable.__init__(self, baseline_variable = baseline_variable)
