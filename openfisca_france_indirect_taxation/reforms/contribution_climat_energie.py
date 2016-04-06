# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'contribution_climat_energie',
        name = u"Réforme telle que prévue par la loi",
        reference = tax_benefit_system,
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
        "description": "contribution_climat_energie",
        "children": {
            "essence": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": "float",
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 1.694}],
                "values": [{'start': u'2015-01-01', 'stop': '2015-12-31', 'value': 3.509}],
                "values": [{'start': u'2016-01-01', 'stop': '2016-12-31', 'value': 5.324}],
                "values": [{'start': u'2017-01-01', 'stop': '2017-12-31', 'value': 7.381}],
                "values": [{'start': u'2018-01-01', 'stop': '2018-12-31', 'value': 9.438}],
                "values": [{'start': u'2019-01-01', 'stop': '2019-12-31', 'value': 11.495}],
                },
            "diesel": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 1.862}],
                "values": [{'start': u'2015-01-01', 'stop': '2015-12-31', 'value': 3.857}],
                "values": [{'start': u'2016-01-01', 'stop': '2016-12-31', 'value': 5.852}],
                "values": [{'start': u'2017-01-01', 'stop': '2017-12-31', 'value': 8.113}],
                "values": [{'start': u'2018-01-01', 'stop': '2018-12-31', 'value': 10.374}],
                "values": [{'start': u'2019-01-01', 'stop': '2019-12-31', 'value': 12.635}],
                },
            "gaz": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du gaz (en euros par kWh)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': u'2014-01-01', 'stop': '2014-12-31', 'value': 0.00168}],
                "values": [{'start': u'2015-01-01', 'stop': '2015-12-31', 'value': 0.00348}],
                "values": [{'start': u'2016-01-01', 'stop': '2016-12-31', 'value': 0.00528}],
                "values": [{'start': u'2017-01-01', 'stop': '2017-12-31', 'value': 0.00732}],
                "values": [{'start': u'2018-01-01', 'stop': '2018-12-31', 'value': 0.00936}],
                "values": [{'start': u'2019-01-01', 'stop': '2019-12-31', 'value': 0.0114}],
                },
            },
        }

    reference_legislation_json_copy['children']['contribution_climat_energie'] = reform_legislation_subtree
    return reference_legislation_json_copy
