# -*- coding: utf-8 -*-


import logging
import os
import pandas as pd


from openfisca_survey_manager.coicop import build_raw_coicop_nomenclature
from openfisca_france_indirect_taxation.utils import assets_directory

log = logging.getLogger(__name__)


legislation_directory = os.path.join(
    assets_directory,
    'legislation',
    )

taxe_by_categorie_fiscale_number = {
    0: '',
    1: 'tva_taux_super_reduit',
    2: 'tva_taux_reduit',
    3: 'tva_taux_plein',
    4: 'tva_taux_intermediaire',
    7: 'cigarettes',
    8: 'cigares',
    9: 'tabac_a_rouler',
    10: 'alcools_forts',
    11: 'tva_taux_plein',
    12: 'vin',
    13: 'biere',
    14: 'ticpe',
    15: 'assurance_transport',
    16: 'assurance_sante',
    17: 'autres_assurances'
    }


def build_complete_coicop_nomenclature(to_csv = True):
    coicop_nomenclature = build_raw_coicop_nomenclature()
    items = [
        ('Cigares et cigarillos', '02.2.1'),
        ('Cigarettes', '02.2.2'),
        ("Tabac sous d'autres formes et produits connexes", '02.2.3'),
        ('Stupéfiants ', '02.3'),
        ]

    for label_poste, code_coicop in items:
        label_division = 'Boissons alcoolisées et tabac'
        label_groupe = 'Tabac'
        label_classe = label_sous_classe = label_poste
        data = dict(
            label_division = [label_division],
            label_groupe = [label_groupe],
            label_classe = [label_classe],
            label_sous_classe = [label_sous_classe],
            label_poste = [label_poste],
            code_coicop = [code_coicop],
            )
        coicop_nomenclature = pd.concat(
            [coicop_nomenclature, pd.DataFrame.from_dict(data, dtype = 'str')],
            ignore_index = True
            )
        coicop_nomenclature.sort_values('code_coicop', inplace = True)

    if to_csv:
        coicop_nomenclature.to_csv(
            os.path.join(legislation_directory, 'nomenclature_coicop.csv'),
            )

    return coicop_nomenclature[['label_division', 'label_groupe', 'label_classe',
       'label_sous_classe', 'label_poste', 'code_coicop']].copy()


if __name__ == '__main__':
    coicop_nomenclature = build_complete_coicop_nomenclature(False)
    print(coicop_nomenclature.dtypes)
