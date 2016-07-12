# -*- coding: utf-8 -*-


import glob
import itertools
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from .param import preprocessing

from . import entities
from . import scenarios


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class FranceIndirectTaxationTaxBenefitSystem(TaxBenefitSystem):
    """French indirect taxation tax benefit system"""
    CURRENCY = u"€"
    preprocess_legislation = staticmethod(preprocessing.preprocess_legislation)

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities.entities)
        self.Scenario = scenarios.Scenario
        param_file = os.path.join(COUNTRY_DIR, 'param', 'parameters.xml')
        self.add_legislation_params(param_file)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'model'))
        for extension_dir in EXTENSIONS_DIRECTORIES:
            self.load_extension(extension_dir)
        self.prefill_cache()

    def prefill_cache(self):
        # Define and poste_* and categorie fiscales variables
        from .model.consommation import postes_coicop
        postes_coicop.preload_postes_coicop_data_frame(self)
        from .model.consommation import categories_fiscales
        categories_fiscales.preload_categories_fiscales_data_frame(self)
