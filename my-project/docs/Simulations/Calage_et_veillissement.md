# Calage et vieillissement

L'objectif du modèle est de pouvoir simuler, sur une base représentative de la population Française et pour une année donnée, les effets de la fiscalité indirecte (quels qu'en soient les paramètres). Dans un premier temps, il est nécessaire de s'assurer que la base constituée rend bien compte des comportements de consommation et des revenus de la population Française pour l'année des données, on parle de calage des données. 
Ensuite, cette base peut être mise à jour pour une année cible, on parle de veillissement.
    
## La consommation des ménages

### Calage    

Les données de BdF sous-estiment fortement la consommation des ménages. En se basant sur la comptabilité nationale pour l'année des données, on peut caler les dépenses pour que les agrégats correspondent. On utilise la base la plus récente dans la comptabilité nationale nous permettant d'obtenir des agrégats de consommation des ménages à un niveau fin : [Consommation finale effective par fonction](https://www.insee.fr/fr/statistiques/fichier/8068592/T_CONSO_EFF_FONCTION.xlsx). La nomenclature COICOP des données BdF a été ajustée au préalable pour être compatible avec cette source. On se place au niveau le plus fin possible (124 postes de consommation). Autrement dit, on veut que sur chacun de ces 124 postes de consommation, la somme pondérée des dépenses dans BdF soit égale aux dépenses totales de ce poste dans la comptabilité nationale pour l'année 2017.

### Vieillissement

Une fois que les dépenses de consommation sont alignées sur la comptabilité nationale pour l'année des données, il est possible de les vieillir pour représenter n'importe quelle année cible. On peut vieillir la consommation et les revenus jusqu'en 2023 en utilisant les bases de données de la comptabilité nationale utilisées pour l'étape de calage. 
Pour l'année 2024, la méthode consiste à veillir jusqu'à 2023 puis utiliser les comptes trimestriels pour inflater de 2023 à 2024 : [Consommation des ménages par produit](https://www.insee.fr/fr/statistiques/fichier/8358378/t_conso_val.xls). Lors de cette dernière étape la consommation est inflatée uniformément.

Ces deux opérations sont réalisés à l'aide des fonctions du code `calage_consommation_bdf.py`. 

## Les revenus (et les niveaux de vie)

On fait le choix de caler et vieillir les niveaux de vie par dixième d'individus. Pour cela on peut utiliser plusieurs sources comme l'ERFS ou bien les niveaux de vie moyens par dixième dans la base de TaxIPP. Peut importe la source, la fonction `calage_bdf_niveau_vie` du fichier `Calage_revenus_bdf.py` permet d'inflater (ou déflater) les revenus disponibles des ménages de sortes à avoir les bons niveaux de vie moyens par dixième d'individus.