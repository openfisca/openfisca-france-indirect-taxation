#! /usr/bin/env python
# -*- coding: utf-8 -*-


"""France specific indirect taxation model for OpenFisca -- a versatile microsimulation free software"""


from setuptools import setup, find_packages


classifiers = """\
Development Status :: 3 - Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Topic :: Scientific/Engineering :: Information Analysis
"""

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-France-Indirect-Taxation',
    version = '0.4.dev0',

    author = 'OpenFisca Team',
    author_email = 'contact@openfisca.fr',
    classifiers = [classifier for classifier in classifiers.split('\n') if classifier],
    description = doc_lines[0],
    keywords = 'benefit france indirect microsimulation social tax',
    license = 'http://www.fsf.org/licensing/licenses/agpl-3.0.html',
    long_description = '\n'.join(doc_lines[2:]),
    url = 'https://github.com/openfisca/openfisca-france-indirect-taxation',

    extras_require = dict(
        dev = [
            'pdbpp',
            ],
        test = [
            'matplotlib',
            'nose',
            'pandas >= 0.17',
            'seaborn',
            ],
        survey = [
            'OpenFisca-Survey-Manager',
            ],
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'Babel >= 0.9.4',
        'Biryani[datetimeconv] >= 0.10.2dev',
        'numpy >= 1.6',
        'OpenFisca-Core >= 0.5.4',
        'PyYAML >= 3.10',
        ],
    packages = find_packages(),
    test_suite = 'nose.collector',
    )
