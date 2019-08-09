# -*- coding: utf-8 -*-


from openfisca_core import reforms
from openfisca_core.parameters import ParameterNode


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'taxes_carburants',
        name = "Réforme de l'imposition indirecte des carburants",
        use_baseline =tax_benefit_system,
        )

    reform = Reform()
    reform.modify_parameters(modifier_function = modify_parameters)
    return reform

# Cette réforme consiste en un rattrapage de la fiscalité du diesel sur celle de l'essence. Les valeurs imputées
# correspondent donc à la différence entre la fiscalité des deux carburants à ces dates.


def modify_parameters(parameters):
    node = ParameterNode(
        'taxes_carburants',
        data = {
            "description": "taxes_carburants",
            "diesel": {
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                "unit": 'currency',
                "values": {
                    '2010-01-01': 17.85,
                    '2015-01-01': 15.59,
                    '2016-01-01': 15.31,
                    },
                },
            },
        )
    parameters.add_child('taxes_carburants', node)
    return parameters
