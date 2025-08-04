import numpy as np
import pandas as pd
import os
from openfisca_france_indirect_taxation.utils import assets_directory

def split_aggregated_poste(df, to_split, new_postes):
    ''' Ventile les postes agrégés en sous-postes en utilisant d'autres données sur la consommation touristique.'''
    
    other_data_tourisme = pd.read_excel(os.path.join(assets_directory,'legislation','Consommation_touristique_2010_2018.xlsx'), index_col= 0)
    other_data_tourisme['Postes de dépenses'] = other_data_tourisme['Postes de dépenses'].str.strip()
    total = other_data_tourisme.loc[other_data_tourisme['Postes de dépenses'].isin(new_postes),[2018]].sum(axis = 0).values[0]

    for poste in new_postes : 
        
        share = other_data_tourisme.loc[other_data_tourisme['Postes de dépenses'] == poste,2018].values[0] / total 
        df.loc[df.index.max()+1,'Poste de dépenses'] = poste
        df.loc[df['Poste de dépenses'] == poste,[2019,2020,2021,2022]] = (df.loc[df['Poste de dépenses'] == to_split,[2019,2020,2021,2022]].apply(lambda x : share*x, axis = 0)).values[0]

    return(df)

postes_tourisme = ['Hébergements touristiques marchands',
 'Restaurants et cafés',
 'Transports par avion',
 'Transports par train',
 'Transports par autocar',
 'Transports fluviaux et maritimes',
 'Location de véhicules de tourisme',
 'Remontées mécaniques',
 'Musées, spectacles et autres activités culturelles',
 'Activités sportives et de loisirs',
'Location d\'articles de sport et loisirs',
'Services des voyagistes et agences de voyages',
'Carburants et péages',	
'Aliments et boissons',	
'Biens de consommation durables spécifiques',	
'Autres biens de consommation et autres services',
'Dépenses touristiques intérieures (C = A + B)'
 ]

def get_repartition_depenses_touristique(target_year): 
    ''' Renvoit la répartition des dépenses touristiques entre différents postes de consommation.'''
    
    data_tourisme_file_path = os.path.join(
    assets_directory,
    'legislation',
    'sect-tour-conso-int-conso.xlsx'
    )
    
    if target_year <= 2019 :
        year = 2019
    elif target_year > 2022 :
        year = 2022
    else :
        year = target_year
        
    data_tourisme = pd.read_excel(data_tourisme_file_path, header = [3,4])
    data_tourisme.set_index([('Poste de dépenses','Unnamed: 0_level_1')], inplace= True)
    target_label = "Consommation des non-résidents (consommation récepteur)"
    data_tourisme = data_tourisme.loc[:, data_tourisme.columns.get_level_values(1) == target_label]
    data_tourisme.columns = data_tourisme.columns.get_level_values(0)
    data_tourisme.reset_index(inplace = True)
    data_tourisme.rename({('Poste de dépenses', 'Unnamed: 0_level_1') : 'Poste de dépenses'}, axis = 1, inplace = True)
    data_tourisme['Poste de dépenses'] = data_tourisme['Poste de dépenses'].str.strip() 
    data_tourisme = data_tourisme.loc[data_tourisme['Poste de dépenses'].isin(postes_tourisme),]
    
    # On ventile certains postes agrégés
    data_tourisme = split_aggregated_poste(data_tourisme, 'Carburants et péages', ['Carburants','Péages'])
    data_tourisme = split_aggregated_poste(data_tourisme, 'Autres biens de consommation et autres services', ['Autres biens de consommation (6)', 'Autres services (7)', 'Taxis et autres services de transports urbains'])
    data_tourisme.set_index('Poste de dépenses', inplace = True)
    data_tourisme.drop(index = ['Carburants et péages', 'Autres biens de consommation et autres services','Dépenses touristiques intérieures (C = A + B)'], axis = 1, inplace = True)

    percentage_df = data_tourisme.div(data_tourisme.sum(axis = 0))
    percentage_df = percentage_df[[year]]

    return(percentage_df)

