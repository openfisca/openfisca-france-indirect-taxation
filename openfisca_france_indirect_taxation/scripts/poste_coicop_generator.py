
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


@reference_formula
class poste_coicop_111(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Pain et c\xe9r\xe9ales']"

    def function(self, simulation, period):
        poste_coicop_111 = simulation.calculate(111, period)
        return period, poste_coicop_111


@reference_formula
class poste_coicop_112(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Viande']"

    def function(self, simulation, period):
        poste_coicop_112 = simulation.calculate(112, period)
        return period, poste_coicop_112


@reference_formula
class poste_coicop_113(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Poisson et fruits de mer']"

    def function(self, simulation, period):
        poste_coicop_113 = simulation.calculate(113, period)
        return period, poste_coicop_113


@reference_formula
class poste_coicop_114(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Lait, fromage et \u0153ufs']"

    def function(self, simulation, period):
        poste_coicop_114 = simulation.calculate(114, period)
        return period, poste_coicop_114


@reference_formula
class poste_coicop_115(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Huiles et graisses']"

    def function(self, simulation, period):
        poste_coicop_115 = simulation.calculate(115, period)
        return period, poste_coicop_115


@reference_formula
class poste_coicop_1151(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Margarines et autres graisses v\xe9g\xe9tales']"

    def function(self, simulation, period):
        poste_coicop_1151 = simulation.calculate(1151, period)
        return period, poste_coicop_1151


@reference_formula
class poste_coicop_116(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Fruits']"

    def function(self, simulation, period):
        poste_coicop_116 = simulation.calculate(116, period)
        return period, poste_coicop_116


@reference_formula
class poste_coicop_117(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'L\xe9gumes']"

    def function(self, simulation, period):
        poste_coicop_117 = simulation.calculate(117, period)
        return period, poste_coicop_117


@reference_formula
class poste_coicop_118(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Sucre, confiture, miel, chocolat et confiserie']"

    def function(self, simulation, period):
        poste_coicop_118 = simulation.calculate(118, period)
        return period, poste_coicop_118


@reference_formula
class poste_coicop_1181(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Confiserie']"

    def function(self, simulation, period):
        poste_coicop_1181 = simulation.calculate(1181, period)
        return period, poste_coicop_1181


@reference_formula
class poste_coicop_119(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Produits alimentaires non compris ailleurs']"

    def function(self, simulation, period):
        poste_coicop_119 = simulation.calculate(119, period)
        return period, poste_coicop_119


@reference_formula
class poste_coicop_121(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Caf\xe9, th\xe9 et cacao']"

    def function(self, simulation, period):
        poste_coicop_121 = simulation.calculate(121, period)
        return period, poste_coicop_121


@reference_formula
class poste_coicop_122(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'Eaux min\xe9rales, boissons rafra\xeechissantes, jus de fruits et  de l\xe9gumes']"

    def function(self, simulation, period):
        poste_coicop_122 = simulation.calculate(122, period)
        return period, poste_coicop_122


@reference_formula
class poste_coicop_211(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Alcools de bouche ']"

    def function(self, simulation, period):
        poste_coicop_211 = simulation.calculate(211, period)
        return period, poste_coicop_211


@reference_formula
class poste_coicop_212(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Vin et boissons ferment\xe9es']"

    def function(self, simulation, period):
        poste_coicop_212 = simulation.calculate(212, period)
        return period, poste_coicop_212


@reference_formula
class poste_coicop_213(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Bi\xe8re']"

    def function(self, simulation, period):
        poste_coicop_213 = simulation.calculate(213, period)
        return period, poste_coicop_213


@reference_formula
class poste_coicop_2201(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Cigarettes']"

    def function(self, simulation, period):
        poste_coicop_2201 = simulation.calculate(2201, period)
        return period, poste_coicop_2201


@reference_formula
class poste_coicop_2202(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Cigares et cigarillos']"

    def function(self, simulation, period):
        poste_coicop_2202 = simulation.calculate(2202, period)
        return period, poste_coicop_2202


@reference_formula
class poste_coicop_2203(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u">>> Tabac sous d'autres formes"]"

    def function(self, simulation, period):
        poste_coicop_2203 = simulation.calculate(2203, period)
        return period, poste_coicop_2203


@reference_formula
class poste_coicop_230(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Stup\xe9fiants']"

    def function(self, simulation, period):
        poste_coicop_230 = simulation.calculate(230, period)
        return period, poste_coicop_230


@reference_formula
class poste_coicop_311(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Tissus pour habillement']"

    def function(self, simulation, period):
        poste_coicop_311 = simulation.calculate(311, period)
        return period, poste_coicop_311


@reference_formula
class poste_coicop_312(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'V\xeatements']"

    def function(self, simulation, period):
        poste_coicop_312 = simulation.calculate(312, period)
        return period, poste_coicop_312


@reference_formula
class poste_coicop_313(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Autres articles et accessoires d'habillement"]"

    def function(self, simulation, period):
        poste_coicop_313 = simulation.calculate(313, period)
        return period, poste_coicop_313


@reference_formula
class poste_coicop_314(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Nettoyage, r\xe9paration et location d'articles d'habillement"]"

    def function(self, simulation, period):
        poste_coicop_314 = simulation.calculate(314, period)
        return period, poste_coicop_314


@reference_formula
class poste_coicop_321(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Chaussures diverses']"

    def function(self, simulation, period):
        poste_coicop_321 = simulation.calculate(321, period)
        return period, poste_coicop_321


@reference_formula
class poste_coicop_322(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Cordonnerie et location de chaussures']"

    def function(self, simulation, period):
        poste_coicop_322 = simulation.calculate(322, period)
        return period, poste_coicop_322


@reference_formula
class poste_coicop_411(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Loyers effectivement pay\xe9s par les locataires']"

    def function(self, simulation, period):
        poste_coicop_411 = simulation.calculate(411, period)
        return period, poste_coicop_411


@reference_formula
class poste_coicop_412(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres loyers effectifs']"

    def function(self, simulation, period):
        poste_coicop_412 = simulation.calculate(412, period)
        return period, poste_coicop_412


@reference_formula
class poste_coicop_421(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Loyers fictifs des propri\xe9taires occupants']"

    def function(self, simulation, period):
        poste_coicop_421 = simulation.calculate(421, period)
        return period, poste_coicop_421


@reference_formula
class poste_coicop_422(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres loyers fictifs']"

    def function(self, simulation, period):
        poste_coicop_422 = simulation.calculate(422, period)
        return period, poste_coicop_422


@reference_formula
class poste_coicop_431(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Fournitures pour travaux d'entretien et de r\xe9paration des logements"]"

    def function(self, simulation, period):
        poste_coicop_431 = simulation.calculate(431, period)
        return period, poste_coicop_431


@reference_formula
class poste_coicop_432(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Services concernant l'entretien et les r\xe9parations du logement"]"

    def function(self, simulation, period):
        poste_coicop_432 = simulation.calculate(432, period)
        return period, poste_coicop_432


@reference_formula
class poste_coicop_441(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Alimentation en eau']"

    def function(self, simulation, period):
        poste_coicop_441 = simulation.calculate(441, period)
        return period, poste_coicop_441


@reference_formula
class poste_coicop_442(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Collecte des ordures m\xe9nag\xe8res']"

    def function(self, simulation, period):
        poste_coicop_442 = simulation.calculate(442, period)
        return period, poste_coicop_442


@reference_formula
class poste_coicop_443(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Reprise des eaux us\xe9es']"

    def function(self, simulation, period):
        poste_coicop_443 = simulation.calculate(443, period)
        return period, poste_coicop_443


@reference_formula
class poste_coicop_444(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Service divers li\xe9s au logement non compris ailleurs']"

    def function(self, simulation, period):
        poste_coicop_444 = simulation.calculate(444, period)
        return period, poste_coicop_444


@reference_formula
class poste_coicop_451(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Electricit\xe9']"

    def function(self, simulation, period):
        poste_coicop_451 = simulation.calculate(451, period)
        return period, poste_coicop_451


@reference_formula
class poste_coicop_4511(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Facture EDF GDF non dissociables']"

    def function(self, simulation, period):
        poste_coicop_4511 = simulation.calculate(4511, period)
        return period, poste_coicop_4511


@reference_formula
class poste_coicop_452(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Gaz']"

    def function(self, simulation, period):
        poste_coicop_452 = simulation.calculate(452, period)
        return period, poste_coicop_452


@reference_formula
class poste_coicop_4522(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Achat de butane, propane']"

    def function(self, simulation, period):
        poste_coicop_4522 = simulation.calculate(4522, period)
        return period, poste_coicop_4522


@reference_formula
class poste_coicop_453(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Combustibles liquides']"

    def function(self, simulation, period):
        poste_coicop_453 = simulation.calculate(453, period)
        return period, poste_coicop_453


@reference_formula
class poste_coicop_454(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Combustibles solides']"

    def function(self, simulation, period):
        poste_coicop_454 = simulation.calculate(454, period)
        return period, poste_coicop_454


@reference_formula
class poste_coicop_455(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Energie thermique']"

    def function(self, simulation, period):
        poste_coicop_455 = simulation.calculate(455, period)
        return period, poste_coicop_455


@reference_formula
class poste_coicop_511(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Meubles et articles d'ameublement"]"

    def function(self, simulation, period):
        poste_coicop_511 = simulation.calculate(511, period)
        return period, poste_coicop_511


@reference_formula
class poste_coicop_512(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Tapis et rev\xeatements de sols divers']"

    def function(self, simulation, period):
        poste_coicop_512 = simulation.calculate(512, period)
        return period, poste_coicop_512


@reference_formula
class poste_coicop_513(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u"R\xe9paration de meubles, d'articles d'ameublement et de rev\xeatements souples pour le sol"]"

    def function(self, simulation, period):
        poste_coicop_513 = simulation.calculate(513, period)
        return period, poste_coicop_513


@reference_formula
class poste_coicop_520(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Article de m\xe9nage en textiles']"

    def function(self, simulation, period):
        poste_coicop_520 = simulation.calculate(520, period)
        return period, poste_coicop_520


@reference_formula
class poste_coicop_531(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Gros appareils m\xe9nagers, \xe9lectriques ou non']"

    def function(self, simulation, period):
        poste_coicop_531 = simulation.calculate(531, period)
        return period, poste_coicop_531


@reference_formula
class poste_coicop_532(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Petits appareils \xe9lectrom\xe9angers']"

    def function(self, simulation, period):
        poste_coicop_532 = simulation.calculate(532, period)
        return period, poste_coicop_532


@reference_formula
class poste_coicop_533(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"R\xe9paration d'appareils m\xe9nagers"]"

    def function(self, simulation, period):
        poste_coicop_533 = simulation.calculate(533, period)
        return period, poste_coicop_533


@reference_formula
class poste_coicop_540(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Verrerie, vaisselle et ustensiles de m\xe9nage']"

    def function(self, simulation, period):
        poste_coicop_540 = simulation.calculate(540, period)
        return period, poste_coicop_540


@reference_formula
class poste_coicop_551(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Gros outillage et mat\xe9riel']"

    def function(self, simulation, period):
        poste_coicop_551 = simulation.calculate(551, period)
        return period, poste_coicop_551


@reference_formula
class poste_coicop_552(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Petit outillage et accessoires divers']"

    def function(self, simulation, period):
        poste_coicop_552 = simulation.calculate(552, period)
        return period, poste_coicop_552


@reference_formula
class poste_coicop_561(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Biens d'\xe9quipement m\xe9nager non durables"]"

    def function(self, simulation, period):
        poste_coicop_561 = simulation.calculate(561, period)
        return period, poste_coicop_561


@reference_formula
class poste_coicop_562(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services domestiques et services m\xe9nagers']"

    def function(self, simulation, period):
        poste_coicop_562 = simulation.calculate(562, period)
        return period, poste_coicop_562


@reference_formula
class poste_coicop_611(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Produits pharmaceutiques']"

    def function(self, simulation, period):
        poste_coicop_611 = simulation.calculate(611, period)
        return period, poste_coicop_611


@reference_formula
class poste_coicop_612(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Produits m\xe9dicaux divers']"

    def function(self, simulation, period):
        poste_coicop_612 = simulation.calculate(612, period)
        return period, poste_coicop_612


@reference_formula
class poste_coicop_613(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Appareils et mat\xe9riel th\xe9rapeutiques']"

    def function(self, simulation, period):
        poste_coicop_613 = simulation.calculate(613, period)
        return period, poste_coicop_613


@reference_formula
class poste_coicop_621(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services m\xe9dicaux']"

    def function(self, simulation, period):
        poste_coicop_621 = simulation.calculate(621, period)
        return period, poste_coicop_621


@reference_formula
class poste_coicop_622(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services dentaires']"

    def function(self, simulation, period):
        poste_coicop_622 = simulation.calculate(622, period)
        return period, poste_coicop_622


@reference_formula
class poste_coicop_623(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services param\xe9dicaux']"

    def function(self, simulation, period):
        poste_coicop_623 = simulation.calculate(623, period)
        return period, poste_coicop_623


@reference_formula
class poste_coicop_630(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services hospitaliers']"

    def function(self, simulation, period):
        poste_coicop_630 = simulation.calculate(630, period)
        return period, poste_coicop_630


@reference_formula
class poste_coicop_711(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Voitures automobiles']"

    def function(self, simulation, period):
        poste_coicop_711 = simulation.calculate(711, period)
        return period, poste_coicop_711


@reference_formula
class poste_coicop_712(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Motocycles']"

    def function(self, simulation, period):
        poste_coicop_712 = simulation.calculate(712, period)
        return period, poste_coicop_712


@reference_formula
class poste_coicop_713(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Bicyclettes']"

    def function(self, simulation, period):
        poste_coicop_713 = simulation.calculate(713, period)
        return period, poste_coicop_713


@reference_formula
class poste_coicop_721(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Pi\xe8ces de rechange et accessoires pour v\xe9hicules de tourisme ']"

    def function(self, simulation, period):
        poste_coicop_721 = simulation.calculate(721, period)
        return period, poste_coicop_721


@reference_formula
class poste_coicop_722(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Carburants et lubrifiants pour v\xe9hicules de tourisme']"

    def function(self, simulation, period):
        poste_coicop_722 = simulation.calculate(722, period)
        return period, poste_coicop_722


@reference_formula
class poste_coicop_723(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Entretien et r\xe9paration de v\xe9hicules particuliers']"

    def function(self, simulation, period):
        poste_coicop_723 = simulation.calculate(723, period)
        return period, poste_coicop_723


@reference_formula
class poste_coicop_724(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services divers li\xe9s aux v\xe9hicules particuliers']"

    def function(self, simulation, period):
        poste_coicop_724 = simulation.calculate(724, period)
        return period, poste_coicop_724


@reference_formula
class poste_coicop_731(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Transport ferroviaire de passagers']"

    def function(self, simulation, period):
        poste_coicop_731 = simulation.calculate(731, period)
        return period, poste_coicop_731


@reference_formula
class poste_coicop_732(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Transport routier de passagers']"

    def function(self, simulation, period):
        poste_coicop_732 = simulation.calculate(732, period)
        return period, poste_coicop_732


@reference_formula
class poste_coicop_733(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Transport a\xe9rien de passagers']"

    def function(self, simulation, period):
        poste_coicop_733 = simulation.calculate(733, period)
        return period, poste_coicop_733


@reference_formula
class poste_coicop_734(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Transport maritime et fluvial de passagers']"

    def function(self, simulation, period):
        poste_coicop_734 = simulation.calculate(734, period)
        return period, poste_coicop_734


@reference_formula
class poste_coicop_735(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Transport combin\xe9 de passagers']"

    def function(self, simulation, period):
        poste_coicop_735 = simulation.calculate(735, period)
        return period, poste_coicop_735


@reference_formula
class poste_coicop_736(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services de transport divers']"

    def function(self, simulation, period):
        poste_coicop_736 = simulation.calculate(736, period)
        return period, poste_coicop_736


@reference_formula
class poste_coicop_810(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services postaux']"

    def function(self, simulation, period):
        poste_coicop_810 = simulation.calculate(810, period)
        return period, poste_coicop_810


@reference_formula
class poste_coicop_831(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Mat\xe9riel de t\xe9l\xe9phonie et de t\xe9l\xe9copie']"

    def function(self, simulation, period):
        poste_coicop_831 = simulation.calculate(831, period)
        return period, poste_coicop_831


@reference_formula
class poste_coicop_832(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services de t\xe9l\xe9phonie et de t\xe9l\xe9copie']"

    def function(self, simulation, period):
        poste_coicop_832 = simulation.calculate(832, period)
        return period, poste_coicop_832


@reference_formula
class poste_coicop_911(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u"Mat\xe9riel de r\xe9ception, d'enregistrement et de reproduction du son et de l'image"]"

    def function(self, simulation, period):
        poste_coicop_911 = simulation.calculate(911, period)
        return period, poste_coicop_911


@reference_formula
class poste_coicop_912(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'Mat\xe9riel photographique et cin\xe9matographique et appareils optiques']"

    def function(self, simulation, period):
        poste_coicop_912 = simulation.calculate(912, period)
        return period, poste_coicop_912


@reference_formula
class poste_coicop_913(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Mat\xe9riel de traitement de l'information"]"

    def function(self, simulation, period):
        poste_coicop_913 = simulation.calculate(913, period)
        return period, poste_coicop_913


@reference_formula
class poste_coicop_914(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Supports d'enregistrement"]"

    def function(self, simulation, period):
        poste_coicop_914 = simulation.calculate(914, period)
        return period, poste_coicop_914


@reference_formula
class poste_coicop_915(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u"R\xe9paration de mat\xe9riel audiovisuel, photographique et de traitement de l'information"]"

    def function(self, simulation, period):
        poste_coicop_915 = simulation.calculate(915, period)
        return period, poste_coicop_915


@reference_formula
class poste_coicop_921(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Biens durables pour loisirs de plein air']"

    def function(self, simulation, period):
        poste_coicop_921 = simulation.calculate(921, period)
        return period, poste_coicop_921


@reference_formula
class poste_coicop_922(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u"Instruments de musique et biens durables destin\xe9s aux loisirs d'int\xe9rieur"]"

    def function(self, simulation, period):
        poste_coicop_922 = simulation.calculate(922, period)
        return period, poste_coicop_922


@reference_formula
class poste_coicop_923(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'Entretien et r\xe9paration des autres biens durables \xe0 fonction r\xe9cr\xe9atives et culturelles']"

    def function(self, simulation, period):
        poste_coicop_923 = simulation.calculate(923, period)
        return period, poste_coicop_923


@reference_formula
class poste_coicop_931(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Jeux, jouets et passe-temps']"

    def function(self, simulation, period):
        poste_coicop_931 = simulation.calculate(931, period)
        return period, poste_coicop_931


@reference_formula
class poste_coicop_932(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'Articles de sport, mat\xe9riel de camping et mat\xe9riel pour activit\xe9s de plein air']"

    def function(self, simulation, period):
        poste_coicop_932 = simulation.calculate(932, period)
        return period, poste_coicop_932


@reference_formula
class poste_coicop_933(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Produits pour jardin, plantes et fleurs']"

    def function(self, simulation, period):
        poste_coicop_933 = simulation.calculate(933, period)
        return period, poste_coicop_933


@reference_formula
class poste_coicop_934(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Animaux de compagnie et articles connexes']"

    def function(self, simulation, period):
        poste_coicop_934 = simulation.calculate(934, period)
        return period, poste_coicop_934


@reference_formula
class poste_coicop_935(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'Services v\xe9t\xe9rinaires et autres services pour animaux de compagnie']"

    def function(self, simulation, period):
        poste_coicop_935 = simulation.calculate(935, period)
        return period, poste_coicop_935


@reference_formula
class poste_coicop_941(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services r\xe9cr\xe9atifs et sportifs']"

    def function(self, simulation, period):
        poste_coicop_941 = simulation.calculate(941, period)
        return period, poste_coicop_941


@reference_formula
class poste_coicop_942(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Services culturels']"

    def function(self, simulation, period):
        poste_coicop_942 = simulation.calculate(942, period)
        return period, poste_coicop_942


@reference_formula
class poste_coicop_943(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Jeux de hasard']"

    def function(self, simulation, period):
        poste_coicop_943 = simulation.calculate(943, period)
        return period, poste_coicop_943


@reference_formula
class poste_coicop_951(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Livre']"

    def function(self, simulation, period):
        poste_coicop_951 = simulation.calculate(951, period)
        return period, poste_coicop_951


@reference_formula
class poste_coicop_952(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Journaux et publications p\xe9riodiques']"

    def function(self, simulation, period):
        poste_coicop_952 = simulation.calculate(952, period)
        return period, poste_coicop_952


@reference_formula
class poste_coicop_953(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Imprim\xe9s divers']"

    def function(self, simulation, period):
        poste_coicop_953 = simulation.calculate(953, period)
        return period, poste_coicop_953


@reference_formula
class poste_coicop_954(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Papeterie et mat\xe9riel de dessin']"

    def function(self, simulation, period):
        poste_coicop_954 = simulation.calculate(954, period)
        return period, poste_coicop_954


@reference_formula
class poste_coicop_960(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Forfaits touristiques ']"

    def function(self, simulation, period):
        poste_coicop_960 = simulation.calculate(960, period)
        return period, poste_coicop_960


@reference_formula
class poste_coicop_1010(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Enseignement pr\xe9\xe9l\xe9mentaire et primaire']"

    def function(self, simulation, period):
        poste_coicop_1010 = simulation.calculate(1010, period)
        return period, poste_coicop_1010


@reference_formula
class poste_coicop_1020(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Enseignement secondaire']"

    def function(self, simulation, period):
        poste_coicop_1020 = simulation.calculate(1020, period)
        return period, poste_coicop_1020


@reference_formula
class poste_coicop_1030(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Enseignement postsecondaire non sup\xe9rieur']"

    def function(self, simulation, period):
        poste_coicop_1030 = simulation.calculate(1030, period)
        return period, poste_coicop_1030


@reference_formula
class poste_coicop_1040(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Enseignement sup\xe9rieur']"

    def function(self, simulation, period):
        poste_coicop_1040 = simulation.calculate(1040, period)
        return period, poste_coicop_1040


@reference_formula
class poste_coicop_1050(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Enseignement non d\xe9fini par niveau']"

    def function(self, simulation, period):
        poste_coicop_1050 = simulation.calculate(1050, period)
        return period, poste_coicop_1050


@reference_formula
class poste_coicop_11112(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Restauration \xe0 emporter']"

    def function(self, simulation, period):
        poste_coicop_11112 = simulation.calculate(11112, period)
        return period, poste_coicop_11112


@reference_formula
class poste_coicop_11113(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Restauration sur place']"

    def function(self, simulation, period):
        poste_coicop_11113 = simulation.calculate(11113, period)
        return period, poste_coicop_11113


@reference_formula
class poste_coicop_11114(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'>>> Consommation de boissons alcoolis\xe9es']"

    def function(self, simulation, period):
        poste_coicop_11114 = simulation.calculate(11114, period)
        return period, poste_coicop_11114


@reference_formula
class poste_coicop_1112(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Cantines']"

    def function(self, simulation, period):
        poste_coicop_1112 = simulation.calculate(1112, period)
        return period, poste_coicop_1112


@reference_formula
class poste_coicop_1120(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Services d'h\xe9bergement"]"

    def function(self, simulation, period):
        poste_coicop_1120 = simulation.calculate(1120, period)
        return period, poste_coicop_1120


@reference_formula
class poste_coicop_1211(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Salons de coiffure et instituts de soins et de beaut\xe9']"

    def function(self, simulation, period):
        poste_coicop_1211 = simulation.calculate(1211, period)
        return period, poste_coicop_1211


@reference_formula
class poste_coicop_1212(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Appareils \xe9lectriques pour soins corporels']"

    def function(self, simulation, period):
        poste_coicop_1212 = simulation.calculate(1212, period)
        return period, poste_coicop_1212


@reference_formula
class poste_coicop_1213(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres appareils, articles et produits pour soins corporels']"

    def function(self, simulation, period):
        poste_coicop_1213 = simulation.calculate(1213, period)
        return period, poste_coicop_1213


@reference_formula
class poste_coicop_1220(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Prostitution']"

    def function(self, simulation, period):
        poste_coicop_1220 = simulation.calculate(1220, period)
        return period, poste_coicop_1220


@reference_formula
class poste_coicop_1231(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Articles de bijouterie et horlogerie']"

    def function(self, simulation, period):
        poste_coicop_1231 = simulation.calculate(1231, period)
        return period, poste_coicop_1231


@reference_formula
class poste_coicop_1232(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres effets personnels']"

    def function(self, simulation, period):
        poste_coicop_1232 = simulation.calculate(1232, period)
        return period, poste_coicop_1232


@reference_formula
class poste_coicop_1240(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Protection sociale']"

    def function(self, simulation, period):
        poste_coicop_1240 = simulation.calculate(1240, period)
        return period, poste_coicop_1240


@reference_formula
class poste_coicop_1251(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Assurance vie']"

    def function(self, simulation, period):
        poste_coicop_1251 = simulation.calculate(1251, period)
        return period, poste_coicop_1251


@reference_formula
class poste_coicop_1252(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Assurance habitation']"

    def function(self, simulation, period):
        poste_coicop_1252 = simulation.calculate(1252, period)
        return period, poste_coicop_1252


@reference_formula
class poste_coicop_1253(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Assurance maladie']"

    def function(self, simulation, period):
        poste_coicop_1253 = simulation.calculate(1253, period)
        return period, poste_coicop_1253


@reference_formula
class poste_coicop_1254(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Assurance transports']"

    def function(self, simulation, period):
        poste_coicop_1254 = simulation.calculate(1254, period)
        return period, poste_coicop_1254


@reference_formula
class poste_coicop_1255(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres assurances']"

    def function(self, simulation, period):
        poste_coicop_1255 = simulation.calculate(1255, period)
        return period, poste_coicop_1255


@reference_formula
class poste_coicop_1261(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u"Co\xfbts des services d'interm\xe9diation financi\xe8re indirectement mesur\xe9s"]"

    def function(self, simulation, period):
        poste_coicop_1261 = simulation.calculate(1261, period)
        return period, poste_coicop_1261


@reference_formula
class poste_coicop_1262(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres services financiers non compris ailleurs']"

    def function(self, simulation, period):
        poste_coicop_1262 = simulation.calculate(1262, period)
        return period, poste_coicop_1262


@reference_formula
class poste_coicop_1270(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'Autres services non compris ailleurs']"

    def function(self, simulation, period):
        poste_coicop_1270 = simulation.calculate(1270, period)
        return period, poste_coicop_1270


@reference_formula
class poste_coicop_9901(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"caution pour la location d'un logement"]"

    def function(self, simulation, period):
        poste_coicop_9901 = simulation.calculate(9901, period)
        return period, poste_coicop_9901


@reference_formula
class poste_coicop_9902(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'achats de logements, garages, parkings, box et terrains']"

    def function(self, simulation, period):
        poste_coicop_9902 = simulation.calculate(9902, period)
        return period, poste_coicop_9902


@reference_formula
class poste_coicop_9903(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"Gros travaux d'entretien dans les logements"]"

    def function(self, simulation, period):
        poste_coicop_9903 = simulation.calculate(9903, period)
        return period, poste_coicop_9903


@reference_formula
class poste_coicop_9911(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'imp\xf4ts et taxes de la r\xe9sidence principale']"

    def function(self, simulation, period):
        poste_coicop_9911 = simulation.calculate(9911, period)
        return period, poste_coicop_9911


@reference_formula
class poste_coicop_9912(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'imp\xf4ts et taxes r\xe9sidence secondaire ou autre logement']"

    def function(self, simulation, period):
        poste_coicop_9912 = simulation.calculate(9912, period)
        return period, poste_coicop_9912


@reference_formula
class poste_coicop_9913(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'imp\xf4ts sur le revenu']"

    def function(self, simulation, period):
        poste_coicop_9913 = simulation.calculate(9913, period)
        return period, poste_coicop_9913


@reference_formula
class poste_coicop_9914(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'taxes automobile']"

    def function(self, simulation, period):
        poste_coicop_9914 = simulation.calculate(9914, period)
        return period, poste_coicop_9914


@reference_formula
class poste_coicop_9915(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'autres imp\xf4ts et taxes']"

    def function(self, simulation, period):
        poste_coicop_9915 = simulation.calculate(9915, period)
        return period, poste_coicop_9915


@reference_formula
class poste_coicop_9921(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'remboursements de pr\xeats r\xe9sidence principale']"

    def function(self, simulation, period):
        poste_coicop_9921 = simulation.calculate(9921, period)
        return period, poste_coicop_9921


@reference_formula
class poste_coicop_9922(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'remboursements de pr\xeats r\xe9sidence secondaire ou autre logement']"

    def function(self, simulation, period):
        poste_coicop_9922 = simulation.calculate(9922, period)
        return period, poste_coicop_9922


@reference_formula
class poste_coicop_9923(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'autres remboursements de pr\xeats']"

    def function(self, simulation, period):
        poste_coicop_9923 = simulation.calculate(9923, period)
        return period, poste_coicop_9923


@reference_formula
class poste_coicop_9931(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'argent donn\xe9 au sein du m\xe9nage']"

    def function(self, simulation, period):
        poste_coicop_9931 = simulation.calculate(9931, period)
        return period, poste_coicop_9931


@reference_formula
class poste_coicop_9932(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[ u'aides et cadeaux en argent offerts par le m\xe9nage (\xe0 des membres de la famille ne']"

    def function(self, simulation, period):
        poste_coicop_9932 = simulation.calculate(9932, period)
        return period, poste_coicop_9932


@reference_formula
class poste_coicop_9933(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u'cadeaux offerts (argent ou bien) sai']"

    def function(self, simulation, period):
        poste_coicop_9933 = simulation.calculate(9933, period)
        return period, poste_coicop_9933


@reference_formula
class poste_coicop_9941(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"[u"pr\xe9l\xe8vements de l'employeur"]"

    def function(self, simulation, period):
        poste_coicop_9941 = simulation.calculate(9941, period)
        return period, poste_coicop_9941

