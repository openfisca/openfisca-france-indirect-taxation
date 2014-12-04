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


from openfisca_core.columns import AgeCol, FloatCol
from openfisca_core.formulas import SimpleFormulaColumn
from ..entities import Individus
from openfisca_france_indirect_taxation import reference_formula

from openfisca_france_indirect_taxation.model.tva import montant_tva
from openfisca_france_indirect_taxation.param.param import P_tva_taux_plein
from openfisca_france_indirect_taxation.param.param import P_tva_taux_intermediaire
from openfisca_france_indirect_taxation.param.param import P_tva_taux_reduit
from openfisca_france_indirect_taxation.param.param import P_tva_taux_super_reduit


@reference_formula
class age(SimpleFormulaColumn):
    column = AgeCol
    entity_class = Individus
    label = u"Age de l'individu"

    def function(self, birth, period):
        return (np.datetime64(period.date) - birth).astype('timedelta64[Y]')

    def get_output_period(self, period):
        return period.start.period(u'year').offset('first-of')


@reference_formula
class montant_tva_taux_plein(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Montant de la TVA acquitée à taux plein"

    def function(self, consommation_tva_taux_plein):
        return montant_tva(P_tva_taux_plein, consommation_tva_taux_plein)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_tva_taux_intermediaire(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Montant de la TVA acquitée à taux intermediaire"

    def function(self, consommation_tva_taux_intermediaire):
        return montant_tva(P_tva_taux_intermediaire, consommation_tva_taux_intermediaire)

    def get_output_period(self, period):
        return period

@reference_formula
class montant_tva_taux_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Montant de la TVA acquitée à taux reduit"

    def function(self, consommation_tva_taux_reduit):
        return montant_tva(P_tva_taux_reduit, consommation_tva_taux_reduit)

    def get_output_period(self, period):
        return period


@reference_formula
class montant_tva_taux_super_reduit(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Montant de la TVA acquitée à taux super reduit"

    def function(self, consommation_tva_taux_super_reduit):
        return montant_tva(P_tva_taux_super_reduit, consommation_tva_taux_super_reduit)

    def get_output_period(self, period):
        return period