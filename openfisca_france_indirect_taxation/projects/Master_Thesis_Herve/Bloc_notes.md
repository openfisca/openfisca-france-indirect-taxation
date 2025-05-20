- Légère modification dans l'enquête logement : renommer le fichier MENLOG_DIFF en menlog_diff
- Quelques modifications des scripts que j'ai du faire:
	- openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\build_survey_data\step_5_data_from_matching.py : 
	 ligne 43, platform.system() (les parenthèses n'y étaient pas) 
	- dans le fichier .config/openfisca-survey-manager/config.ini :  
	rajouter les lignes
	[exe]
	r_libs_user = C:\Users\veve1\AppData\Local\R\win-library\4.3
	rscript = C:\Program Files\R\R-4.3.0\bin\Rscript.exe

	- openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\build_survey_data\matching_erfs\step_1_build_dataframes.py :
	ligne 16 year_erfs = 2017
	ligne 23 (table = 'fpr_menage_2017') 
	ligne 24 (table = 'fpr_mrf17e17t4')
	Simplement pour utiliser les données ERFS 2017 au lieu de 2013

	- dans tous les scripts .R de openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\assets\matching:
	remplacer les chemins en ('~/') par les chemins complets ('C:/Users/...')
	- openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\build_survey_data\matching_bdf_entd\step_2_homogenize_variables.py :
	ligne 129 (niveau_vie_quintile) : il restait un niveau_vie_decile à remplacer par niveau_vie_quintile
	- openfisca-france-indirect-taxation\openfisca_france_indirect_taxation\surveys.py : 
	déplacer la ligne `survey_scenario.initialize_weights()`