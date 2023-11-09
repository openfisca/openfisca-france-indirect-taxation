# -*- coding: utf-8 -*-


import os
import pandas

from slugify import slugify

from openfisca_france_indirect_taxation.utils import assets_directory


elasticities_path = os.path.join(
    assets_directory,
    'aliss',
    )

elasticities_origin_xlsx = os.path.join(
    elasticities_path,
    'elasticites.xlsx'
    )

tables = [
    dict(
        age = None,
        revenus = None,
        skiprows = 4,
        sheetname = 'B.3',
        parse_cols = 'C:T',
        name = 'Food Expenditure Elasticities'
        ),
    dict(
        age = None,
        revenus = None,
        skiprows = 6,
        sheetname = 'B.4',
        parse_cols = 'B:Y',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Full sample'
        ),
    dict(
        age = 0,
        revenus = 3,
        skiprows = 5,
        sheetname = 'B5',
        parse_cols = 'B:Y',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Well off and less than 30 years old'
        ),
    dict(
        age = 1,
        revenus = 3,
        skiprows = 4,
        sheetname = 'B6',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Well off and aged between 30 and 45'
        ),
    dict(
        age = 2,
        revenus = 3,
        skiprows = 5,
        sheetname = 'B7',
        parse_cols = 'B:Y',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Well off and aged between 45 and 60'
        ),
    dict(
        age = 3,
        revenus = 3,
        skiprows = 4,
        sheetname = 'B8',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Well off and more than 60'
        ),
    dict(
        age = 0,
        revenus = 2,
        skiprows = 5,
        sheetname = 'B9',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Upper average and less than 30 years old'
        ),
    dict(
        age = 1,
        revenus = 2,
        skiprows = 5,
        sheetname = 'B10',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Upper average and aged between 30 and 45'
        ),
    dict(
        age = 2,
        revenus = 2,
        skiprows = 4,
        sheetname = 'B11',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Upper average and aged between 45 and 60'
        ),
    dict(
        age = 3,
        revenus = 2,
        skiprows = 4,
        sheetname = 'B12',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Upper average and aged more than 60'
        ),
    dict(
        age = 0,
        revenus = 1,
        skiprows = 4,
        sheetname = 'B13',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Lower average and less than 30 years old'
        ),
    dict(
        age = 1,
        revenus = 1,
        skiprows = 4,
        sheetname = 'B14',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Lower average and aged between 30 and 45'
        ),
    dict(
        age = 2,
        revenus = 1,
        skiprows = 4,
        sheetname = 'B15',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Lower average and aged between 45 and 60'
        ),
    dict(
        age = 3,
        revenus = 1,
        skiprows = 4,
        sheetname = 'B16',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Lower average and aged more than 60'
        ),
    dict(
        age = 0,
        revenus = 0,
        skiprows = 4,
        sheetname = 'B17',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Modest and less than 30 years old'
        ),
    dict(
        age = 1,
        revenus = 0,
        skiprows = 4,
        sheetname = 'B18',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Modest and aged between 30 and 45'
        ),
    dict(
        age = 2,
        revenus = 0,
        skiprows = 4,
        sheetname = 'B19',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Modest and aged between 45 and 60'
        ),
    dict(
        age = 3,
        revenus = 0,
        skiprows = 4,
        sheetname = 'B20',
        parse_cols = 'C:Z',
        name = 'Compensated Own-Price and Cross-Price Elasticities -- Modest and aged more than 60'
        ),
    ]

cross_price_elasticities = pandas.DataFrame()

for table in tables:
    age = table.pop('age')
    name = table.pop('name')
    revenus = table.pop('revenus')
    df = pandas.read_excel(elasticities_origin_xlsx, **table)
    df.dropna(inplace = True)
    df.set_index('Unnamed: 0', inplace = True)
    df.index.name = 'product'

    if age is None or revenus is None:
        df.name = name
        csv_path_name = os.path.join(elasticities_path, slugify(name) + '.csv')
        df.to_csv(csv_path_name)

    else:
        df['age'] = age
        df['revenus'] = revenus
        cross_price_elasticities = cross_price_elasticities.append(df)

csv_path_name = os.path.join(
    elasticities_path,
    'cross_price_elasticities.csv',
    )
cross_price_elasticities.to_csv(csv_path_name)
