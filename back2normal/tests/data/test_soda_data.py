from data import soda_data
import pandas as pd



def test_soda_data_groupby_query():

    soda_obj_groupby_query = soda_data.SodaData("Traffic Crashes - Crashes",
                         "TRAFFIC_CRASHES",
                         "85ca-t3if",
                         ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                         group_by=['CRASH_DATE'])

    correct_query = "https://data.cityofchicago.org/resource/85ca-t3if.json"\
                    "?$query=SELECT COUNT(CRASH_RECORD_ID), "\
                    "CRASH_DATE GROUP BY CRASH_DATE"

    assert correct_query == soda_obj_groupby_query.request_url