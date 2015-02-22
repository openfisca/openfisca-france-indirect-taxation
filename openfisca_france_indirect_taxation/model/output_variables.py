# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014 OpenFisca Team
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


import numpy as np


from openfisca_core.accessors import law
from openfisca_core.columns import AgeCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn
from ..entities import Individus, Menages
from .. import reference_formula

from openfisca_france_indirect_taxation.model.tva import tax_from_expense_including_tax
from openfisca_france_indirect_taxation.model.droit_d_accise_alcool import montant_droit_d_accise_alcool
from openfisca_france_indirect_taxation.param.param import (
    # P_tva_taux_plein, P_tva_taux_intermediaire, P_tva_taux_reduit,
    # P_tva_taux_super_reduit,
    P_alcool_0211, P_alcool_0212, P_alcool_0213
    )


@reference_formula
class age(SimpleFormulaColumn):
    column = AgeCol
    entity_class = Individus
    label = u"Age de l'individu"

    def function(self, simulation, period):
        birth = simulation.calculate('birth', period)
        return period, (np.datetime64(period.date) - birth).astype('timedelta64[Y]')


@reference_formula
class consommation_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux intermédiaire"

    def function(self, simulation, period):
        categorie_fiscale_4 = simulation.calculate('categorie_fiscale_4', period)
        return period, categorie_fiscale_4



@reference_formula
class consommation_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux plein"

    def function(self, simulation, period):
        categorie_fiscale_3 = simulation.calculate('categorie_fiscale_3', period)
        categorie_fiscale_11 = simulation.calculate('categorie_fiscale_11', period)
        return period, categorie_fiscale_3 + categorie_fiscale_11


@reference_formula
class consommation_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux réduit"

    def function(self, simulation, period):
        categorie_fiscale_2 = simulation.calculate('categorie_fiscale_2', period)
        return period, categorie_fiscale_2


@reference_formula
class consommation_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux super réduit"

    def function(self, simulation, period):
        categorie_fiscale_1 = simulation.calculate('categorie_fiscale_1', period)
        return period, categorie_fiscale_1


#reference_input_variable(
#    column = FloatCol,
#    entity_class = Individus,
#    label = u"Consommation droit d'accise alcool 0211",
#    name = 'consommation_alcool_0211',
#    )
#
#reference_input_variable(
#    column = FloatCol,
#    entity_class = Individus,
#    label = u"Consommation droit d'accise alcool 0212",
#    name = 'consommation_alcool_0212',
#    )
#
#reference_input_variable(
#    column = FloatCol,
#    entity_class = Individus,
#    label = u"Consommation droit d'accise alcool 0213",
#    name = 'consommation_alcool_0213',
#    )

@reference_formula
class montant_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux plein"

    def function(self, simulation, period):
        consommation_tva_taux_plein = simulation.calculate('consommation_tva_taux_plein', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        return period, tax_from_expense_including_tax(consommation_tva_taux_plein, taux)


@reference_formula
class montant_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    def function(self, simulation, period):
        consommation_tva_taux_intermediaire = simulation.calculate('consommation_tva_taux_intermediaire')
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_intermediaire
        return period, tax_from_expense_including_tax(consommation_tva_taux_intermediaire, taux)


@reference_formula
class montant_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, simulation, period):
        consommation_tva_taux_reduit = simulation.calculate('consommation_tva_taux_reduit', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_reduit, taux)


@reference_formula
class montant_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, simulation, period):
        consommation_tva_taux_super_reduit = simulation.calculate('consommation_tva_taux_super_reduit', period)
        taux = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        return period, tax_from_expense_including_tax(consommation_tva_taux_super_reduit, taux)


@reference_formula
class montant_tva_total(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée"

    def function(self, simulation, period):
        montant_tva_taux_super_reduit = simulation.calculate('montant_tva_taux_super_reduit', period)
        montant_tva_taux_reduit = simulation.calculate('montant_tva_taux_reduit', period)
        montant_tva_taux_intermediaire = simulation.calculate('montant_tva_taux_intermediaire', period)
        montant_tva_taux_plein = simulation.calculate('montant_tva_taux_plein', period)
        return period, montant_tva_taux_super_reduit+ montant_tva_taux_reduit+ montant_tva_taux_intermediaire+montant_tva_taux_plein


@reference_formula
class montant_droit_d_accise_alcool_0211(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0211"

    def function(self, simulation, period):
        consommation_alcool_0211 = simulation.calculate('consommation_alcool_0211', period)
        return period, montant_droit_d_accise_alcool(P_alcool_0211, consommation_alcool_0211)


@reference_formula
class montant_droit_d_accise_alcool_0212(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0212"

    def function(self, simulation, period):
        consommation_alcool_0212 = simulation.calculate('consommation_alcool_0212', period)
        return period, montant_droit_d_accise_alcool(P_alcool_0212, consommation_alcool_0212)


@reference_formula
class montant_droit_d_accise_alcool_0213(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0213"

    def function(self, simulation, period):
        consommation_alcool_0213 = simulation.calculate('consommation_alcool_0213', period)
        return period, montant_droit_d_accise_alcool(P_alcool_0213, consommation_alcool_0213)


@reference_formula
class niveau_de_vie(SimpleFormulaColumn): 
    column = FloatCol
    entity_class = Menages
    label = u"Revenus disponibles divisés par ocde10 soit le nombre d'unités de consommation du ménage"
    
    def function(self, simulation, period):
        rev_disponible = simulation.calculate('rev_disponible',period)
        ocde10 = simulation.calculate('ocde10',period)
        return period, rev_disponible/ocde10
        

        