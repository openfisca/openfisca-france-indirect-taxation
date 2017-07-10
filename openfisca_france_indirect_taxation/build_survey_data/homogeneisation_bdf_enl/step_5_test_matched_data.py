# -*- coding: utf-8 -*-

# Dans ce script, on test la qualité de l'appariement.

from __future__ import division


import pandas as pd

import os
import pkg_resources


# Importation des bases de données appariées et de la base de référence ENL
default_config_files_directory = os.path.join(
    pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)


data_enl = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matching_enl.csv'
        ), sep =',', decimal = '.'
    )


data_matched = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched.csv'
        ), sep =',', decimal = '.'
    )

    
data_matched_random = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_random.csv'
        ), sep =',', decimal = '.'
    )


data_matched_rank = pd.read_csv(
    os.path.join(
        default_config_files_directory,
        'openfisca_france_indirect_taxation',
        'assets',
        'matching',
        'data_matched_rank.csv'
        ), sep =',', decimal = '.'
    )



"""
Test : share of people having trouble with heat in general
    With sampling weights
"""

# In total
print sum(data_enl['pondmen'] * (data_enl['gchauf_n'] != 0)) / sum(data_enl['pondmen'])
print sum(data_matched['pondmen'] * (data_matched['gchauf_n'] != 0)) / sum(data_matched['pondmen'])
print sum(data_matched_random['pondmen'] * (data_matched_random['gchauf_n'] != 0)) / sum(data_matched_random['pondmen'])
print sum(data_matched_rank['pondmen'] * (data_matched_rank['gchauf_n'] != 0)) / sum(data_matched_rank['pondmen'])

# By income decile
for i in range(1,11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    data_matched_rank_decile = data_matched_rank.query('niveau_vie_decile == {}'.format(i))
    
    print i, 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_n'] != 0)) / sum(data_enl_decile['pondmen']), \
        100 * sum(data_matched_decile['pondmen'] * (data_matched_decile['gchauf_n'] != 0)) / sum(data_matched_decile['pondmen']), \
        100 * sum(data_matched_random_decile['pondmen'] * (data_matched_random_decile['gchauf_n'] != 0)) / sum(data_matched_random_decile['pondmen']), \
        100 * sum(data_matched_rank_decile['pondmen'] * (data_matched_rank_decile['gchauf_n'] != 0)) / sum(data_matched_rank_decile['pondmen'])

    del data_enl_decile, data_matched_decile, data_matched_random_decile, data_matched_rank_decile

"""
Test : share of people having trouble with heat because of the cost
    With sampling weights
"""

# In total
print 100 * sum(data_enl['pondmen'] * (data_enl['gchauf_3'] == 1)) / sum(data_enl['pondmen'])
print 100 * sum(data_matched['pondmen'] * (data_matched['gchauf_3'] == 1)) / sum(data_matched['pondmen'])
print 100 * sum(data_matched_random['pondmen'] * (data_matched_random['gchauf_3'] == 1)) / sum(data_matched_random['pondmen'])
print 100 * sum(data_matched_rank['pondmen'] * (data_matched_rank['gchauf_3'] == 1)) / sum(data_matched_rank['pondmen'])

# By income decile
for i in range(1,11):
    data_enl_decile = data_enl.query('niveau_vie_decile == {}'.format(i))
    data_matched_decile = data_matched.query('niveau_vie_decile == {}'.format(i))
    data_matched_random_decile = data_matched_random.query('niveau_vie_decile == {}'.format(i))
    data_matched_rank_decile = data_matched_rank.query('niveau_vie_decile == {}'.format(i))
    
    print i, 100 * sum(data_enl_decile['pondmen'] * (data_enl_decile['gchauf_3'] == 1)) / sum(data_enl_decile['pondmen']), \
        100 * sum(data_matched_decile['pondmen'] * (data_matched_decile['gchauf_3'] == 1)) / sum(data_matched_decile['pondmen']), \
        100 * sum(data_matched_random_decile['pondmen'] * (data_matched_random_decile['gchauf_3'] == 1)) / sum(data_matched_random_decile['pondmen']), \
        100 * sum(data_matched_rank_decile['pondmen'] * (data_matched_rank_decile['gchauf_3'] == 1)) / sum(data_matched_rank_decile['pondmen'])

    del data_enl_decile, data_matched_decile, data_matched_random_decile, data_matched_rank_decile
    


"""
Test : share of people having trouble with heat in general
"""

# In total
print float(len(data_enl.query('gchauf_n != 0'))) / len(data_enl) * 100
print float(len(data_matched.query('gchauf_n != 0'))) / len(data_matched) * 100
print float(len(data_matched_random.query('gchauf_n != 0'))) / len(data_matched_random) * 100
print float(len(data_matched_rank.query('gchauf_n != 0'))) / len(data_matched_rank) * 100


# By income decile
for i in range(1,11):
    number_enl = len(data_enl.query('niveau_vie_decile == {}'.format(i)))
    number_matched = len(data_matched.query('niveau_vie_decile == {}'.format(i)))
    number_matched_random = len(data_matched_random.query('niveau_vie_decile == {}'.format(i)))
    number_matched_rank = len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)))

    number_enl_gchauf_n = \
        len(data_enl.query('niveau_vie_decile == {}'.format(i)).query('gchauf_n != 0'))
    number_matched_gchauf_n = \
        len(data_matched.query('niveau_vie_decile == {}'.format(i)).query('gchauf_n != 0'))
    number_matched_random_gchauf_n = \
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('gchauf_n != 0'))
    number_matched_rank_gchauf_n = \
        len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)).query('gchauf_n != 0'))
    
    gchauf_n_enl = (
        float(number_enl_gchauf_n) /
        number_enl
        )
    gchauf_n_matched = (
        float(number_matched_gchauf_n) /
        number_matched
        )
    gchauf_n_matched_random = (
        float(number_matched_random_gchauf_n) /
        number_matched_random
        )
    gchauf_n_matched_rank = (
        float(number_matched_rank_gchauf_n) /
        number_matched_rank
        )
    
    print i, gchauf_n_enl * 100, gchauf_n_matched * 100, \
        gchauf_n_matched_random * 100, gchauf_n_matched_rank * 100


