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


from pandas import DataFrame

from openfisca_survey_manager.survey_collections import SurveyCollection

import openfisca_france_indirect_taxation
from openfisca_france_indirect_taxation.surveys import SurveyScenario, get_input_data_frame


def run_survey_simulation(year = None):
    assert year is not None
    input_data_frame = get_input_data_frame(year)
    TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()
    tax_benefit_system = TaxBenefitSystem()
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    simulation = survey_scenario.new_simulation()
    simulation.calculate('tva_taux_plein')

    return simulation, DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in [
                'ident_men',
                'pondmen',
                'decuc',
                'poste_01_1_1_1_1',
                'poste_11_1_1_1_1',
                'depenses_ticpe',
                'depenses_carburants',
                'tva_taux_plein',
                'tva_taux_intermediaire',
                'tva_taux_reduit',
                'tva_taux_super_reduit',
                ]
            ])
        )


def test_survey_simulation():
    for year in [2000, 2005, 2011]:
        yield run_survey_simulation, year


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    for year in [2000, 2005, 2011]:
        df = run_survey_simulation(year)
        print df
        print df.columns
        print df.describe()
