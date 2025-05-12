### Calcul des dépenses hors-taxes

Pour chacun des postes, une variable `depense_ht_poste_` est calculée en retirant la TVA aux dépenses TTC, à l'aide de la fonction `generate_depenses_ht_postes_variables()`.
Il est important de noter que le SurveyScenario utilise les paramètres définis dans le système socio-fiscal (de base ou réformé) pour effectuer ce calcul. Ainsi, un système dont on a changé les taux de TVA prend en compte ces nouveaux taux pour calculer les dépenses ht, ce qui aboutit à avoir des dépenses ht différentes entre la baseline et le système réformé.