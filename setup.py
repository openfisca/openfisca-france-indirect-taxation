#! /usr/bin/env python


'''France specific indirect taxation model for OpenFisca -- a versatile microsimulation free software.'''


from setuptools import setup, find_namespace_packages


classifiers = ''' \
Development Status :: 3 - Alpha
License :: OSI Approved :: GNU Affero General Public License v3
Operating System :: POSIX
Programming Language :: Python
Programming Language :: Python :: 3.9
Programming Language :: Python :: 3.10
Programming Language :: Python :: 3.11
Topic :: Scientific/Engineering :: Information Analysis
'''

doc_lines = __doc__.split('\n')


setup(
    name = 'OpenFisca-France-Indirect-Taxation',
    version = '0.5.2',

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
            'autopep8 >= 2.0.2, < 3.0',
            'flake8 >= 6.0.0, < 7.0',
            'flake8-bugbear >= 23.3.12, < 24.0',
            'ipdb >= 0.13.13, < 0.14.0',
            'matplotlib >= 3.7.1, < 4.0',
            'nbconvert >= 7.2.10, < 8.0',
            'OpenFisca-Survey-Manager',
            'ruamel.yaml >= 0.17.21, < 0.18.0',
            'seaborn >= 0.12.2, < 0.13.0',
            'statsmodels >= 0.13.5, < 0.14.0',
            'xlrd >= 2.0.1, < 3.0',
            'openpyxl',
            ],
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        'numexpr',
        'OpenFisca-Core >= 43, < 44',
        'pandas >= 2.0.3, < 3.0',
        'python-slugify >= 8.0.1, < 9.0',
        ],
    packages = find_namespace_packages(),
    )
