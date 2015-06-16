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
from openfisca_france_indirect_taxation.example.utils_example import df_weighted_average_grouped

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


    df2000 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2000)
    Wconcat2000 = df_weighted_average_grouped(dataframe = df2000, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2000['montant_taxe_{}'.format(1)] = Wconcat2000['montant_tva_total']
    Wconcat2000['montant_taxe_{}'.format(2)] = Wconcat2000['montant_tipp']
    Wconcat2000['montant_taxe_{}'.format(3)] = Wconcat2000['montant_taxe_assurance_sante'] + Wconcat2000['montant_taxe_assurance_transport'] + Wconcat2000['montant_taxe_autres_assurances']
    Wconcat2000['montant_taxe_{}'.format(4)] = Wconcat2000['montant_droit_d_accise_vin'] + Wconcat2000['montant_droit_d_accise_biere'] + Wconcat2000['montant_droit_d_accise_alcools_forts']
    Wconcat2000['montant_taxe_{}'.format(5)] = Wconcat2000['montant_droit_d_accise_cigares'] + Wconcat2000['montant_droit_d_accise_cigarette'] + Wconcat2000['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2000['montant_total'] = (Wconcat2000['montant_taxe_{}'.format(1)] + Wconcat2000['montant_taxe_{}'.format(2)] + Wconcat2000['montant_taxe_{}'.format(3)] + Wconcat2000['montant_taxe_{}'.format(4)] + Wconcat2000['montant_taxe_{}'.format(5)])
    Wconcat2000['2000'] = Wconcat2000['montant_total'] / Wconcat2000['rev_disponible']
    df_to_graph_2000 = Wconcat2000['2000']

    df2005 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2005)
    Wconcat2005 = df_weighted_average_grouped(dataframe = df2005, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2005['montant_taxe_{}'.format(1)] = Wconcat2005['montant_tva_total']
    Wconcat2005['montant_taxe_{}'.format(2)] = Wconcat2005['montant_tipp']
    Wconcat2005['montant_taxe_{}'.format(3)] = Wconcat2005['montant_taxe_assurance_sante'] + Wconcat2005['montant_taxe_assurance_transport'] + Wconcat2005['montant_taxe_autres_assurances']
    Wconcat2005['montant_taxe_{}'.format(4)] = Wconcat2005['montant_droit_d_accise_vin'] + Wconcat2005['montant_droit_d_accise_biere'] + Wconcat2005['montant_droit_d_accise_alcools_forts']
    Wconcat2005['montant_taxe_{}'.format(5)] = Wconcat2005['montant_droit_d_accise_cigares'] + Wconcat2005['montant_droit_d_accise_cigarette'] + Wconcat2005['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2005['montant_total'] = (Wconcat2005['montant_taxe_{}'.format(1)] + Wconcat2005['montant_taxe_{}'.format(2)] + Wconcat2005['montant_taxe_{}'.format(3)] + Wconcat2005['montant_taxe_{}'.format(4)] + Wconcat2005['montant_taxe_{}'.format(5)])
    Wconcat2005['2005'] = Wconcat2005['montant_total'] / Wconcat2005['rev_disponible']
    df_to_graph_2005 = Wconcat2005['2005']

    df2011 = simulate_df(var_to_be_simulated = var_to_be_simulated, year = 2011)
    df2011.decile[df2011.decuc == 10] = 10
    Wconcat2011 = df_weighted_average_grouped(dataframe = df2011, groupe = 'decile', varlist = var_to_be_simulated)

    Wconcat2011['montant_taxe_{}'.format(1)] = Wconcat2011['montant_tva_total']
    Wconcat2011['montant_taxe_{}'.format(2)] = Wconcat2011['montant_tipp']
    Wconcat2011['montant_taxe_{}'.format(3)] = Wconcat2011['montant_taxe_assurance_sante'] + Wconcat2011['montant_taxe_assurance_transport'] + Wconcat2011['montant_taxe_autres_assurances']
    Wconcat2011['montant_taxe_{}'.format(4)] = Wconcat2011['montant_droit_d_accise_vin'] + Wconcat2011['montant_droit_d_accise_biere'] + Wconcat2011['montant_droit_d_accise_alcools_forts']
    Wconcat2011['montant_taxe_{}'.format(5)] = Wconcat2011['montant_droit_d_accise_cigares'] + Wconcat2011['montant_droit_d_accise_cigarette'] + Wconcat2011['montant_droit_d_accise_tabac_a_rouler']

    Wconcat2011['montant_total'] = (Wconcat2011['montant_taxe_{}'.format(1)] + Wconcat2011['montant_taxe_{}'.format(2)] + Wconcat2011['montant_taxe_{}'.format(3)] + Wconcat2011['montant_taxe_{}'.format(4)] + Wconcat2011['montant_taxe_{}'.format(5)])
    Wconcat2011['2011'] = Wconcat2011['montant_total'] / Wconcat2011['rev_disponible']
    df_to_graph_2011 = Wconcat2011['2011']

    axes = df_to_graph_2000.plot(
        stacked = True
        )
    axes = df_to_graph_2005.plot(
        stacked = True
        )
    axes = df_to_graph_2011.plot(
        stacked = True
        )

    plt.axhline(0, color = 'k')

    def percent_formatter(x, pos = 0):
        return '%1.0f%%' % (100 * x)

    axes.yaxis.set_major_formatter(ticker.FuncFormatter(percent_formatter))
    axes.set_xticklabels(['1', '2', '3', '4' ,'5' ,'6' ,'7' ,'8' ,'9' ,'10'], rotation=0)

    axes.legend(
        bbox_to_anchor = (1, 1),
        )

    plt.show()
