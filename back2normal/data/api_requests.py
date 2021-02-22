import os
import requests
import sqlite3
import pandas as pd
from util import basic_io


class RequestResponse:

    def __init__(self, request_url, params, query=""):

        self.request = None
        self.response = None
        self.data_df = None

        # for reviewing datatypes
        self.header_fields = None
        self.header_dtypes = None
        self.df_dtypes = None

        self._get_request(request_url, params)

    def _get_request(self, request_url, params, query=""):
        # need to implement query
        # https://dev.socrata.com/docs/queries/

        self.request = requests.Request(request_url, params)
        self.response = self.request.prepare()

    def print_request(self):
        # doesn't work, but for debugging queries
        print('{}{}{}'.format(
            self.request.method, self.request.url,
            ''.join('{}={}'.format(k, v) for k, v in self.request.headers.items())
        ))


APP_TOKEN_STR = "app_token"
path_to_keys = os.path.join('config', 'socrata_chicago_keys.json')
keys = basic_io.read_json_to_dict(path_to_keys)
params={"$$app_token": keys[APP_TOKEN_STR]}

response_obj = RequestResponse("https://data.cityofchicago.org/resource/naz8-j4nc.json", params)
response_obj.print_request()





