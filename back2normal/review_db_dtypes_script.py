import os
import sys
from data import api_requests
from util import basic_io


def main():

    APP_TOKEN_STR = "app_token"
    path_to_keys = os.path.join('./config', 'socrata_chicago_keys.json')
    keys = basic_io.read_json_to_dict(path_to_keys)
    params={"$$app_token": keys[APP_TOKEN_STR]}

    response_obj = api_requests.RequestResponse("https://data.cityofchicago.org/resource/naz8-j4nc.json", params)
    response_obj.print_request()


if __name__ == "__main__":
    main()

