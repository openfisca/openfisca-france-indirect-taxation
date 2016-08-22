# Calage et ajustement en utilisant les aggrégats kantar et les élasticités

Nous décrivons ici les étapes nécessaires au calage des dépenses issues de l'enquête budegt des familles
à l'aide des agrégats des postes Kantar fournis par ALISS ainsi que des élasticités estimées sur des ensembles
de ces postes Kantar.


## Spécificité de l'exercice

Nous disposons de plusieurs nomenclature:
 - une nomenclature des postes Coicop enrichie afin que chaque poste dispose d'un taux de taxation indirecte.
Cette nomenclature est la nomenclature naturelle du modèle. Elle es détaillée dans la section [idoine] (../../.../docs/data.md)

 - une nomenclature Kantar plus fine que la nomenclature Coicop

 - une nomenclature agrégée dite nomenclature F  

## Calage de la dépense initiale sur les dépenses de l'enquête budget des familles

Partant de'hypothèse que les dépenses alimentaires sont plus fiables dans l'enquête budget des familles (2011)
que dans les enquêtes Kantar, nous calons les parts budgétaires alimentaires (part dans le budget alimentaire)
des différents postes        


## Elasticités des postes agrégés

Il s'agit élasticités prix directes et croisées, de catégories de produit données dans la nomenclature assez agrégée, dite nomenclature F, pour des ménages types (T). Les ménages types (T) sont définis en croisant 4 catégories de revenu et 4 catégories d'âge. Ces données sont fournies disponibles dans l'article de Caillavet et. al (TODO link).

 - La nomenclature F est donnée dans la table A1 de Caillavet et. al.  (TODO link). 
 - Les ménages types (T) sont définis en croisant 4 catégories de revenu et 4 catégories d’âge et sont définis
dans la table A2 de Caillavet et. al. (TODO link).
 - Les tables B4-B16 rassemblent les élasticités prix directes et croisées pour les 16 catégories de ménage. Elles sont disponibles pour chaque type de ménage dans ce [répertoire] (https://github.com/openfisca/openfisca-france-indirect-taxation/tree/api_migration/openfisca_france_indirect_taxation/assets/aliss) mais également rassemblée dans ce [fichier] (https://github.com/openfisca/openfisca-france-indirect-taxation/blob/api_migration/openfisca_france_indirect_taxation/assets/aliss/cross_price_elasticities.csv). 
 - La table B3 rassemble les élasticités-dépenses qui son également disponibles dans ce [fichier] (https://github.com/openfisca/openfisca-france-indirect-taxation/blob/api_migration/openfisca_france_indirect_taxation/assets/aliss/food-expenditure-elasticities.csv).  

Afin de pouvoir utiliser ces élasticités, il est nécessaire de pouvoir passer de la nomenclature Coicop à la nomenclature F.
Cette dernière est une nomenclature agrégée de la nomenclature Kantar. Le laboratoire ALISS a donc fournir une table appariant les produits de la nomenclature Kantar à ceux de la nomenclature Coicop d’un côté et à ceux de la nomemclature F de l’autre.
Il faut noter cependant qu'une catégorie de la nomenclature Kantar n’appartient qu’à une seule catégorie Nomenclature F et à une seule catégorie de la nomenclature Coicop. En sus de la correspondance entre produits, sont fournis les quantités consommées, les prix unitaires et le poids des populations concernées ventilées au niveau des ménages types mentionnés ci-dessus.

La base fournie par ALISS est traitée dans le script [calibration_aliss] (../../build_survey_data/calibration_aliss.py). Le  calcul des dépenses selon les différentes nomenclature est réalisé par la fonction [`compute_expenditures`] ( ../../build_survey_data/calibration_aliss.py#L190). Le fichier produit est [consultable] (./expenditures.csv). 

A l'aide des matrices de passage de la nomenclature F à la nomenclature Kantar, il est possible selon certaine hypothèses (voir Annexe) de déduire des élastcités sur les produits de la nomenclature Kantar à l'aide de ceux de la nomenclature F pour chacun des ménages types (Voir la fonction [`compute_kantar_elasticities`] (../../build_survey_data/calibration_aliss.py#251))

## Calage et intégration de la réaction comportmentale

Les données d'entrée du modèle de micro-simulation TAXIPP sont les données budget des familles obéissant à la nomenclature Coicop. Elles sont utilisées pour caler les données Kantar au niveau des ménages types mentionnées ci-dessus. Ces cales sont conservées pour usage ultérieure.

Une fois déduites les élastcités au niveau des produits de la nomenclature Kantar, il est possible de déterminer les nouveaux budgets alimentaires des ménages types.  

Il est alors possible d'utiliser les cales calculées précédemment pour caler les budgets alimentaires dans le modèle TAXIPP.
L'analyse des divers impacts sur les revenus des ménages peut ainsi être conduite dans le modèle TAXIPP ( (Voir la fonction [`get_adjusted_input_data_frame`] (../../build_survey_data/calibration_aliss.py#515)).


