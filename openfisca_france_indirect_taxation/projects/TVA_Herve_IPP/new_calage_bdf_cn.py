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
def new_get_bdf_aggregates(data_year = None):
    ''' Calcule les agrégats de Bdf pour l'année des données.'''
    assert data_year is not None
    depenses = get_input_data_frame(data_year)
    liste_variables = depenses.columns.tolist()
    liste_postes = [element for element in liste_variables if element[:6] == 'poste_'] + ['rev_disponible', 'rev_disp_yc_loyerimpute', 'loyer_impute']

    bdf_aggregates_by_poste = pd.DataFrame()
    for poste in liste_postes:
        bdf_aggregates_by_poste.loc[poste, 'bdf_aggregates'] = (depenses[poste] * depenses['pondmen']).sum()
        
    return bdf_aggregates_by_poste

def remove_prefixes(lst):
    lst_sorted = sorted(lst, key = len, reverse = True)
    filtered = []
    
    for item in lst_sorted:
        if not any(item != other and item in other for other in filtered):
            filtered.append(item)
    
    return filtered

def format_poste(code):
    if code.startswith("poste_"):
        num_part = code[6:] 
        formatted_num = "_".join([num_part[:2]] + list(num_part[2:]))
        return f"poste_{formatted_num}"
    return code

ajust_postes_cn = {
    'CP0942' : 'CP09421', #Location, entretien et réparation de gros biens durables à fonction récréactive (S)
    'CP0943' : 'CP09422', #Location et réparation de jeux, jouets et articles de loisirs (S)
    'CP0944' : 'CP09423', #Location et réparaton d'articles de sport, de matériel de camping et activités de plein air (S)
    'CP0946' : 'CP09424', #Services récréatifs et sportifs (S)
    'CP0945' : 'CP09631', #Services vétérinaires et autres pour animaux de companies
    'CP0963' : 'CP09632', #Services photographiques
    'CP081'  : 'CP0811' , #Matériel d'information et de communication
    'CP082'  : 'CP0812' , #Logiciels à l'exclusion des jeux 
    'CP102'  : 'CP1021' , #Enseignement secondaire
    'CP103'  : 'CP1022' , #Enseignement post-secondaire non supérieur
}

def sum_and_remove(data_frame, col, rows_to_sum, new_row) :
    data = data_frame.copy()
    new_index = data.index.max() + 1
    data.loc[new_index] = data[data[col].isin(rows_to_sum)].sum(numeric_only=True)
    data.loc[new_index, col ] = new_row
    data = data[~data[col].isin(rows_to_sum)]
    
    return data

