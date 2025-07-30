# -*- coding: utf-8 -*-

from openfisca_core.parameters import ParameterNode
from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'contribution_climat_energie',
        name = 'Réforme telle que prévue par la loi',
        use_baseline = tax_benefit_system,
        )

    reform = Reform()
    reform.modify_parameters(modifier_function = modify_parameters)
    return reform

# Montants de taxe prévus par la loi Contribution climat-énergie. 7€ en 2014, 14,5€ en 2015, 22€ en 2016,
# 30,5€ en 2017, 39€ en 2018 et 47.5€ en 2019 En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :
# Todo : voir comment on met en place cette réforme sachant qu'elle est déjà partiellement entrée dans les prix.


def modify_parameters(parameters):
    node = ParameterNode(
        'contribution_climat_energie',
        data = {
            'description': 'contribution_climat_energie',
            'essence': {
                'description': "Surcroît de prix de l'essence (en euros par hectolitres)",
                'unit': 'currency',
                'values': {
                    '2014-01-01': 1.694,
                    '2015-01-01': 3.509,
                    '2016-01-01': 5.324,
                    '2017-01-01': 7.381,
                    '2018-01-01': 9.438,
                    '2019-01-01': 11.495,
                    },
                },
            'diesel': {
                'description': 'Surcroît de prix du diesel (en euros par hectolitres)',
                'unit': 'currency',
                'values': {
                    '2014-01-01': 1.862,
                    '2015-01-01': 3.857,
                    '2016-01-01': 5.852,
                    '2017-01-01': 8.113,
                    '2018-01-01': 10.374,
                    '2019-01-01': 12.635,
                    },
                },
            'gaz': {
                'description': 'Surcroît de prix du gaz (en euros par kWh)',
                'unit': 'currency',
                'values': {
                    '2014-01-01': 0.00168,
                    '2015-01-01': 0.00348,
                    '2016-01-01': 0.00528,
                    '2017-01-01': 0.00732,
                    '2018-01-01': 0.00936,
                    '2019-01-01': 0.0114,
                    }
                }
            }
        )
    parameters.add_child('contribution_climat_energie', node)
    return parameters
