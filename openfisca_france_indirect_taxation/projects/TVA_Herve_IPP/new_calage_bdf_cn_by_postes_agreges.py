import pandas as pd
import os 
import csv 

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.utils import assets_directory, get_input_data_frame
from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

''' Données sources utilisées : 
    - Consommation des ménages en 2023 (base 2020) : https://www.insee.fr/fr/statistiques/fichier/8068592/T_CONSO_EFF_FONCTION.xlsx 
    - Revenu disponible des ménages en 2023 (base 2020) :  https://www.insee.fr/fr/statistiques/fichier/8068630/T_2101.xlsx
    - Comptes trimestriels pour l'année 2024 (base 2020) : https://www.insee.fr/fr/statistiques/fichier/8358378/t_conso_val.xls
    '''
    
def get_bdf_aggregates(data_year = None):
    ''' Calcule les agrégats de Bdf pour l'année des données.'''
    assert data_year is not None
    depenses = get_input_data_frame(2017)
    liste_variables = depenses.columns.tolist()
    postes_agreges = ['poste_{}'.format(index) for index in ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12", "13"]]
    for poste in postes_agreges:
        depenses[poste] = 0
        for element in liste_variables:
            if element[:8] == poste:
                depenses[poste] += depenses[element]
            
    depenses_by_poste_agrege = depenses[postes_agreges]      
    depenses_by_poste_agrege = pd.concat([depenses_by_poste_agrege, depenses['pondmen']], axis = 1)
    bdf_aggregates_by_poste_agrege = pd.DataFrame()
    for poste_agrege in postes_agreges:
        bdf_aggregates_by_poste_agrege.loc[poste_agrege, 'bdf_aggregates'] = (depenses_by_poste_agrege[poste_agrege] * depenses_by_poste_agrege['pondmen']).sum()
        
    return bdf_aggregates_by_poste_agrege

def get_cn_aggregates(target_year = None):
    ''' Calcule les agrégats de compta nat utilisables pour un année cible.'''
    assert target_year is not None

    parametres_fiscalite_file_path = os.path.join(
            assets_directory,
            'legislation',
            'conso_eff_fonction_2023.xls'
            )

    masses_cn_data_frame = pd.read_excel(parametres_fiscalite_file_path, sheet_name = "MEURcour", header = 4)
    masses_cn_data_frame.rename(columns={'Unnamed: 0' : 'Code' , 'Unnamed: 1' : 'Label'}, inplace = True)
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', '{}'.format(target_year)]].copy()
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame.loc[:,'Code'].str.replace(r'^CP','',regex=True)
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame.loc[:,'Code'].str.strip()
    
    
    codes_postes_agreges = ["0{}".format(i) for i in range(1, 10)] + ["10", "11", "12","13"]

    masses_cn_13postes_data_frame = masses_cn_data_frame.loc[masses_cn_data_frame['Code'].isin(codes_postes_agreges)]
    masses_cn_13postes_data_frame.loc[:,'Code'] = masses_cn_13postes_data_frame.loc[:,'Code'].astype(str).apply(lambda x: f"poste_{x}")
    masses_cn_13postes_data_frame.set_index('Code', inplace = True)
    masses_cn_13postes_data_frame.rename(columns= {'{}'.format(target_year): 'conso_CN_{}'.format(target_year)}, inplace= True)

    return masses_cn_13postes_data_frame*1e6

def get_inflators_bdf_to_cn(data_year):
    '''Calcule l'inflateur de calage à partir des masses de comptabilité nationale.'''    
    data_cn = get_cn_aggregates(data_year)
    data_bdf = get_bdf_aggregates(data_year)
    masses = data_cn.merge(data_bdf, left_index = True, right_index = True)
    masses.rename(columns = {'bdf_aggregates': 'conso_bdf{}'.format(data_year)}, inplace = True)
    
    return (masses['conso_CN_{}'.format(data_year)] / masses['conso_bdf{}'.format(data_year)]).to_dict()

def get_inflators_cn_to_cn(target_year, data_year):
    '''
        Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.
    '''
    data_year_cn_aggregates = get_cn_aggregates(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    return dict(
        (key, target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        for key in list(data_year_cn_aggregates.keys())
        )
    
def get_inflators(target_year,data_year):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    inflators_bdf_to_cn = get_inflators_bdf_to_cn(data_year)
    inflators_cn_to_cn = get_inflators_cn_to_cn(target_year,data_year)
    
    tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    liste_variables = list(tax_benefit_system.variables.keys())
    ratio_by_variable = dict()
    for element in liste_variables:
        for key in list(inflators_cn_to_cn.keys()):
            if element[:8] == key:
                ratio_by_variable[element] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]

    return ratio_by_variable

def get_inflators_by_year(rebuild = False, year_range = None, data_year = None):
    if year_range is None:
        year_range = range(2000, 2020)

    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in year_range:
            inflators = get_inflators(target_year = target_year, data_year = data_year)
            inflators_by_year[target_year] = inflators

        writer_inflators = csv.writer(open(os.path.join(assets_directory, 'inflateurs', 'inflators_by_postes_agreges_by_year.csv'), 'w'))
        for year in year_range:
            for key, value in list(inflators_by_year[year].items()):
                writer_inflators.writerow([key, value, year])

        return inflators_by_year
    else:
        re_build_inflators = dict()
        inflators_from_csv = pd.read_csv(os.path.join(assets_directory, 'inflateurs', 'inflators_by_postes_agreges_by_year.csv'),
            index_col = 0, header = None)
        for year in year_range:
            inflators_from_csv_by_year = inflators_from_csv[inflators_from_csv[2] == year]
            inflators_to_dict = pd.DataFrame.to_dict(inflators_from_csv_by_year)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators