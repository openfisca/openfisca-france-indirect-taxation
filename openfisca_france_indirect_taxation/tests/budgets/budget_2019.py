# TODO : les résultats qui servent de cibles ne semblent pas bon après les corrections faites fin 2021 / début 2022.
#  Il faudrait refaire le test avec de nouvelles cibles.

# import numpy as np
# import os
# import pandas as pd
# import pytest

# from openfisca_france_indirect_taxation.location import openfisca_france_indirect_taxation_location
# from openfisca_france_indirect_taxation.projects.budgets.simul_reformes_tabac import simulate_reforme_tabac
# from openfisca_france_indirect_taxation.projects.budgets.simul_reformes_energie import simulate_reformes_energie
# from openfisca_france_indirect_taxation.assets.tests.resultats_reformes_energie_thomas_initial import results


# @pytest.mark.parametrize("baseline_year", ['2017', '2018'])
# def test_plf_2019_reforme_tabac(baseline_year):
#     variation_relative_depenses_tabac = simulate_reforme_tabac(year = 2019, baseline_year = baseline_year, graph = False)
#     assert baseline_year in ['2017', '2018']
#     if baseline_year == '2017':
#         reforme = "2018_2019"
#     if baseline_year == '2018':
#         reforme = "2019"
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


# def test_plf_2019_reformes_energie():
#     df = simulate_reformes_energie(graph = False)
#     for variable in results.columns:
#         # assert ((df['{}'.format(variable)] - results['{}'.format(variable)]) < 1).all()
#         np.testing.assert_allclose(
#             df['{}'.format(variable)].values,
#             results['{}'.format(variable)].values,
#             atol = 5
#             )
