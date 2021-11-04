# La valeur provient de la littérature.
# Hill & Legoupil (2018) trouvent -0,5 sur la période 1950-2015 et -0,4 sur la période 2000-2015

elasticite_tabac = -0.5#-0.78


# Consommation agrége de cigarettes (nombre de paquets consommés en France par an)
# Source : https://www.douane.gouv.fr/la-douane/opendata/categories/tabacs-manufactures/statistiques-des-ventes-en-france-continentale-et
# Ce lien renseigne pour le nombre de cigarettes consommées par mois en France métropolitaine
# On en déduit le nombre de paquets de 20 cigarettes consommés par an en France métropolitaine.

nombre_paquets_cigarettes_by_year = {
    2017: 2.21e9,
    2018: 2.01e9,
    2019: 1.86e9,
    2020: 1.78e9,
    }
