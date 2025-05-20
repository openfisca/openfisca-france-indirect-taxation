# Guide d'installation
<br>

## Cloner le repo indirect-taxation (plus précisément la branche nomics-master qui nous intéresse)

- git clone -b 'nomics-master' 'https://github.com/Hervedarr31/openfisca-france-indirect-taxation.git' 

## Créer et configurer un nouvel environnement virtuel

### Option 1 : avec pyenv et pip 

- `py -3.9 -m venv openfiscaenv` 
- `myenv\Scripts\activate` <br>

### Option 2 : avec conda et le fichier environment.yml

- Se placer dans le dossier openfisca-france-indirect-taxation
- modifier le fichier `environment.yml` pour indiquer le nom (name: openfiscaenv) et le chemin (ex: prefix : C:\Users\user1\miniconda3\envs) 
- `conda env create -f environment.yml`

## Installer openfisca-france-indirect-taxation

- se placer dans le dossier openfisca-france-indirect-taxation
- `pip install -e .` 

## Configurer le chemin des données sources

- Aller dans le sous-dossier nommé `runner` du repo Openfisca-France-Indirect-Taxation.
- Copier les fichiers `openfisca_survey_manager_config` et `openfisca_survey_manager_raw_data` et les coller dans son dossier `\.config` (dans `C:\Users\user1\.config`) au sein d'un sous-dossier à nommer `openfisca-survey-manager`. 
- Renommer les deux fichiers respectivement `config` et `raw_data`.
- S'assurer que l'extension des fichiers est bien .ini
- Dans le fichier `raw_data`, renseigner le chemin des données sources indiquées (BDF, EL, ET, ERFS FPR). 
Toutes ces données sont présentes dans le dossier (`C:\Users\user1\OneDrive\Documents\Projet\Data\`). Supprimer les lignes correspondantes aux données "aliss".
- Créer un dossier `data_collections` à l'endroit souhaité (ex :  `C:\Users\user1\OneDrive\Documents\Projet\Data\data_collections`) ainsi que deux sous-dossiers à l'intérieur nommés `tmp` et `output`.
- Dans le fichier `config`, renseigner les chemins de ces dossiers aux lignes correspondantes.<br><br>


## Construire les collections 

Depuis le dossier "openfisca-france-indirect-taxation", lancer les scripts suivants :
 
- `build-collection -c budget_des_familles -d -m -s 2011`
- `build-collection -c budget_des_familles -d  -s 2017` #on a retiré le -m pour que le fichiers de métadonnées soit complété et non écrasé

- `build-collection -c enquete_logement -d -m -s 2006`
- `build-collection -c enquete_logement -d  -s 2013` #on a retiré le -m pour que le fichiers de métadonnées soit complété et non écrasé


- `build-collection -c enquete_transports -d -m -s 2008`
- `build-collection -c enquete_transports -d  -s 2019` #on a retiré les -m pour que le fichiers de métadonnées soit complété et non écrasé


- `build-collection -c erfs_fpr -d -m -s 2015`
- `build-collection -c erfs_fpr -d -s 2017` #on a retiré les -m pour que le fichiers de métadonnées soit complété et non écrasé

Lors de l'exécution de ces scripts, éventuellement prendre garde aux problèmes de chemin d'accès aux répertoires de données. 
!!! Le module gère les espaces mais pas les accents !!! <br>
Pour la doc :  https://pypi.org/project/OpenFisca-Survey-Manager/0.47.2/

## Construire les données
- Lancer le script `openfisca_france_indirect_taxation\scripts\build_survey_data.py`

