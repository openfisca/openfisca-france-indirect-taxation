## Importation des données d'enquêtes brutes

Afin de manipuler les tables des différentes enquêtes par l'intermdéiaire de programmes écrit en python, il convient de convertir les données brutes sous le format [HDF5](https://www.hdfgroup.org/HDF5/). Sous ce format, les tables sont aisément manipulables à l'aide de la bibliothèque [pandas](pandas.pydata.org).
La conversion est réalisée par le script [build_collection](../openfisca_survey_manager/scripts/build_collection.py) fourni avec le package [openfisca-survey-manager](https://github.com/openfisca/openfisca-survey-manager).

## Construction de la base d'entrée du modèle

La construction de la base d'entrée du modèle à partir des données d'enquête, une fois celles-ci converties au format HDF5 se fait en plusieurs étapes. 
Quatre étapes en parallèle traitent les données issues des différentes tables de Budget de famille en s'adaptant aux différents millésimes :
1. Gestion des dépenses de consommation : `build_depenses_homogenisees()` et `build_imputation_loyers_proprietaires()`.
2. Gestion des véhicules : `build_homogeneisation_vehicules()`.
3. Gestion des variables socio-démographiques:  `build_homogeneisation_caracteristiques_sociales()`.
4. Gestion des variables revenus: `build_homogeneisation_revenus_menages()`.

Une cinquième étape réalise l'[appariemment](Appariemment.md) avec les autres enquêtes (ENL, ENTD, ERFS).

La construction est réalisée par le script [build_survey_data](../openfisca_france_indirect_taxation/build_survey_data).