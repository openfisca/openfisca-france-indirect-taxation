# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:05:22 2015

@author: thomas.douenne
"""

import sys
import pkg_resources
import os
import pandas as pd


def main():
    from ipp_macro_series_parser.agregats_transports.parser_cleaner_prix_carburants import prix_annuel_carburants_90_14
    prix_annuel_carburants_90_14['Date'] = prix_annuel_carburants_90_14['Date'].astype(int)
    prix_annuel_carburants_90_14 = prix_annuel_carburants_90_14.set_index('Date')
    all_values = {}
    for element in ['diesel_ttc']:
        prix_annuel_carburants = prix_annuel_carburants_90_14['{}'.format(element)]
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
            values['value'] = prix_annuel_carburants.loc[year] * 100
            all_values[element].append(values)

        prix_carburants['children'][element] = {
            "@type": "Parameter",
            "description": element.replace('_', ' '),
            "format": "float",
            "values": all_values[element]
            }

        assets_directory = os.path.join(
            pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
            )

        prix_annuel_carburants = pd.DataFrame(prix_carburants.items())
        prix_annuel_carburants.to_csv(os.path.join(
            assets_directory, 'openfisca_france_indirect_taxation', 'assets', 'prix_annuel_carburants.csv')
            )


if __name__ == "__main__":
    sys.exit(main())
