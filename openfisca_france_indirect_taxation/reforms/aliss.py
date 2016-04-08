# -*- coding: utf-8 -*-

from __future__ import division


import os
import pandas
import pkg_resources



from openfisca_core import reforms

from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import generate_variables
from openfisca_france_indirect_taxation.build_survey_data.calibration_aliss import (
    add_poste_coicop,
    build_clean_aliss_data_frame,
    )


aliss_refom_path = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'reforms',
    'aliss_reform_data.csv',
    )

aliss_reform_data = pandas.read_csv(aliss_refom_path)
reform_names = aliss_reform_data.columns[1:].tolist()
aliss_uncomplete = build_clean_aliss_data_frame()
aliss = add_poste_coicop(aliss_uncomplete)
aliss_extract = aliss[['nomf', 'nomc', 'poste_bdf']].copy()
aliss_extract.drop_duplicates(inplace = True)
legislation_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
    'openfisca_france_indirect_taxation',
    'assets',
    'legislation',
    )
codes_coicop_data_frame = pandas.read_csv(
    os.path.join(legislation_directory, 'coicop_legislation.csv'),
    )
# year = 2011
# legislation = codes_coicop_data_frame.query('start <= @year & @year <= stop')[['code_bdf', 'categorie_fiscale']].copy()
legislation = codes_coicop_data_frame[['code_bdf', 'categorie_fiscale']].copy()
legislation.rename(columns = {'code_bdf': 'poste_bdf'}, inplace = True)
aliss_legislation = aliss_extract.merge(legislation)
aliss_legislation.rename(columns = {'poste_bdf': 'code_bdf'}, inplace = True)
aliss_reform = aliss_legislation.merge(aliss_reform_data)

mismatch = aliss_reform.groupby(['code_bdf']).filter(
    lambda x: (
        x.sante.nunique() > 1 or
        x.environnement.nunique() > 1 or
        x.tva_sociale.nunique() > 1
        )).copy()

mismatch.nomc = mismatch.nomc.str.decode('latin-1').str.encode('utf-8')
mismatch.to_csv('reform_mismatch.csv', index = False)



boum

def build_reform_sante(tax_benefit_system):
    Reform = reforms.make_reform(
        key = 'aliss_sante',
        name = u"Réforme Santé de l'imposition indirecte des biens alimentaires",
        reference = tax_benefit_system,
        )
    from openfisca_france_indirect_taxation.model.consommation.categories_fiscales import categories_fiscales_data_frame
    aliss_reform.columns
    categories_fiscales_reform = aliss_reform[['sante', 'code_bdf']].drop_duplicates().copy()

    categories_fiscales_reform.rename(columns=({'sante': 'categorie_fiscale'}), inplace = True)
    categories_fiscales_reform.code_bdf.duplicated().sum()
    year = 2011
    categories_fiscales = categories_fiscales_data_frame.query('start <= @year & @year <= stop').copy()
    assert not categories_fiscales.code_bdf.duplicated().any()

    categories_fiscales = categories_fiscales.merge(categories_fiscales_reform, on = ['code_bdf'])
    assert not categories_fiscales.code_bdf.duplicated().any(), "there are {} duplicated".format(
        categories_fiscales.code_bdf.duplicated().sum())

    df2 = categories_fiscales.query("categorie_fiscale_x != categorie_fiscale_y")


    generate_variables(
        categories_fiscales = categories_fiscales,
        Reform = Reform,
        tax_benefit_system = tax_benefit_system,
        )

    reform = Reform()
    # reform.modify_legislation_json(modifier_function = modify_legislation_json)
    return reform

