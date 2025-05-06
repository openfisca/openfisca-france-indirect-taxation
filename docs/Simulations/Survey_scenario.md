
# Créer un survey scenario

La méthode `create` de la classe SurveyScenario prend comme arguments : 
- `data_year` : année des données à utiliser;
- `input_data_frame` : données d'entrées pour la simulation, si rien n'est précisé le survey scenario va les chercher en utilisant la fonction `get_input_data_frame`pour l'année des données;  
- `calibration_kwargs` : ...;
- `inflation_kwargs` : dictionnaire utiliser pour caler/viellir les données, le dictionnaire renseigne pour chaque variable à inflater, soit le coefficient multiplicatif ('inflator_by_variable'), soit la cible à atteindre ('target_by_variable');
- `elasticities` : élasticités à utiliser pour simuler avec réponse comportementale;  
- `baseline_tax_benefit_system` : système socio-fiscal de référence;
- `reform` : fonction qui, appliquée au système de référence, donne le système réformé (optionnel, et appliqué seulement si `tax_benefit_sytem`n'est pas renseigné)
- `tax_benefit_system` : système socio-fiscal contenant une réforme par rapport au `baseline_tax_benefit_system` (optionnel); 
- ` year` : année de la simulation.

# Système socio-fiscal 

Le système socio-fiscal de base est celui de la classe `FranceIndirectTaxationTaxBenefitSystem`. 
Il rassemble tous les paramètres de la législation codés dans le modèle (openfisca_france_indirect_taxation/parameters/), des données de prix et de montants (`preprocessing` et `series_rv`) ainsi que toutes les variables définies dans le modèle (openfisca_france_indirect_taxation/variables). Tous les postes de consommation venant de la nomenclature COICOP ainsi que leur catégorie fiscale associée y sont également présents. 

## Calcul des dépenses hors-taxes

Pour chacun des postes, une variable `depense_ht_poste_` est calculée en retirant la TVA aux dépenses TTC, à l'aide de la fonction `generate_depenses_ht_postes_variables()`.
Il est important de noter que le SurveyScenario utilise les paramètres définis dans le système socio-fiscal (de base ou réformé) pour effectuer ce calcul. Ainsi, un système dont on a changé les taux de TVA prend en compte ces nouveaux taux pour calculer les dépenses ht, ce qui aboutit à avoir des dépenses ht différentes entre la baseline et le système réformé.