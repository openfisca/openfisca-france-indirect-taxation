# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from openfisca_core import reforms


def preprocess_legislation(legislation_json):
    '''
    Preprocess the legislation parameters to add prices and amounts from national accounts
    '''
    import os
    import pkg_resources
    import pandas as pd

    default_config_files_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
    prix_carburants = pd.read_csv(
        os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'prix_annuel_carburants.csv'
            ), sep =';'
        )
    prix_carburants['Date'] = prix_carburants['Date'].astype(int)
    prix_carburants = prix_carburants.set_index('Date')

    all_values = {}
    for element in ['diesel_ht', 'diesel_ttc', 'super_95_ht', 'super_95_ttc', 'super_98_ht', 'super_98_ttc',
            'super_95_e10_ht', 'super_95_e10_ttc', 'gplc_ht', 'gplc_ttc', 'super_plombe_ht', 'super_plombe_ttc']:
        prix_carburants = prix_carburants['{}'.format(element)]
        all_values['{}'.format(element)] = []
        prix_carburants = {
            "@type": "Node",
            "description": "prix des carburants en euros par hectolitre",
            "children": {},
            }
        for year in range(1990, 2015):
            values = dict()
            values['start'] = u'{}-01-01'.format(year)
            values['stop'] = u'{}-12-31'.format(year)
            values['value'] = prix_carburants.loc[year] * 100
            all_values[element].append(values)

        prix_carburants['children'][element] = {
            "@type": "Parameter",
            "description": element.replace('_', ' '),
            "format": "float",
            "values": all_values[element]
            }

    legislation_json['children']['imposition_indirecte']['children']['prix_carburants'] = \
        prix_carburants

    return legislation_json