dico_postes_tourisme = {
'Aliments et boissons' : ['poste_01_1_1', 'poste_01_1_2', 'poste_01_1_3', 'poste_01_1_4', 'poste_01_1_5', 'poste_01_1_6', 'poste_01_1_7', 'poste_01_1_8', 'poste_01_1_9',
'poste_01_2_1', 'poste_01_2_2', 'poste_01_2_3', 'poste_01_2_5', 'poste_01_2_6', 'poste_01_2_9', 'poste_01_3_1',
'poste_02_1_1', 'poste_02_1_2', 'poste_02_1_3', 'poste_02_1_9',
'poste_02_3', 'poste_02_4', 'poste_02_5_1',] ,
'Biens de consommation durables spécifiques' : ['poste_03_1_1', 'poste_03_1_2', 'poste_03_2_1'],
'Carburants' : 'poste_07_2_2', 
'Péages' : 'poste_07_2_4',
'Location de véhicules de tourisme' : 'poste_07_2_4',
'Transports par train' : 'poste_07_3_1',
'Transports par autocar' : 'poste_07_3_2',
'Transports par avion' : 'poste_07_3_3',
'Transports fluviaux et maritimes': 'poste_07_3_4',
'Location d\'articles de sport et loisirs' : 'poste_09_4_2',
'Remontées mécaniques' : 'poste_09_4_2',
'Activités sportives et de loisirs' : 'poste_09_4_2',
'Musées, spectacles et autres activités culturelles' : 'poste_09_6_1', 
'Services des voyagistes et agences de voyages' : 'poste_09_8',
'Restaurants et cafés' : 'poste_11_1_1',
'Hébergements touristiques marchands' : 'poste_11_2',
'Autres services (7)': 'poste_13_9',
'Taxis et autres services de transports urbains': 'poste_13_9',			
'Autres biens de consommation (6)': 'poste_13_2' , 
}

def calculate_share_cn(liste_poste,cn_df):

    total = cn_df.loc[cn_df.index.isin(liste_poste)].sum(axis = 0)
    share_df = cn_df.loc[cn_df.index.isin(liste_poste)].div(total).reset_index()
    share_df.columns = ['Code','Part']
    
    return(share_df)

def get_correction_territoriale(target_year, masses_cn_postes, liste_postes_cn):
    
    # On prend le solde territorial dans la compta nat
    parametres_fiscalite_file_path = os.path.join(
            assets_directory,
            'legislation',
            'conso_eff_fonction_2023.xls'
            )
    
    df_cn = pd.read_excel(parametres_fiscalite_file_path, sheet_name = "MEURcour", header = 4)
    df_cn.rename(columns={'Unnamed: 0' : 'Code' , 'Unnamed: 1' : 'Label'}, inplace = True)
    df_cn = df_cn.loc[:, ['Code', '{}'.format(target_year)]].copy()
    df_cn.loc[df_cn['Code'] == 'CP16']
    solde_territorial = df_cn.loc[df_cn['Code'] == 'CP16','{}'.format(target_year)]
    
    # On récupère la répartition de la consommation touristique des étrangers en France 
    percentage_df = get_repartition_depenses_touristique(target_year)

    # On ventile le solde territorial  selon cette répartition
    correction_territoriale = pd.DataFrame()
    correction_territoriale['Solde territorial'] = percentage_df * solde_territorial.values[0]
    correction_territoriale = correction_territoriale.reset_index().rename({'Poste de dépenses' : 'Label'}, axis = 1)
    correction_territoriale['Code'] = correction_territoriale['Label'].map(dico_postes_tourisme)

    correction_territoriale['Code'] = correction_territoriale['Code'].apply(lambda x: x if isinstance(x, list) else [x]) 
    correction_territoriale = correction_territoriale.explode('Code').reset_index(drop = True)

    liste_poste_01_02 = [element for element in liste_postes_cn if element[:8] in ['poste_01','poste_02']]
    share_df_1 = calculate_share_cn(liste_poste = liste_poste_01_02, cn_df = masses_cn_postes)
    share_df_2 = calculate_share_cn(liste_poste = ['poste_03_1_1', 'poste_03_1_2', 'poste_03_2_1'], cn_df = masses_cn_postes)
    share_df = pd.concat([share_df_1,share_df_2])

    correction_territoriale = correction_territoriale.merge(share_df, how = 'left', on = 'Code')
    correction_territoriale.fillna(1, inplace= True)
    correction_territoriale['Solde territorial'] = correction_territoriale['Solde territorial'] * correction_territoriale['Part']
    correction_territoriale.drop(labels = 'Part', axis = 1, inplace = True)
    
    return(correction_territoriale)