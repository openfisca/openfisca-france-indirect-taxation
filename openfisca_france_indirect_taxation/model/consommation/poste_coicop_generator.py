
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

from ..base import *


reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Pain et céréales",
    name = u'poste_coicop_111'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Viande",
    name = u'poste_coicop_112'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Poisson et fruits de mer",
    name = u'poste_coicop_113'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Lait, fromage et œufs",
    name = u'poste_coicop_114'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Huiles et graisses",
    name = u'poste_coicop_115'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Margarines et autres graisses végétales",
    name = u'poste_coicop_1151'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Fruits",
    name = u'poste_coicop_116'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Légumes",
    name = u'poste_coicop_117'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Sucre, confiture, miel, chocolat et confiserie",
    name = u'poste_coicop_118'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Confiserie",
    name = u'poste_coicop_1181'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Produits alimentaires non compris ailleurs",
    name = u'poste_coicop_119'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Café, thé et cacao",
    name = u'poste_coicop_121'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Eaux minérales, boissons rafraîchissantes, jus de fruits et  de légumes",
    name = u'poste_coicop_122'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Alcools de bouche ",
    name = u'poste_coicop_211'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Vin et boissons fermentées",
    name = u'poste_coicop_212'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Bière",
    name = u'poste_coicop_213'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Cigarettes",
    name = u'poste_coicop_2201'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Cigares et cigarillos",
    name = u'poste_coicop_2202'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Tabac sous d'autres formes",
    name = u'poste_coicop_2203'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Stupéfiants",
    name = u'poste_coicop_230'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Tissus pour habillement",
    name = u'poste_coicop_311'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Vêtements",
    name = u'poste_coicop_312'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres articles et accessoires d'habillement",
    name = u'poste_coicop_313'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Nettoyage, réparation et location d'articles d'habillement",
    name = u'poste_coicop_314'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Chaussures diverses",
    name = u'poste_coicop_321'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Cordonnerie et location de chaussures",
    name = u'poste_coicop_322'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Loyers effectivement payés par les locataires",
    name = u'poste_coicop_411'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres loyers effectifs",
    name = u'poste_coicop_412'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Loyers fictifs des propriétaires occupants",
    name = u'poste_coicop_421'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres loyers fictifs",
    name = u'poste_coicop_422'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Fournitures pour travaux d'entretien et de réparation des logements",
    name = u'poste_coicop_431'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services concernant l'entretien et les réparations du logement",
    name = u'poste_coicop_432'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Alimentation en eau",
    name = u'poste_coicop_441'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Collecte des ordures ménagères",
    name = u'poste_coicop_442'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Reprise des eaux usées",
    name = u'poste_coicop_443'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Service divers liés au logement non compris ailleurs",
    name = u'poste_coicop_444'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Electricité",
    name = u'poste_coicop_451'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Facture EDF GDF non dissociables",
    name = u'poste_coicop_4511'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Gaz",
    name = u'poste_coicop_452'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Achat de butane, propane",
    name = u'poste_coicop_4522'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Combustibles liquides",
    name = u'poste_coicop_453'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Combustibles solides",
    name = u'poste_coicop_454'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Energie thermique",
    name = u'poste_coicop_455'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Meubles et articles d'ameublement",
    name = u'poste_coicop_511'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Tapis et revêtements de sols divers",
    name = u'poste_coicop_512'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Réparation de meubles, d'articles d'ameublement et de revêtements souples pour le sol",
    name = u'poste_coicop_513'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Article de ménage en textiles",
    name = u'poste_coicop_520'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Gros appareils ménagers, électriques ou non",
    name = u'poste_coicop_531'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Petits appareils électroméangers",
    name = u'poste_coicop_532'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Réparation d'appareils ménagers",
    name = u'poste_coicop_533'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Verrerie, vaisselle et ustensiles de ménage",
    name = u'poste_coicop_540'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Gros outillage et matériel",
    name = u'poste_coicop_551'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Petit outillage et accessoires divers",
    name = u'poste_coicop_552'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Biens d'équipement ménager non durables",
    name = u'poste_coicop_561'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services domestiques et services ménagers",
    name = u'poste_coicop_562'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Produits pharmaceutiques",
    name = u'poste_coicop_611'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Produits médicaux divers",
    name = u'poste_coicop_612'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Appareils et matériel thérapeutiques",
    name = u'poste_coicop_613'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services médicaux",
    name = u'poste_coicop_621'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services dentaires",
    name = u'poste_coicop_622'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services paramédicaux",
    name = u'poste_coicop_623'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services hospitaliers",
    name = u'poste_coicop_630'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Voitures automobiles",
    name = u'poste_coicop_711'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Motocycles",
    name = u'poste_coicop_712'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Bicyclettes",
    name = u'poste_coicop_713'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Pièces de rechange et accessoires pour véhicules de tourisme ",
    name = u'poste_coicop_721'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Carburants et lubrifiants pour véhicules de tourisme",
    name = u'poste_coicop_722'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Entretien et réparation de véhicules particuliers",
    name = u'poste_coicop_723'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services divers liés aux véhicules particuliers",
    name = u'poste_coicop_724'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Transport ferroviaire de passagers",
    name = u'poste_coicop_731'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Transport routier de passagers",
    name = u'poste_coicop_732'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Transport aérien de passagers",
    name = u'poste_coicop_733'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Transport maritime et fluvial de passagers",
    name = u'poste_coicop_734'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Transport combiné de passagers",
    name = u'poste_coicop_735'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services de transport divers",
    name = u'poste_coicop_736'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services postaux",
    name = u'poste_coicop_810'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Matériel de téléphonie et de télécopie",
    name = u'poste_coicop_831'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services de téléphonie et de télécopie",
    name = u'poste_coicop_832'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Matériel de réception, d'enregistrement et de reproduction du son et de l'image",
    name = u'poste_coicop_911'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Matériel photographique et cinématographique et appareils optiques",
    name = u'poste_coicop_912'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Matériel de traitement de l'information",
    name = u'poste_coicop_913'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Supports d'enregistrement",
    name = u'poste_coicop_914'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Réparation de matériel audiovisuel, photographique et de traitement de l'information",
    name = u'poste_coicop_915'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Biens durables pour loisirs de plein air",
    name = u'poste_coicop_921'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Instruments de musique et biens durables destinés aux loisirs d'intérieur",
    name = u'poste_coicop_922'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Entretien et réparation des autres biens durables à fonction récréatives et culturelles",
    name = u'poste_coicop_923'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Jeux, jouets et passe-temps",
    name = u'poste_coicop_931'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Articles de sport, matériel de camping et matériel pour activités de plein air",
    name = u'poste_coicop_932'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Produits pour jardin, plantes et fleurs",
    name = u'poste_coicop_933'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Animaux de compagnie et articles connexes",
    name = u'poste_coicop_934'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services vétérinaires et autres services pour animaux de compagnie",
    name = u'poste_coicop_935'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services récréatifs et sportifs",
    name = u'poste_coicop_941'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services culturels",
    name = u'poste_coicop_942'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Jeux de hasard",
    name = u'poste_coicop_943'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Livre",
    name = u'poste_coicop_951'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Journaux et publications périodiques",
    name = u'poste_coicop_952'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Imprimés divers",
    name = u'poste_coicop_953'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Papeterie et matériel de dessin",
    name = u'poste_coicop_954'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Forfaits touristiques ",
    name = u'poste_coicop_960'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Enseignement préélémentaire et primaire",
    name = u'poste_coicop_1010'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Enseignement secondaire",
    name = u'poste_coicop_1020'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Enseignement postsecondaire non supérieur",
    name = u'poste_coicop_1030'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Enseignement supérieur",
    name = u'poste_coicop_1040'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Enseignement non défini par niveau",
    name = u'poste_coicop_1050'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Restauration à emporter",
    name = u'poste_coicop_11112'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Restauration sur place",
    name = u'poste_coicop_11113'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u">>> Consommation de boissons alcoolisées",
    name = u'poste_coicop_11114'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Cantines",
    name = u'poste_coicop_1112'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Services d'hébergement",
    name = u'poste_coicop_1120'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Salons de coiffure et instituts de soins et de beauté",
    name = u'poste_coicop_1211'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Appareils électriques pour soins corporels",
    name = u'poste_coicop_1212'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres appareils, articles et produits pour soins corporels",
    name = u'poste_coicop_1213'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Prostitution",
    name = u'poste_coicop_1220'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Articles de bijouterie et horlogerie",
    name = u'poste_coicop_1231'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres effets personnels",
    name = u'poste_coicop_1232'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Protection sociale",
    name = u'poste_coicop_1240'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Assurance vie",
    name = u'poste_coicop_1251'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Assurance habitation",
    name = u'poste_coicop_1252'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Assurance maladie",
    name = u'poste_coicop_1253'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Assurance transports",
    name = u'poste_coicop_1254'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres assurances",
    name = u'poste_coicop_1255'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Coûts des services d'intermédiation financière indirectement mesurés",
    name = u'poste_coicop_1261'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres services financiers non compris ailleurs",
    name = u'poste_coicop_1262'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Autres services non compris ailleurs",
    name = u'poste_coicop_1270'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"caution pour la location d'un logement",
    name = u'poste_coicop_9901'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"achats de logements, garages, parkings, box et terrains",
    name = u'poste_coicop_9902'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"Gros travaux d'entretien dans les logements",
    name = u'poste_coicop_9903'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"impôts et taxes de la résidence principale",
    name = u'poste_coicop_9911'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"impôts et taxes résidence secondaire ou autre logement",
    name = u'poste_coicop_9912'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"impôts sur le revenu",
    name = u'poste_coicop_9913'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"taxes automobile",
    name = u'poste_coicop_9914'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"autres impôts et taxes",
    name = u'poste_coicop_9915'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"remboursements de prêts résidence principale",
    name = u'poste_coicop_9921'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"remboursements de prêts résidence secondaire ou autre logement",
    name = u'poste_coicop_9922'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"autres remboursements de prêts",
    name = u'poste_coicop_9923'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"argent donné au sein du ménage",
    name = u'poste_coicop_9931'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"aides et cadeaux en argent offerts par le ménage (à des membres de la famille ne",
    name = u'poste_coicop_9932'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"cadeaux offerts (argent ou bien) sai",
    name = u'poste_coicop_9933'
    )

reference_input_variable(
    column = FloatCol(),
    entity_class = Menages,
    label = u"prélèvements de l'employeur",
    name = u'poste_coicop_9941'
    )
