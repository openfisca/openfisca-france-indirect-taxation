import numpy
import pandas as pd
import os
import ast
import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

from wquantiles import quantile
from openfisca_survey_manager.utils import asof

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.examples.utils_example import (
    wavg,
    collapse,
    dataframe_by_group,
    graph_builder_bar,
    df_weighted_average_grouped)
from openfisca_france_indirect_taxation.almost_ideal_demand_system.utils import add_niveau_vie_decile
from openfisca_france_indirect_taxation.surveys import SurveyScenario
from openfisca_france_indirect_taxation.projects.Master_Thesis_Herve.Reform_carbon_tax import carbon_tax_rv
from openfisca_france_indirect_taxation.calibration import get_inflators_by_year_energy

data_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data"
output_path = "C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Output"
                           
df_elasticities = pd.read_csv(os.path.join(data_path,'Reform_parameters/Elasticities_literature.csv'), sep = ";")
df_elasticities[['elas_price_1_1','elas_price_2_2','elas_price_3_3']].astype(float)

df_elas_vect = pd.read_csv(os.path.join(data_path,'Reform_parameters/Elasticities_Douenne_20.csv'), index_col = [0])
df_elas_vect = pd.melt(frame = df_elas_vect , id_vars = ["niveau_vie_decile", 'ref_elasticity'], var_name = 'strate_2', value_name = 'elas_price_1_1')
    
