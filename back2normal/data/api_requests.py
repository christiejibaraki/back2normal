import os
import requests
import pandas as pd
from util import api_util


class SocrataAPIClient:

    def __init__(self, request_url):

        self.request_url = None
        self.params = self._get_app_token_params()
        self.response = None
        self.data_df = None

        # for reviewing datatypes
        self.header_fields = None
        self.header_dtypes = None
        self.df_dtypes = None

        self._get_request(request_url)

    @staticmethod
    def _get_app_token_params():
        token = api_util.get_socrata_app_token()
        return {"$$app_token": token, "$$limit": 5000}

    def _get_request(self, request_url):
        # For header codes included in response object: 
        # https://dev.socrata.com/docs/response-codes.html

        # Difference between a Request and a Response object:
        # https://requests.readthedocs.io/en/master/user/advanced/#request-and-response-objects
        # get and parse response
        self.response = requests.get(request_url, self.params)
        self.request_url = self.response.request.url
        if self.response.status_code != 200:
            raise Exception(f"request error: "
                            f"{self.response.headers['X-Error-Message']}\n"
                            f"{self.request_url}")

        self.header_fields = self.response.headers['X-SODA2-Fields']
        self.header_dtypes = self.response.headers['X-SODA2-Types']

        # convert to pandas df
        self.data_df = pd.DataFrame.from_dict(self.response.json())
        self.df_dtypes = self.data_df.dtypes

    def convert_types(self):
        # making this a method that's not called by constructor for now
        # but eventually probably makes sense to have constructor do
        # converting itself or call this method
        self.data_df = self.data_df.apply(pd.to_numeric, errors='ignore')
        self.data_df = self.data_df.convert_dtypes(convert_integer=False)
        self.df_dtypes = self.data_df.dtypes
