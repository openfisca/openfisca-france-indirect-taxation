#! /usr/bin/env python


"""France specific indirect taxation model for OpenFisca -- a versatile microsimulation free software."""


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
            'autopep8 >= 1.4.0, < 1.6.0',
            'flake8 >= 3.9.0, < 4.0.0',
            'flake8-bugbear >= 19.3.0, < 20.0.0',
            'ipdb >=0.13.9, < 1.0.0',
            'matplotlib <= 3.4.3, < 4.0.0',
            'nbconvert >= 5.5.0, < 6.0.0',
            "pytest < 6.0",
            'ruamel.yaml >= 0.17.16, < 1.0.0',
            'seaborn >= 0.11.2, < 1.0.0',
            ],
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'Babel >= 2.9.1, < 3.0.0',
        'OpenFisca-Core >= 35.8.0, < 36.0',
        'OpenFisca-Survey-Manager >= 0.46.11, < 1.0',
        'python-slugify >= 5.0.2, < 6.0.0',
        'xlrd >= 2.0.1, < 3.0.0',
        "statsmodels >= 0.10.1, < 1.0",
        ],
    packages = find_packages(),
    )
