from datetime import datetime
from data import soda_data, api_requests, data_transformations
from util import basic_io, api_util


def test_get_zip_code_from_mapbox():
    app_token = api_util.get_mapbox_app_token()

    long = -73.989
    lat = 40.733
    zip = data_transformations.get_zipcode_from_mapbox(long, lat, app_token)

    assert zip == 10003, "simple zipcode test failed"


def test_get_next_saturday():
    input = "2020-04-28T17:56:00.000"  # answer is 5/2/2020, week 18
    yyyymmdd_str = input[0:input.find("T")]
    assert data_transformations.get_next_saturday(yyyymmdd_str) \
           == datetime.strptime("2020-05-02", "%Y-%m-%d")


def test_get_cdc_mmr_week():
    input = "2020-04-28T17:56:00.000"  # answer is 5/2/2020, week 18
    yyyymmdd_str = input[0:input.find("T")]
    assert data_transformations.get_cdc_mmwr_week(yyyymmdd_str) == 18


def test_cdc_lookup_resource():
    week_ending_to_cdc_week_dict =\
        basic_io.read_json_to_dict("resources/cdc_week.json")

    assert week_ending_to_cdc_week_dict["2020-05-02"] == 18
    assert week_ending_to_cdc_week_dict["2023-04-15"] == 15
    assert week_ending_to_cdc_week_dict["2024-12-28"] == 52
    assert week_ending_to_cdc_week_dict["2026-01-03"] == 53
    assert week_ending_to_cdc_week_dict["2022-01-01"] == 52
    assert week_ending_to_cdc_week_dict["2016-01-09"] == 1
    assert week_ending_to_cdc_week_dict["2018-04-07"] == 14
    assert week_ending_to_cdc_week_dict["2021-01-02"] == 53


def test_get_chicago_zipcodes():
    zipcodes = data_transformations.get_chicago_zipcodes()
    assert len(zipcodes) == 59
    assert isinstance(zipcodes[0], str)


def test_compute_moving_avg_from_daily_data():
    daily_vacc_data = soda_data.datasets[0]
    response = api_requests.SocrataAPIClient(daily_vacc_data.request_url)
    response.convert_dtypes()
    daily_data_df = response.data_df

    data_transformations.compute_moving_avg_from_daily_data(
        daily_data_df, 'zip_code', 'date', ['total_doses_daily'])

    # avg = (daily_data_df["total_doses_daily"]
    #        [daily_data_df['zip_code' == "60637"]])
    #
    # print(avg)



