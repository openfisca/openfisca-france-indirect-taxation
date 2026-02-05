import pandas as pd
import os
import csv

from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem
from openfisca_france_indirect_taxation.utils import assets_directory, get_input_data_frame
from openfisca_france_indirect_taxation.Correction_territoriale import get_correction_territoriale
# from openfisca_survey_manager.survey_collections import SurveyCollection
# from openfisca_survey_manager import default_config_files_directory as config_files_directory

''' Données sources utilisées :
    - Consommation des ménages en 2023 (base 2020) : https://www.insee.fr/fr/statistiques/fichier/8068592/T_CONSO_EFF_FONCTION.xlsx
    - Comptes trimestriels pour l'année 2024 (base 2020) : (conso) https://www.insee.fr/fr/statistiques/fichier/8358378/t_conso_val.xls
    - Compte de la santé 2024 : https://drees.solidarites-sante.gouv.fr/sites/default/files/2024-12/CNS2024%20-%20Vue%20d%27ensemble.xlsx
    - Compte satellite du tourisme : https://www.insee.fr/fr/statistiques/fichier/2015846/sect-tour-conso-int.zip
    - Revenu disponible des ménages en 2023 (base 2020) :  https://www.insee.fr/fr/statistiques/fichier/8068630/T_2101.xlsx
    - Comptes trimestriels pour l'année 2024 (base 2020) : (revenus) https://www.insee.fr/fr/statistiques/fichier/8358386/t_men_val.xls
    '''


def get_bdf_aggregates(data_year = None):
    ''' Calcule les agrégats de Bdf pour l'année des données.'''
    assert data_year is not None
    depenses = get_input_data_frame(data_year)
    liste_variables = depenses.columns.tolist()
    liste_postes = [element for element in liste_variables if element[:6] == 'poste_'] + ['rev_disponible', 'rev_disp_yc_loyerimpute', 'loyer_impute']

    bdf_aggregates_by_poste = pd.DataFrame(
        index=liste_postes,
        columns=['bdf_aggregates']
        )
    bdf_aggregates_by_poste['bdf_aggregates'] = (depenses[liste_postes].mul(depenses['pondmen'], axis=0)).sum(axis=0)
    
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
    'CP0942': 'CP09421',    # Location, entretien et réparation de gros biens durables à fonction récréactive (S)
    'CP0943': 'CP09422',    # Location et réparation de jeux, jouets et articles de loisirs (S)
    'CP0944': 'CP09423',    # Location et réparaton d'articles de sport, de matériel de camping et activités de plein air (S)
    'CP0946': 'CP09424',    # Services récréatifs et sportifs (S)
    'CP0945': 'CP09631',    # Services vétérinaires et autres pour animaux de companies
    'CP0963': 'CP09632',    # Services photographiques
    'CP081': 'CP0811',      # Matériel d'information et de communication
    'CP082': 'CP0812',      # Logiciels à l'exclusion des jeux
    'CP102': 'CP1021',      # Enseignement secondaire
    'CP103': 'CP1022',      # Enseignement post-secondaire non supérieur
    }


def sum_and_remove(data_frame, col, rows_to_sum, new_row):
    data = data_frame.copy()
    new_index = data.index.max() + 1
    data.loc[new_index] = data[data[col].isin(rows_to_sum)].sum(numeric_only=True)
    data.loc[new_index, col] = new_row
    data = data[~data[col].isin(rows_to_sum)]

    return data


def get_reste_a_charge_sante_cn(target_year):
    '''La compta nat regroupe les dépenses des ménages et des organismes complémentaires. A l'aide du compte de santé, on
    calcule la part des dépenses de santé des ménages, à isoler dans la compta nat.'''
    depenses_sante_file_path = os.path.join(
        assets_directory,
        'depenses',
        'CNS2024_Vue_d_ensemble.xlsx'
        )

    depenses_sante = pd.read_excel(depenses_sante_file_path, sheet_name = "Graph 7", header = 4, usecols = [i for i in range(1, 16)])
    depenses_sante = depenses_sante.drop(index = [3, 4, 5], axis = 0).rename({'Unnamed: 1': 'Financeur'}, axis = 1)

    menages = float(depenses_sante.loc[depenses_sante['Financeur'] == 'Ménages', target_year].iloc[0])
    complementaires = float(depenses_sante.loc[depenses_sante['Financeur'] == 'Organismes complémentaires', target_year].iloc[0])
    part_menages = menages / (menages + complementaires)
    return part_menages


