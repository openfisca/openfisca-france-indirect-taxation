# -*- coding: utf-8 -*-


from openfisca_core.model_api import Variable, YEAR


class YearlyVariable(Variable):
    def __init__(self, name, attributes, variable_class):
        self.name = name
        self.attributes = attributes
        self.attributes['definition_period'] = YEAR
        self.variable_class = variable_class
        Variable.__init__(self, self.name, self.attributes, self.variable_class)


