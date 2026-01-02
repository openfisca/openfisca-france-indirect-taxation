# -*- coding: utf-8 -*-


import glob
import os

from openfisca_core.taxbenefitsystems import TaxBenefitSystem
from openfisca_france_indirect_taxation.parameters import preprocessing

from openfisca_france_indirect_taxation import entities


COUNTRY_DIR = os.path.dirname(os.path.abspath(__file__))
EXTENSIONS_PATH = os.path.join(COUNTRY_DIR, 'extensions')
EXTENSIONS_DIRECTORIES = glob.glob(os.path.join(EXTENSIONS_PATH, '*/'))


class FranceIndirectTaxationTaxBenefitSystem(TaxBenefitSystem):
    '''French indirect taxation tax benefit system'''
    CURRENCY = '€'
    preprocess_legislation = staticmethod(preprocessing.preprocess_legislation)

    def __init__(self):
        TaxBenefitSystem.__init__(self, entities.entities)
        param_dir = os.path.join(COUNTRY_DIR, 'parameters')
        self.load_parameters(param_dir)
        self.add_variables_from_directory(os.path.join(COUNTRY_DIR, 'variables'))
        for extension_dir in EXTENSIONS_DIRECTORIES:
            self.load_extension(extension_dir)
        self.prefill_cache()
        self.parameters = self.preprocess_legislation(self.parameters)

    def prefill_cache(self):
        '''Load data for poste_*, categorie fiscales & prix carburants variables'''
        from openfisca_france_indirect_taxation.variables.consommation import postes_coicop
        postes_coicop.preload_postes_bdf_data_frame(self)
        from openfisca_france_indirect_taxation.variables.consommation import categories_fiscales
        categories_fiscales.preload_categories_fiscales_data_frame(self)
        from .parameters import prix_carburants
        prix_carburants.preload_prix_carburant_par_annee_par_carburant_par_region_en_hectolitre()
        prix_carburants.preload_prix_carburant_par_annee_par_carburant_en_hectolitre()
