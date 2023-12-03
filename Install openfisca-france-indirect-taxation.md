**Fork le repo indirect-taxation**

- gh repo fork https://github.com/openfisca/openfisca-france-indirect-taxation

** Cloner le repo indirect-taxation** (plus précisément la branche nomics-master qui nous intéresse)

- git clone -b 'nomics-master' 'https://github.com/Hervedarr31/openfisca-france-indirect-taxation.git' 

**Créer et configurer un nouvel environnement virtuel**

-(avec pyenv et pip): 
	- `py -3.9 -m venv hervenv` 
	- `hervenv\Scripts\activate`
	- Installer openfisca-france-indirect-taxation :
		- se placer dans le dossier openfisca-france-indirect-taxation
		- `pip install -e .` 
		- normalement les autres packages nécessaire sont importés dans les bonnes versions
 ( OpenFisca-Core==35.12.0 et OpenFisca-Survey-Manager==0.47.2)

-(avec conda et le fichier environment.yml du git nomics-master):

	- se placer dans le dossier openfisca-france-indirect-taxation
	- modifier le fichier environment.yml pour indiquer le nom (name: openfiscaenv) et le chemin (ex: prefix : C:\Users\veve1\miniconda3\envs) 
	- conda env create -f environment.yml
	- Installer openfisca-france-indirect-taxation :
		- se placer dans le dossier openfisca-france-indirect-taxation
		- `pip install -e .` 


**Configurer le chemin des données sources**

   - Aller dans le sous-dossier nommé `runner` du repo Openfisca-France-Indirect-Taxation.
   - Copier les fichiers `openfisca_survey_manager_config` et `openfisca_survey_manager_raw_data` et les coller dans son dossier `\.config` (dans C:\Users\veve1\.config) au sein d'un sous-dossier à nommer `openfisca-survey-manager`. 
   - Renommer les deux fichiers respectivement `config` et `raw_data`.
   - S'assurer que l'extension des fichiers est bien .ini
   - Dans le fichier `raw_data`, renseigner le chemin des données sources indiquées (BDF, EL, ET, ERFS FPR). 
Toutes ces données sont présentes dans le dossier (C:\Users\veve1\OneDrive\Documents\ENSAE 3A\Memoire MiE\Data). Supprimer les lignes correspondantes aux données "aliss".
   - Créer un dossier `data_collections` à l'endroit souhaité (ex :  `C:\Users\veve1\OneDrive\Documents\ENSAE 3A\Memoire MiE\Data\data_collections`) ainsi que deux sous-dossiers à l'intérieur nommés `tmp` et `output`.
   - Dans le fichier `config`, renseigner les chemins de ces dossiers aux lignes correspondantes.<br><br>


**Construire les collections**

Depuis le dossier "openfisca-france-indirect-taxation", lancer les scripts suivants :
- `build-collection -c budget_des_familles -d -m -s 2011`
- `build-collection -c budget_des_familles -d  -s 2017` #on a retiré le -m pour que le fichiers de métadonnées soit complété et non écrasé

- `build-collection -c enquete_logement -d -m -s 2006`
- `build-collection -c enquete_logement -d  -s 2013` #on a retiré le -m pour que le fichiers de métadonnées soit complété et non écrasé


- `build-collection -c enquete_transports -d -m -s 2008`
- `build-collection -c enquete_transports -d  -s 2019` #on a retiré les -m pour que le fichiers de métadonnées soit complété et non écrasé


- `build-collection -c erfs_fpr -d -m -s 2015`
- `build-collection -c erfs_fpr -d -s 2017`#on a retiré les -m pour que le fichiers de métadonnées soit complété et non écrasé

Lors de l'exécution de ces scripts, éventuellement prendre garde aux problèmes de chemin d'accès aux répertoires de données. 
!!! Le module gère les espaces mais pas les accents !!!
Pour la doc :  https://pypi.org/project/OpenFisca-Survey-Manager/0.47.2/

**Construire les données**
- Lancer le script `openfisca_france_indirect_taxation\scripts\build_survey_data.py`
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

