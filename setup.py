#! /usr/bin/env python


'''France specific indirect taxation model for OpenFisca -- a versatile microsimulation free software.'''


from setuptools import setup, find_packages


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
            'autopep8',
            'flake8',
            'flake8-bugbear',
            'ipdb',
            'matplotlib',
            'nbconvert',
            # 'OpenFisca-Survey-Manager',
            'OpenFisca-Survey-Manager @ git+https://github.com/openfisca/openfisca-survey-manager.git@version_leap',
            'pytest',
            'ruamel.yaml',
            'seaborn',
            'statsmodels',
            'xlrd',
            ],
        ),
    include_package_data = True,  # Will read MANIFEST.in
    install_requires = [
        # 'OpenFisca-Core >= 38.0.1, < 39.0.0',
        'OpenFisca-Core @ git+https://github.com/openfisca/openfisca-core.git@version_leap',
        'pandas',
        'python-slugify',
        ],
    packages = find_packages(),
    )
