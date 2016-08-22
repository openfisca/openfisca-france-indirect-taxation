# Calage et ajustement en utilisant les aggrégats kantar et les élasticités

Nous décrivons ici les étapes nécessaires au calage des dépenses issues de l'enquête budegt des familles
à l'aide des agrégats des postes Kantar fournis par ALISS ainsi que des élasticités estimées sur des ensembles
de ces postes Kantar.


## Spécificité de l'exercice

Nous disposons de plusieurs nomenclature:
 - une nomenclature des postes COICOP enrichie afin que chaque poste dispose d'un taux de taxation indirecte.
Cette nomenclature est la nomenclature naturelle du modèle. Elle es détaillée dans la section [idoine] (../../.../docs/data.md)

 - une nomenclature Kantar plus fine que la nomenclature COICOP

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