def simulate_reformes_energie(elas_vect, elasticites, year, reform, bonus_cheques_uc):

    ident_men = pd.HDFStore("C:/Users/veve1/OneDrive/Documents/ENSAE 3A/Memoire MiE/Data/data_collections/output/openfisca_indirect_taxation_data_2017.h5")['input'][['ident_men','pondmen', 'rev_disponible','ocde10','strate']]
    ident_men['ident_men'] = ident_men.ident_men.astype(numpy.int64)
    ident_men = add_niveau_vie_decile(ident_men)

    data_year = 2017
    inflators_by_year = get_inflators_by_year_energy(rebuild = True, year_range = range(2011, 2020), data_year = data_year)
    
    if elas_vect == True :
        # elasticités vectorielles : on a une elasctitié-prix du carburant par décile de niveau de vie x type de ville 
        dict_strate = { 0 : 'Rural' , 1 : 'Small cities' , 2 : 'Medium cities' , 3 : 'Large cities' , 4 : 'Paris'}
        ident_men['strate_2'] = ident_men['strate'].apply(lambda x : dict_strate.get(x))
        ident_men = ident_men.merge(right = elasticites , how = 'inner' , on = ['niveau_vie_decile','strate_2'])
        ident_men['elas_price_1_1'] = ident_men['elas_price_1_1'].apply( lambda x : ast.literal_eval(x)[0])
        ident_men = ident_men[['ident_men','elas_price_1_1']]
    
    else:
        # elasticités scalaires : on prend des élasticités agrégées par type de bien
        ident_men['elas_price_1_1'] = elasticites['elas_price_1_1'].reset_index()['elas_price_1_1'][0] # transport fuel
        ident_men['elas_price_2_2'] = elasticites['elas_price_2_2'].reset_index()['elas_price_2_2'][0] # housing fuel
        ident_men['elas_price_3_3'] = elasticites['elas_price_3_3'].reset_index()['elas_price_3_3'][0] # other non durable goods ??
        ident_men = ident_men[['ident_men','elas_price_1_1','elas_price_2_2','elas_price_3_3']]
        
    elasticities = ident_men 
        
    inflation_kwargs = dict(inflator_by_variable = inflators_by_year[year])

    simulated_variables = [
        'bonus_cheques_energie_uc',
        'bonus_cheques_energie_menage',
        'contributions_reforme',
        'emissions_CO2_carburants',
        'emissions_CO2_carburants_'+ reform.key[0],
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        #'rev_disp_loyerimput', plutot rev_disponible pour être cohérent
        'rev_disponible',
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
    menages_reform = indiv_df_reform['menage']
    df_sum = dataframe_by_group(survey_scenario, category = 'niveau_vie_decile', variables = simulated_variables, aggfunc = 'sum')

    # Certains ménages tout en bas de la distribution des revenus disp ont des revenus nuls ou très proches de 0.
    # On va remplacer tous les ménages des 2 premiers percentiles par un ménage moyen qui porte tout le poids de ces 2 percentiles:
    
    # On calcule le 2e percentile (de la distribution des revenus) et on prend cette tranche du dataframe.
    rev_disponible_2_perc = menages_reform['rev_disponible'].quantile(0.02)
    perc_2 = menages_reform[menages_reform['rev_disponible'] <= rev_disponible_2_perc]

    # On calcule la moyenne pondéré pour les variables de la simuation et on affecte à la variable de pondération, la somme de toutes les pondérations.
    list_var = simulated_variables
    list_var.remove('pondmen')
    average_perc_2 = df_weighted_average_grouped(perc_2,'niveau_vie_decile',list_var)
    average_perc_2['pondmen'] = perc_2['pondmen'].sum()
    
    # On retire ces ménages du dataframe menages_reform et on remplace par le ménage moyen
    menages_reform = menages_reform[menages_reform['rev_disponible'] > rev_disponible_2_perc] 
    menages_reform = pd.concat([menages_reform,average_perc_2])

    # Les effets qui vont nous intéresser : le taux d'effort, les transferts nets dus à la réforme et les gagnants/perdants de la réforme.
    menages_reform['Effort_rate'] = menages_reform['contributions_reforme'] / menages_reform['rev_disponible'] * 100
    
    if bonus_cheques_uc == True :
        menages_reform['Net_transfers_reform'] = menages_reform['bonus_cheques_energie_uc'] - menages_reform['contributions_reforme']
    else :  
        menages_reform['Net_transfers_reform'] = menages_reform['bonus_cheques_energie_menage'] - menages_reform['contributions_reforme']
         
    menages_reform['Is_losers'] = menages_reform['Net_transfers_reform'] < 0
    menages_reform['Reduction_CO2'] = (menages_reform['emissions_CO2_carburants_carbon_tax_rv'] / menages_reform['emissions_CO2_carburants'] - 1)*100
    menages_reform['Reduction_CO2'] = menages_reform['Reduction_CO2'].fillna(0) 
    
    ref_elasticity = elasticites['ref_elasticity'].reset_index()['ref_elasticity'][0]
    menages_reform['ref_elasticity'] = ref_elasticity
    menages_reform['niveau_vie_decile'] = menages_reform['niveau_vie_decile'].astype(int)
    var_to_graph = ['Is_losers', 'Effort_rate', 'Net_transfers_reform', 'emissions_CO2_carburants_carbon_tax_rv', 'emissions_CO2_carburants' ]
    by_decile = df_weighted_average_grouped(menages_reform,'niveau_vie_decile',var_to_graph).reset_index()
    total = df_weighted_average_grouped(menages_reform,'ref_elasticity',var_to_graph).reset_index().drop('ref_elasticity',axis = 1)
    total['niveau_vie_decile'] = 'Total'
    to_graph = pd.concat([by_decile, total])
    to_graph['emissions_CO2_carburants_carbon_tax_rv'] = to_graph['emissions_CO2_carburants_carbon_tax_rv']/1000
    to_graph['emissions_CO2_carburants'] = to_graph['emissions_CO2_carburants']/1000
    to_graph['Reduction_CO2'] = (to_graph['emissions_CO2_carburants_carbon_tax_rv']/ to_graph['emissions_CO2_carburants'] - 1)*100
    to_graph['ref_elasticity'] = ref_elasticity
    
    return (to_graph, menages_reform, df_sum)

def run_all_elasticities(data_elasticities = df_elasticities, year = 2019, reform = carbon_tax_rv,bonus_cheques_uc = True):
    to_graph = pd.DataFrame(columns = {'ref_elasticity','niveau_vie_decile','Is_losers','Effort_rate','Net_transfers_reform','Reduction_CO2'})
    menages_reform = pd.DataFrame(columns = {'ref_elasticity', 
        'bonus_cheques_energie_uc',
        'bonus_cheques_energie_menage',
        'contributions_reforme',
        'emissions_CO2_carburants',
        'emissions_CO2_carburants_'+ reform.key[0],       
        'ticpe_totale',
        'ticpe_totale_'+ reform.key[0],
        #'rev_disp_loyerimput',
        'rev_disponible',
        'pondmen',
        'ocde10',
        'niveau_vie_decile'
        })
    for elas in data_elasticities['ref_elasticity']:
        elasticities = data_elasticities[data_elasticities['ref_elasticity'] == elas]
        to_concat = simulate_reformes_energie(elas_vect = False, elasticites = elasticities, year = year, reform = reform, bonus_cheques_uc = bonus_cheques_uc)
        to_graph = pd.concat([to_graph,to_concat[0]])
        menages_reform = pd.concat([menages_reform, to_concat[1]])
    return (to_graph,menages_reform)