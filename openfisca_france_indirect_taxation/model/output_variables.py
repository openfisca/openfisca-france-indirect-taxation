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

    def function(self, birth, period):
        return (np.datetime64(period.date) - birth).astype('timedelta64[Y]')

    def get_output_period(self, period):
        return period


@reference_formula
class consommation_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux intermédiaire"

    def function(self, categorie_fiscale_4):
        return categorie_fiscale_4

    def get_output_period(self, period):
        return period


@reference_formula
class consommation_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux plein"

    def function(self, categorie_fiscale_3, categorie_fiscale_11):
        return categorie_fiscale_3 + categorie_fiscale_11

    def get_output_period(self, period):
        return period


@reference_formula
class consommation_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux réduit"

    def function(self, categorie_fiscale_1):
        return categorie_fiscale_1

    def get_output_period(self, period):
        return period


@reference_formula
class consommation_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Consommation soumis à une TVA à taux super réduit"

    def function(self, categorie_fiscale_2):
        return categorie_fiscale_2

    def get_output_period(self, period):
        return period

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

    def function(self, consommation_tva_taux_plein, taux = law.imposition_indirecte.tva.taux_plein):
        return tax_from_expense_including_tax(consommation_tva_taux_plein, taux)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux intermediaire"

    def function(self, consommation_tva_taux_intermediaire, taux = law.imposition_indirecte.tva.taux_intermediaire):
        return tax_from_expense_including_tax(consommation_tva_taux_intermediaire, taux)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, consommation_tva_taux_reduit, taux = law.imposition_indirecte.tva.taux_reduit):
        return tax_from_expense_including_tax(consommation_tva_taux_reduit, taux)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, consommation_tva_taux_super_reduit, taux = law.imposition_indirecte.tva.taux_super_reduit):
        return tax_from_expense_including_tax(consommation_tva_taux_super_reduit, taux)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_droit_d_accise_alcool_0211(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0211"

    def function(self, consommation_alcool_0211):
        return montant_droit_d_accise_alcool(P_alcool_0211, consommation_alcool_0211)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_droit_d_accise_alcool_0212(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0212"

    def function(self, consommation_alcool_0212):
        return montant_droit_d_accise_alcool(P_alcool_0212, consommation_alcool_0212)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_droit_d_accise_alcool_0213(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Menages
    label = u"Montant des droits d'accises sur les alcools poste 0213"

    def function(self, consommation_alcool_0213):
        return montant_droit_d_accise_alcool(P_alcool_0213, consommation_alcool_0213)

    def get_output_period(self, period):
        return period
