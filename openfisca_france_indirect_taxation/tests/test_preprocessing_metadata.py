from openfisca_france_indirect_taxation import FranceIndirectTaxationTaxBenefitSystem


def test_prix_carburants_metadata():
    tbs = FranceIndirectTaxationTaxBenefitSystem()
    parameters = tbs.parameters

    prix_carburants = parameters.prix_carburants

    # List of fuels processed in the loop in preprocessing.py
    fuels_to_check = [
        'diesel_ttc',
        'super_95_ttc',
        'super_98_ttc',
        'super_plombe_ttc',
        ]

    for fuel_name in fuels_to_check:
        assert hasattr(prix_carburants, fuel_name), f"{fuel_name} should exist in parameters"
        param = getattr(prix_carburants, fuel_name)

        # Check metadata existence
        assert hasattr(param, 'metadata'), f"{fuel_name} should have metadata"
        metadata = param.metadata

        # Check last_value_still_valid_on
        assert 'last_value_still_valid_on' in metadata, f"{fuel_name} metadata should have 'last_value_still_valid_on'"
        last_valid_date = metadata['last_value_still_valid_on']

        # Check reference
        assert 'reference' in metadata, f"{fuel_name} metadata should have 'reference'"
        assert last_valid_date in metadata['reference'], f"{fuel_name} reference should contain entry for {last_valid_date}"

        ref_content = metadata['reference'][last_valid_date]

        if fuel_name == 'super_plombe_ttc':
            # Special case for super_plombe_ttc which has no ref details in the code
            assert ref_content == {}, f"{fuel_name} reference should be empty dict as per code"
            assert last_valid_date == "2005-12-31"
        else:
            # Other fuels should have title and href
            assert 'title' in ref_content, f"{fuel_name} reference should have title"
            assert 'href' in ref_content, f"{fuel_name} reference should have href"

            # Check the max date in values
            instants = [v.instant_str for v in param.values_list]
            max_instant = max(instants)

            last_valid_year = int(last_valid_date[:4])
            max_instant_year = int(max_instant[:4])

            # Based on the code analysis: range(2018, most_recent_year) excludes most_recent_year
            # So max_instant_year should be last_valid_year - 1
            assert max_instant_year == last_valid_year - 1, \
                f"Expected max value year {last_valid_year - 1} but got {max_instant_year}. " \
                f"last_value_still_valid_on is {last_valid_date}"
