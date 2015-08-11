# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 16:05:22 2015

@author: thomas.douenne
"""

import sys


def main(dataframe):
    dataframe['Date'] = dataframe['Date'].astype(int)
    dataframe = dataframe.set_index('Date')
    all_values = {}
    for element in ['diesel_ttc']:
        prix_annuel_carburants = dataframe['{}'.format(element)]
        all_values['{}'.format(element)] = []
        prix_carbu = {
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

        prix_carbu['children'][element] = {
            "@type": "Parameter",
            "description": element.replace('_', ' '),
            "format": "float",
            "values": all_values[element]
            }

if __name__ == "__main__":
    sys.exit(main())
