# TODO : les résultats qui servent de cibles ne semblent pas bon après les corrections faites fin 2021 / début 2022.
#  Il faudrait refaire le test avec de nouvelles cibles.

# import numpy as np
# import os
# import pandas as pd
# import pytest

# from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location
# from openfisca_france_indirect_taxation.projects.budgets.simul_reformes_tabac import simulate_reforme_tabac


# @pytest.mark.parametrize("baseline_year", ['2017', '2019'])
# def test_plf_2020_reforme_tabac(baseline_year):
#     variation_relative_depenses_tabac = simulate_reforme_tabac(year = 2020, baseline_year = baseline_year, graph = False)
#     assert baseline_year in ['2017', '2019']
#     if baseline_year == '2017':
#         reforme = "2018_2020"
#     if baseline_year == '2019':
#         reforme = "2020"
#     test_assets_directory = os.path.join(
#         openfisca_france_indirect_taxation_location,
#         'openfisca_france_indirect_taxation',
#         'assets',
#         'tests'
#         )
#     resultats_a_reproduire = pd.read_csv(
#         os.path.join(test_assets_directory, "resultats_reformes_tabac_budget_{}.csv".format(reforme)),
#         header = None
#         )

#     np.testing.assert_allclose(
#         variation_relative_depenses_tabac,
#         resultats_a_reproduire[0].values,
#         atol = 1e-5
#         )
