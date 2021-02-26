import os
from data import api_requests, dbclient, soda_data
from util import basic_io

APP_TOKEN_STR = "app_token"

path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)
params = {"$$app_token": keys[APP_TOKEN_STR]}

response_obj = api_requests.RequestResponse("https://data.cityofchicago.org/resource/naz8-j4nc.json", params)
response_obj.convert_types() #converts dtypes
print(response_obj.request_url)
print(response_obj.df_dtypes)

table_name = "test_table"
db = dbclient.DBClient()
db.create_table_from_pandas(response_obj.data_df, table_name)
print(db.get_table_info(table_name))

#### select specific fields
response_obj_fields = api_requests.RequestResponse(
    "https://data.cityofchicago.org/resource/naz8-j4nc.json",
    params, ["cases_total", "deaths_total"])
print(response_obj_fields.request_url)
print(response_obj_fields.df_dtypes)
response_obj_fields.convert_types() #converts dtypes
print(response_obj_fields.df_dtypes)

#### group by some attribute
#### i picked an arbitrary dataset that would be good for testing this
response_obj_slct_group = api_requests.RequestResponse(
    "https://data.cityofchicago.org/resource/mq3i-nnqe.json",
    params, ["on_street", "COUNT(stop_id)"], ["on_street"])
print(response_obj_slct_group.request_url)
print(response_obj_slct_group.header_fields)
print(response_obj_slct_group.df_dtypes)
response_obj_slct_group.convert_types() #converts dtypes
print(response_obj_slct_group.df_dtypes)



#### add datasets from dict
#### errors out for more complex objects, POINT (-87.622844 41.886262)
#### force to string? don't include?

for data_obj in soda_data.datasets:
    api_resp = api_requests.RequestResponse(data_obj.base_url,
                                            params,
                                            data_obj.desired_attr_lst)
    api_resp.convert_types()
    db.create_table_from_pandas(api_resp.data_df, data_obj.table_name)
    print(db.get_table_info(data_obj.table_name))

