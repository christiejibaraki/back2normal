import os
from data import api_requests, dbclient, soda_data, daily_case_data_by_zip_pull
from util import basic_io

APP_TOKEN_STR = "app_token"

path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)
params = {"$$app_token": keys[APP_TOKEN_STR]}

#### add datasets from dict
#### errors out for more complex objects, POINT (-87.622844 41.886262)
#### force to string? don't include?

db = dbclient.DBClient()

for data_obj in soda_data.datasets:
    api_resp = api_requests.SocrataAPIClient(data_obj.request_url,
                                             params)
    api_resp.convert_types()
    db.create_table_from_pandas(api_resp.data_df, data_obj.table_name)
    print(db.get_table_info(data_obj.table_name))
    print(api_resp.request_url)
    

#Testing more complex query with WHERE and GROUP BY fields
#This query is not working--and i think the WHERE clause
#is the problem
# CRASH_DATE is a Floating Timestamp Datatype
    # https://dev.socrata.com/docs/datatypes/floating_timestamp.html#,
soda_obj_complex_query = soda_data.SodaData("Traffic Crashes - Crashes",
                         "TRAFFIC_CRASHES",
                         "85ca-t3if",
                         ["COUNT(CRASH_RECORD_ID)", "CRASH_DATE"],
                         group_by=['CRASH_DATE'],
                         where=["CRASH_DATE > 2020-01-01T14:00:00"])
print(soda_obj_complex_query.request_url)

api_resp_complex = api_requests.SocrataAPIClient(soda_obj_complex_query.request_url,
                                             params)
print(api_resp_complex.request_url)
print(api_resp_complex.header_fields)
print(api_resp_complex.data_df)


# daily covid data by zipcod
daily_covid_data = daily_case_data_by_zip_pull.get_daily_covid_data_from_api(testing=True)
db.create_table_from_pandas(daily_covid_data, 'IDPH_COVID_DAILY')
print(db.get_table_info('IDPH_COVID_DAILY'))
