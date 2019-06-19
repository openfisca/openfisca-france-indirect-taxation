# -*- coding: utf-8 -*-

from __future__ import division


from openfisca_france_indirect_taxation.model.base import *  # noqa analysis:ignore


class age_carte_grise(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"âge de la carte grise du véhicule principal"


class age_vehicule(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"âge du véhicule principal"


class aides_logement(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage touche des aides au logement"


class bat_av_49(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le bâtiment date d'avant 1949"


class bat_49_74(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le bâtiment date d'entre 1949 et 1974"


class bat_ap_74(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le bâtiment date d'après 1974"


class cataeu(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"catégorie de la commune de résidence 2011"


class dip14pr(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Diplôme de la personne de référence"


class ident_men(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Identifiant du ménage"


class isolation_fenetres(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Qualité de l'isolation des fenêtres"


class isolation_murs(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Qualité de l'isolation des murs"


class isolation_toit(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Qualité de l'isolation du toit"


class identifiant_menage(YearlyVariable):
    value_type = str
    entity = Menage
    label = u"Code identifiant le ménage"


class log_indiv(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage vie dans un logement individuel"


class majorite_double_vitrage(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Majorité de double vitrage dans le logement"


class ocde10(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"unités de consommation"


class ouest_sud(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage vit dans l'ouest ou le sud de la France"


class paris(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Le ménage vit en région parisienne"


class petite_ville(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Le ménage vit dans une petite ville"


class pondmen(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Pondération du ménage"


class rural(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage vit en milieu rural"


class situacj(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Situation du conjoint vis-à-vis du travail"


class situapr(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Situation de la personne de référence vis-à-vis du travail"


class surfhab_d(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Taille du logement en m2"


class strate(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"catégorie de la commune de résidence"


class stalog(YearlyVariable):
    value_type = int
    entity = Menage
    label = u"Statut du logement (1 = propriétaire)"


class tchof(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"unité urbaine"


class tuu(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"unité urbaine"


class typmen(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"type du ménage"


class vag(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"numéro de la vague d'interrogation du ménage"


class vp_deplacements_pro(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage utilise son véhicule particulier pour ses déplacements pro"


class vp_domicile_travail(YearlyVariable):
    value_type = float
    entity = Menage
    label = u"Le ménage utilise son véhicule particulier pour se rendre à son travail"


class TypesZeat(Enum):
    __order__ = 'dom region_parisienne bassin_parisien nord est ouest sud centre mediterrannee'  # Needed to keep the order in Python 2
    dom = "dom",
    region_parisienne = "region_parisienne",
    bassin_parisien = "bassin_parisien",
    nord = "nord",
    est = "est",
    ouest = "ouest",
    sud = "sud-ouest",
    centre = "centre-est",
    mediterrannee = "mediterrannee"


class zeat(YearlyVariable):
    value_type = Enum
    possible_values = TypesZeat
    default_value = TypesZeat.dom
    entity = Menage
    label = u"Zone d'étude et d'aménagement du territoire"
