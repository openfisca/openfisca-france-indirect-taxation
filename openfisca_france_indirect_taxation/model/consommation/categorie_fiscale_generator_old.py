
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

from datetime import date

from ..base import *


'categorie_fiscale: 0'


class categorie_fiscale_0(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 0"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1112', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_0 = 0
        for each_variable in ['230', '411', '412', '421', '422', '621', '622', '623', '630', '810', '943', '1010', '1020', '1030', '1040', '1050', '1220', '1261', '9901', '9902', '9911', '9912', '9913', '9914', '9915', '9921', '9922', '9923', '9931', '9932', '9941']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_0 = simulation.calculate(element, period)
            categorie_fiscale_0 += bien_pour_categorie_fiscale_0
        return period, categorie_fiscale_0

'categorie_fiscale: 1'


class categorie_fiscale_1(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 1"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_1 = 0
        for each_variable in ['611', '952']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_1 = simulation.calculate(element, period)
            categorie_fiscale_1 += bien_pour_categorie_fiscale_1
        return period, categorie_fiscale_1

'categorie_fiscale: 2'


class categorie_fiscale_2(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 2"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '441', '442', '443', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1120', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '11113', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '431', '432', '441', '442', '443', '562', '613', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '11113', '1112', '1120', '1240', '9903', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '613', '1112', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '613', '1112', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_2 = 0
        for each_variable in ['111', '112', '113', '114', '115', '116', '117', '118', '119', '121', '122', '613', '1112', '9933']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_2 = simulation.calculate(element, period)
            categorie_fiscale_2 += bien_pour_categorie_fiscale_2
        return period, categorie_fiscale_2

'categorie_fiscale: 3'


class categorie_fiscale_3(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 3"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11112', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11112', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11112', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11112', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '431', '432', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '562', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1240', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11113', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_3 = 0
        for each_variable in ['1151', '1181', '311', '312', '313', '314', '321', '322', '444', '451', '4511', '452', '4522', '453', '454', '455', '511', '512', '513', '520', '531', '532', '533', '540', '551', '552', '561', '612', '711', '712', '713', '721', '723', '724', '736', '831', '832', '911', '912', '913', '914', '915', '921', '922', '923', '931', '932', '933', '934', '935', '953', '954', '960', '11114', '1211', '1212', '1213', '1231', '1232', '1262', '1270']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_3 = simulation.calculate(element, period)
            categorie_fiscale_3 += bien_pour_categorie_fiscale_3
        return period, categorie_fiscale_3

'categorie_fiscale: 4'


class categorie_fiscale_4(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 4"

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_4 = 0
        for each_variable in ['431', '432', '441', '442', '443', '562', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '11113', '1120', '1240', '9903']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_4 = simulation.calculate(element, period)
            categorie_fiscale_4 += bien_pour_categorie_fiscale_4
        return period, categorie_fiscale_4

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_4 = 0
        for each_variable in ['431', '432', '441', '442', '443', '562', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '11113', '1120', '1240', '9903']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_4 = simulation.calculate(element, period)
            categorie_fiscale_4 += bien_pour_categorie_fiscale_4
        return period, categorie_fiscale_4

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_4 = 0
        for each_variable in ['431', '432', '441', '442', '443', '562', '731', '732', '733', '734', '735', '941', '942', '951', '11112', '11113', '1120', '1240', '9903']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_4 = simulation.calculate(element, period)
            categorie_fiscale_4 += bien_pour_categorie_fiscale_4
        return period, categorie_fiscale_4

'categorie_fiscale: 7'


class categorie_fiscale_7(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 7"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_7 = 0
        for each_variable in ['2201']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_7 = simulation.calculate(element, period)
            categorie_fiscale_7 += bien_pour_categorie_fiscale_7
        return period, categorie_fiscale_7

'categorie_fiscale: 8'


class categorie_fiscale_8(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 8"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_8 = 0
        for each_variable in ['2202']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_8 = simulation.calculate(element, period)
            categorie_fiscale_8 += bien_pour_categorie_fiscale_8
        return period, categorie_fiscale_8

'categorie_fiscale: 9'


class categorie_fiscale_9(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 9"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_9 = 0
        for each_variable in ['2203']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_9 = simulation.calculate(element, period)
            categorie_fiscale_9 += bien_pour_categorie_fiscale_9
        return period, categorie_fiscale_9

'categorie_fiscale: 10'


class categorie_fiscale_10(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 10"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_10 = 0
        for each_variable in ['211']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_10 = simulation.calculate(element, period)
            categorie_fiscale_10 += bien_pour_categorie_fiscale_10
        return period, categorie_fiscale_10

'categorie_fiscale: 12'


class categorie_fiscale_12(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 12"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_12 = 0
        for each_variable in ['212']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_12 = simulation.calculate(element, period)
            categorie_fiscale_12 += bien_pour_categorie_fiscale_12
        return period, categorie_fiscale_12

'categorie_fiscale: 13'


class categorie_fiscale_13(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 13"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_13 = 0
        for each_variable in ['213']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_13 = simulation.calculate(element, period)
            categorie_fiscale_13 += bien_pour_categorie_fiscale_13
        return period, categorie_fiscale_13

'categorie_fiscale: 14'


class categorie_fiscale_14(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 14"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_14 = 0
        for each_variable in ['722']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_14 = simulation.calculate(element, period)
            categorie_fiscale_14 += bien_pour_categorie_fiscale_14
        return period, categorie_fiscale_14

'categorie_fiscale: 15'


class categorie_fiscale_15(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 15"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_15 = 0
        for each_variable in ['1254']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_15 = simulation.calculate(element, period)
            categorie_fiscale_15 += bien_pour_categorie_fiscale_15
        return period, categorie_fiscale_15

'categorie_fiscale: 16'


class categorie_fiscale_16(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 16"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_16 = 0
        for each_variable in ['1253']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_16 = simulation.calculate(element, period)
            categorie_fiscale_16 += bien_pour_categorie_fiscale_16
        return period, categorie_fiscale_16

'categorie_fiscale: 17'


class categorie_fiscale_17(DatedVariable):
    column = FloatCol
    entity_class = Menages
    label = u"Categorie fiscale 17"

    @dated_function(start = date(1994, 1, 1), stop = date(1994, 12, 31))
    def function_1994(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(1995, 1, 1), stop = date(1995, 12, 31))
    def function_1995(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(1996, 1, 1), stop = date(1996, 12, 31))
    def function_1996(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(1997, 1, 1), stop = date(1997, 12, 31))
    def function_1997(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(1998, 1, 1), stop = date(1998, 12, 31))
    def function_1998(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(1999, 1, 1), stop = date(1999, 12, 31))
    def function_1999(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2000, 1, 1), stop = date(2000, 12, 31))
    def function_2000(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2001, 1, 1), stop = date(2001, 12, 31))
    def function_2001(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2002, 1, 1), stop = date(2002, 12, 31))
    def function_2002(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2003, 1, 1), stop = date(2003, 12, 31))
    def function_2003(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2004, 1, 1), stop = date(2004, 12, 31))
    def function_2004(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2005, 1, 1), stop = date(2005, 12, 31))
    def function_2005(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2006, 1, 1), stop = date(2006, 12, 31))
    def function_2006(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2007, 1, 1), stop = date(2007, 12, 31))
    def function_2007(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2008, 1, 1), stop = date(2008, 12, 31))
    def function_2008(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2009, 1, 1), stop = date(2009, 12, 31))
    def function_2009(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2010, 1, 1), stop = date(2010, 12, 31))
    def function_2010(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2011, 1, 1), stop = date(2011, 12, 31))
    def function_2011(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2012, 1, 1), stop = date(2012, 12, 31))
    def function_2012(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_2013(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17

    @dated_function(start = date(2014, 1, 1), stop = date(2014, 12, 31))
    def function_2014(self, simulation, period):
        categorie_fiscale_17 = 0
        for each_variable in ['1251', '1252', '1255']:
            element = 'poste_coicop_' + each_variable
            bien_pour_categorie_fiscale_17 = simulation.calculate(element, period)
            categorie_fiscale_17 += bien_pour_categorie_fiscale_17
        return period, categorie_fiscale_17
