# -*- coding: utf-8 -*-


from __future__ import division


from ..base import *  # noqa analysis:ignore


class elas_exp_1(Variable):
    column = FloatCol(default = 0)  # FloatCol(default = 0)
    entity_class = Menages
    label = u"Elasticité dépense carburants"
