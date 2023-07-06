# On essaye de réutiliser le code ~\openfisca_france_indirect_taxation\examples\benjello_candidates_to_removal\master_thesis\loosers_within_income_deciles.py
import numpy
import pandas as pd
import os
import seaborn as sns
from matplotlib import pyplot as plt

from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    wavg,
    collapse,
    dataframe_by_group,
    graph_builder_bar)
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.budgets.reforme_energie_budgets_2018_2019 import officielle_2019_in_2017
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy


ident_men = pd.DataFrame(pd.HDFStore("C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data/data_collections/output/openfisca_indirect_taxation_data_2017.h5")['input']['ident_men'])
ident_men['ident_men'] = ident_men.ident_men.astype(numpy.int64)

data_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data"
output_path = os.path.join(data_path,'donnees_simulations')
                           
df_elasticities = pd.read_csv(os.path.join(data_path,'Elasticities_literature.csv'), sep = ";")
df_elasticities[['elas_price_1_1','elas_price_2_2','elas_price_3_3']].astype(float)
    
def simulate_reformes_energie(elasticites,year,reform):

    data_year = 2017
    # on veut faire les simulations sur les quantités avant réforme
    # idéalement on voudrait l'évolution des quantités pour les années jusque 2022 s'il n'y avait pas eu de réforme
    # mais en l'absence d'information on considère que la consommation reste constante dans le contrefactuel.
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    inflators_by_year[2018] = inflators_by_year[2017]
    inflators_by_year[2019] = inflators_by_year[2017]
    inflators_by_year[2020] = inflators_by_year[2017]
    inflators_by_year[2021] = inflators_by_year[2017]
    inflators_by_year[2022] = inflators_by_year[2017]

    # elasticités : le programme de T. Douenne n'a pas été bien adapté (pas le temps) et du coup on a pas d'élasticité pour tout le monde
    # on prend des élasticités agrégées par type de bien
    ident_men['elas_price_1_1'] = elasticites['elas_price_1_1'].reset_index()['elas_price_1_1'][0] # transport fuel
    ident_men['elas_price_2_2'] = elasticites['elas_price_2_2'].reset_index()['elas_price_2_2'][0] # housing fuel
    ident_men['elas_price_3_3'] = elasticites['elas_price_3_3'].reset_index()['elas_price_3_3'][0] # other non durable goods ??

    elasticities = ident_men

    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    simulated_variables = [
        'cheques_energie',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        ]

    baseline_tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    asof(baseline_tax_benefit_system, "2018-01-01")  # A modifier
    survey_scenario = SurveyScenario.create(
        elasticities = elasticities,
        inflation_kwargs = inflation_kwargs,
        baseline_tax_benefit_system = baseline_tax_benefit_system,
        reform = reform,
        year = year,
        data_year = data_year
        )

    indiv_df_reform = survey_scenario.create_data_frame_by_entity(simulated_variables, period = year)
    menages_reform= indiv_df_reform['menage']

    menages_reform['Net_apres_cheques_energie'] = menages_reform['cheques_energie'] - \
        (menages_reform['ticpe_totale_'+ reform.key[0]] - menages_reform['ticpe_totale']) 
    menages_reform['taux_effort'] = (menages_reform['ticpe_totale_carbon_tax_rv'] - menages_reform['ticpe_totale']) / menages_reform['rev_disp_loyerimput'] * 100
    menages_reform['is_losers'] = menages_reform['Net_apres_cheques_energie'] <0 
    
    to_graph = pd.DataFrame(data = {'niveau_vie_decile' : [1.0 , 2.0 , 3.0 , 4.0, 5.0 , 6.0 , 7.0 , 8.0 , 9.0 , 10.0, 'Total']})
    for var in ['is_losers','taux_effort','Net_apres_cheques_energie']:
        by_decile = pd.DataFrame(data = collapse(menages_reform,'niveau_vie_decile',var)).reset_index().rename(columns = { 0 : var}) 
        total = pd.DataFrame(data = {'niveau_vie_decile' : 'Total', var : wavg(menages_reform, var)}, index = [0]) 
        to_merge = pd.concat([by_decile, total])
        to_graph = to_graph.merge(right = to_merge, how = 'inner', on = 'niveau_vie_decile') 
    
    ref_elasticity = elasticites['ref_elasticity'].reset_index()['ref_elasticity'][0]
    menages_reform['ref_elasticity'] = ref_elasticity
    to_graph['ref_elasticity'] = ref_elasticity
    return (to_graph,menages_reform)

def run_all_elasticities(data_elasticities = df_elasticities, year = 2019, reform = officielle_2019_in_2017):
    to_graph = pd.DataFrame(columns = {'ref_elasticity','niveau_vie_decile','is_losers','taux_effort','Net_apres_cheques_energie'})
    menages_reform = pd.DataFrame(columns = {'ref_elasticity', 
        'cheques_energie',       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        'rev_disp_loyerimput',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        })
    for elas in data_elasticities['ref_elasticity']:
        elasticities = data_elasticities[data_elasticities['ref_elasticity'] == elas]
        to_concat = simulate_reformes_energie(elasticites = elasticities, year = year, reform = reform)
        to_graph = pd.concat([to_graph,to_concat[0]])
        menages_reform = pd.concat([menages_reform, to_concat[1]])
    return (to_graph,menages_reform)
    
def graph_winners_losers(data,year):
    plt.figure(figsize= (10,7.5)) 
    # Si on veut avoir la part de gagnants qui complète la bar jusqu'à 1 
    #data['total'] = 1
    #bar1 = sns.barplot(x="niveau_vie_decile", y = 'total', data = data, hue = 'ref_elasticity', palette = sns.color_palette("muted"), saturation = .2, width=.9)
    bar2 = sns.barplot(x="niveau_vie_decile", y = 'losers', data = data, hue = 'ref_elasticity', palette = sns.color_palette("Paired"), width = .9)
    plt.xlabel('Revenu decile', fontdict = {'fontsize' : 12})
    plt.ylabel('Share of net losers from the reform', fontdict = {'fontsize' : 12})
    plt.legend()
    plt.savefig(os.path.join(path,'Winners_losers_reform_{}_year{}.png'.format(reform.key[0],year)))    
    return

