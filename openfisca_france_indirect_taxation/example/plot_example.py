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


from pandas import DataFrame, concat
import matplotlib.pyplot as plt

import openfisca_france_indirect_taxation
from openfisca_survey_manager.surveys import SurveyCollection


from openfisca_france_indirect_taxation.surveys import SurveyScenario


def get_input_data_frame(year):
    openfisca_survey_collection = SurveyCollection.load(collection = "openfisca_indirect_taxation")
    openfisca_survey = openfisca_survey_collection.surveys["openfisca_indirect_taxation_data_{}".format(year)]
    input_data_frame = openfisca_survey.get_values(table = "input")
    input_data_frame.reset_index(inplace = True)
    return input_data_frame


def simulate_df(year = 2005):
    '''
    Construction de la DataFrame à partir de laquelle sera faite l'analyse des données
    '''
    input_data_frame = get_input_data_frame(year)
    TaxBenefitSystem = openfisca_france_indirect_taxation.init_country()

    tax_benefit_system = TaxBenefitSystem()
    survey_scenario = SurveyScenario().init_from_data_frame(
        input_data_frame = input_data_frame,
        tax_benefit_system = tax_benefit_system,
        year = year,
        )
    simulation = survey_scenario.new_simulation()

    return DataFrame(
        dict([
            (name, simulation.calculate(name)) for name in [
                'montant_tva_taux_plein',
                'consommation_tva_taux_plein',
                'categorie_fiscale_11',
                'montant_tva_taux_intermediaire',
                'consommation_tva_taux_intermediaire',
                'montant_tva_taux_reduit',
                'montant_tva_taux_super_reduit',
                'montant_tva_total',
                'ident_men',
                'pondmen',
                'decuc',
                'age',
                'revtot',
                'rev_disponible',
                'ocde10',
                'niveau_de_vie'
                ]
            ])
        )

def wavg(groupe, var):
    '''
    Fonction qui calcule la moyenne pondérée par groupe d'une variable
    '''
    d = groupe[var]
    w = groupe['pondmen']
    return (d * w).sum() / w.sum()

def collapse(dataframe, groupe, var):
    '''
    Pour une variable, fonction qui calcule la moyenne pondérée au sein de chaque groupe.
    '''
    grouped = dataframe.groupby([groupe])
    var_weighted_grouped = grouped.apply(lambda x: wavg(groupe = x,var =var))
    return var_weighted_grouped

def df_weighted_average_grouped(dataframe, groupe, varlist):
    '''
    Agrège les résultats de weighted_average_grouped() en une unique dataframe pour la liste de variable 'varlist'.
    '''
    return DataFrame(
        dict([
            (var,collapse(dataframe, groupe, var)) for var in varlist
        ])
        )


if __name__ == '__main__':
    import logging
    log = logging.getLogger(__name__)
    import sys
    logging.basicConfig(level = logging.INFO, stream = sys.stdout)

    ## Exemple : graphe par décile de revenu par uc du montant moyen (avec pondéréation) de tva aux taux plein et intermédiaires.

    # Constition d'une base de données agrégée par décile (= collapse en stata)
    df = simulate_df()
    Wconcat= df_weighted_average_grouped(dataframe = df, groupe = 'decuc', varlist = ['montant_tva_total','revtot'])
    df_to_plot = Wconcat['montant_tva_total']/Wconcat['revtot']


    # Plot du graphe avec matplotlib
    plt.figure();
    df_to_plot.plot(kind='bar', stacked=True); plt.axhline(0, color='k')
    Wconcat.plot(kind='bar', stacked=True); plt.axhline(0, color='k')


    ## Autres exemples :

    # Construction d'une base aggrégée selon les déciles. Attention : pas de pondération
    df_grouped_by_decuc = df.groupby(['decuc']).mean()
    df_grouped_by_decuc =df_grouped_by_decuc[['montant_tva_taux_plein','montant_tva_taux_intermediaire','montant_tva_taux_reduit','montant_tva_taux_super_reduit',]]

    # Une autre solution pour construire une base aggrégée selon les déciles. Attention : pas de pondération
    dfG = df.groupby(['decuc'], as_index=False)
    dfG = dfG.agg( { 'montant_tva_taux_plein' : { 'Meanmontant_tva_taux_plein':  'mean',
                                           'SDmontant_tva_taux_pleine': 'std'},
                    'montant_tva_taux_reduit': { 'Mmontant_tva_taux_reduit' : 'mean',}
                                          } )