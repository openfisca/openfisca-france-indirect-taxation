# Imputations de certaines dépenses 

L'appariemment BdF-ENTD est utilisé pour imputer les dépenses annuelles de carburants des ménages à partir des distances parcourues.
Pour chaque décile de niveau de vie, pour les ménages ruraux et les autres, on calcule les distances moyennes annuelles parcourues ainsi que les dépenses moyennes annuelles.
Les dépenses de carburants des ménages sont obtenues en multipliant le nombre de km parcourus par le prix moyen au km de leur catégorie (ratio des dépenses moyennes et distances moyennes).

Cette imputation est réalisé à la suite de l'appariemment par la fonction `cale_bdf_entd_matching_data()`.

