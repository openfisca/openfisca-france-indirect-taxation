all: test

uninstall:
		pip freeze | grep -v "^-e" | xargs pip uninstall -y

clean:
		rm -rf build dist
		find . -name '*.pyc' -exec rm \{\} \;
		py3clean .

deps:
		pip install --upgrade pip twine wheel

install: deps
		@# Install OpenFisca-France-Indirect-Taxation for development.
		@# `make install` installs the editable version of OpenFisca-France-Indirect-Taxation.
		@# This allows contributors to test as they code.
		pip install --editable .[dev,test] --upgrade

build: clean deps
		@# Install OpenFisca-France-Indirect-Taxation for deployment and publishing.
		@# `make build` allows us to be be sure tests are run against the packaged version
		@# of OpenFisca-France-Indirect-Taxation, the same we put in the hands of users and reusers.
		python setup.py bdist_wheel
		find dist -name "*.whl" -exec pip install --upgrade {}[dev,test] \;

check-syntax-errors:
		python -m compileall -q .

format-style:
		@# Do not analyse .gitignored files.
		@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
		autopep8 `git ls-files | grep "\.py$$"`

check-style:
		@# Do not analyse .gitignored files.
		@# `make` needs `$$` to output `$`. Ref: http://stackoverflow.com/questions/2382764.
		flake8 `git ls-files | grep "\.py$$" | grep -v benjello_candidates_to_removal`

test: clean check-syntax-errors check-style
		@# Launch tests from openfisca_france_indirect_taxation/tests directory (and not .) because TaxBenefitSystem must be initialized
		@# before parsing source files containing formulas.
		openfisca test --country-package openfisca_france_indirect_taxation openfisca_france_indirect_taxation/tests


# IGNORE_OPT=--ignore-files='(tests_aids_categ.py|test_carburants_builder.py|test_categorie_fiscale.py|test_depenses_caburants_ht.py|test_get_poste_categorie_fiscale.py|test_legislations.py|test_simulation.py|test_survey_scenario.py|test_aliss_survey_scenario.py)'
# test-ci: check-syntax-errors
# 	nosetests $(TESTS_DIR) $(IGNORE_OPT) --with-doctest
