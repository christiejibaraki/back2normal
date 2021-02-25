import os
import pytest
from data import data_transformations
from util import basic_io


def test_get_zip_code_from_mapbox():
    path_to_keys = os.path.join('config', 'mapbox_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    app_token = keys["app-token"]

    long = -73.989
    lat = 40.733
    zip = data_transformations.get_zipcode_from_mapbox(long, lat, app_token)

    assert zip == 10003, "simple zipcode test failed"
