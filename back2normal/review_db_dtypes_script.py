import os
import pandas as pd
from data import dbclient, daily_case_data_by_zip, data_transformations, census_api_pull
from data.socrata import soda_data, socrata_api_requests
from data.groundtruth import process_ground_truth_data

pd.set_option('display.max_columns', None)

# Script to demonstrate how classes interact with each other
if os.path.exists(dbclient.DB_PATH):
    print("Deleting existing db and creating a new one for demo purposes\n")
    os.remove(dbclient.DB_PATH)
db = dbclient.DBClient()

# SOCRATA DATA PROCESS [data from https://data.cityofchicago.org]
# 1. get SodaData obj (representing single dataset) from soda_data global const
# 2. use SocrataAPIClient to get dataset, using SodaData.request_url
#    this returns a json that is converted to pandas dataframe
#    by default, all data values are of type str
#
#    MISC data manipulations (e.g. traffic crasehs: add zipcode col from lat, long)
#
# 3. compute weekly averages
# 4. use dbclient to create sql table from the pandas df

# Vaccinations
data_obj = soda_data.VACCINATION_DATA_OBJ  # 1
print(f" ##### making api request and create table for {data_obj.dataset_name} ####")
print(f"    sqlite table will be named {data_obj.sql_table_name}")
api_resp = socrata_api_requests.SocrataAPIClient(data_obj.request_url)  # 2
data_transformations.\
    compute_moving_avg_from_daily_data(api_resp.data_df,
                                       'zip_code',  # should store this
                                       'date',  # this too
                                       data_obj.week_avg_attr_list)  # 3
db.create_table_from_pandas(api_resp.data_df, data_obj.sql_table_name)  # 4
print(f"    request url: {api_resp.request_url}")
print(f"    request headers {api_resp.header_fields}")
print(f"    request header dtypes {api_resp.header_dtypes}")
print("~~~~ pandas df dtypes ~~~~")
print(api_resp.data_df.dtypes)
print("~~~~ sql table info ~~~~~")
print(db.get_table_info(data_obj.sql_table_name))
print(f"nrow df:{len(api_resp.data_df)}\n")
print(api_resp.data_df.tail())

# DAILY COVID DATA BY ZIP
# [data from https://il-covid-zip-data.s3.us-east-2.amazonaws.com/latest/zips.csv]
# 1. use function get daily covid dataset as pandas df
#    if testing = True, data is read from csv resource
# 2. compute weekly average columns
# 3. use dbclient to create sql table from pandas df

daily_covid_data = daily_case_data_by_zip.get_daily_covid_data_from_api(testing=True)  # 1
daily_case_data_by_zip.compute_7_day_mavg_columns_for_IDPH_data(daily_covid_data)  # 2
print(daily_covid_data.tail())
db.create_table_from_pandas(daily_covid_data, daily_case_data_by_zip.SQL_TABLE_NM)  # 3
print("\nDAILY COVID DATA Table Info")
print(db.get_table_info(daily_case_data_by_zip.SQL_TABLE_NM))

# GROUND TRUTH Foot Traffic Data BY ZIP
# 1. use function to read in and combine ground truth CSVs
#    this returns a single pandas dataframe
# 2. compute weekly average columns
# 3. use dbclient to create sql table from pandas df

daily_foot_traffic_data = process_ground_truth_data.get_combined_ground_truth_data()  # 1
process_ground_truth_data.compute_moving_avg(daily_foot_traffic_data)  # 2
db.create_table_from_pandas(daily_foot_traffic_data, process_ground_truth_data.SQL_TABLE_NAME)  # 3

print("\nDAILY FOOT TRAFFIC Table Info")
print(db.get_table_info(process_ground_truth_data.SQL_TABLE_NAME))


# SOCRATA CRASH DATA
# THIS IS FOR TESTING/DATA EXPLORATION ONLY
# file for computing counts and creating this test csv is:
#       sandbox/data/create_zipcode_crash_for_testing.py
# file for processing the traffic data and getting zipcode from mapbox api:
#       process_traffic_crash_data.py

traffic_crash_sql_table_name = "TRAFFIC_CRASH_DATA"
crash_file = os.path.join("resources", "zipcode_crash_data_testing.csv")
crash_data = pd.read_csv(crash_file)
data_transformations.\
    compute_moving_avg_from_daily_data(crash_data,
                                       'zipcode',
                                       'SHORT_DATE',
                                       ['crash_count'])
db.create_table_from_pandas(crash_data, traffic_crash_sql_table_name)  # 3

print("\nDAILY TRAFFIC CRASH Table Info")
print(db.get_table_info(traffic_crash_sql_table_name))

# CENSUS Data
census_df = census_api_pull.get_census_data_from_api()
