#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from nose.tools import nottest

from openfisca_core.tools.test_runner import generate_tests

from openfisca_france_indirect_taxation.tests import base

nottest(generate_tests)

options_by_dir = {
    'reforms/aliss_environnement': {
        'reforms': ['aliss_environnement'],
        },
    'reforms/aliss_sante': {
        'reforms': ['aliss_sante'],
        },
    'reforms/aliss_tva_sociale': {
        'reforms': ['aliss_tva_sociale'],
        },
    'formulas': {},
    }

options_by_dir = collections.OrderedDict((
    (
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'formulas')),
        dict(
            calculate_output = False,
            default_absolute_error_margin = 0.005,
            ),
        ),
    ))

def test():
    for directory, options in options_by_dir.iteritems():
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), directory))

        if options.get('requires'):
            # Check if the required package was successfully imported in tests/base.py
            if getattr(base, options.get('requires')) is None:
                continue

        if not options.get('default_relative_error_margin') and not options.get('default_absolute_error_margin'):
            options['default_absolute_error_margin'] = 0.005

        if options.get('requires'):
            # Check if the required package was successfully imported in tests/base.py
            if getattr(base, options.get('requires')) is None:
                continue

        reform_keys = options.get('reforms')
        tax_benefit_system = base.get_cached_composed_reform(
            reform_keys = reform_keys,
            tax_benefit_system = base.tax_benefit_system,
            ) if reform_keys is not None else base.tax_benefit_system

        test_generator = generate_tests(tax_benefit_system, path, options)

        for test in test_generator:
            yield test

