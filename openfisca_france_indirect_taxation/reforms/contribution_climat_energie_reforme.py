# -*- coding: utf-8 -*-

from openfisca_core.parameters import ParameterNode
from openfisca_core.reforms import Reform


# Montants de taxe prévus par la loi Contribution climat-énergie. 7€ en 2014, 14,5€ en 2015, 22€ en 2016,
# 30,5€ en 2017, 39€ en 2018 et 47.5€ en 2019 En utilisant nos données d'équivalence entre consommation et émission,
# on met en place les montants de taxe suivants :
# Dans cette réforme on suppose qu'on impute à la législation de 2014 une augmentation équivalente à ce qui est prévu
# par la loi pour les années à venir.


def modify_parameters(parameters):
    node = ParameterNode(
        'contribution_climat_energie_reforme',
        data = {
            'description': 'contribution_climat_energie_reforme',
            'diesel_2014_2015': {
                'description': 'Surcroît de prix du diesel (en euros par hectolitres)',
                # TODO "unit": '?',
                'unit': 'currency',
                'values': {'2014-01-01': 3.857 - 1.862}
                },
            'diesel_2014_2016': {
                'description': 'Surcroît de prix du diesel (en euros par hectolitres)',
                # TODO "unit": '?',
                'unit': 'currency',
                'values': {'2014-01-01': 5.852 - 1.862}
                },
            'essence_2014_2015': {
                'description': "Surcroît de prix de l'essence (en euros par hectolitres)",
                'unit': 'currency',
                'values': {'2014-01-01': 3.509 - 1.694}
                },
            'essence_2014_2016': {
                'description': "Surcroît de prix de l'essence (en euros par hectolitres)",
                'unit': 'currency',
                'values': {'2014-01-01': 5.324 - 1.694}
                },
            'fioul_domestique_2014_2015': {
                'description': 'Surcroît de prix du fioul domestique (en euros par litre)',
                'unit': 'currency',
                'values': {'2014-01-01': 0.04495 - 0.0217}
                },
            'fioul_domestique_2014_2016': {
                'description': 'Surcroît de prix du fioul domestique (en euros par litre)',
                'unit': 'currency',
                'values': {'2014-01-01': 0.0682 - 0.0217}
                },
            'gaz_2014_2015': {
                'description': 'Surcroît de prix du gaz (en euros par kWh)',
                # TODO "unit": '?',
                'unit': 'currency',
                'values': {'2014-01-01': 0.00348 - 0.00168}
                },
            'gaz_2014_2016': {
                'description': 'Surcroît de prix du gaz (en euros par kWh)',
                # TODO "unit": '?',
                'unit': 'currency',
                'values': {'2014-01-01': 0.00528 - 0.00168}
                },
            'abaissement_tva_taux_plein_2014_2015': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.004}
                },
            'abaissement_tva_taux_plein_2014_2016': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.008}
                },
            'abaissement_tva_taux_plein_bis_2014_2015': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.002}
                },
            'abaissement_tva_taux_plein_bis_2014_2016': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.005}
                },
            'abaissement_tva_taux_reduit_2014_2015': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.004}
                },
            'abaissement_tva_taux_reduit_2014_2016': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.006}
                },
            'abaissement_tva_taux_super_reduit_2014_2015': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.004}
                },
            'abaissement_tva_taux_super_reduit_2014_2016': {
                'description': 'Baisse de la TVA à taux plein pour obtenir un budget constant',
                # TODO "unit": '?',
                'values': {'2010-01-01': 0.006}
                },
            },
        )
    parameters.add_child('contribution_climat_energie_reforme', node)
    return parameters


class contribution_climat_energie_reforme(Reform):
    key = 'contribution_climat_energie_reforme',
    name = 'Réforme de la contribution climat energie anticipée simulée sur les données de 2014',

    def apply(self):
        self.modify_parameters(modifier_function = modify_parameters)
        variables = [
            ]
        for variable in variables:
            self.add_variable(variable)
