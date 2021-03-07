from data import census_api_pull


def test_get_census_data_from_api():
    
    census_df = census_api_pull.get_census_data_from_api()

    assert len(census_df) == 58
    assert isinstance(census_df.zipcode[0], str)