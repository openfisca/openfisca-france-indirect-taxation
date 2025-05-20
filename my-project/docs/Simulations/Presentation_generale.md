# Simulations
Une fois la base de données construite, le modèle openfisca-france-indirect-taxation consiste à connecter ces données à un calculateur socio-fiscal (à savoir OpenFisca-france), et à utiliser cette jointure pour produire des simulations. Cette partie de la documentation décrit ces processus. 

L'ensemble de ces opérations sont réalisées autour de la définition et de l'utilisation de *survey scenarios*. Un *survey scenario* est le fruit de trois composantes : un jeu de données, un ou deux systèmes socio-fiscaux (un système "baseline" et un système réformé le cas échéant) et un ensebmle d'opérations pour faire le lien entre données et simulateur socio-fiscal. Dit autrement, la création d'un survey scenario consiste à générer une ou deux simulations, c'est-à-dire une ou deux applications d'un système socio-fiscal (un *tax and benefit system*) à des données.

- Préalablement à la création d'un *survey scenario*, il faut définir les systèmes socio-fiscaux qui doivent lui être associés. Cette opération est expliquée dans la partie [Legislation](./Legislation.md).
- La connexion entre données et simulateur nécessite également des opérations d'ajustement, notamment des ajustements des données afin qu'elle puissent être appliquées au système socio-fiscal (vieillissement des bases de données notamment). Ces opérations sont dtéaillées dans la partie [Calage et vieillissement](./Calage_et_veillissement.md).
- La création du *survey scenario* est expliquée dans la partie [Survey Scenario](./Survey_scenario.md).
- L'utilisation du *survey scenario* pour simuler la législation de TVA en vigueur ainsi qu'une réforme est décrite dans cet [Exemple](./Exemple_utilisation.md).

