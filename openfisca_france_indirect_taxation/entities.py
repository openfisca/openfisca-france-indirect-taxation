# -*- coding: utf-8 -*-


from openfisca_core.entities import build_entity


Individu = build_entity(
    key = "individu",
    plural = "individus",
    label = u'Individu',
    is_person = True
    )


Menage = build_entity(
    key = "menage",
    plural = "menages",
    label = u'Ménage',
    roles = [
        {
            'key': 'personne_de_reference',
            'label': u'Personne de référence',
            'max': 1
            },
        {
            'key': 'conjoint',
            'label': u'Conjoint',
            'max': 1
            },
        {
            'key': 'enfant',
            'plural': 'enfants',
            'label': u'Enfants',
            'max': 2
            },
        {
            'key': 'autre',
            'plural': 'autres',
            'label': u'Autres'
            }
        ]
    )


entities = [Individu, Menage]
