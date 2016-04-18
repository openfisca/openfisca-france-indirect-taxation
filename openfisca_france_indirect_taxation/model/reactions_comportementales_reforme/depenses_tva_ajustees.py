# -*- coding: utf-8 -*-

from __future__ import division


from ..base import * # noqa analysis:ignore


class depenses_tva_taux_plein_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_2014_2015
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_plein_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - cce 2014-2016"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_2014_2016
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_plein_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_plein_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = simulation.legislation_at(period.start).taxes_carburants.abaissement_tva_taux_plein
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_plein_bis_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plei bis après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein_bis = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_bis_2014_2015
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_bis_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_bis_ajustees


class depenses_tva_taux_plein_bis_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein bis après réaction à la réforme - cce 2014-2016"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein_bis = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_plein_bis_2014_2016
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_bis_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_bis_ajustees


class depenses_tva_taux_plein_bis_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein bis après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein_bis = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_plein_bis
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_bis_ajustees = (
            depenses_tva_taux_plein *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_plein_bis) / (1 + taux_plein))
            )

        return period, depenses_tva_taux_plein_bis_ajustees


class depenses_tva_taux_plein_bis_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux plein après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_plein = simulation.calculate('depenses_tva_taux_plein', period)
        taux_plein = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_plein
        abaissement_tva_taux_plein = \
            simulation.legislation_at(period.start).taxes_carburants.abaissement_tva_taux_plein_bis
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_plein_ajustees = \
            depenses_tva_taux_plein * (1 + (1 + elasticite) * (- abaissement_tva_taux_plein) / (1 + taux_plein))

        return period, depenses_tva_taux_plein_ajustees


class depenses_tva_taux_reduit_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_reduit_2014_2015
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees


class depenses_tva_taux_reduit_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - cce 2014-2016"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_reduit_2014_2016
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees


class depenses_tva_taux_reduit_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees


class depenses_tva_taux_reduit_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux reduit après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_reduit = simulation.calculate('depenses_tva_taux_reduit', period)
        taux_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_reduit
        abaissement_tva_taux_reduit = \
            simulation.legislation_at(period.start).taxes_carburants.abaissement_tva_taux_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_reduit_ajustees = \
            depenses_tva_taux_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_reduit) / (1 + taux_reduit))

        return period, depenses_tva_taux_reduit_ajustees


class depenses_tva_taux_super_reduit_ajustees_cce_2014_2015(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - cce 2014-2015"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_super_reduit_2014_2015
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = \
            depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

        return period, depenses_tva_taux_super_reduit_ajustees


class depenses_tva_taux_super_reduit_ajustees_cce_2014_2016(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - cce 2014-2016"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = (
            simulation.legislation_at(period.start).contribution_climat_energie_reforme.abaissement_tva_taux_super_reduit_2014_2016
            )
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = \
            depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

        return period, depenses_tva_taux_super_reduit_ajustees


class depenses_tva_taux_super_reduit_ajustees_taxe_carbone(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA à taux super reduit après réaction à la réforme - taxe carbone"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = simulation.legislation_at(period.start).taxe_carbone.abaissement_tva_taux_super_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = \
            depenses_tva_taux_super_reduit * (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))

        return period, depenses_tva_taux_super_reduit_ajustees


class depenses_tva_taux_super_reduit_ajustees_taxes_carburants(Variable):
    column = FloatCol
    entity_class = Menages
    label = u"Dépenses sur les biens assujetis à la TVA tx super reduit après réaction à la réforme - taxes carburants"

    def function(self, simulation, period):
        depenses_tva_taux_super_reduit = simulation.calculate('depenses_tva_taux_super_reduit', period)
        taux_super_reduit = simulation.legislation_at(period.start).imposition_indirecte.tva.taux_super_reduit
        abaissement_tva_taux_super_reduit = \
            simulation.legislation_at(period.start).taxes_carburants.abaissement_tva_taux_super_reduit
        elasticite = simulation.calculate('elas_price_3_3')
        depenses_tva_taux_super_reduit_ajustees = (
            depenses_tva_taux_super_reduit *
            (1 + (1 + elasticite) * (- abaissement_tva_taux_super_reduit) / (1 + taux_super_reduit))
            )
        return period, depenses_tva_taux_super_reduit_ajustees