def get_cn_aggregates(target_year):
    ''' Calcule les agrégats de compta nat utilisables pour un année cible.'''
    # Dépenses de conso
    conso_effective_file_path = os.path.join(
        assets_directory,
        'depenses',
        'conso_eff_fonction_2023.xls'
        )

    masses_cn_data_frame = pd.read_excel(conso_effective_file_path, sheet_name = "MEURcour", header = 4)
    masses_cn_data_frame.rename(columns={'Unnamed: 0': 'Code', 'Unnamed: 1': 'Label'}, inplace = True)
    masses_cn_data_frame = masses_cn_data_frame.loc[:, ['Code', '{}'.format(target_year)]].copy()
    masses_cn_data_frame.replace(to_replace = ajust_postes_cn, inplace= True)
    masses_cn_data_frame.loc[:, 'Code'] = masses_cn_data_frame.loc[:, 'Code'].str.replace(r'^CP', '', regex=True)
    masses_cn_data_frame.loc[:, 'Code'] = masses_cn_data_frame.loc[:, 'Code'].str.strip()

    masses_cn_data_frame.dropna(inplace = True)
    masses_cn_data_frame.loc[:, 'Code'] = masses_cn_data_frame['Code'].astype(str).apply(lambda x: f"poste_{x}")
    masses_cn_data_frame.loc[:, 'Code'] = masses_cn_data_frame['Code'].astype(str).apply(lambda x: format_poste(x))

    # On garde les agrégats à un niveau supérieur pour correspondre à Bdf
    masses_cn_data_frame = masses_cn_data_frame[~masses_cn_data_frame['Code'].isin(['poste_04_2_1', 'poste_04_2_2',
                                                                                    'poste_05_1_1', 'poste_05_1_2', 'poste_05_2_1', 'poste_05_2_2',
                                                                                    'poste_06_1', 'poste_06_2', 'poste_06_3', 'poste_06_4'])]

    # On regroupe certains postes de consommation sous la même étiquette
    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_08_1_1', 'poste_08_1_2'],
                                          new_row = 'poste_08_1')

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_09_4_2_1', 'poste_09_4_2_2', 'poste_09_4_2_3', 'poste_09_4_2_4'],
                                          new_row = 'poste_09_4_2')

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_09_6_3_1', 'poste_09_6_3_2'],
                                          new_row = 'poste_09_6_3')

    masses_cn_data_frame = sum_and_remove(data_frame = masses_cn_data_frame,
                                          col = 'Code',
                                          rows_to_sum = ['poste_10_2_1', 'poste_10_2_2'],
                                          new_row = 'poste_10_2')
    # On ajoute les lignes "Autres dépenses de ..." pour chaque poste agrégé et on les mets à 0
    liste_postes_nuls = ['poste_01_3_1', 'poste_02_5_1', 'poste_03_3_1', 'poste_04_6_1', 'poste_05_7_1', 'poste_07_1_4', 'poste_07_5_1',
                         'poste_08_4_1', 'poste_09_9_1', 'poste_10_6_1', 'poste_11_1_3', 'poste_12_3_3_1', 'poste_12_8_1', 'poste_12_9_1']
    for poste in liste_postes_nuls:
        masses_cn_data_frame = sum_and_remove(masses_cn_data_frame, 'Code', [], poste)

    # Correction dépenses de santé
    part_menages = get_reste_a_charge_sante_cn(target_year)
    masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == 'poste_06', '{}'.format(target_year)] = part_menages * masses_cn_data_frame.loc[masses_cn_data_frame['Code'] == 'poste_06', '{}'.format(target_year)]
    liste_postes_cn = remove_prefixes(masses_cn_data_frame['Code'].tolist())

    liste_13postes = ["poste_0{}".format(i) for i in range(1, 10)] + ["poste_10", "poste_11", "poste_12", "poste_13"]
    liste_postes_cn = [element for element in liste_postes_cn if element[:8] in liste_13postes]
    masses_cn_postes_data_frame = masses_cn_data_frame.loc[masses_cn_data_frame['Code'].isin(liste_postes_cn)]
    masses_cn_postes_data_frame.set_index('Code', inplace = True)

    # Correction territoriale
    correction_territoriale = get_correction_territoriale(2022, masses_cn_postes_data_frame, liste_postes_cn)
    masses_cn_postes_data_frame = masses_cn_postes_data_frame.merge(correction_territoriale.groupby(by = 'Code').sum(), 'left', left_index= True, right_index= True)
    masses_cn_postes_data_frame['{} corrigé'.format(target_year)] = masses_cn_postes_data_frame['{}'.format(target_year)] + masses_cn_postes_data_frame['Solde territorial'].fillna(0)

    masses_cn_postes_data_frame.rename(columns= {'{} corrigé'.format(target_year): 'conso_CN_{}'.format(target_year)}, inplace= True)
    masses_cn_postes_data_frame.rename({'poste_04_2': 'loyer_impute'}, inplace = True)

    return masses_cn_postes_data_frame * int(1e6)


def get_inflators_bdf_to_cn(data_year):
    '''Calcule l'inflateur de calage à partir des masses de comptabilité nationale.'''
    data_cn = get_cn_aggregates(data_year)
    liste_postes_cn = data_cn.index.tolist()

    data_bdf = get_bdf_aggregates(data_year)
    data_bdf_postes_cn = pd.DataFrame()
    liste_postes_bdf = data_bdf.index.tolist()

    bdf_aggregates = {poste: 0 for poste in liste_postes_cn}
    for poste in liste_postes_cn:
        for element in liste_postes_bdf:
            if poste in element:
                bdf_aggregates[poste] += float(data_bdf.loc[element].iloc[0])
    data_bdf_postes_cn = pd.DataFrame.from_dict(bdf_aggregates, orient='index', columns=['bdf_aggregates'])

    masses = data_cn.merge(data_bdf_postes_cn, left_index = True, right_index = True)
    masses.rename(columns = {'bdf_aggregates': 'conso_bdf{}'.format(data_year)}, inplace = True)

    inflators_bdf_to_cn = (masses['conso_CN_{}'.format(data_year)] / masses['conso_bdf{}'.format(data_year)]).to_dict()
    return {k: v for k, v in inflators_bdf_to_cn.items() if v != float('inf')}


