

import logging
import pandas


from openfisca_survey_manager.temporary import temporary_store_decorator
from openfisca_survey_manager.survey_collections import SurveyCollection
from openfisca_survey_manager import default_config_files_directory as config_files_directory

from openfisca_france_indirect_taxation.build_survey_data.utils import ident_men_dtype


log = logging.getLogger(__name__)


@temporary_store_decorator(config_files_directory = config_files_directory, file_name = 'indirect_taxation_tmp')
def build_homogeneisation_revenus_menages(temporary_store = None, year = None):
    '''Build menage consumption by categorie fiscale dataframe '''

    assert temporary_store is not None
    temporary_store.open()
    assert year is not None
    # Load data
    bdf_survey_collection = SurveyCollection.load(
        collection = 'budget_des_familles', config_files_directory = config_files_directory)
    survey = bdf_survey_collection.get_survey('budget_des_familles_{}'.format(year))

# Homogeneisation des donnees sur les revenus des menages
# Calcul d'un proxi du revenu disponible des menages

# Homogeneisation des bases de ressources

    if year == 1995:
        # La base 95 permet de distinguer taxe d'habitation et impôts fonciers.
        # On calcule leur montant relatif pour l'appliquer à 00 et 05
        menrev = survey.get_values(
            table = 'menrev',
            variables = [
                'impfon',
                'imphab',
                'ir',
                'irbis',
                'mena',
                'ponderr',
                'revaid',
                'revcho',
                'revfam',
                'revind',
                'revinv',
                'revlog',
                'revpat',
                'revret',
                'revrmi',
                'revsal',
                'revsec',
                'revtot',
                ],
            )
        menage = survey.get_values(
            table = 'socioscm',
            variables = ['exdep', 'exrev', 'mena']
            )

        menage.set_index('mena')
        menrev = menrev.merge(menage, left_index = True, right_index = True)
        # cette étape de ne garder que les données dont on est sûr de la qualité et de la véracité
        # exdep = 1 si les données sont bien remplies pour les dépenses du ménage
        # exrev = 1 si les données sont bien remplies pour les revenus du ménage

        menrev = menrev[(menrev.exdep == 1) & (menrev.exrev == 1)]

        menrev['foncier_hab'] = menrev.imphab + menrev.impfon
        menrev['part_IMPHAB'] = menrev.imphab / menrev.foncier_hab
        menrev['part_IMPFON'] = menrev.impfon / menrev.foncier_hab

        menrev['revsoc'] = (
            menrev.revret + menrev.revcho + menrev.revfam + menrev.revlog + menrev.revinv + menrev.revrmi
            )
        for variable in ['revcho', 'revfam', 'revinv', 'revlog', 'revret', 'revrmi']:
            del menrev[variable]

        menrev['revact'] = menrev['revsal'] + menrev['revind'] + menrev['revsec']
        menrev.rename(
            columns = dict(
                revpat = 'revpat',
                impfon = 'impfon',
                imphab = 'imphab',
                revaid = 'somme_obl_recue',
                ),
            inplace = True
            )
        menrev['impot_revenu'] = menrev['ir'] + menrev['irbis']

        rev_disp = survey.get_values(
            table = 'menrev',
            variables = ['revtot', 'revret', 'revcho', 'revfam', 'revlog', 'revinv', 'revrmi', 'imphab', 'impfon',
                'revaid', 'revsal', 'revind', 'revsec', 'revpat', 'mena', 'ponderr', 'ir', 'irbis'],
            )
        rev_disp.set_index('mena', inplace=True)

        menage2 = survey.get_values(
            table = 'socioscm',
            variables = ['exdep', 'exrev', 'mena']
            )

        menage2.set_index('mena', inplace = True)
        rev_disp = menage2.merge(rev_disp, left_index = True, right_index = True)

        rev_disp = rev_disp[(rev_disp.exrev == 1) & (rev_disp.exdep == 1)]

        rev_disp['revsoc'] = (
            rev_disp['revret'] + rev_disp['revcho'] + rev_disp['revfam'] + rev_disp['revlog'] + rev_disp['revinv']
            + rev_disp['revrmi']
            )
        rev_disp['impot_revenu'] = rev_disp['ir'] + rev_disp['irbis']

        rev_disp.rename(
            columns = dict(
                revaid = 'somme_obl_recue',
                ),
            inplace = True
            )
        rev_disp.somme_obl_recue = rev_disp.somme_obl_recue.fillna(0)

        rev_disp['revact'] = rev_disp['revsal'] + rev_disp['revind'] + rev_disp['revsec']
        rev_disp['revtot'] = rev_disp['revact'] + rev_disp['revpat'] + rev_disp['revsoc'] + rev_disp['somme_obl_recue']
        rev_disp['revact'] = rev_disp['revsal'] + rev_disp['revind'] + rev_disp['revsec']

        rev_disp.rename(
            columns = dict(
                ponderr = 'pondmen',
                mena = 'ident_men',
                revind = 'act_indpt',
                revsal = 'salaires',
                revsec = 'autres_rev',
                ),
            inplace = True
            )

        rev_disp['autoverses'] = '0'
        rev_disp['somme_libre_recue'] = '0'
        rev_disp['autres_ress'] = '0'

        # /* Le revenu disponible se calcule à partir de revtot à laquelle on retrancher la taxe d'habitation
        # et l'impôt sur le revenu, plus éventuellement les CSG et CRDS.
        # La variable revtot est la somme des revenus d'activité, sociaux, du patrimoine et d'aide. */
        #
        rev_disp['rev_disponible'] = rev_disp.revtot - rev_disp.impot_revenu - rev_disp.imphab
        loyers_imputes = temporary_store['depenses_bdf_{}'.format(year)]
        loyers_imputes.rename(
            columns = {'0411': 'loyer_impute'},
            inplace = True,
            )

        rev_dispbis = loyers_imputes.merge(rev_disp, left_index = True, right_index = True)
        rev_disp['rev_disp_loyerimput'] = rev_disp['rev_disponible'] - rev_dispbis['loyer_impute']

        for var in ['somme_obl_recue', 'act_indpt', 'revpat', 'salaires', 'autres_rev', 'rev_disponible', 'impfon',
                'imphab', 'revsoc', 'revact', 'impot_revenu', 'revtot', 'rev_disp_loyerimput']:
            rev_disp[var] = rev_disp[var] / 6.55957  # CONVERSION EN EUROS

        temporary_store['revenus_{}'.format(year)] = rev_disp

    elif year == 2000:
        # TODO: récupérer plutôt les variables qui viennent de la table dépenses (dans temporary_store)
        rev_disp = survey.get_values(
            table = 'consomen',
            variables = ['c13141', 'c13111', 'c13121', 'c13131', 'pondmen', 'ident'],
            )
        menage = survey.get_values(
            table = 'menage',
            variables = ['ident', 'revtot', 'revact', 'revsoc', 'revpat', 'rev70', 'rev71', 'revt_d', 'pondmen',
                'rev10', 'rev11', 'rev20', 'rev21'],
            ).sort_values(by = ['ident'])
        menage.index = menage.index.astype(ident_men_dtype)
        rev_disp.index = rev_disp.index.astype(ident_men_dtype)
        revenus = menage.join(rev_disp, how = 'outer', rsuffix = 'rev_disp')
        revenus.fillna(0, inplace = True)
        revenus.rename(
            columns = dict(
                c13111 = 'impot_res_ppal',
                c13141 = 'impot_revenu',
                c13121 = 'impot_autres_res',
                rev70 = 'somme_obl_recue',
                rev71 = 'somme_libre_recue',
                revt_d = 'autres_ress',
                ident = 'ident_men',
                rev10 = 'act_indpt',
                rev11 = 'autoverses',
                rev20 = 'salaires',
                rev21 = 'autres_rev',
                ),
            inplace = True
            )

        var_to_ints = ['pondmen', 'impot_autres_res', 'impot_res_ppal', 'pondmenrev_disp', 'c13131']
        for var_to_int in var_to_ints:
            revenus.loc[revenus[var_to_int].isnull(), var_to_int] = 0
            revenus[var_to_int] = revenus[var_to_int].astype(int)

        revenus['imphab'] = 0.65 * (revenus.impot_res_ppal + revenus.impot_autres_res)
        revenus['impfon'] = 0.35 * (revenus.impot_res_ppal + revenus.impot_autres_res)

        loyers_imputes = temporary_store['depenses_bdf_{}'.format(year)]
        variables = ['poste_04_2_1']
        loyers_imputes = loyers_imputes[variables]

        loyers_imputes.rename(
            columns = {'poste_04_2_1': 'loyer_impute'},
            inplace = True,
            )

        temporary_store['loyers_imputes_{}'.format(year)] = loyers_imputes
        loyers_imputes.index = loyers_imputes.index.astype(ident_men_dtype)

        revenus.set_index('ident_men', inplace = True)
        revenus.index = revenus.index.astype(ident_men_dtype)
        assert set(revenus.index) == set(loyers_imputes.index), 'revenus and loyers_imputes indexes are not equal'
        revenus = revenus.merge(loyers_imputes, left_index = True, right_index = True)
        revenus['rev_disponible'] = revenus.revtot - revenus.impot_revenu - revenus.imphab
        revenus['rev_disponible'] = revenus['rev_disponible'] * (revenus['rev_disponible'] >= 0)
        revenus['rev_disp_loyerimput'] = revenus.rev_disponible + revenus.loyer_impute

        var_to_ints = ['loyer_impute']
        for var_to_int in var_to_ints:
            revenus[var_to_int] = revenus[var_to_int].astype(int)

        temporary_store['revenus_{}'.format(year)] = revenus

    elif year == 2005:
        c05d = survey.get_values(
            table = 'c05d',
            variables = ['c13111', 'c13121', 'c13141', 'pondmen', 'ident_men'],
            )
        rev_disp = c05d.sort_values(by = ['ident_men'])
        del c05d
        menage = survey.get_values(
            table = 'menage',
            variables = ['ident_men', 'revtot', 'revact', 'revsoc', 'revpat', 'rev700_d', 'rev701_d',
                'rev999_d', 'rev100_d', 'rev101_d', 'rev200_d', 'rev201_d'],
            ).sort_values(by = ['ident_men'])
        rev_disp.set_index('ident_men', inplace = True)
        menage.set_index('ident_men', inplace = True)
        menage.index = menage.index.astype('str')
        rev_disp.index = rev_disp.index.astype('str')
        assert menage.index.dtype == rev_disp.index.dtype, 'menage ({}) and revdisp ({}) dtypes differs'.format(
            menage.index.dtype, rev_disp.index.dtype)
        revenus = pandas.concat([menage, rev_disp], axis = 1)
        assert len(menage.index) == len(revenus.index)
        revenus.rename(
            columns = dict(
                rev100_d = 'act_indpt',
                rev101_d = 'autoverses',
                rev200_d = 'salaires',
                rev201_d = 'autres_rev',
                rev700_d = 'somme_obl_recue',
                rev701_d = 'somme_libre_recue',
                rev999_d = 'autres_ress',
                c13111 = 'impot_res_ppal',
                c13141 = 'impot_revenu',
                c13121 = 'impot_autres_res',
                ),
            inplace = True
            )
        # Ces pondérations (0.65 0.35) viennent de l'enquête BdF 1995 qui distingue taxe d'habitation et impôts
        # fonciers. A partir de BdF 1995,
        # On a calculé que la taxe d'habitation représente en moyenne 65% des impôts locaux, et que les impôts
        # fonciers en représentenr 35%.
        # On applique ces taux aux enquêtes 2000 et 2005.
        revenus['imphab'] = 0.65 * (revenus.impot_res_ppal + revenus.impot_autres_res)
        revenus['impfon'] = 0.35 * (revenus.impot_res_ppal + revenus.impot_autres_res)
        del revenus['impot_autres_res']
        del revenus['impot_res_ppal']

        # Calculer le revenu disponible avec et sans le loyer imputé
        loyers_imputes = temporary_store['depenses_bdf_{}'.format(year)]
        variables = ['poste_04_2_1']
        loyers_imputes = loyers_imputes[variables]
        loyers_imputes.rename(
            columns = {'poste_04_2_1': 'loyer_impute'},
            inplace = True,
            )
        temporary_store['loyers_imputes_{}'.format(year)] = loyers_imputes
        loyers_imputes.index = loyers_imputes.index.astype('str')
        assert revenus.index.dtype == loyers_imputes.index.dtype
        assert set(revenus.index) == set(loyers_imputes.index), '''revenus and loyers_imputes indexes are not equal.
In revenus and not in loyers_imputes:
{}
In loyers_imputes and not in revenus:
{}
'''.format(set(revenus.index) - set(loyers_imputes.index), set(loyers_imputes.index) - set(revenus.index))
        revenus = revenus.merge(loyers_imputes, left_index = True, right_index = True)
        revenus['rev_disponible'] = revenus.revtot - revenus.impot_revenu - revenus.imphab
        revenus['rev_disponible'] = revenus['rev_disponible'] * (revenus['rev_disponible'] >= 0)
        revenus['rev_disp_loyerimput'] = revenus.rev_disponible + revenus.loyer_impute

        temporary_store['revenus_{}'.format(year)] = revenus

    elif year in [2011, 2017]:
        c05_variables = ['c13111', 'c13121', 'c13141', 'pondmen', 'ident_men']
        c05 = survey.get_values(
            table = 'c05',
            variables = c05_variables,
            ignorecase = True,
            lowercase = True
            )

        rev_disp = c05.sort_values(by = ['ident_men'])
        del c05, c05_variables

        menage_variables = [
            'ident_men',
            'rev700',
            'rev701',
            'rev999',
            'revact',
            'revindep',
            'revpat',
            'revsoc',
            'revtot',
            'salaires',
            ]

        menage = survey.get_values(
            table = 'menage',
            variables = menage_variables,
            ignorecase = True
            )

        menage = menage.sort_values(by = ['ident_men'])

        rev_disp.index = rev_disp.index.astype(ident_men_dtype)
        menage.index = menage.index.astype(ident_men_dtype)
        rev_disp.set_index('ident_men', inplace = True)
        menage.set_index('ident_men', inplace = True)
        revenus = pandas.concat([menage, rev_disp], axis = 1)
        menage.index.name = 'ident_men'
        revenus.index.name = 'ident_men'

        # Ces revenus sont déjà intégrés dans revindep et salaires
        # rev101_d = "autoverses",
        # rev201_d = "autres_rev",
        revenus.rename(
            columns = dict(
                revindep = 'act_indpt',
                salaires = 'salaires',
                rev700 = 'somme_obl_recue',
                rev701 = 'somme_libre_recue',
                rev999 = 'autres_ress',
                c13111 = 'impot_res_ppal',
                c13141 = 'impot_revenu',
                c13121 = 'impot_autres_res',
                ),
            inplace = True
            )
        revenus['imphab'] = 0.65 * (revenus.impot_res_ppal + revenus.impot_autres_res)
        revenus['impfon'] = 0.35 * (revenus.impot_res_ppal + revenus.impot_autres_res)
        del revenus['impot_autres_res']
        del revenus['impot_res_ppal']

        loyers_imputes = temporary_store['depenses_bdf_{}'.format(year)]
        variables = ['poste_04_2_1']  # loyers imputés
        loyers_imputes = loyers_imputes[variables].copy()
        loyers_imputes.rename(
            columns = {'poste_04_2_1': 'loyer_impute'},
            inplace = True,
            )
        temporary_store['loyers_imputes_{}'.format(year)] = loyers_imputes
        revenus = revenus.merge(loyers_imputes, left_index = True, right_index = True)
        revenus['rev_disponible'] = revenus.revtot - revenus.impot_revenu - revenus.imphab
        revenus['rev_disponible'] = revenus['rev_disponible'] * (revenus['rev_disponible'] >= 0)
        revenus['rev_disp_loyerimput'] = revenus.rev_disponible + revenus.loyer_impute
        temporary_store['revenus_{}'.format(year)] = revenus
        temporary_store.close()