# By size of urban unit
for i in range(1,9):
    number_enl = len(data_enl.query('tuu == {}'.format(i)))
    number_matched = len(data_matched.query('tuu == {}'.format(i)))

    number_enl_gchauf_n = \
        len(data_enl.query('tuu == {}'.format(i)).query('gchauf_n != 0'))
    number_matched_gchauf_n = \
        len(data_matched.query('tuu == {}'.format(i)).query('gchauf_n != 0'))
    
    gchauf_n_enl = (
        float(number_enl_gchauf_n) /
        number_enl
        )
    gchauf_n_matched = (
        float(number_matched_gchauf_n) /
        number_matched
        )
    
    print i, gchauf_n_enl * 100, gchauf_n_matched * 100

    
"""
Test : share of people having trouble with heat because it is too expensive
"""

# In total
print float(len(data_enl.query('gchauf_3 == 1'))) / len(data_enl) * 100
print float(len(data_matched.query('gchauf_3 == 1'))) / len(data_matched) * 100
print float(len(data_matched_random.query('gchauf_3 == 1'))) / len(data_matched_random) * 100
print float(len(data_matched_rank.query('gchauf_3 == 1'))) / len(data_matched_rank) * 100


# By income niveau_vie_decile
for i in range(1,11):
    number_enl = len(data_enl.query('niveau_vie_decile == {}'.format(i)))
    number_matched = len(data_matched.query('niveau_vie_decile == {}'.format(i)))
    number_matched_random = len(data_matched_random.query('niveau_vie_decile == {}'.format(i)))
    number_matched_rank = len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)))

    
    number_enl_gchauf_3 = \
        len(data_enl.query('niveau_vie_decile == {}'.format(i)).query('gchauf_3 == 1'))
    number_matched_gchauf_3 = \
        len(data_matched.query('niveau_vie_decile == {}'.format(i)).query('gchauf_3 == 1'))
    number_matched_random_gchauf_3 = \
        len(data_matched_random.query('niveau_vie_decile == {}'.format(i)).query('gchauf_3 == 1'))
    number_matched_rank_gchauf_3 = \
        len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)).query('gchauf_3 == 1'))
    
    gchauf_3_enl = (
        float(number_enl_gchauf_3) /
        number_enl
        )
    gchauf_3_matched = (
        float(number_matched_gchauf_3) /
        number_matched
        )
    gchauf_3_matched_random = (
        float(number_matched_random_gchauf_3) /
        number_matched_random
        )
    gchauf_3_matched_rank = (
        float(number_matched_rank_gchauf_3) /
        number_matched_rank
        )
    
    print i, gchauf_3_enl * 100, gchauf_3_matched * 100, \
        gchauf_3_matched_random * 100, gchauf_3_matched_rank * 100


