# -*- coding: utf-8 -*-


def init_single_entity(scenario, autres = None, axes = None, conjoint = None, enfants = None,
        menage = None, period = None, personne_de_reference =None):
    if enfants is None:
        enfants = []
    if autres is None:
        autres = []
    assert personne_de_reference is not None
    menage = menage.copy() if menage is not None else {}

    menages = {}
    individus = {}

    count_so_far = 0
    for nth in range(0, 1):
        menage_nth = menage.copy() if menage is not None else {}
        group = [personne_de_reference, conjoint] + (enfants or [])
        for index, individu in enumerate(group):
            if individu is None:
                continue
            id = individu.get('id')
            if id is None:
                individu = individu.copy()
                id = 'ind{}'.format(index + count_so_far)
            individus[id] = individu
            if index <= 1:
                if index == 0:
                    menage_nth['personne_de_reference'] = id
                else:
                    menage_nth['conjoint'] = id
            else:
                menage_nth.setdefault('enfants', []).append(id)

        count_so_far += len(group)
        menages["m{}".format(nth)] = menage_nth

    dict = {
        'period': period,
        'menages': menages,
        'individus': individus
        }
    if axes:
        dict['axes'] = axes
    scenario.init_from_dict(dict)
    return scenario
