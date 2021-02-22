import os
from data import api_requests, dbclient
from util import basic_io

APP_TOKEN_STR = "app_token"


def main():

    path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    params={"$$app_token": keys[APP_TOKEN_STR]}

    response_obj = api_requests.RequestResponse("https://data.cityofchicago.org/resource/naz8-j4nc.json", params)

    table_name = "test_table"
    db = dbclient.DBClient()
    db.create_table_from_pandas(response_obj.data_df, table_name)
    print(db.get_table_info(table_name))


if __name__ == "__main__":
    main()
