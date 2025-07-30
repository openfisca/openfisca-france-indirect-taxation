# -*- coding: utf-8 -*-


from openfisca_france_indirect_taxation.variables.base import *  # noqa analysis:ignore


class age_carte_grise(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'âge de la carte grise du véhicule principal'


class age_vehicule(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'âge du véhicule principal'


class aides_logement(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Le ménage touche des aides au logement'

class aise(YearlyVariable):
    value_type = float
    entity = Menage 
    label = "Sentiment du ménage par rapport à son budget actuel"
    
    
class bat_av_49(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Le bâtiment date d'avant 1949"


class bat_49_74(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Le bâtiment date d'entre 1949 et 1974"


class bat_ap_74(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Le bâtiment date d'après 1974"


class cataeu(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'catégorie de la commune de résidence 2011'


class dip14pr(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Diplôme de la personne de référence'


class ident_men(YearlyVariable):
    value_type = str
    entity = Menage
    label = 'Identifiant du ménage'


class isolation_fenetres(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Qualité de l'isolation des fenêtres"


class isolation_murs(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Qualité de l'isolation des murs"


class isolation_toit(YearlyVariable):
    value_type = int
    entity = Menage
    label = "Qualité de l'isolation du toit"


class identifiant_menage(YearlyVariable):
    value_type = str
    entity = Menage
    label = 'Code identifiant le ménage'


class log_indiv(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Le ménage vie dans un logement individuel'


class majorite_double_vitrage(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'Majorité de double vitrage dans le logement'


class ocde10(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'unités de consommation'


class ouest_sud(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Le ménage vit dans l'ouest ou le sud de la France"


class paris(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'Le ménage vit en région parisienne'


class petite_ville(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'Le ménage vit dans une petite ville'


class pondmen(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'Pondération du ménage'


class rural(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Le ménage vit en milieu rural'


class situacj(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Situation du conjoint vis-à-vis du travail'


class situapr(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Situation de la personne de référence vis-à-vis du travail'

class situaagr(YearlyVariable):
    value_type = float
    entity = Menage
    label = "Situation de l'autre personne du groupe de référence vis-à-vis du travail"

class surfhab_d(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Taille du logement en m2'


class strate(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'catégorie de la commune de résidence'


class stalog(YearlyVariable):
    value_type = int
    entity = Menage
    label = 'Statut du logement (1 = propriétaire)'


class tchof(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'unité urbaine'


class tuu(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'unité urbaine'


class typmen(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'type du ménage'


class vag(YearlyVariable):
    value_type = float
    entity = Menage
    label = "numéro de la vague d'interrogation du ménage"


class vp_deplacements_pro(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Le ménage utilise son véhicule particulier pour ses déplacements pro'


class vp_domicile_travail(YearlyVariable):
    value_type = float
    entity = Menage
    label = 'Le ménage utilise son véhicule particulier pour se rendre à son travail'


class TypesZeat(Enum):
    __order__ = 'dom region_parisienne bassin_parisien nord est ouest sud centre mediterrannee'  # Needed to keep the order in Python 2
    dom = 'dom',
    region_parisienne = 'region_parisienne',
    bassin_parisien = 'bassin_parisien',
    nord = 'nord',
    est = 'est',
    ouest = 'ouest',
    sud = 'sud-ouest',
    centre = 'centre-est',
    mediterrannee = 'mediterrannee'


class zeat(YearlyVariable):
    value_type = Enum
    possible_values = TypesZeat
    default_value = TypesZeat.dom
    entity = Menage
    label = "Zone d'étude et d'aménagement du territoire"
