# -*- coding: utf-8 -*-

import os
import pandas as pd
import pkg_resources

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.examples.calage_bdf_cn_energy import get_inflators_by_year_energy
from openfisca_france_indirect_taxation.examples.utils_example import graph_builder_bar, dataframe_by_group
from openfisca_france_indirect_taxation.projects.base import nombre_paquets_cigarettes_by_year
from openfisca_france_indirect_taxation.projects.calage_depenses_cigarettes import create_reforme_calage_depenses_cigarettes
from openfisca_france_indirect_taxation.projects.budget_2019.reforme_tabac_budgets_2018_2019 import create_reforme_tabac_budgets_2018_2019

inflators_by_year = get_inflators_by_year_energy(rebuild = False)
year = 2016
data_year = 2011
inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

simulated_variables = [
    'depenses_cigarettes_calibre_par_decile',
    'depenses_cigarettes_calibre_apres_reforme_mars_2018',
    'depenses_cigarettes_calibre_apres_reforme_mars_2019',
    'depenses_cigarettes_calibre_apres_reforme_novembre_2019',
    'depenses_cigares',
    'depenses_tabac_a_rouler',
    'depenses_tabac_a_rouler_apres_reforme_mars_2018',
    'depenses_tabac_a_rouler_apres_reforme_mars_2019',
    'depenses_tabac_a_rouler_apres_reforme_novembre_2019',
    'depenses_tabac_calibre',
    'rev_disp_loyerimput',
    'depenses_tot',
    'pondmen',
    'depenses_tabac_post_reforme',
    ]

tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()

for baseline_year in ['2017', '2018']:
    
    # Recalage des dépenses de cigarettes BDF sur consommations agrégées officielles

    reforme_calage = create_reforme_calage_depenses_cigarettes(
        agregat_depenses = nombre_paquets_cigarettes_by_year[int(baseline_year)], 
        year_calage =  baseline_year,
    )
    tax_benefit_system = reforme_calage(tax_benefit_system)

    # Applicatin des réformes de la fiscalité tabac
    
    reform = create_reforme_tabac_budgets_2018_2019(baseline_year = baseline_year)
    tax_benefit_system = reform(tax_benefit_system)

    survey_scenario = SurveyScenario.create(
        inflation_kwargs = inflation_kwargs,
        tax_benefit_system = tax_benefit_system,
        year = year,
        data_year = data_year
        )
    
    df_reforme = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)['menage']
    df = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables)
           
    print(survey_scenario.compute_aggregate(variable = 'depenses_cigarettes_calibre', period = year)/1e9)

    df['variation_depenses_tabac'] = (
        df['depenses_tabac_post_reforme'] 
         - df['depenses_tabac_calibre']
         )
    df['variation_relative_depenses_tabac'] = (
        df['variation_depenses_tabac']
        / df['rev_disp_loyerimput']
        )
    graph_builder_bar(df['variation_relative_depenses_tabac'], False)
    print("Coût total de la réforme (baseline : {}): {} milliards d'euros".format(
        baseline_year,
        df['variation_depenses_tabac'].mean() * df_reforme['pondmen'].sum() / 1e9)
        )

    if baseline_year == '2017':
        reforme = "2018_2019"
    if baseline_year == '2018':
        reforme = "2019"
    test_assets_directory = os.path.join(
        pkg_resources.get_distribution('openfisca_france_indirect_taxation').location,
        'openfisca_france_indirect_taxation',
        'assets',
        'tests'
        )
    resultats_a_reproduire = pd.read_csv(
        os.path.join(test_assets_directory, "resultats_reformes_tabac_budget_{}.csv".format(reforme)),
        header = None
        )
    df['ecart'] = abs(
        df['variation_relative_depenses_tabac'].values 
        - resultats_a_reproduire[0].values
        )
    df['resultats_a_reproduire'] = resultats_a_reproduire[0].values
    assert (df['ecart'] < 1e-5).all()
