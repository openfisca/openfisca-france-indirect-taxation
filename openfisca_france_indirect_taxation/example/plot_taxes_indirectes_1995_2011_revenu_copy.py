# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 18:57:00 2015

@author: Etienne
"""

# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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


from __future__ import division

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from openfisca_france_indirect_taxation.example.utils_example import simulate_df
from openfisca_france_indirect_taxation.example.utils_example import df_weighted_average_grouped, percent_formatter

if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    list_coicop12 = []
    for coicop12_index in range(1, 13):
        list_coicop12.append('coicop12_{}'.format(coicop12_index))

    var_to_be_simulated = [
        'decuc',
        'age',
        'montant_tva_total',
        'montant_tipp',
        'montant_droit_d_accise_vin',
        'montant_droit_d_accise_biere',
        'montant_droit_d_accise_alcools_forts',
        'montant_droit_d_accise_cigarette',
        'montant_droit_d_accise_cigares',
        'montant_droit_d_accise_tabac_a_rouler',
        'montant_taxe_assurance_transport',
        'montant_taxe_assurance_sante',
        'montant_taxe_autres_assurances',
        'decile',
        'revtot',
        'rev_disponible',
        'ident_men',
        'pondmen',
        'somme_coicop12'
        ]


    var_to_be_simulated += list_coicop12

    p = dict()
    for year in [2000, 2005, 2011]:
        simulation_data_frame = simulate_df(var_to_be_simulated = var_to_be_simulated, year = year)
        aggregates_data_frame = df_weighted_average_grouped(dataframe = simulation_data_frame, groupe = 'decile', varlist = var_to_be_simulated)
        if year == 2011:
            simulation_data_frame.decile[simulation_data_frame.decuc == 10] = 10

        aggregates_data_frame['montant_taxe_1'] = aggregates_data_frame['montant_tva_total']
        aggregates_data_frame['montant_taxe_2'] = aggregates_data_frame['montant_tipp']
        aggregates_data_frame['montant_taxe_3'] = aggregates_data_frame['montant_taxe_assurance_sante'] + aggregates_data_frame['montant_taxe_assurance_transport'] + aggregates_data_frame['montant_taxe_autres_assurances']
        aggregates_data_frame['montant_taxe_4'] = aggregates_data_frame['montant_droit_d_accise_vin'] + aggregates_data_frame['montant_droit_d_accise_biere'] + aggregates_data_frame['montant_droit_d_accise_alcools_forts']
        aggregates_data_frame['montant_taxe_5'] = aggregates_data_frame['montant_droit_d_accise_cigares'] + aggregates_data_frame['montant_droit_d_accise_cigarette'] + aggregates_data_frame['montant_droit_d_accise_tabac_a_rouler']

        aggregates_data_frame['montant_total'] = (aggregates_data_frame['montant_taxe_{}'.format(1)] + aggregates_data_frame['montant_taxe_{}'.format(2)] + aggregates_data_frame['montant_taxe_{}'.format(3)] + aggregates_data_frame['montant_taxe_{}'.format(4)] + aggregates_data_frame['montant_taxe_{}'.format(5)])
        aggregates_data_frame['{}'.format(year)] = aggregates_data_frame['montant_total'] / aggregates_data_frame['rev_disponible']
        p['{}'.format(year)] = aggregates_data_frame['{}'.format(year)]



        axes = p['{}'.format(year)].plot(
            stacked = True
            )

        plt.axhline(0, color = 'k')

        axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
        axes.set_xticklabels(['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'], rotation=0)

        axes.legend(
            bbox_to_anchor = (1, 1),
            )

    plt.show()

