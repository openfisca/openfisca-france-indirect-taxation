
# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from openfisca_france_indirect_taxation.model.base import *


class poste_coicop_111(
    column = FloatCol()
    entity_class = Menages
    label = u"Pain et céréales"

class poste_coicop_112(
    column = FloatCol()
    entity_class = Menages
    label = u"Viande"

class poste_coicop_113(
    column = FloatCol()
    entity_class = Menages
    label = u"Poisson et fruits de mer"

class poste_coicop_114(
    column = FloatCol()
    entity_class = Menages
    label = u"Lait, fromage et œufs"

class poste_coicop_115(
    column = FloatCol()
    entity_class = Menages
    label = u"Huiles et graisses"

class poste_coicop_1151(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Margarines et autres graisses végétales"

class poste_coicop_116(
    column = FloatCol()
    entity_class = Menages
    label = u"Fruits"

class poste_coicop_117(
    column = FloatCol()
    entity_class = Menages
    label = u"Légumes"

class poste_coicop_118(
    column = FloatCol()
    entity_class = Menages
    label = u"Sucre, confiture, miel, chocolat et confiserie"

class poste_coicop_1181(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Confiserie"

class poste_coicop_119(
    column = FloatCol()
    entity_class = Menages
    label = u"Produits alimentaires non compris ailleurs"

class poste_coicop_121(
    column = FloatCol()
    entity_class = Menages
    label = u"Café, thé et cacao"

class poste_coicop_122(
    column = FloatCol()
    entity_class = Menages
    label = u"Eaux minérales, boissons rafraîchissantes, jus de fruits et  de légumes"

class poste_coicop_211(
    column = FloatCol()
    entity_class = Menages
    label = u"Alcools de bouche "

class poste_coicop_212(
    column = FloatCol()
    entity_class = Menages
    label = u"Vin et boissons fermentées"

class poste_coicop_213(
    column = FloatCol()
    entity_class = Menages
    label = u"Bière"

class poste_coicop_2201(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Cigarettes"

class poste_coicop_2202(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Cigares et cigarillos"

class poste_coicop_2203(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Tabac sous d'autres formes"

class poste_coicop_230(
    column = FloatCol()
    entity_class = Menages
    label = u"Stupéfiants"

class poste_coicop_311(
    column = FloatCol()
    entity_class = Menages
    label = u"Tissus pour habillement"

class poste_coicop_312(
    column = FloatCol()
    entity_class = Menages
    label = u"Vêtements"

class poste_coicop_313(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres articles et accessoires d'habillement"

class poste_coicop_314(
    column = FloatCol()
    entity_class = Menages
    label = u"Nettoyage, réparation et location d'articles d'habillement"

class poste_coicop_321(
    column = FloatCol()
    entity_class = Menages
    label = u"Chaussures diverses"

class poste_coicop_322(
    column = FloatCol()
    entity_class = Menages
    label = u"Cordonnerie et location de chaussures"

class poste_coicop_411(
    column = FloatCol()
    entity_class = Menages
    label = u"Loyers effectivement payés par les locataires"

class poste_coicop_412(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres loyers effectifs"

class poste_coicop_421(
    column = FloatCol()
    entity_class = Menages
    label = u"Loyers fictifs des propriétaires occupants"

class poste_coicop_422(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres loyers fictifs"

class poste_coicop_431(
    column = FloatCol()
    entity_class = Menages
    label = u"Fournitures pour travaux d'entretien et de réparation des logements"

class poste_coicop_432(
    column = FloatCol()
    entity_class = Menages
    label = u"Services concernant l'entretien et les réparations du logement"

class poste_coicop_441(
    column = FloatCol()
    entity_class = Menages
    label = u"Alimentation en eau"

class poste_coicop_442(
    column = FloatCol()
    entity_class = Menages
    label = u"Collecte des ordures ménagères"

class poste_coicop_443(
    column = FloatCol()
    entity_class = Menages
    label = u"Reprise des eaux usées"

class poste_coicop_444(
    column = FloatCol()
    entity_class = Menages
    label = u"Service divers liés au logement non compris ailleurs"

class poste_coicop_451(
    column = FloatCol()
    entity_class = Menages
    label = u"Electricité"

class poste_coicop_4511(
    column = FloatCol()
    entity_class = Menages
    label = u"Facture EDF GDF non dissociables"

class poste_coicop_452(
    column = FloatCol()
    entity_class = Menages
    label = u"Gaz"

class poste_coicop_4522(
    column = FloatCol()
    entity_class = Menages
    label = u"Achat de butane, propane"

class poste_coicop_453(
    column = FloatCol()
    entity_class = Menages
    label = u"Combustibles liquides"

class poste_coicop_454(
    column = FloatCol()
    entity_class = Menages
    label = u"Combustibles solides"

class poste_coicop_455(
    column = FloatCol()
    entity_class = Menages
    label = u"Energie thermique"

class poste_coicop_511(
    column = FloatCol()
    entity_class = Menages
    label = u"Meubles et articles d'ameublement"

class poste_coicop_512(
    column = FloatCol()
    entity_class = Menages
    label = u"Tapis et revêtements de sols divers"

class poste_coicop_513(
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation de meubles, d'articles d'ameublement et de revêtements souples pour le sol"

class poste_coicop_520(
    column = FloatCol()
    entity_class = Menages
    label = u"Article de ménage en textiles"

class poste_coicop_531(
    column = FloatCol()
    entity_class = Menages
    label = u"Gros appareils ménagers, électriques ou non"

class poste_coicop_532(
    column = FloatCol()
    entity_class = Menages
    label = u"Petits appareils électroméangers"

class poste_coicop_533(
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation d'appareils ménagers"

class poste_coicop_540(
    column = FloatCol()
    entity_class = Menages
    label = u"Verrerie, vaisselle et ustensiles de ménage"

class poste_coicop_551(
    column = FloatCol()
    entity_class = Menages
    label = u"Gros outillage et matériel"

class poste_coicop_552(
    column = FloatCol()
    entity_class = Menages
    label = u"Petit outillage et accessoires divers"

class poste_coicop_561(
    column = FloatCol()
    entity_class = Menages
    label = u"Biens d'équipement ménager non durables"

class poste_coicop_562(
    column = FloatCol()
    entity_class = Menages
    label = u"Services domestiques et services ménagers"

class poste_coicop_611(
    column = FloatCol()
    entity_class = Menages
    label = u"Produits pharmaceutiques"

class poste_coicop_612(
    column = FloatCol()
    entity_class = Menages
    label = u"Produits médicaux divers"

class poste_coicop_613(
    column = FloatCol()
    entity_class = Menages
    label = u"Appareils et matériel thérapeutiques"

class poste_coicop_621(
    column = FloatCol()
    entity_class = Menages
    label = u"Services médicaux"

class poste_coicop_622(
    column = FloatCol()
    entity_class = Menages
    label = u"Services dentaires"

class poste_coicop_623(
    column = FloatCol()
    entity_class = Menages
    label = u"Services paramédicaux"

class poste_coicop_630(
    column = FloatCol()
    entity_class = Menages
    label = u"Services hospitaliers"

class poste_coicop_711(
    column = FloatCol()
    entity_class = Menages
    label = u"Voitures automobiles"

class poste_coicop_712(
    column = FloatCol()
    entity_class = Menages
    label = u"Motocycles"

class poste_coicop_713(
    column = FloatCol()
    entity_class = Menages
    label = u"Bicyclettes"

class poste_coicop_721(
    column = FloatCol()
    entity_class = Menages
    label = u"Pièces de rechange et accessoires pour véhicules de tourisme "

class poste_coicop_722(
    column = FloatCol()
    entity_class = Menages
    label = u"Carburants et lubrifiants pour véhicules de tourisme"

class poste_coicop_723(
    column = FloatCol()
    entity_class = Menages
    label = u"Entretien et réparation de véhicules particuliers"

class poste_coicop_724(
    column = FloatCol()
    entity_class = Menages
    label = u"Services divers liés aux véhicules particuliers"

class poste_coicop_731(
    column = FloatCol()
    entity_class = Menages
    label = u"Transport ferroviaire de passagers"

class poste_coicop_732(
    column = FloatCol()
    entity_class = Menages
    label = u"Transport routier de passagers"

class poste_coicop_733(
    column = FloatCol()
    entity_class = Menages
    label = u"Transport aérien de passagers"

class poste_coicop_734(
    column = FloatCol()
    entity_class = Menages
    label = u"Transport maritime et fluvial de passagers"

class poste_coicop_735(
    column = FloatCol()
    entity_class = Menages
    label = u"Transport combiné de passagers"

class poste_coicop_736(
    column = FloatCol()
    entity_class = Menages
    label = u"Services de transport divers"

class poste_coicop_810(
    column = FloatCol()
    entity_class = Menages
    label = u"Services postaux"

class poste_coicop_831(
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de téléphonie et de télécopie"

class poste_coicop_832(
    column = FloatCol()
    entity_class = Menages
    label = u"Services de téléphonie et de télécopie"

class poste_coicop_911(
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de réception, d'enregistrement et de reproduction du son et de l'image"

class poste_coicop_912(
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel photographique et cinématographique et appareils optiques"

class poste_coicop_913(
    column = FloatCol()
    entity_class = Menages
    label = u"Matériel de traitement de l'information"

class poste_coicop_914(
    column = FloatCol()
    entity_class = Menages
    label = u"Supports d'enregistrement"

class poste_coicop_915(
    column = FloatCol()
    entity_class = Menages
    label = u"Réparation de matériel audiovisuel, photographique et de traitement de l'information"

class poste_coicop_921(
    column = FloatCol()
    entity_class = Menages
    label = u"Biens durables pour loisirs de plein air"

class poste_coicop_922(
    column = FloatCol()
    entity_class = Menages
    label = u"Instruments de musique et biens durables destinés aux loisirs d'intérieur"

class poste_coicop_923(
    column = FloatCol()
    entity_class = Menages
    label = u"Entretien et réparation des autres biens durables à fonction récréatives et culturelles"

class poste_coicop_931(
    column = FloatCol()
    entity_class = Menages
    label = u"Jeux, jouets et passe-temps"

class poste_coicop_932(
    column = FloatCol()
    entity_class = Menages
    label = u"Articles de sport, matériel de camping et matériel pour activités de plein air"

class poste_coicop_933(
    column = FloatCol()
    entity_class = Menages
    label = u"Produits pour jardin, plantes et fleurs"

class poste_coicop_934(
    column = FloatCol()
    entity_class = Menages
    label = u"Animaux de compagnie et articles connexes"

class poste_coicop_935(
    column = FloatCol()
    entity_class = Menages
    label = u"Services vétérinaires et autres services pour animaux de compagnie"

class poste_coicop_941(
    column = FloatCol()
    entity_class = Menages
    label = u"Services récréatifs et sportifs"

class poste_coicop_942(
    column = FloatCol()
    entity_class = Menages
    label = u"Services culturels"

class poste_coicop_943(
    column = FloatCol()
    entity_class = Menages
    label = u"Jeux de hasard"

class poste_coicop_951(
    column = FloatCol()
    entity_class = Menages
    label = u"Livre"

class poste_coicop_952(
    column = FloatCol()
    entity_class = Menages
    label = u"Journaux et publications périodiques"

class poste_coicop_953(
    column = FloatCol()
    entity_class = Menages
    label = u"Imprimés divers"

class poste_coicop_954(
    column = FloatCol()
    entity_class = Menages
    label = u"Papeterie et matériel de dessin"

class poste_coicop_960(
    column = FloatCol()
    entity_class = Menages
    label = u"Forfaits touristiques "

class poste_coicop_1010(
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement préélémentaire et primaire"

class poste_coicop_1020(
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement secondaire"

class poste_coicop_1030(
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement postsecondaire non supérieur"

class poste_coicop_1040(
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement supérieur"

class poste_coicop_1050(
    column = FloatCol()
    entity_class = Menages
    label = u"Enseignement non défini par niveau"

class poste_coicop_11112(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Restauration à emporter"

class poste_coicop_11113(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Restauration sur place"

class poste_coicop_11114(
    column = FloatCol()
    entity_class = Menages
    label = u">>> Consommation de boissons alcoolisées"

class poste_coicop_1112(
    column = FloatCol()
    entity_class = Menages
    label = u"Cantines"

class poste_coicop_1120(
    column = FloatCol()
    entity_class = Menages
    label = u"Services d'hébergement"

class poste_coicop_1211(
    column = FloatCol()
    entity_class = Menages
    label = u"Salons de coiffure et instituts de soins et de beauté"

class poste_coicop_1212(
    column = FloatCol()
    entity_class = Menages
    label = u"Appareils électriques pour soins corporels"

class poste_coicop_1213(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres appareils, articles et produits pour soins corporels"

class poste_coicop_1220(
    column = FloatCol()
    entity_class = Menages
    label = u"Prostitution"

class poste_coicop_1231(
    column = FloatCol()
    entity_class = Menages
    label = u"Articles de bijouterie et horlogerie"

class poste_coicop_1232(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres effets personnels"

class poste_coicop_1240(
    column = FloatCol()
    entity_class = Menages
    label = u"Protection sociale"

class poste_coicop_1251(
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance vie"

class poste_coicop_1252(
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance habitation"

class poste_coicop_1253(
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance maladie"

class poste_coicop_1254(
    column = FloatCol()
    entity_class = Menages
    label = u"Assurance transports"

class poste_coicop_1255(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres assurances"

class poste_coicop_1261(
    column = FloatCol()
    entity_class = Menages
    label = u"Coûts des services d'intermédiation financière indirectement mesurés"

class poste_coicop_1262(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres services financiers non compris ailleurs"

class poste_coicop_1270(
    column = FloatCol()
    entity_class = Menages
    label = u"Autres services non compris ailleurs"

class poste_coicop_9901(
    column = FloatCol()
    entity_class = Menages
    label = u"caution pour la location d'un logement"

class poste_coicop_9902(
    column = FloatCol()
    entity_class = Menages
    label = u"achats de logements, garages, parkings, box et terrains"

class poste_coicop_9903(
    column = FloatCol()
    entity_class = Menages
    label = u"Gros travaux d'entretien dans les logements"

class poste_coicop_9911(
    column = FloatCol()
    entity_class = Menages
    label = u"impôts et taxes de la résidence principale"

class poste_coicop_9912(
    column = FloatCol()
    entity_class = Menages
    label = u"impôts et taxes résidence secondaire ou autre logement"

class poste_coicop_9913(
    column = FloatCol()
    entity_class = Menages
    label = u"impôts sur le revenu"

class poste_coicop_9914(
    column = FloatCol()
    entity_class = Menages
    label = u"taxes automobile"

class poste_coicop_9915(
    column = FloatCol()
    entity_class = Menages
    label = u"autres impôts et taxes"

class poste_coicop_9921(
    column = FloatCol()
    entity_class = Menages
    label = u"remboursements de prêts résidence principale"

class poste_coicop_9922(
    column = FloatCol()
    entity_class = Menages
    label = u"remboursements de prêts résidence secondaire ou autre logement"

class poste_coicop_9923(
    column = FloatCol()
    entity_class = Menages
    label = u"autres remboursements de prêts"

class poste_coicop_9931(
    column = FloatCol()
    entity_class = Menages
    label = u"argent donné au sein du ménage"

class poste_coicop_9932(
    column = FloatCol()
    entity_class = Menages
    label = u"aides et cadeaux en argent offerts par le ménage (à des membres de la famille ne"

class poste_coicop_9933(
    column = FloatCol()
    entity_class = Menages
    label = u"cadeaux offerts (argent ou bien) sai"

class poste_coicop_9941(
    column = FloatCol()
    entity_class = Menages
    label = u"prélèvements de l'employeur"
