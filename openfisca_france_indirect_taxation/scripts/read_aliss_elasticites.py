# -*- coding: utf-8 -*-


import os
import pandas
import pkg_resources


elasticities_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'aliss',
    'elasticites.xlsx',
    )


tables = [
    dict(
        skiprows = 4,
        sheetname = 'B.3',
        parse_cols = "C:T",
        name = 'Food Expenditure Elasticities'
        ),
    ]

for table in tables:
    name = table.pop('name')
    df = pandas.read_excel(elasticities_path, **table)
    df.dropna(inplace = True)
    df.set_index('Unnamed: 0', inplace = True)
    df.index.name = 'product'
    df.name = name