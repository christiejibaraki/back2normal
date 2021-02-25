import os
from datetime import datetime
from data import data_transformations
from util import basic_io

# @before???


def test_get_zip_code_from_mapbox():
    path_to_keys = os.path.join('config', 'mapbox_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    app_token = keys["app-token"]

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


