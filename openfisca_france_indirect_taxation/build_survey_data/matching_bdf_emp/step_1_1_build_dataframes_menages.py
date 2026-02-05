# -*- coding: utf-8 -*-

# Dans ce script on importe les données des enquêtes BdF 2017 et EMP 2019.
# Pour chacune des deux enquêtes on importe les variables qui seront
# susceptibles d'êtres utilisées dans l'appariement des bases de données.


# To do : add information about vehicles


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager.paths import default_config_files_directory as config_files_directory


def load_data_menages_bdf_emp(year_data):
    # Load emp data :
    year_emp = 2019

    emp_survey_collection = SurveyCollection.load(
        collection = 'enquete_transports', config_files_directory = config_files_directory
        )
    survey_emp = emp_survey_collection.get_survey('enquete_transports_{}'.format(year_emp))

    input_emp_tcm_menage = survey_emp.get_values(table = 'tcm_men_public_V2')
    input_emp_menage = survey_emp.get_values(table = 'q_menage_public_V2')

    # Load BdF data :
    year_bdf = year_data
    openfisca_survey_collection = SurveyCollection.load(collection = 'openfisca_indirect_taxation')
    openfisca_survey = openfisca_survey_collection.get_survey('openfisca_indirect_taxation_data_{}'.format(year_bdf))
    input_bdf = openfisca_survey.get_values(table = 'input')
    input_bdf.reset_index(inplace = True)

    # Create variable for total spending
    liste_variables = input_bdf.columns.tolist()
    postes_agreges = ['poste_{}'.format(index) for index in
        ['0{}'.format(i) for i in range(1, 10)] + ['10', '11', '12', '13']
        ]
    input_bdf['depenses_tot'] = 0
    for element in liste_variables:
        for poste in postes_agreges:
            if element[:8] == poste:
                input_bdf['depenses_tot'] += input_bdf[element]

    # Set variables :
    if year_emp == 2008:                # Enquête ENTD 2008 
        variables_tcm_menage_emp = [
            'ident_men',
            'agepr',
            'cs42pr',
            'dip14pr',
            'nactifs',
            'nbuc',             # ocde10
            'nenfants',
            'nivie10',          # déciles de revenu par uc
            'npers',
            'numcom_au2010',    # cataeu
            'pondv1',           # poids ménage
            'revuc',            # revenus simulés par UC
            'rlog',             # allocations logement
            'situapr',
            'tu99',
            'tau99',
            # 'typlog',
            'typmen5',          # type ménage
            # To be completed
            ]

        variables_menage_emp = [
            'ident_men',
            'v1_logpiec',       # nombre de pièces dans logement
            'v1_logocc',        # statut d'occupation du logement
            'v1_logloymens',    # loyer mensuel calculé
            ]
    if year_emp == 2019:
        variables_tcm_menage_emp = [
            'ident_men',
            'agepr',
            'cs42pr',
            'dipdetpr',              # diplôme le plus élevé de la personne de référence
            'nactifs',               # nombre d'actifs dans le ménage  
            'coeffuc',               # ocde10
            'nenfants',              # nombre d'enfants dans le ménage
            'decile_rev',            # décile de revenu consolidé
            'decile_rev_uc',         # décile de revenu par uc
            'npers',                 # nombre de personnes dans le ménage
            # 'numcom_au2010',       # cataeu
            'pond_menc',             # poids ménage
            # 'rev_final_uc',        # revenus simulés par UC   (pas dispo dans la table public demander table chercheur)
            # 'rlog',                # allocations logement     (pas dispo dans la table public demander table chercheur)
            'situapr',               # situation professionnelle de la personne de référence 
            'tuu2017_res',           # tranche d'unité urbaine de la commune de résidence
            # 'tau99',               (pas dispo dans la table public demander table chercheur ??)
            # 'typlog',
            'typmen5',               # type ménage
            # To be completed
            ]

        variables_menage_emp = [
            'ident_men',
            'jnbveh',             # nb de voitures particulières
            ]
    
    variables_menage_bdf = [
        'ident_men',
        'aidlog1',
        'aidlog2',
        'agepr',            # âge de la pr
        'cataeu',
        'cs42pr',
        'dip14pr',
        'mloy_d',           # loyer mensuel
        'nactifs',
        'nbphab',
        'nenfants',
        'npers',
        'ocde10',           # nb unités de conso
        'pondmen',
        'poste_07_2_2_1',   # modifié Hervé 25/04 (07_2_2_1_1 -> 07_2_2_1)
        'rev_disponible',   # revenu disponible
        'revtot',           # revenu total
        'situapr',
        'stalog',
        'tau',
        'tuu',
        # 'typlog',
        'typmen',
        # To be completed
        ]

    # Keep relevant variables :
    tcm_menage_emp_keep = input_emp_tcm_menage[variables_tcm_menage_emp]
    menage_emp_keep = input_emp_menage[variables_menage_emp]
    menage_bdf_keep = input_bdf[variables_menage_bdf]

    # Merge emp tables into one dataframe
    data_emp = tcm_menage_emp_keep.merge(menage_emp_keep, on = 'ident_men')

    del input_emp_tcm_menage, input_emp_menage, input_bdf

    return menage_bdf_keep, data_emp


if __name__ == '__main__':
    data_bdf, data_emp = load_data_menages_bdf_emp(2017)
