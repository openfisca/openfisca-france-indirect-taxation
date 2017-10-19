# -*- coding: utf-8 -*-

from __future__ import division

import statsmodels.formula.api as smf
import os
import pkg_resources

from openfisca_france_indirect_taxation.build_survey_data.matching_erfs.step_2_homogenize_variables import \
    homogenize_definitions
from openfisca_france_indirect_taxation.build_survey_data.utils import \
    histogrammes
import matplotlib.pyplot as plt


def graph_builder_line(x_var, y_var):
    plt.plot(x_var, y_var, 'o')
    return plt.show()


data = homogenize_definitions()
data_erfs = data[0]
data_bdf = data[1]

#regression = smf.ols(formula = 'rev_disponible ~ \
#    ocde10',
#    data = data_bdf).fit()
#print regression.summary()

data_erfs['position_rev_disponible'] = data_erfs['rev_disponible'].argsort().argsort()
data_erfs['position_rev_disponible'] = data_erfs['position_rev_disponible'] / len(data_erfs) 

data_erfs['position_revdecm'] = data_erfs['revdecm'].argsort().argsort()
data_erfs['position_revdecm'] = data_erfs['position_revdecm'] / len(data_erfs) 

print data_erfs[['position_rev_disponible'] + ['rev_disponible']]

graph_builder_line(data_erfs['position_revdecm'], data_erfs['position_rev_disponible'])
graph_builder_line(data_erfs['revdecm'], data_erfs['rev_disponible'])

assets_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location
    )
data_erfs.to_csv(os.path.join(assets_directory, 'openfisca_france_indirect_taxation', 'assets', 'to_graph',
    'data_erfs.csv'), sep = ';')
