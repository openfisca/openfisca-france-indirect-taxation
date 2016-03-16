#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import division

import os
import pandas as pd
import pkg_resources
import logging

from biryani.strings import slugify

from openfisca_core.columns import FloatCol
from openfisca_core.formulas import Variable


from openfisca_france_indirect_taxation.model.base import *


log = logging.getLogger(__name__)


codes_coicop_data_frame = None

legislation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'legislation',
    )


def generate_variables():
    codes_bdf = [element for element in codes_coicop_data_frame.code_bdf.unique()]
    for code_bdf in codes_bdf:
        label = codes_coicop_data_frame.query('code_bdf == @code_bdf')['label'].drop_duplicates().tolist()
        assert len(label) == 1, u"Too many labels for {}: {}".format(code_bdf, label)
        label = label[0]
        code_coicop = codes_coicop_data_frame.query('code_bdf == @code_bdf')['code_coicop'].drop_duplicates().tolist()
        assert len(code_coicop) == 1, u"Too many code_coicop for {}: {}".format(code_bdf, code_coicop)
        code_coicop = code_coicop[0]
        class_name = u"poste_{}".format(slugify(unicode(code_coicop), separator = u'_'))
        log.info(u'Creating variable {} with label {}'.format(class_name, label.decode('utf-8')))
        # Trick to create a class with a dynamic name.
        type(class_name.encode('utf-8'), (Variable,), dict(
            column = FloatCol,
            entity_class = Menages,
            label = label.decode('utf-8'),
            ))


def preload_postes_coicop_data_frame():
    global codes_coicop_data_frame
    if codes_coicop_data_frame is None:
        codes_coicop_data_frame = pd.read_csv(
            os.path.join(legislation_directory, 'coicop_legislation.csv'),
            )
        codes_coicop_data_frame = codes_coicop_data_frame.query('not (code_bdf != code_bdf)')[  # NaN removal
            ['code_coicop', 'code_bdf', 'label', 'categorie_fiscale']].copy()
        codes_coicop_data_frame = codes_coicop_data_frame.loc[
            codes_coicop_data_frame.code_coicop.str[:2].astype(int) <= 12
            ].copy()
        generate_variables()
