# Calage et vieillissement

L'objectif du modèle est de pouvoir simuler, sur une base représentative de la population Française et pour une année donnée, les effets de la fiscalité indirecte (quels qu'en soient les paramètres). Dans un premier temps, il est nécessaire de s'assurer que la base constituée rend bien compte des comportements de consommation et des revenus de la population Française pour l'année des données, on parle de calage des données. 
Ensuite, cette base peut être mise à jour pour une année cible, on parle de veillissement.
    
## Calage

Les données de BdF sous-estiment fortement la consommation des ménages. En se basant sur la comptabilité nationale pour l'année des données, on peut caler les dépenses pour que les agrégats correspondent.

### La consommation des ménages

On utilise la base la plus récente dans la comptabilité nationale nous permettant d'obtenir des agrégats de consommation des ménages à un niveau fin (https://www.insee.fr/fr/statistiques/fichier/8068592/T_CONSO_EFF_FONCTION.xlsx). La nomenclature COICOP des données BdF a été ajustée au préalable pour être compatible avec cette source. On se place au niveau le plus fin possible (124 postes de consommation).

### Les revenus 

On utilise la base la plus récente dans la comptabilité nationale nous permettant d'obternie les revenus disponibles des ménages ainsi que les loyers imputés (https://www.insee.fr/fr/statistiques/fichier/8068630/T_2101.xlsx). 


## Vieillissement

Une fois que les dépenses de consommation sont alignées sur la comptabilité nationale pour l'année des données, il est possible de les vieillir pour représenter n'importe quelle année cible. On peut vieillir la consommation et les revenus jusqu'en 2023 en utilisant les bases de données de la comptabilité nationale utilisées pour l'étape de calage. 
Pour l'année 2024, la méthode consiste à veillir jusqu'à 2023 puis utiliser les comptes trimestriels pour inflater de 2023 à 2024 (consommation : https://www.insee.fr/fr/statistiques/fichier/8358378/t_conso_val.xls ; revenus : https://www.insee.fr/fr/statistiques/fichier/8358386/t_men_val.xls). La consommation est inflatée uniformément.

Ces deux opérations sont réalisés à l'aide des fonctions du code `new_calage_bdf_cn.py`.