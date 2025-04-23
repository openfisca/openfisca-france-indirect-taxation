# Calage et vieillissement

L'objectif du modèle est de pouvoir simuler, sur une base représentative de la population Française et pour une année donnée, les effets de la fiscalité indirecte (quels qu'en soient les paramètres). Il est donc nécessaire de s'assurer que la base consitituée rend bien compte des comportements de consommation de la population Française pour l'année des données, on parle de calage des données. Ensuite, cette base peut être mise à jour pour une année cible, on parle de veillissement.
    
## Calage
    Les données de BdF sous-estiment fortement la consommation des ménages. En se basant sur la comptabilité nationale pour l'année des données, on peut caler les dépenses pour que les agrégats correspondent.

## Vieillissement
    Une fois que les dépenses de consommation sont alignées sur la comptabilité nationale pour l'année des données, il est possible de les vieillir pour représenter n'importe qu'elle année cible.

Ces deux opérations peuvent être réalisés poste agrégé par poste agrégé, via les fonctions du code `new_calage_bdf_cn_by_postes_agreges` ou au niveau le plus fin permis par la comptabilité nationale, via les fonctions du code `new_calage_bdf_cn`.