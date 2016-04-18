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


from .caracteristiques_menages import (  # noqa analysis:ignore
    autres_caracteristiques,
    demographie,
    )
from .consommation import (  # noqa analysis:ignore
    categories_fiscales,
    consommation_menages,
    depenses_energies,
    emissions_co2,
    postes_coicop,
    quantites_energie,
    )
from reactions_comportementales_reforme import (  # noqa analysis:ignore
    contributions_ajustees_taxe_carbone,
    contributions_ajustees_taxes_carburants,
    contributions_ajustees_cce_2014_2015,
    contributions_ajustees_cce_2014_2016,
    depenses_energies_ajustees,
    depenses_tva_ajustees,
    elasticites,
    emissions_ajustees,
    quantites_ajustees,
    )
from .revenus import (  # noqa analysis:ignore
    revenus_menages,
    )
from .taxes_indirectes import (  # noqa analysis:ignore
    alcools,
    assurances,
    tabacs,
    ticpe,
    totaux,
    tva,
    )
from .vehicules import (  # noqa analysis:ignore
    vehicules_menages,
    )
