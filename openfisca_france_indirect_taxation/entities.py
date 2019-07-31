# -*- coding: utf-8 -*-


from openfisca_core.entities import build_entity

Individu = build_entity(
    key = "individu",
    plural = "individus",
    label = 'Individu',
    is_person = True
    )


Menage = build_entity(
    key = "menage",
    plural = "menages",
    label = 'Ménage',
    roles = [
        {
            'key': 'personne_de_reference',
            'label': 'Personne de référence',
            'max': 1
            },
        {
            'key': 'conjoint',
            'label': 'Conjoint',
            'max': 1
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': 'Enfants',
            'max': 2
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': 'Autres'
            }
        ]
    )


entities = [Individu, Menage]
