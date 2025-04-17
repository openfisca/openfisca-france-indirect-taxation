# Préparation des données

## Les différents types de données

Plusieurs jeux de données différents par leur origine et leurs fonctions sont potentiellement mobilisées par le modèle de microsimulation:

- des données micro issues d'enquêtes sur la consommation individuelle des ménages (enquête budget des familles de l'INSEE ou autre),
- des informations tirées de la législation (taux de TVA, TICPE, _etc_.),
- des données agrégées afin d'effectuer d'inflater en masse, de réaliser des calages (éventuellement sur marges) et ou de veillir les données microéconomiques.

## Génération des tables de correspondance entre les différents type de données

Pour que le modèle de microsimulation soit à la fois assez générique pour répondre aux besoins divers des utilisateur et simple d'usage, il est nécessaire de pouvoir combiner efficacement les différents type de données et plus particulièrement celles concernant les postes de consommation qu'ils faut donc pouvoir repérer dans les différentes sources de données.

Comme les postes de consommation présents dans ces sources peuvent être plus ou moins agrégés, il est nécessaire de pouvoir réaliser une correspondance entre les différents postes de consommation issues des différentes sources, quelque soit leur niveaux d'agrégations.

A cette fin, une [table pivot] (https://github.com/openfisca/openfisca-france-indirect-taxation/blob/master/openfisca_france_indirect_taxation/assets/legislation/nomenclature_coicop.csv) est construite à partir de la [nomenclature COICOP] (http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/coicop1998/coicop1998.htm). Elle est enrichie par des postes supplémentaires en cas de nécessité (finesse insuffisante comme pour le tabac par exemple, postes non présents comme stupéfiants et prostitution).

Elle est produite à partir de sources brutes par l'exécution du programme `build_coicop_nomenclature`.
[TODO: à détailler, exemple d'exécution après mise en forme du script]

Des tables de correspondance sont également réalisées entre cette table pivot, les informations législatives et les données d'enquète.

### Table de correspondance entre la nomenclature COICOP enrichie et la législation

Les taux d'imposition des différents produits sont renseignés dans une [table de correspondance](https://github.com/openfisca/openfisca-france-indirect-taxation/blob/master/openfisca_france_indirect_taxation/assets/legislation/coicop_legislation.csv) construite à partir d'informations législatives.

Elle est produite à partir de sources brutes par l'exécution du programme `build_coicop_legislation`.
[TODO: à détailler, exemple d'exécution après mise en forme du script]

## Importation des données d'enquêtes brutes

Le modèle de taxation indirecte peut être alimentée par des données d'enquête.
Il est pariculièrement adapté aux données de l'enquête [budget des familles](http://www.reseau-quetelet.cnrs.fr/spip/article.php3?id_article=128&lang=fr&ords_target=simple&ords_source=simple_form)
de l'INSEE telles que fournies par le [réseau Quetelet](http://www.reseau-quetelet.cnrs.fr/spip/).

Afin de manipuler les tables des différentes enquêtes budget des familles par l'intermdéiaire de programmes écrit en python, il convient de convertir les données brutes sous le format [HDF5](https://www.hdfgroup.org/HDF5/). Sous ce format, les tables sont aisément manipulables à l'aide de la bibliothèque [pandas] (pandas.pydata.org).
La conversion est réalisée par le script [build_collection](https://github.com/openfisca/openfisca-survey-manager/blob/master/openfisca_survey_manager/scripts/build_collection.py) fourni avec le package [openfisca-survey-manager](https://github.com/openfisca/openfisca-survey-manager).

Les années traitées sont les enquêtes budget des familles 2011, 2005, 2000.

## Construction de la base d'entrée du modèle

La construction de la base d'entrée du modèle à partir des données d'enquête, une fois celle-ci converties au format HDF5 se fait en [plusieurs étapes](https://github.com/openfisca/openfisca-france-indirect-taxation/tree/master/openfisca_france_indirect_taxation/build_survey_data).
