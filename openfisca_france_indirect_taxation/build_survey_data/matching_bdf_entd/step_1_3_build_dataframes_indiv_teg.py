# -*- coding: utf-8 -*-


from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.matching_bdf_entd.step_1_2_build_dataframes_vehicles import \
    build_df_menages_vehicles

from openfisca_survey_manager.temporary import TemporaryStore


temporary_store = TemporaryStore.create(file_name = 'transport_tmp')


def load_data_indiv_teg():

    year_entd = 2008

    entd_survey_collection = SurveyCollection.load(
        collection = 'enquete_transport', config_files_directory = config_files_directory
        )
    survey_entd = entd_survey_collection.get_survey('enquete_transport_{}'.format(year_entd))
    input_indiv_teg = survey_entd.get_values(table = 'q_ind_lieu_teg')

    variables_indiv_teg = [
        'ident_men',
        'noi',  # numero de l'indiv dans le menage
        'typlieu',  # numéro du lieu de travail pour l'indiv
        'v1_btravdist',
        'v1_btravtempsa',  # Durée habituelle pour faire le trajet aller au TEG (en min)
        'v1_btravtempsr',  # Durée habituelle pour faire le trajet retour du TEG (en min)
        'v1_btravnbarj',  # Nb d'aller-retour/jour de dplct
        'v1_btravbarf',  # Nb de jours/sem. où X se rend à son lieu de travail étude ou garde (TEG), en gral
        'v1_btravmoyen1s',  # Façon habituelle de se rendre au TEG, moy. 1
        'distrteg',  # Distance routière domicile – lieu de TEG (source Odomatrix Inra-Insee) (en km)
        ]

    # Keep relevant variables :
    indiv_teg_keep = input_indiv_teg[variables_indiv_teg]

    return indiv_teg_keep


def merge_indiv_teg_menage():
    data_menages = build_df_menages_vehicles()
    data_menages_entd = data_menages[0]
    data_bdf = data_menages[1]

    data_teg = load_data_indiv_teg()

    data_teg.rename(
        columns = {
            'v1_btravtempsa': 'duree_trajet_aller_teg',
            'v1_btravtempsr': 'duree_trajet_retour_teg',
            'v1_btravnbarj': 'nb_aller_retour_jour_teg',
            'v1_btravbarf': 'nb_jours_deplacement_teg',
            'v1_btravmoyen1s': 'mode_principal_deplacement_teg',
            'distrteg': 'distance_routiere_teg',
            },
        inplace = True,
        )

    data_teg['duree_trajet_aller_retour_teg'] = (
        data_teg['duree_trajet_aller_teg']
        + data_teg['duree_trajet_retour_teg']
        )
    data_teg['distance_routiere_hebdomadaire_par_teg'] = (
        data_teg['distance_routiere_teg'] * data_teg['nb_aller_retour_jour_teg'] * data_teg['nb_jours_deplacement_teg']
        )

    data_teg['distance_routiere_hebdomadaire_teg'] = data_teg.groupby(['ident_men'])['distance_routiere_hebdomadaire_par_teg'].transform('sum')
    data_teg['duree_moyenne_trajet_aller_retour_teg'] = data_teg.groupby(['ident_men'])['duree_trajet_aller_retour_teg'].transform('sum')
    data_teg['noi_max'] = data_teg.groupby(['ident_men'])['noi'].transform('max')
    data_teg['duree_moyenne_trajet_aller_retour_teg'] = data_teg['duree_moyenne_trajet_aller_retour_teg'] / data_teg['noi_max']

    data_teg = data_teg.query('noi == 1').query('typlieu == 1')
    data_teg = data_teg.fillna(0)

    data_teg = data_teg[['ident_men'] + ['distance_routiere_hebdomadaire_teg'] +
        ['duree_moyenne_trajet_aller_retour_teg'] + ['mode_principal_deplacement_teg']]
    data_teg['ident_men'] = data_teg['ident_men'].astype(str)
    data_menages_entd['ident_men'] = data_menages_entd['ident_men'].astype(str)

    data_entd = data_menages_entd.merge(data_teg, on = 'ident_men', how='left')
    data_entd = data_entd.fillna(0)

    return data_entd, data_bdf


if __name__ == "__main__":
    data = merge_indiv_teg_menage()
    data_entd = data[0]
    data_bdf = data[1]
