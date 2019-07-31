# -*- coding: utf-8 -*-

import os
import pkg_resources
import pandas as pd
from ruamel import yaml

"""
    Create yaml files for prix_carburants
"""


file_path = os.path.join(
    pkg_resources.get_distribution('openfisca-france-indirect-taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'prix',
    'prix_mensuel_carburants.csv'
    )

output_file_path = os.path.join(
    pkg_resources.get_distribution('openfisca-france-indirect-taxation').location,
    'openfisca_france_indirect_taxation',
    'parameters',
    'imposition_indirecte',
    'prix_carburants.yaml',
    )

df = pd.read_csv(file_path)
date = df.Date.str.split("/", n = 1, expand = True)
date[1] = date[1].where(date[1].str.len() == 2, "0" + date[1])
date['date'] = date[0] + '-' + date[1] + '-01'
df['date'] = date['date']
df.drop(columns = ['Date'], inplace = True)
df = (df
    .set_index('date')
    .sort_index()
      )


prices_by_name = dict()
for column in df:
    series = (df[column]
        .dropna()
        .sort_index(ascending = False)
              )
    prices_by_date = series.to_dict()
    for date, price in list(prices_by_date.items()):
        prices_by_date[date] = dict(value = price)
    prices_by_name[column] = dict(values = prices_by_date)

with open(output_file_path, 'w') as outfile:
    yaml.safe_dump(prices_by_name, outfile, default_flow_style = False, width = 1000)
