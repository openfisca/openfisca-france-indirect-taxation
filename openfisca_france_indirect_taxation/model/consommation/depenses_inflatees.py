# -*- coding: utf-8 -*-

from __future__ import division


from datetime import date
import os
import pkg_resources
import pandas

from ..base import *  # noqa analysis:ignore


class poste_coicop_722_inflate(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses en carburants après calage"

    def function(self, simulation, period):
        default_config_files_directory = os.path.join(
            pkg_resources.get_distribution('openfisca_france_indirect_taxation').location)
        parametres_fiscalite_file_path = os.path.join(
            default_config_files_directory,
            'openfisca_france_indirect_taxation',
            'assets',
            'legislation',
            'Parametres fiscalite indirecte.xls'
            )

        masses_cn_data_frame = pandas.read_excel(parametres_fiscalite_file_path, sheetname = "consommation_CN")
        if year_data != year_calage:
            masses_cn_12postes_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data, year_calage]]
        else:
            masses_cn_12postes_data_frame = masses_cn_data_frame.loc[:, ['Code', year_data]]

        masses_ticpe_cn = int(
            masses_cn_12postes_data_frame[year_calage][masses_cn_12postes_data_frame['Code'] == '            07.2.2'].values
            )
        poste_coicop_722 = simulation.calculate('poste_coicop_722', period)
        pondmen = simulation.calculate('pondmen', period)
        masses_ticpe_bdf = (poste_coicop_722 * pondmen).sum() / 1e6
        ratio_ticpe = masses_ticpe_cn / masses_ticpe_bdf
        poste_coicop_722_inflate = poste_coicop_722 * ratio_ticpe

        return period, poste_coicop_722_inflate