def new_get_cn_aggregates(target_year) :
    ''' Calcule les agrégats de compta nat utilisables pour un année cible.'''
    # Dépenses de conso
    parametres_fiscalite_file_path = os.path.join(
            assets_directory,
            'legislation',
            'conso_eff_fonction_2023.xls'
            )

    masses_cn_data_frame = pd.read_excel(parametres_fiscalite_file_path, sheet_name = "MEURcour", header = 4)
    masses_cn_data_frame.rename(columns={'Unnamed: 0' : 'Code' , 'Unnamed: 1' : 'Label'}, inplace = True)
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', '{}'.format(target_year)]].copy()
    masses_cn_data_frame.replace(to_replace = ajust_postes_cn, inplace= True)
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame.loc[:,'Code'].str.replace(r'^CP','',regex=True)
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame.loc[:,'Code'].str.strip()

    masses_cn_data_frame.dropna(inplace = True)
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame['Code'].astype(str).apply(lambda x: f"poste_{x}")
    masses_cn_data_frame.loc[:,'Code'] = masses_cn_data_frame['Code'].astype(str).apply(lambda x: format_poste(x))

    # On garde les agrégats à un niveau supérieur pour correspondre à Bdf
    masses_cn_data_frame = masses_cn_data_frame[~masses_cn_data_frame['Code'].isin(['poste_04_2_1', 'poste_04_2_2','poste_05_1_1','poste_05_1_2','poste_05_2_1', 'poste_05_2_2'])]
    
    # On regroupe certains postes de consommation sous la même étiquette 
    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_08_1_1', 'poste_08_1_2'],
                                          new_row = 'poste_08_1' )

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_09_4_2_1', 'poste_09_4_2_2', 'poste_09_4_2_3', 'poste_09_4_2_4'],
                                          new_row = 'poste_09_4_2' )

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_09_6_3_1', 'poste_09_6_3_2'],
                                          new_row = 'poste_09_6_3' )

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_10_2_1', 'poste_10_2_2'],
                                          new_row = 'poste_10_2' )
    # On ajoute les lignes "Autres dépenses de ..." pour chaque poste agrégé et on les mets à 0
    liste_postes_nuls = ['poste_01_3_1', 'poste_02_5_1', 'poste_03_3_1', 'poste_04_6_1' , 'poste_05_7_1', 'poste_07_1_4','poste_07_5_1',
                         'poste_08_4_1', 'poste_09_9_1', 'poste_10_6_1', 'poste_11_1_3', 'poste_12_3_3_1','poste_12_8_1', 'poste_12_9_1']
    for poste in liste_postes_nuls :
        masses_cn_data_frame = sum_and_remove(masses_cn_data_frame, 'Code', [], poste)
    
    liste_postes_cn = remove_prefixes(masses_cn_data_frame['Code'].tolist())
    liste_postes_cn.remove('poste__Z')
    liste_13postes = ["poste_0{}".format(i) for i in range(1, 10)] + ["poste_10", "poste_11", "poste_12", "poste_13"]
    liste_postes_cn = [element for element in liste_postes_cn if element[:8] in liste_13postes]

    masses_cn_postes_data_frame = masses_cn_data_frame.loc[masses_cn_data_frame['Code'].isin(liste_postes_cn)]
    masses_cn_postes_data_frame.set_index('Code', inplace = True)
    masses_cn_postes_data_frame.rename(columns= {'{}'.format(target_year): 'conso_CN_{}'.format(target_year)}, inplace= True)

    # Revenus 
    parametres_fiscalite_file_path = os.path.join(
        assets_directory,
        'legislation',
        'T_2101_2023.xls'
        )
    revenus_cn = pd.read_excel(parametres_fiscalite_file_path, sheet_name = "T_2101", header = 4)
    revenus_cn.rename(columns={'Unnamed: 0' : 'Code' , 'Unnamed: 1' : 'Label'}, inplace = True)
    revenus_cn = revenus_cn.loc[revenus_cn['Label'] == 'Revenu disponible brut']
    revenus_cn  = revenus_cn.loc[revenus_cn['2017'] > 1000] # On enlève la ligne "Evolution en (%)"
    revenus_cn.replace({'B6G' : 'rev_disp_yc_loyerimpute'}, inplace= True)
    revenus_cn = revenus_cn[['Code','{}'.format(target_year)]]
    revenus_cn.loc[:,'{}'.format(target_year)] = revenus_cn.loc[:,'{}'.format(target_year)] * 1e3
    revenus_cn.set_index('Code', inplace = True)
    revenus_cn.rename(columns= {'{}'.format(target_year): 'conso_CN_{}'.format(target_year)}, inplace= True)
    
    masses_cn_postes_data_frame = masses_cn_postes_data_frame.append(revenus_cn)
    masses_cn_postes_data_frame.rename({'poste_04_2' : 'loyer_impute'}, inplace = True)
    masses_cn_postes_data_frame.loc['rev_disponible'] = masses_cn_postes_data_frame.loc['rev_disp_yc_loyerimpute'] - masses_cn_postes_data_frame.loc['loyer_impute']
       
    return masses_cn_postes_data_frame*1e6

def new_get_inflators_bdf_to_cn(data_year):
    '''Calcule l'inflateur de calage à partir des masses de comptabilité nationale.'''
    data_cn = new_get_cn_aggregates(data_year)
    liste_postes_cn = data_cn.index.tolist()

    data_bdf = new_get_bdf_aggregates(data_year)
    data_bdf_postes_cn = pd.DataFrame()
    liste_postes_bdf = data_bdf.index.tolist()

    data_bdf_postes_cn = pd.DataFrame(index=[0])
    for poste in liste_postes_cn:
        data_bdf_postes_cn[poste] = 0
        for element in liste_postes_bdf:
            if poste in element:
                data_bdf_postes_cn[poste] += float(data_bdf.loc[element])
    data_bdf_postes_cn = data_bdf_postes_cn.transpose()
    data_bdf_postes_cn.rename(columns={0 : 'bdf_aggregates'}, inplace = True)

    masses = data_cn.merge(data_bdf_postes_cn, left_index = True, right_index = True)
    masses.rename(columns = {'bdf_aggregates': 'conso_bdf{}'.format(data_year)}, inplace = True)
    
    inflators_bdf_to_cn = (masses['conso_CN_{}'.format(data_year)] / masses['conso_bdf{}'.format(data_year)]).to_dict()
    return {k : v for k,v in inflators_bdf_to_cn.items() if v!= float('inf')}

