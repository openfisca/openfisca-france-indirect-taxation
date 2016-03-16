#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division

from datetime import date

from openfisca_core.columns import FloatCol
from openfisca_core.formulas import Variable


from openfisca_france_indirect_taxation.model.base import *
from openfisca_france_indirect_taxation.utils import get_parametres_fiscalite_data_frame


postes_coicop_data_frame = None


def generate_variables():
    postes_coicop_list = [element for element in postes_coicop_data_frame.posteCOICOP.values]
    for poste in postes_coicop_list:
        extraction_condition = postes_coicop_data_frame.posteCOICOP == int(poste)
        liste_annees = postes_coicop_data_frame.loc[
            extraction_condition,
            'annee'].copy()
        # assert liste_annees.shape == (21L,), "Some goods do not exist during certain years"
        label = postes_coicop_data_frame.loc[
            extraction_condition,
            'description'].values.squeeze().tolist()
        class_name = u'poste_coicop_{}'.format(poste)
        # Trick to create a class with a dynamic name.
        type(class_name.encode('utf-8'), (Variable,), dict(
            column = FloatCol,
            entity_class = Menages,
            label = label.decode('utf-8'),
            ))


def preload_postes_coicop_data_frame():
    global postes_coicop_data_frame
    if postes_coicop_data_frame is None:
        postes_coicop_data_frame = get_parametres_fiscalite_data_frame()
        postes_coicop_data_frame = postes_coicop_data_frame[
            ['posteCOICOP', 'annee', 'description', 'categoriefiscale']].copy()
        postes_coicop_data_frame.drop_duplicates('posteCOICOP', keep = 'last', inplace = True)
        generate_variables()


def preload_new_postes_coicop_data_frame():
    global postes_coicop_data_frame
    if codes_coicop_data_frame is None:
        codes_coicop_data_frame = pd.read_csv(
            os.path.join(legislation_directory, 'coicop_legislation.csv'),
            )
        codes_coicop_data_frame = codes_coicop_data_frame.query('not (code_bdf != code_bdf)')[  # NaN removal
            ['code_coicop', 'code_bdf', 'label']].copy()
        codes_coicop_data_frame = codes_coicop_data_frame.loc[
            codes_coicop_data_frame.code_coicop.str[:2].astype(int) <= 12
            ].copy()
        generate_new_variables()
