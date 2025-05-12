# Survey Scenario

Un *Survey Scenario* est un ensemble d'une ou deux simulations. Chacune de ces simulations consiste en la combinaison entre une base de données ordonnées et structurée, munie d'un système socio-fiscal fonctionnant sur ces données. Le *Survey Scenario* permet ainsi d'interfacer données et système socio-fiscal, et de faire des calculs sur une référence (baseline), et des réformes (le cas échéant). 

## Créer un survey scenario

La méthode `create` de la classe SurveyScenario prend comme arguments : 
- `data_year` : année des données à utiliser;
- `input_data_frame` : données d'entrées pour la simulation, si rien n'est précisé le survey scenario va les chercher en utilisant la fonction `get_input_data_frame` pour l'année des données;  
- `calibration_kwargs` : ...;
- `inflation_kwargs` : dictionnaire utiliser pour caler/viellir les données, le dictionnaire renseigne pour chaque variable à inflater, soit le coefficient multiplicatif (`inflator_by_variable`), soit la cible à atteindre (`target_by_variable`);
- `elasticities` : élasticités à utiliser pour simuler avec réponse comportementale;  
- `baseline_tax_benefit_system` : système socio-fiscal de référence;
- `reform` : fonction qui, appliquée au système de référence, donne le système réformé (optionnel, et appliqué seulement si `tax_benefit_sytem`n'est pas renseigné);
- `tax_benefit_system` : système socio-fiscal contenant une réforme par rapport au `baseline_tax_benefit_system` (optionnel); 
- ` year` : année de la simulation.