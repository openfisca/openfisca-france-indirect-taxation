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
    entry_points = {
        'console_scripts': ['build-survey-data=openfisca_france_indirect_taxation.scripts.build_survey_data:main'],
        },

    extras_require = dict(
        dev = [
            "autopep8 ==1.4.4",
            "flake8 >=3.7.0,<3.8.0",
            # "flake8-print", Bring back when one has time to clear all prints
            'matplotlib',
            'nbconvert >= 5.5.0',
            "pytest < 5.0",
            'pdbpp',
            'ruamel.yaml',
            'seaborn',
            ],
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'Babel >= 0.9.4',
        'OpenFisca-Core >= 0.5.4',
        'OpenFisca-Survey-Manager >= 0.35,<1.0',
        'python-slugify',
        'PyYAML >= 3.10',
        "numpy >= 1.11, <1.16",  # openfisca-survey-manager deps and https://github.com/openfisca/openfisca-survey-manager/pull/79            'pandas >= 0.17',
        "pandas <= 0.24.2",
        ],
    packages = find_packages(),
    )
