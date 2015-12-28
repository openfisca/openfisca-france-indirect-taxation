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


from __future__ import division


import logging
import pandas

from openfisca_survey_manager.temporary import temporary_store_decorator
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.utils import get_transfert_data_frames
from openfisca_france_indirect_taxation.build_survey_data.step_0_1_1_homogeneisation_donnees_depenses \
    import normalize_code_coicop

from openfisca_france_indirect_taxation.build_survey_data.utils \
    import ident_men_dtype

log = logging.getLogger(__name__)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def build_menage_consumption_by_categorie_fiscale(temporary_store = None, year_calage = None, year_data = None):
    """Build menage consumption by categorie fiscale dataframe """
    assert temporary_store is not None
    assert year_calage is not None
    assert year_data is not None

    # Load matrices de passage
    matrice_passage_data_frame, selected_parametres_fiscalite_data_frame = \
        get_transfert_data_frames(year = year_data)

    # Load data
    coicop_data_frame = temporary_store['depenses_bdf_{}'.format(year_calage)]

    # Grouping by categorie_fiscale
    selected_parametres_fiscalite_data_frame = \
        selected_parametres_fiscalite_data_frame[['posteCOICOP', 'categoriefiscale']]
    selected_parametres_fiscalite_data_frame.set_index('posteCOICOP', inplace = True)

    # Normalisation des coicop de la feuille excel pour être cohérent avec depenses_calees
    normalized_poste_coicop = [
        normalize_code_coicop(coicop)
        for coicop in selected_parametres_fiscalite_data_frame.index
        ]
    selected_parametres_fiscalite_data_frame.index = normalized_poste_coicop

    categorie_fiscale_by_coicop = selected_parametres_fiscalite_data_frame.to_dict()['categoriefiscale']
    for key in categorie_fiscale_by_coicop.keys():
        import math
        if not math.isnan(categorie_fiscale_by_coicop[key]):
            categorie_fiscale_by_coicop[key] = int(categorie_fiscale_by_coicop[key])
        if math.isnan(categorie_fiscale_by_coicop[key]):
            categorie_fiscale_by_coicop[key] = 0
        assert type(categorie_fiscale_by_coicop[key]) == int

    categorie_fiscale_labels = [
        categorie_fiscale_by_coicop.get(coicop)
        for coicop in coicop_data_frame.columns
        ]
    # TODO: gérer les catégorie fiscales "None" = dépenses énergétiques (4) & tabac (2)
    tuples = zip(categorie_fiscale_labels, coicop_data_frame.columns)
    coicop_data_frame.columns = pandas.MultiIndex.from_tuples(tuples, names=['categoriefiscale', 'coicop'])

    categorie_fiscale_data_frame = coicop_data_frame.groupby(level = 0, axis = 1).sum()
    rename_columns = dict(
        [(number, "categorie_fiscale_{}".format(number)) for number in categorie_fiscale_data_frame.columns]
        )
    categorie_fiscale_data_frame.rename(
        columns = rename_columns,
        inplace = True,
        )
    categorie_fiscale_data_frame['role_menage'] = 0
    categorie_fiscale_data_frame.index = categorie_fiscale_data_frame.index.astype(ident_men_dtype)
    temporary_store["menage_consumption_by_categorie_fiscale_{}".format(year_calage)] = categorie_fiscale_data_frame


if __name__ == '__main__':
    import sys
    import time
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)
    deb = time.clock()
    year_calage = 2005
    year_data_list = [2000, 2005, 2010]
    build_menage_consumption_by_categorie_fiscale(year_calage, year_data_list)
    log.info("step 01 demo duration is {}".format(time.clock() - deb))
