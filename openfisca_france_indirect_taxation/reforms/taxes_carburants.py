# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'taxes_carburants',
        name = u"Réforme de l'imposition indirecte des carburants",
        reference = tax_benefit_system,
        )

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform

# Cette réforme consiste en un rattrapage de la fiscalité du diesel sur celle de l'essence. Les valeurs imputées
# correspondent donc à la différence entre la fiscalité des deux carburants à ces dates.

# On propose aussi deux réformes de redistribution : un abaissement de 1 point de TVA à taux plein, ou un abaissement
# de 0.5 point accompagné d'une baisse d'un point sur la TVA à taux réduit et super réduit. Ces redistributions sont
# telles que le budget doit être constant lorsqu'on simule sur les données 2011 inflatées pour 2014.


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "taxes_carburants",
        "children": {
            "diesel": {
                "@type": "Parameter",
                "description": u"Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2014-12-31', 'value': 17.85},
                    {'start': u'2015-01-01', 'stop': '2015-12-31', 'value': 15.59},
                    {'start': u'2016-01-01', 'stop': '2017-12-31', 'value': 15.31},
                    ],
                },
            "essence": {
                "@type": "Parameter",
                "description": u"Surcroît de prix de l'essence (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0},
                    ],
                },
            "abaissement_tva_taux_plein": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            "abaissement_tva_taux_plein_bis": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux plein pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.005},
                    ],
                },
            "abaissement_tva_taux_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux réduit pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            "abaissement_tva_taux_super_reduit": {
                "@type": "Parameter",
                "description": u"Baisse de la TVA à taux super réduit pour obtenir un budget constant",
                "format": 'float',
                "values": [
                    {'start': u'2010-01-01', 'stop': '2017-12-31', 'value': 0.01},
                    ],
                },
            },
        }

    reference_legislation_json_copy['children']['taxes_carburants'] = reform_legislation_subtree
    return reference_legislation_json_copy
