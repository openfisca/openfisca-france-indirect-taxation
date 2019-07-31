# -*- coding: utf-8 -*-


from openfisca_core import reforms


def build_reform(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'taxes_carburants',
        name = "Réforme de l'imposition indirecte des carburants",
        use_baseline =tax_benefit_system,
        )

    reform = Reform()
    reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform

# Cette réforme consiste en un rattrapage de la fiscalité du diesel sur celle de l'essence. Les valeurs imputées
# correspondent donc à la différence entre la fiscalité des deux carburants à ces dates.


def modify_legislation_json(reference_legislation_json_copy):
    reform_legislation_subtree = {
        "@type": "Node",
        "description": "taxes_carburants",
        "children": {
            "diesel": {
                "@type": "Parameter",
                "description": "Surcroît de prix du diesel (en euros par hectolitres)",
                "format": 'float',
                "unit": 'currency',
                "values": [{'start': '2010-01-01', 'stop': '2014-12-31', 'value': 17.85}],
                "values": [{'start': '2015-01-01', 'stop': '2015-12-31', 'value': 15.59}],
                "values": [{'start': '2016-01-01', 'stop': '2017-12-31', 'value': 15.31}],
                },
            },
        }
    reference_legislation_json_copy['children']['taxes_carburants'] = reform_legislation_subtree
    return reference_legislation_json_copy
