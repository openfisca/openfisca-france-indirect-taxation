# Les différents types de données et leur articulation

Afin de réaliser le modèle de microsimulation le plus adpaté aux besoins de l'utilisateur, il est nécessaire d'exploiter différents type de données:
 - données micro issues d'enquêtes sur la consommation individuelle des ménages (enquête budget des familles de l'INSEE ou autre),
 - informations tirées de la législation (taux de TVA, TICPE, _etc_.),
 - données agrégées afin d'effectuer d'inflater en masse, de réaliser des calages (éventuellement sur marges) et ou de veillir les données microéconomiques.

Il est nécessaire de pouvoir réaliser une correspondace entre les différents postes de consommation (et leurs divers agrégats)

# Préparation des données

## Importation des données brutes

Le modèles de taxation indirecte peut être alimenter par des données d'enquête.
Il est pariculièrement adapté aux données de l'enquête [budget des familles] (http://www.reseau-quetelet.cnrs.fr/spip/article.php3?id_article=128&lang=fr&ords_target=simple&ords_source=simple_form)
de l'INSEE telles que livrées par le [réseau Quetelet] (http://www.reseau-quetelet.cnrs.fr/spip/).

Afin de manipuler les tables des différentes enquêtes budget des familles par l'intermdéiaire de programmes écrit en python, il convient de convertir les données brutes sous le format [HDF5] (https://www.hdfgroup.org/HDF5/). Sous ce format, les tables sont aisément manipulables à l'aide de la bibliothèque [pandas] (pandas.pydata.org).
La conversion est réalisée par le script [build_collection] (https://github.com/openfisca/openfisca-survey-manager/blob/master/openfisca_survey_manager/scripts/build_collection.py) fourni avec le package [openfisca-survey-manager] (https://github.com/openfisca/openfisca-survey-manager).

Les années traitées sont 2011, 2005, 2000.

## Construction de la base d'entrée du modèle

La construction de la base d'entrée du modèle à partir des données d'enquête, une fois celle-ci converties au format HDF5 se fait en [plusieurs étapes] (https://github.com/openfisca/openfisca-france-indirect-taxation/tree/master/openfisca_france_indirect_taxation/build_survey_data).   
