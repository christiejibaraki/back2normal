from data import soda_data, api_requests
import pandas as pd
import os
from util import basic_io


def test_soda_data_groupby_query():

    APP_TOKEN_STR = "app_token"

    path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    params = {"$$app_token": keys[APP_TOKEN_STR]}

    soda_obj_groupby_query = soda_data.SodaData("Traffic Crashes - Crashes",
                         "TRAFFIC_CRASHES",
                         "85ca-t3if",
                         ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                         group_by=['CRASH_DATE'])

    api_resp_groupby = api_requests.SocrataAPIClient(soda_obj_groupby_query.request_url,
                                             params)

    correct_query = "https://data.cityofchicago.org/resource/85ca-t3if.json"\
                    "?$query=SELECT COUNT(CRASH_RECORD_ID), "\
                    "CRASH_DATE GROUP BY CRASH_DATE"

    assert correct_query == soda_obj_groupby_query.request_url
    assert api_resp_groupby.response.status_code == 200

def test_soda_data_groupby_and_where_query():

    APP_TOKEN_STR = "app_token"

    path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    params = {"$$app_token": keys[APP_TOKEN_STR]}

    soda_obj_complex_query = soda_data.SodaData("Traffic Crashes - Crashes",
                            "TRAFFIC_CRASHES",
                            "85ca-t3if",
                            ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                            group_by=['CRASH_DATE'],
                            where=["CRASH_DATE > '2020-01-01T14:00:00'"])
    print(soda_obj_complex_query.request_url)

    api_resp_complex = api_requests.SocrataAPIClient(soda_obj_complex_query.request_url,
                                                params)


    correct_query = "https://data.cityofchicago.org/resource/85ca-t3if.json"\
        "?$query=SELECT COUNT(CRASH_RECORD_ID), CRASH_DATE WHERE " \
            "CRASH_DATE > '2020-01-01T14:00:00' GROUP BY CRASH_DATE"


    assert correct_query == soda_obj_complex_query.request_url
    assert api_resp_complex.response.status_code == 200