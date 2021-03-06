import pandas as pd
from data import api_requests, dbclient, soda_data,\
    daily_case_data_by_zip_pull, data_transformations
from data.groundtruth import process_ground_truth_data
from data.zillow import process_zillow_data

pd.set_option('display.max_columns', None)

# Script to demonstrate how classes interact with each other
db = dbclient.DBClient()

# SOCRATA DATA PROCESS [data from https://data.cityofchicago.org]
# 1. get SodaData obj (representing single dataset) from soda_data.datasets
#       (a dict where key is dataset name, value is SodaData object)
# 2. use SocrataAPIClient to get dataset, using SodaData.request_url
#    this returns a json that is converted to pandas dataframe
#    by default, all data values are of type str
# 3. convert_dtypes() infers correct data types for pandas df
# 4. compute weekly averages
# 5. use dbclient to create sql table from the pandas df

for data_obj in soda_data.datasets.values():
    print(f" ##### making api request and create table for {data_obj.dataset_name} ####")
    print(f"    sqlite table will be named {data_obj.sql_table_name}")
    api_resp = api_requests.SocrataAPIClient(data_obj.request_url)  # 2
    api_resp.convert_dtypes()  # 3
    data_transformations.\
        compute_moving_avg_from_daily_data(api_resp.data_df,
                                           'zip_code',  # should store this
                                           'date',  # this too
                                           data_obj.week_avg_attr_list)  # 4
    db.create_table_from_pandas(api_resp.data_df, data_obj.sql_table_name)  # 5
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

daily_covid_data = daily_case_data_by_zip_pull.get_daily_covid_data_from_api(testing=True)  # 1
daily_case_data_by_zip_pull.compute_weekly_columns_for_IDPH_data(daily_covid_data)  # 2
print(daily_covid_data.tail())
db.create_table_from_pandas(daily_covid_data, 'DAILY_COVID_CASE_DATA')  # 3
print("\nDAILY COVID DATA Table Info")
print(db.get_table_info('IDPH_COVID_DAILY'))


# GROUND TRUTH Foot Traffic Data BY ZIP
# 1. use function to read in and combine ground truth CSVs
#    this returns a single pandas dataframe
# 2. use dbclient to create sql table from pandas df

### I'd like to remove the spaces from these column names (C.I.)
daily_foot_traffic_data = process_ground_truth_data.get_combined_ground_truth_data()
db.create_table_from_pandas(daily_foot_traffic_data, 'DAILY_FOOT_TRAFFIC_DATA')
print("\nDAILY FOOT TRAFFIC Table Info")
print(db.get_table_info('DAILY_FOOT_TRAFFIC_DATA'))

# ZILLOW ZORI Data
chicago_area_rents, chicago_city_rents = process_zillow_data.get_zillow_zori_data()
print("\nZILLOW Data")
print(chicago_area_rents.columns)
print(chicago_city_rents.columns)
