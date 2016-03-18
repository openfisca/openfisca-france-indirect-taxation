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

import openfisca_france_indirect_taxation
from openfisca_survey_manager import default_config_files_directory as config_files_directory
from openfisca_survey_manager.survey_collections import SurveyCollection


from openfisca_france_indirect_taxation.surveys import SurveyScenario


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(
        collection = "openfisca_indirect_taxation", config_files_directory = config_files_directory)
    openfisca_survey = openfisca_survey_collection.get_survey("openfisca_indirect_taxation_data_{}".format(year))
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def test_survey_simulation(year = None):
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

    return DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in [
                'tva_taux_plein',
                'tva_taux_intermediaire',
                'tva_taux_reduit',
                'tva_taux_super_reduit',
                'ident_men',
                'pondmen',
                'decuc',
                'poste_coicop_01_1_1_1_1',
                'depenses_carburants',
                ]
            ])
        )


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    for year in [2011]:
        df = test_survey_simulation(year)
        print df
        print df.columns
        print df.poste_coicop_01_1_1_1_1.describe()
