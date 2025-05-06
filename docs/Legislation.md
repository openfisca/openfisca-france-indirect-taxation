L'objectif du modèle est de pouvoir simuler, sur une base représentative de la population Française et pour une année donnée, les effets de la fiscalité indirecte.
Pour cela il convient de disposer des données de consommation des ménages et d'identifier quelle fiscalité s'applique à chacune de ses consommations.

La partie qui suit détaille les procédures qui permettent d'associer à chaque consommation présente dans les données, la fiscalité qui s'y rapporte.

# La nomenclature COICOP 

La consommation des ménages issue de l'enquête Budget de familles est classifiée selon la [nomenclature COICOP](https://www.insee.fr/fr/information/2408172).
Comme les postes de consommation issus de différentes sources peuvent être plus ou moins agrégés (comme par exemple dans les fichiers de la conmptabilité nationale utilisés pour le calage et vieillissement), il est nécessaire de pouvoir réaliser une correspondance entre les différents postes de consommation issues des différentes sources, quelque soit leur niveaux d'agrégations.

A cette fin, une [table pivot](openfisca_france_indirect_taxation/assets/legislation/nomenclature_coicop.csv) est construite à partir de la [nomenclature COICOP] (http://www.insee.fr/fr/methodes/default.asp?page=nomenclatures/coicop1998/coicop1998.html). Elle est enrichie par des postes supplémentaires en cas de nécessité (finesse insuffisante comme pour le tabac par exemple, postes non présents comme stupéfiants et prostitution). 

Elle est produite par l'exécution du programme `build_coicop_nomenclature`.

# Table de correspondance COICOP / legislation 

Les régimes d'imposition des différentes consommations sont renseignées dans une [table de correspondance](openfisca_france_indirect_taxation/assets/legislation/coicop_legislation.csv) construite à partir d'informations législatives sur la période 1994-2024.

Elle est produite par l'exécution du programme `build_coicop_legislation`.

# Les paramètres de la législation 

La plupart des paramètres de la législation nécessaires pour simuler la fiscalité indirecte sont regroupés dans le modèle. Ce sont des séries qui donnent, pour chaque année où il est modifié, la valeur d’un paramètre de la législation (ex: le taux normal de TVA, la TICPE sur le diesel ...). Actuellement, le modèle gère la TVA, les taxes sur le tabac et les alcools, les assurances, et les énergies. Côté préstation, le chèque énergie est également modélisé.
