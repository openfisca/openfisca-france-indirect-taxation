# -*- coding: utf-8 -*-
"""
Created on Mon Jan 19 16:08:59 2015

@author: Etienne
"""

import pandas
import matplotlib.pyplot
import numpy

a = pandas.io.stata.read_stata('C:/Users/Etienne/Documents/data/budget_des_familles/2005/stata/c05d.dta')

# print a.pondmen[2]

b = len(a.pondmen)

facts = []
for i in range(b):
    facts.append(a.pondmen[i])

niveau_vie_decile = []
for j in range(1, 11):
    niveau_vie_decile.append(numpy.percentile(facts, 10 * j))

print niveau_vie_decile

figsize = (8, 6)
matplotlib.pyplot.plot(facts, label = "courbe")
matplotlib.pyplot.xlabel("n")
matplotlib.pyplot.legend()

# print numpy.percentile(facts,10*7)

c = 0
d = 0

for k in range(b):
    if a.pondmen[k] <= numpy.percentile(facts, 10):
        c = c + a.c01112[k]

print c / b