def get_inflators_cn_to_cn(target_year, data_year):
    '''Calcule l'inflateur de vieillissement à partir des masses de comptabilité nationale.'''
    data_year_cn_aggregates = get_cn_aggregates(data_year)['conso_CN_{}'.format(data_year)].to_dict()
    target_year_cn_aggregates = get_cn_aggregates(target_year)['conso_CN_{}'.format(target_year)].to_dict()

    ratios = {key: (target_year_cn_aggregates[key] / data_year_cn_aggregates[key])
        if data_year_cn_aggregates[key] != 0 else 0
        for key in list(data_year_cn_aggregates.keys())}
    return ratios


def get_inflators(target_year, data_year):
    '''
    Calcule les ratios de calage (bdf sur cn pour année de données) et de vieillissement
    à partir des masses de comptabilité nationale et des masses de consommation de bdf.
    '''
    inflators_bdf_to_cn = get_inflators_bdf_to_cn(data_year)
    inflators_cn_to_cn = get_inflators_cn_to_cn(target_year, data_year)

    tax_benefit_system = FranceIndirectTaxationTaxBenefitSystem()
    liste_variables = list(tax_benefit_system.variables.keys())
    ratio_by_variable = dict()
    for element in liste_variables:
        if element[:6] == 'poste_' or element in ['loyer_impute']:
            for key in list(inflators_cn_to_cn.keys()):
                if key in list(inflators_bdf_to_cn.keys()):
                    if key in element:
                        ratio_by_variable[element] = inflators_bdf_to_cn[key] * inflators_cn_to_cn[key]
        elif element in ['depenses_carburants', 'depenses_essence', 'depenses_diesel']:
            ratio_by_variable[element] = inflators_bdf_to_cn['poste_07_2_2'] * inflators_cn_to_cn['poste_07_2_2']
            
    return ratio_by_variable


def get_inflators_cn_23_to_24():
    '''Utilise les comptes trimestriels pour calculer l'inflateur de la conso de 2023 à 2024.'''
    comptes_trimestriels_folder_path = os.path.join(
        assets_directory,
        'depenses')
    # Consommation
    comptes_trim = pd.read_excel(os.path.join(comptes_trimestriels_folder_path, 't_conso_val.xls'), sheet_name = "Niveaux", header = 4)
    comptes_trim.columns = comptes_trim.columns.str.strip()
    comptes_trim = comptes_trim[['Unnamed: 0', 'TOTAL']]

    comptes_trim.rename(columns= {'Unnamed: 0': 'Trimestre'}, inplace = True)
    comptes_trim.dropna(axis = 0, inplace = True)
    total_2024 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2024'), 'TOTAL'].sum()
    total_2023 = comptes_trim.loc[comptes_trim['Trimestre'].str.startswith('2023'), 'TOTAL'].sum()
    inflator_conso = total_2024 / total_2023

    return inflator_conso


def get_inflators_by_year(rebuild = False, year_range = None, data_year = None):
    ''' Récupère les inflateurs pour le veillissement pour toutes les années voulues.'''
    if year_range is None:
        year_range = range(2000, 2025)

    if rebuild is not False:
        inflators_by_year = dict()
        for target_year in year_range:
            if target_year <= 2023:
                inflators = get_inflators(target_year = target_year, data_year = data_year)
                inflators_by_year[target_year] = inflators
            else:
                inflators = get_inflators(target_year = 2023, data_year = data_year)
                inflator_conso = get_inflators_cn_23_to_24()
                inflators_2024 = {
                    key: value * inflator_conso
                    for key, value in inflators.items()
                    }
                inflators_by_year[target_year] = inflators_2024

        writer_inflators = csv.writer(open(os.path.join(assets_directory, 'inflateurs', 'inflators_by_year.csv'), 'w'))
        for year in year_range:
            for key, value in list(inflators_by_year[year].items()):
                writer_inflators.writerow([key, value, year])

        return inflators_by_year
    else:
        re_build_inflators = dict()
        inflators_from_csv = pd.read_csv(os.path.join(assets_directory, 'inflateurs', 'inflators_by_year.csv'),
            index_col = 0, header = None)
        for year in year_range:
            inflators_from_csv_by_year = inflators_from_csv[inflators_from_csv[2] == year]
            inflators_to_dict = pd.DataFrame.to_dict(inflators_from_csv_by_year)
            inflators = inflators_to_dict[1]
            re_build_inflators[year] = inflators

        return re_build_inflators