# By size of urban unit
for i in range(1,9):
    number_enl = len(data_enl.query('tuu == {}'.format(i)))
    number_matched = len(data_matched.query('tuu == {}'.format(i)))

    number_enl_gchauf_3 = \
        len(data_enl.query('tuu == {}'.format(i)).query('gchauf_3 == 1'))
    number_matched_gchauf_3 = \
        len(data_matched.query('tuu == {}'.format(i)).query('gchauf_3 == 1'))
    
    gchauf_3_enl = (
        float(number_enl_gchauf_3) /
        number_enl
        )
    gchauf_3_matched = (
        float(number_matched_gchauf_3) /
        number_matched
        )
    
    print i, gchauf_3_enl * 100, gchauf_3_matched * 100
    


"""
Test : share of people having trouble with heat because of bad isolation
"""

# By income decile
for i in range(1,11):
    number_enl = len(data_enl.query('niveau_vie_decile == {}'.format(i)))
    number_matched = len(data_matched.query('niveau_vie_decile == {}'.format(i)))
    number_matched_rank = len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)))

    number_enl_gchauf_4 = \
        len(data_enl.query('niveau_vie_decile == {}'.format(i)).query('gchauf_4 == 1'))
    number_matched_gchauf_4 = \
        len(data_matched.query('niveau_vie_decile == {}'.format(i)).query('gchauf_4 == 1'))
    number_matched_rank_gchauf_4 = \
        len(data_matched_rank.query('niveau_vie_decile == {}'.format(i)).query('gchauf_4 == 1'))
    
    gchauf_4_enl = (
        float(number_enl_gchauf_4) /
        number_enl
        )
    gchauf_4_matched = (
        float(number_matched_gchauf_4) /
        number_matched
        )
    gchauf_4_matched_rank = (
        float(number_matched_rank_gchauf_4) /
        number_matched_rank
        )
    
    print i, gchauf_4_enl * 100, gchauf_4_matched * 100, gchauf_4_matched_rank * 100


# By size of urban unit
for i in range(1,9):
    number_enl = len(data_enl.query('tuu == {}'.format(i)))
    number_matched = len(data_matched.query('tuu == {}'.format(i)))

    number_enl_gchauf_4 = \
        len(data_enl.query('tuu == {}'.format(i)).query('gchauf_4 == 1'))
    number_matched_gchauf_4 = \
        len(data_matched.query('tuu == {}'.format(i)).query('gchauf_4 == 1'))
    
    gchauf_4_enl = (
        float(number_enl_gchauf_4) /
        number_enl
        )
    gchauf_4_matched = (
        float(number_matched_gchauf_4) /
        number_matched
        )
    
    print i, gchauf_4_enl * 100, gchauf_4_matched * 100
    

    
"""
Placebo test for share of revenue spent in energies :
    How well do we do among income deciles, area and age ?
"""

# Incomes deciles :
for i in range(1,11):
    data_decuc = data_matched.query('decuc == {}'.format(i))
    before = (data_decuc['part_energies_revtot_before'] * data_decuc['pondmen']).sum() / data_decuc['pondmen'].sum()
    after = (data_decuc['part_energies_revtot_after'] * data_decuc['pondmen']).sum() / data_decuc['pondmen'].sum()

    print i, before * 100, after * 100
    del data_decuc

# Area of residence :
for i in [111, 112, 120, 211, 212, 221, 300, 400]: #222
    data_cataeu = data_matched.query('cataeu == {}'.format(i))
    after = (data_cataeu['part_energies_revenu'] * data_cataeu['pondmen']).sum() / data_cataeu['pondmen'].sum()
    before = (data_cataeu['part_energies_revtot'] * data_cataeu['pondmen']).sum() / data_cataeu['pondmen'].sum()

    print i, before * 100, after * 100
    del data_cataeu

# Age :
for i in [25, 35, 45, 55, 65, 75, 85]: 
    data_age = data_matched.query('{0} < agepr < {1}'.format(i - 11, i))
    after = (data_age['part_energies_revenu'] * data_age['pondmen']).sum() / data_age['pondmen'].sum()
    before = (data_age['part_energies_revtot'] * data_age['pondmen']).sum() / data_age['pondmen'].sum()

    print i, before * 100, after * 100
    del data_age
