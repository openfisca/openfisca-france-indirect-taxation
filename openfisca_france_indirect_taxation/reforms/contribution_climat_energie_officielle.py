# -*- coding: utf-8 -*-


from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'contribution_climat_energie_officielle',
        name = "Réforme telle que prévue par la loi",
        use_baseline =tax_benefit_system,
        )

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform

# Montants de taxe prévus par la loi Contribution climat-énergie. 7€ en 2014, 14,5€ en 2015, 22€ en 2016,
# 30,5€ en 2017, 39€ en 2018 et 47.5€ en 2019 En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :
# Todo : voir comment on met en place cette réforme sachant qu'elle est déjà partiellement entrée dans les prix.


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "contribution_climat_energie_officielle",
        "children": {
            "diesel": {
                "@type": "Parameter",
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': '2014-01-01', 'stop': '2014-12-31', 'value': 1.862},
                    {'start': '2015-01-01', 'stop': '2015-12-31', 'value': 3.857},
                    {'start': '2016-01-01', 'stop': '2016-12-31', 'value': 5.852},
                    {'start': '2017-01-01', 'stop': '2017-12-31', 'value': 8.113},
                    {'start': '2018-01-01', 'stop': '2018-12-31', 'value': 10.374},
                    {'start': '2019-01-01', 'stop': '2019-12-31', 'value': 12.635},
                    ],
                },
            "essence": {
                "@type": "Parameter",
                "description": "Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [
                    {'start': '2014-01-01', 'stop': '2014-12-31', 'value': 1.694},
                    {'start': '2015-01-01', 'stop': '2015-12-31', 'value': 3.509},
                    {'start': '2016-01-01', 'stop': '2016-12-31', 'value': 5.324},
                    {'start': '2017-01-01', 'stop': '2017-12-31', 'value': 7.381},
                    {'start': '2018-01-01', 'stop': '2018-12-31', 'value': 9.438},
                    {'start': '2019-01-01', 'stop': '2019-12-31', 'value': 11.495},
                    ],
                },
            "fioul_domestique": {
                "@type": "Parameter",
                "description": "Surcroît de prix du fioul domestique (en euros par litre)",
                "format": "float",
                "unit": 'currency',
                "values": [
                    {'start': '2014-01-01', 'stop': '2014-12-31', 'value': 0.0217},
                    {'start': '2015-01-01', 'stop': '2015-12-31', 'value': 0.04495},
                    {'start': '2016-01-01', 'stop': '2016-12-31', 'value': 0.0682},
                    {'start': '2017-01-01', 'stop': '2017-12-31', 'value': 0.09455},
                    {'start': '2018-01-01', 'stop': '2018-12-31', 'value': 0.1209},
                    {'start': '2019-01-01', 'stop': '2019-12-31', 'value': 0.14725},
                    ],
                },
            "gaz": {
                "@type": "Parameter",
                "description": "Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': '2014-01-01', 'stop': '2014-12-31', 'value': 0.00168},
                    {'start': '2015-01-01', 'stop': '2015-12-31', 'value': 0.00348},
                    {'start': '2016-01-01', 'stop': '2016-12-31', 'value': 0.00528},
                    {'start': '2017-01-01', 'stop': '2017-12-31', 'value': 0.00732},
                    {'start': '2018-01-01', 'stop': '2018-12-31', 'value': 0.00936},
                    {'start': '2019-01-01', 'stop': '2019-12-31', 'value': 0.0114},
                    ],
                },
            },
        }

    reference_legislation_json_copy['children']['contribution_climat_energie_officielle'] = reform_legislation_subtree
    return reference_legislation_json_copy