def new_get_inflators_cn_to_cn(target_year, data_year):
    '''Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.'''
    data_year_cn_aggregates = new_get_cn_aggregates(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = new_get_cn_aggregates(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    ratios =  { key : (target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        if data_year_cn_aggregates[key] != 0 else 0 
        for key in list(data_year_cn_aggregates.keys())}
    return ratios
    
    
def new_get_inflators(target_year,data_year):
    '''
    Fonction qui calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    inflators_bdf_to_cn = new_get_inflators_bdf_to_cn(data_year)
    inflators_cn_to_cn = new_get_inflators_cn_to_cn(target_year,data_year)

    tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    liste_variables = list(tax_benefit_system.variables.keys())
    ratio_by_variable = dict()
    for element in liste_variables:
        if element[:6] == 'poste_' or element[:8] == 'rev_disp' or element == 'loyer_impute':
            for key in list(inflators_cn_to_cn.keys()):
                if key in list(inflators_bdf_to_cn.keys()):
                    if key in element:
                        ratio_by_variable[element] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]

    return ratio_by_variable


def get_inflators_cn_23_to_24():
        '''Utilise les comptes trimestriels pour calculer l'inflateur de la conso et des revenus de 2023 à 2024.'''
        comptes_trimestriels_folder_path = os.path.join(
                assets_directory,'legislation')
        # Consommation
        comptes_trim = pd.read_excel(os.path.join(comptes_trimestriels_folder_path,'t_conso_val.xls'), sheet_name = "Niveaux", header = 4)
        comptes_trim.columns = comptes_trim.columns.str.strip()
        comptes_trim = comptes_trim[['Unnamed: 0', 'TOTAL']]

        comptes_trim.rename(columns= {'Unnamed: 0' : 'Trimestre'}, inplace = True)
        comptes_trim.dropna(axis = 0, inplace = True)
        total_2024 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2024') ,'TOTAL'].sum()
        total_2023 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2023') ,'TOTAL'].sum()
        inflator_conso = total_2024 / total_2023
        
        # Revenus
        comptes_trim = pd.read_excel(os.path.join(comptes_trimestriels_folder_path,'t_men_val.xls'), sheet_name = "Niveaux", header = 4)
        comptes_trim.columns = comptes_trim.columns.str.strip()
        comptes_trim = comptes_trim[['Unnamed: 0', 'Revenu disponible brut']]
        comptes_trim.rename(columns= {'Unnamed: 0' : 'Trimestre'}, inplace = True)
        comptes_trim.dropna(axis = 0, inplace = True)
        total_2024 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2024') ,'Revenu disponible brut'].sum()
        total_2023 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2023') ,'Revenu disponible brut'].sum()
        inflator_revenu = total_2024 / total_2023
        
        return inflator_conso, inflator_revenu
    
def new_get_inflators_by_year(rebuild = False, year_range = None, data_year = None):
    ''' Récupère les inflateurs pour le veillissement pour toutes les année voulues.'''
    if year_range is None:
        year_range = range(2000, 2025)

    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in year_range:
            if target_year <= 2023:
                inflators = new_get_inflators(target_year = target_year, data_year = data_year)
                inflators_by_year[target_year] = inflators
            else:
                inflators = new_get_inflators(target_year = 2023, data_year = data_year)
                inflator_conso, inflator_revenu = get_inflators_cn_23_to_24()
                inflators_2024 = {
                    key : value * inflator_revenu if key in [''] else value * inflator_conso 
                    for key, value in inflators.items()
                    }
                inflators_by_year[target_year] = inflators_2024

        writer_inflators = csv.writer(open(os.path.join(assets_directory, 'inflateurs', 'new_inflators_by_year.csv'), 'w'))
        for year in year_range:
            for key, value in list(inflators_by_year[year].items()):
                writer_inflators.writerow([key, value, year])

        return inflators_by_year
    else:
        re_build_inflators = dict()
        inflators_from_csv = pd.read_csv(os.path.join(assets_directory, 'inflateurs', 'new_inflators_by_year.csv'),
            index_col = 0, header = None)
        for year in year_range:
            inflators_from_csv_by_year = inflators_from_csv[inflators_from_csv[2] == year]
            inflators_to_dict = pd.DataFrame.to_dict(inflators_from_csv_by_year)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators