# Construction

On décrit ci-dessous les différentes étapes pour passer des différentes sources de données brutes à la base qui servira d'entrée au modèle de microsimulation.

## Importation des données d'enquêtes brutes

Afin de manipuler les tables des différentes enquêtes par l'intermdéiaire de programmes écrit en python, il convient de convertir les données brutes sous le format [HDF5](https://www.hdfgroup.org/HDF5/). Sous ce format, les tables sont aisément manipulables à l'aide de la bibliothèque [pandas](https://pandas.pydata.org/).
La conversion est réalisée par le script `build_collection.py` fourni avec le package [openfisca-survey-manager](https://github.com/openfisca/openfisca-survey-manager).

## Construction de la base d'entrée du modèle

La construction de la base d'entrée du modèle à partir des données d'enquête, une fois celles-ci converties au format HDF5 est réalisée par le script `build_survey_data.py`. Elle se fait en plusieurs étapes.

Quatre étapes en parallèle traitent les données issues des différentes tables de Budget de famille en s'adaptant aux différents millésimes : <br>
1. Gestion des dépenses de consommation : `build_depenses_homogenisees()` et `build_imputation_loyers_proprietaires()`. <br>
2. Gestion des véhicules : `build_homogeneisation_vehicules()`. <br>
3. Gestion des variables socio-démographiques :  `build_homogeneisation_caracteristiques_sociales()`. <br>
4. Gestion des variables revenus: `build_homogeneisation_revenus_menages()`. <br>

Une cinquième étape réalise ensuite l'[appariemment](Appariemment.md) avec les autres enquêtes (ENL, ENTD, ERFS).