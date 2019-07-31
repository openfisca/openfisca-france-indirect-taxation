#! /usr/bin/env python
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import matplotlib.pyplot as plt
import numpy as np
import seaborn

seaborn.set_palette(seaborn.color_palette("Set2", 12))

_SQRT2 = np.sqrt(2)     # sqrt(2) with default precision np.float64


def collapsesum(data_frame, by = None, var = None):
    '''
    Pour une variable, fonction qui calcule la moyenne pondérée au sein de chaque groupe.
    '''
    assert by is not None
    assert var is not None
    grouped = data_frame.groupby([by])
    return grouped.apply(lambda x: weighted_sum(groupe = x, var =var))


def find_nearest_inferior(years, year):
    # years = year_data_list
    anterior_years = [
        available_year for available_year in years if available_year <= year
        ]
    return max(anterior_years)


# ident_men_dtype = numpy.dtype('O')
ident_men_dtype = 'str'


def hellinger(p, q):
    return np.sqrt(np.sum((np.sqrt(p) - np.sqrt(q)) ** 2)) / _SQRT2


def histogrammes(list_keys, list_values_bdf, list_values_entd, data_name_1, data_name_2):
    size_hist = np.arange(len(list_keys))
    plot_bdf = plt.bar(size_hist - 0.125, list_values_bdf, color = 'b', align='center', width=0.25)
    plot_entd = plt.bar(size_hist + 0.125, list_values_entd, align='center', width=0.25)
    plt.xticks(size_hist, list_keys)
    plt.legend((plot_bdf[0], plot_entd[0]), (data_name_1, data_name_2))

    return plt


def plots_by_group(function, data_name_1, data_name_2, distance, group):
    fig = plt.figure()

    if group == 'tuu':
        corr = -1
    else:
        corr = 0

    ax1 = fig.add_subplot(521)
    ax1 = function(data_name_1, data_name_2, distance, group, 1 + corr)

    ax2 = fig.add_subplot(522)
    ax2 = function(data_name_1, data_name_2, distance, group, 2 + corr)

    ax3 = fig.add_subplot(523)
    ax3 = function(data_name_1, data_name_2, distance, group, 3 + corr)

    ax4 = fig.add_subplot(524)
    ax4 = function(data_name_1, data_name_2, distance, group, 4 + corr)

    ax5 = fig.add_subplot(525)
    ax5 = function(data_name_1, data_name_2, distance, group, 5 + corr)

    ax6 = fig.add_subplot(526)
    ax6 = function(data_name_1, data_name_2, distance, group, 6 + corr)

    ax7 = fig.add_subplot(527)
    ax7 = function(data_name_1, data_name_2, distance, group, 7 + corr)

    ax8 = fig.add_subplot(528)
    ax8 = function(data_name_1, data_name_2, distance, group, 8 + corr)

    ax9 = fig.add_subplot(529)
    ax9 = function(data_name_1, data_name_2, distance, group, 9 + corr)

    if group == 'niveau_vie_decile':
        ax10 = fig.add_subplot(5, 2, 10)
        ax10 = function(data_name_1, data_name_2, distance, group, 10 + corr)


def weighted_sum(groupe, var):
    '''
    Fonction qui calcule la moyenne pondérée par groupe d'une variable
    '''
    data = groupe[var]
    weights = groupe['pondmen']
    return (data * weights).sum()
